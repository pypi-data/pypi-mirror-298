# -*- coding:utf-8 -*-
import warnings
import pandas as pd
import numpy as np
import chardet
import zipfile
from pandas.tseries.holiday import next_monday
from pyzipper import PyZipFile
import os
import platform
import json
from mdbq.mongo import mongo
from mdbq.mysql import mysql
from mdbq.aggregation import df_types
from mdbq.config import get_myconf
from mdbq.config import set_support
from mdbq.dataframe import converter
import datetime
import time
import re
import shutil
import getpass

warnings.filterwarnings('ignore')
"""
1. DatabaseUpdate: 程序用于对爬虫下载的原始数据进行清洗并入库;
    数据入库时会较检并更新本地 json 文件的 dtypes 信息;
    若 json 缺失 dtypes 信息, 会按 df 类型自动转换并更新本地 json, 可以手动修改添加本地 json 信息，手动修改优先;
2. upload_dir: 函数将一个文件夹上传至数据库;
"""


class DatabaseUpdate:
    """
    清洗文件，并入库，被 tg.py 调用
    """
    def __init__(self, path):
        self.path = path  # 数据所在目录, 即: 下载文件夹
        self.datas: list = []  # 带更新进数据库的数据集合
        self.start_date = '2022-01-01'  # 日期表的起始日期

    def cleaning(self, is_move=True):
        """
        数据清洗, 返回包含 数据库名, 集合名称, 和 df 主体
        修改 cleaning 时，要同步 support 下的 标题对照表.csv
        """
        if not os.path.exists(self.path):
            print(f'1.1.0 初始化时传入了不存在的目录: {self.path}')
            return

        filename = '标题对照表.csv'
        support_file = set_support.SetSupport(dirname='support').dirname
        if not os.path.isfile(os.path.join(support_file, filename)):
            print(f'缺少关键文件支持: {os.path.join(support_file, filename)}')
            return
        df = pd.read_csv(os.path.join(support_file, filename), encoding='utf-8_sig', header=0, na_filter=False)
        datas = df.to_dict('records')  # 转字典
        # print(datas)

        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                if '~$' in name or '.DS' in name or '.localized' in name or '.ini' in name or '$RECYCLE.BIN' in name or 'Icon' in name:
                    continue

                db_name = None  # 初始化/重置变量，避免进入下一个循环
                collection_name = None
                for data in datas:  # 根据标题对照表适配 db_name 和 collection_name
                    if data['关键词1'] in name and data['关键词2'] in name:
                        db_name = data['数据库名']
                        collection_name = data['数据表']
                # print(name, db_name, collection_name)
                # return

                # 只针对 csv, xlsx 文件进行处理
                if not name.endswith('.csv') and not name.endswith('.xls') and not name.endswith('.xlsx'):
                    continue
                df = pd.DataFrame()  # 初始化 df
                encoding = self.get_encoding(file_path=os.path.join(root, name))  # 用于处理 csv 文件
                tg_names = ['营销场景报表', '计划报表', '单元报表', '关键词报表', '人群报表', '主体报表',
                            '其他主体报表',
                            '创意报表', '地域报表', '权益报表']
                for tg_name in tg_names:
                    if tg_name in name and '报表汇总' not in name and name.endswith('.csv'):  # 排除达摩盘报表: 人群报表汇总
                        pattern = re.findall(r'(.*_)\d{8}_\d{6}', name)
                        if not pattern:  # 说明已经转换过
                            continue
                        shop_name = re.findall(r'\d{8}_\d{6}_(.*)\W', name)
                        if shop_name:
                            shop_name = shop_name[0]
                        else:
                            shop_name = ''
                        df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                        if '地域' not in name:  # 除了地域报表, 检查数据的字段是否包含“场景名字”,如果没有,说明没有选“pbix” 模块
                            ck = df.columns.tolist()
                            if '场景名字' not in ck:
                                print(f'1.2.0 {name} 报表字段缺失, 请选择Pbix数据模板下载')
                                continue
                        if len(df) == 0:
                            print(f'1.3.0 {name} 报表是空的, 请重新下载')
                            continue
                        cols = df.columns.tolist()
                        if '日期' not in cols:
                            print(f'1.4.0 {name} 报表不包含分日数据, 已跳过')
                            continue
                        if '省' in cols:
                            if '市' not in cols:
                                print(f'1.5.0 {name} 请下载市级地域报表，而不是省报表')
                                continue
                        # df.replace(to_replace=['\\N'], value=0, regex=False, inplace=True)  # 替换掉特殊字符
                        # df.replace(to_replace=[''], value=0, regex=False, inplace=True)
                        # df.fillna(0, inplace=True)
                        if '省' in df.columns.tolist() and '场景名字' in df.columns.tolist() and '地域报表' in name:
                            db_name = '推广数据2'
                            collection_name = f'完整_{tg_name}'
                        else:
                            db_name = '推广数据2'
                            collection_name = f'{tg_name}'
                if name.endswith('.csv') and '超级直播' in name:
                    # 超级直播
                    df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    pattern = re.findall(r'(.*_)\d{8}_\d{6}', name)
                    if not pattern:  # 说明已经转换过
                        continue
                    shop_name = re.findall(r'\d{8}_\d{6}_(.*)\W', name)
                    if shop_name:
                        shop_name = shop_name[0]
                    else:
                        shop_name = ''
                    # df.replace(to_replace=['\\N'], value=0, regex=False, inplace=True)  # 替换掉特殊字符
                    # df.replace(to_replace=[''], value=0, regex=False, inplace=True)
                elif name.endswith('.xls') and '短直联投' in name:
                    # 短直联投
                    df = pd.read_excel(os.path.join(root, name), sheet_name=None, header=0)
                    df = pd.concat(df)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    # df.replace(to_replace=[''], value=0, regex=False, inplace=True)
                elif name.endswith('.xls') and '视频加速推广' in name:
                    # 超级短视频
                    df = pd.read_excel(os.path.join(root, name), sheet_name=None, header=0)
                    df = pd.concat(df)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    # df.replace(to_replace=[''], value=0, regex=False, inplace=True)
                if '人群报表汇总' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=1, na_filter=False)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                # ----------------- 推广报表 分割线 -----------------
                # ----------------- 推广报表 分割线 -----------------
                date01 = re.findall(r'(\d{4}-\d{2}-\d{2})_\d{4}-\d{2}-\d{2}', str(name))
                date02 = re.findall(r'\d{4}-\d{2}-\d{2}_(\d{4}-\d{2}-\d{2})', str(name))
                attrib_pattern = re.findall(r'(\d+).xlsx', name)  # 天猫商品素材表格, 必不可少
                if name.endswith('.xls') and '生意参谋' in name and '无线店铺流量来源' in name:
                    # 无线店铺流量来源
                    df = pd.read_excel(os.path.join(root, name), header=5)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    # df.replace(to_replace=['-'], value=0, regex=False, inplace=True)
                    # df.replace(to_replace=[','], value='', regex=True, inplace=True)
                    if date01[0] != date02[0]:
                        data_lis = date01[0] + '_' + date02[0]
                        df.insert(loc=0, column='数据周期', value=data_lis)
                    df.insert(loc=0, column='日期', value=date01[0])
                    # 2024-2-19 官方更新了推广渠道来源名称
                    df['三级来源'] = df['三级来源'].apply(
                        lambda x: '精准人群推广' if x == '精准人群推广(原引力魔方)'
                        else '关键词推广' if x == '关键词推广(原直通车)'
                        else '智能场景' if x == '智能场景(原万相台)'
                        else x
                    )
                    db_name = '生意参谋2'
                    if '经营优势' in df['一级来源'].tolist():  # 新版流量
                        if '数据周期' in df.columns.tolist():
                            collection_name='店铺来源_月数据'
                        else:
                            collection_name='店铺来源_日数据'
                    else:  # 旧版流量
                        if '数据周期' in df.columns.tolist():
                            collection_name='店铺来源_月数据_旧版'
                        else:
                            collection_name='店铺来源_日数据_旧版'
                elif name.endswith('.csv') and '客户运营平台_客户列表' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                elif name.endswith('.xls') and '生意参谋' in name and '无线店铺三级流量来源详情' in name:
                    # 店铺来源，手淘搜索，关键词
                    pattern = re.findall(r'(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})', name)
                    df = pd.read_excel(os.path.join(root, name), header=5)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.replace(to_replace=[','], value='', regex=True, inplace=True)
                    df.insert(loc=0, column='日期', value=pattern[0][1])
                    df.rename(columns={
                        '来源名称': '关键词',
                        '收藏商品-支付买家数': '收藏商品_支付买家数',
                        '加购商品-支付买家数': '加购商品_支付买家数',
                    }, inplace=True)
                    if pattern[0][0] != pattern[0][1]:
                        data_lis = pattern[0][0] + '_' + pattern[0][1]
                        df.insert(loc=1, column='数据周期', value=data_lis)

                elif name.endswith('.xls') and '生意参谋' in name and '商品_全部' in name:
                    # 店铺商品排行
                    df = pd.read_excel(os.path.join(root, name), header=4)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    # df.replace(to_replace=['-'], value=0, regex=False, inplace=True)
                    # df.replace(to_replace=[','], value='', regex=True, inplace=True)
                    df.rename(columns={'统计日期': '日期', '商品ID': '商品id'}, inplace=True)
                    if date01[0] != date02[0]:
                        data_lis = date01[0] + '_' + date02[0]
                        df.insert(loc=1, column='数据周期', value=data_lis)
                elif name.endswith('.xls') and '参谋店铺整体日报' in name:
                    # 自助取数，店铺日报
                    df = pd.read_excel(os.path.join(root, name), header=7)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.rename(columns={'统计日期': '日期'}, inplace=True)
                elif name.endswith('.xls') and '参谋每日流量_自助取数_新版' in name:
                    # 自助取数，每日流量
                    df = pd.read_excel(os.path.join(root, name), header=7)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.rename(columns={'统计日期': '日期'}, inplace=True)
                    # 2024-2-19 官方更新了推广渠道来源名称，自助取数没有更新，这里强制更改
                    df['三级来源'] = df['三级来源'].apply(
                        lambda x: '精准人群推广' if x == '引力魔方'
                        else '关键词推广' if x == '直通车'
                        else '智能场景' if x == '万相台'
                        else '精准人群推广' if x == '精准人群推广(原引力魔方)'
                        else '关键词推广' if x == '关键词推广(原直通车)'
                        else '智能场景' if x == '智能场景(原万相台)'
                        else x
                    )
                elif name.endswith('.xls') and '商品sku' in name:
                    # 自助取数，商品sku
                    df = pd.read_excel(os.path.join(root, name), header=7)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.rename(columns={
                        '统计日期': '日期',
                        '商品ID': '商品id',
                        'SKU ID': 'sku id',
                        '商品SKU': '商品sku',
                    }, inplace=True)
                elif name.endswith('.xls') and '参谋店铺流量来源（月）' in name:
                    # 自助取数，月店铺流量来源
                    df = pd.read_excel(os.path.join(root, name), header=7)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.rename(columns={'统计日期': '数据周期'}, inplace=True)
                    # 2024-2-19 官方更新了推广渠道来源名称，自助取数没有更新，这里强制更改
                    df['三级来源'] = df['三级来源'].apply(
                        lambda x: '精准人群推广' if x == '引力魔方'
                        else '关键词推广' if x == '直通车'
                        else '智能场景' if x == '万相台'
                        else '精准人群推广' if x == '精准人群推广(原引力魔方)'
                        else '关键词推广' if x == '关键词推广(原直通车)'
                        else '智能场景' if x == '智能场景(原万相台)'
                        else x
                    )
                    df['日期'] = df['数据周期'].apply(lambda x: re.findall('(.*) ~', x)[0])
                elif name.endswith('.csv') and 'baobei' in name:
                    # 生意经宝贝指标日数据
                    date = re.findall(r's-(\d{4})(\d{2})(\d{2})\.', str(name))
                    if not date:  # 阻止月数据及已转换的表格
                        print(f'{name}  不支持或是已转换的表格')
                        # os.remove(os.path.join(root, name))  # 直接删掉，避免被分到原始文件, encoding 不同会引发错误
                        continue
                    df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        os.remove(os.path.join(root, name))
                        continue
                    if '日期' in df.columns.tolist():
                        df.pop('日期')
                    new_date = '-'.join(date[0])
                    df.insert(loc=0, column='日期', value=new_date)
                    df.replace(to_replace=['--'], value='', regex=False, inplace=True)
                elif name.endswith('.csv') and '店铺销售指标' in name:
                    # 生意经, 店铺指标，仅限月数据，实际日指标也可以
                    name_st = re.findall(r'(.*)\(分日', name)
                    if not name_st:
                        print(f'{name}  已转换的表格')
                        continue
                    df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df['日期'] = df['日期'].astype(str).apply(
                        lambda x: '-'.join(re.findall(r'(\d{4})(\d{2})(\d{2})', x)[0]) if x else x)
                    df.replace(to_replace=['--'], value='', regex=False, inplace=True)
                elif name.endswith('csv') and '省份城市分析' in name:
                    # 生意经，地域分布, 仅限日数据
                    pattern = re.findall(r'(.*[\u4e00-\u9fa5])(\d{4})(\d{2})(\d{2})\.', name)
                    if not pattern or '省份城市分析2' not in name:
                        print(f'{name}  不支持或已转换的表格')
                        # os.remove(os.path.join(root, name))  # 直接删掉，避免被分到原始文件, encoding 不同会引发错误
                        continue
                    date = '-'.join(pattern[0][1:])
                    df = pd.read_csv(os.path.join(root, name), encoding=encoding, header=0, na_filter=False)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df['省'] = df['省份'].apply(lambda x: x if ' ├─ ' not in x and ' └─ ' not in x else None)
                    df['城市'] = df[['省份', '省']].apply(lambda x: '汇总' if x['省'] else x['省份'], axis=1)
                    df['省'].fillna(method='ffill', inplace=True)
                    df['城市'].replace(to_replace=[' ├─ | └─ '], value='', regex=True, inplace=True)
                    pov = df.pop('省')
                    city = df.pop('城市')
                    df.insert(loc=1, column='城市', value=city)
                    df.insert(loc=0, column='日期', value=date)
                    df['省份'] = pov
                    df['省+市'] = df[['省份', '城市']].apply(lambda x: f'{x["省份"]}-{x["城市"]}', axis=1)
                    df.replace('NAN', 0, inplace=True)
                    df['笔单价'] = df.apply(lambda x: 0 if x['销售量'] == 0 else 0 if x['销售量'] == '0' else x['笔单价'], axis=1)
                elif name.endswith('csv') and 'order' in name:
                    # 生意经，订单数据，仅限月数据
                    pattern = re.findall(r'(.*)(\d{4})(\d{2})(\d{2})-(\d{4})(\d{2})(\d{2})', name)
                    if not pattern:
                        print(f'{name}  不支持或已转换的表格')
                        # os.remove(os.path.join(root, name))  # 直接删掉，避免被分到原始文件, encoding 不同会引发错误
                        continue
                    date1 = pattern[0][1:4]
                    date1 = '-'.join(date1)
                    date2 = pattern[0][4:]
                    date2 = '-'.join(date2)
                    date = f'{date1}_{date2}'
                    df = pd.read_csv(os.path.join(root, name), encoding='gb18030', header=0, na_filter=False)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.insert(loc=0, column='日期', value=date1)
                    df.insert(loc=1, column='数据周期', value=date)
                    df['商品id'] = df['宝贝链接'].apply(
                        lambda x: re.sub('.*id=', '', x) if x else x)
                    df.rename(columns={'宝贝标题': '商品标题', '宝贝链接': '商品链接'}, inplace=True)
                    df['颜色编码'] = df['商家编码'].apply(
                        lambda x: ''.join(re.findall(r' .*(\d{4})$', str(x))) if x else x)
                elif name.endswith('.xlsx') and '直播间成交订单明细' in name:
                    # 直播间成交订单明细
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.rename(columns={'场次ID': '场次id', '商品ID': '商品id'}, inplace=True)
                    df['日期'] = df['支付时间'].apply(lambda x: x.strftime('%Y-%m-%d'))
                elif name.endswith('.xlsx') and '直播间大盘数据' in name:
                    # 直播间大盘数据
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.rename(columns={'统计日期': '日期'}, inplace=True)
                elif name.endswith('.xls') and '直播业绩-成交拆解' in name:
                    # 直播业绩-成交拆解
                    df = pd.read_excel(os.path.join(root, name), header=5)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.rename(columns={'统计日期': '日期'}, inplace=True)
                elif name.endswith('.csv') and '淘宝店铺数据' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '人群洞察' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    df.replace(to_replace=['--'], value='', regex=False, inplace=True)
                    df = df[df['人群规模'] != '']
                    if len(df) == 0:
                        continue
                elif name.endswith('.csv') and '客户_客户概况_画像' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '市场排行_店铺' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '类目洞察_属性分析_分析明细_商品发现' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '类目洞察_属性分析_分析明细_汇总' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '类目洞察_价格分析_分析明细_商品发现' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '类目洞察_价格分析_分析明细_汇总' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '搜索排行_搜索' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '竞店分析-销售分析-关键指标对比' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '竞店分析-销售分析-top商品榜' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '竞店分析-来源分析-入店来源' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                elif name.endswith('.csv') and '竞店分析-来源分析-入店搜索词' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                # ----------------------- 京东数据处理分界线 -----------------------
                # ----------------------- 京东数据处理分界线 -----------------------
                elif name.endswith('.xlsx') and '店铺来源_流量来源' in name:
                    # 京东店铺来源
                    if '按天' not in name:
                        print(f'{name} 京东流量请按天下载')
                        continue
                    date01 = re.findall(r'(\d{4})(\d{2})(\d{2})_(\d{4})(\d{2})(\d{2})', str(name))
                    new_date01 = f'{date01[0][0]}-{date01[0][1]}-{date01[0][2]}'
                    new_date02 = f'{date01[0][3]}-{date01[0][4]}-{date01[0][5]}'
                    new_date03 = f'{new_date01}_{new_date02}'
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.insert(loc=0, column='日期', value=new_date01)
                    if new_date01 != new_date02:
                        df.insert(loc=1, column='数据周期', value=new_date03)
                    cols = df.columns.tolist()
                    for col_2024 in cols:  # 京东这个表有字段加了去年日期，删除这些同比数据字段，不然列数量爆炸
                        if '20' in col_2024 and '流量来源' in name:
                            df.drop(col_2024, axis=1, inplace=True)
                elif name.endswith('.xlsx') and '全部渠道_商品明细' in name:
                    # 京东商品明细 文件转换
                    date1 = re.findall(r'_(\d{4})(\d{2})(\d{2})_全部', str(name))
                    if not date1[0]:
                        print(f'{name}: 仅支持日数据')
                        continue
                    if date1:
                        date1 = f'{date1[0][0]}-{date1[0][1]}-{date1[0][2]}'
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    if '10035975359247' in df['商品ID'].values or '10056642622343' in df['商品ID'].values:
                        new_name = f'sku_{date1}_全部渠道_商品明细.csv'
                    elif '10021440233518' in df['商品ID'].values or '10022867813485' in df['商品ID'].values:
                        new_name = f'spu_{date1}_全部渠道_商品明细.csv'
                    else:
                        new_name = f'未分类_{date1}_全部渠道_商品明细.csv'
                    df.rename(columns={'商品ID': '商品id'}, inplace=True)
                    df.insert(loc=0, column='日期', value=date1)
                    df['最近上架时间'].loc[0] = df['最近上架时间'].loc[1]  # 填充这一列, 避免上传 mysql 日期类型报错
                    if 'sku' in new_name:  # 即使有文件对照表，也不能删除这个条件，spu ，sku 是后来加的
                        db_name = '京东数据2'
                        collection_name = 'sku_商品明细'
                    elif 'spu' in new_name:
                        db_name = '京东数据2'
                        collection_name = 'spu_商品明细'
                elif name.endswith('.xlsx') and '搜索分析-排名定位-商品词下排名' in name:
                    # 京东商品词下排名
                    try:
                        df = pd.read_excel(os.path.join(root, name), header=0, engine='openpyxl')
                        if len(df) == 0:
                            print(f'{name} 报表数据为空')
                            continue
                        df.rename(columns={'商品的ID': 'skuid'}, inplace=True)
                        for col in ['词人气', '搜索点击率']:
                            if col in df.columns.tolist():
                                df[col] = df[col].apply(lambda x: round(x, 6) if x else x)
                    except Exception as e:
                        print(e)
                        print(name, '报错')
                        continue
                elif name.endswith('.xlsx') and '搜索分析-排名定位-商品排名' in name:
                    # 京东商品排名
                    date_in = re.findall(r'(\d{4}-\d{2}-\d{2})-搜索', str(name))[0]
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.insert(0, '日期', date_in)  # 插入新列
                    df.rename(columns={'SKU': 'skuid'}, inplace=True)
                    if '点击率' in df.columns.tolist():
                        df['点击率'] = df['点击率'].apply(lambda x: round(x, 6) if x else x)
                elif name.endswith('.xls') and '竞店概况_竞店详情' in name:
                    # 京东，竞争-竞店概况-竞店详情-全部渠道
                    date01 = re.findall(r'全部渠道_(\d{4})(\d{2})(\d{2})_(\d{4})(\d{2})(\d{2})', str(name))
                    start_date = f'{date01[0][0]}-{date01[0][1]}-{date01[0][2]}'
                    # end_date = f'{date01[0][3]}-{date01[0][4]}-{date01[0][5]}'
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df.insert(loc=0, column='日期', value=start_date)
                elif name.endswith('.xls') and 'JD店铺日报_店铺' in name:
                    # 京东 自助报表  店铺日报
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df['日期'] = df['日期'].apply(
                        lambda x: '-'.join(re.findall(r'(\d{4})(\d{2})(\d{2})', str(x))[0])
                    )
                elif name.endswith('.xls') and '商家榜单_女包_整体' in name:
                    # 京东 行业 商家榜单
                    date2 = re.findall(r'_\d{8}-\d+', name)
                    if date2:
                        print(f'{name}: 请下载日数据，不支持其他周期')
                        # os.remove(os.path.join(root, name))  # 直接删掉，避免被分到原始文件, encoding 不同会引发错误
                        continue
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df['日期'] = df['日期'].astype(str).apply(lambda x: f'{x[:4]}-{x[4:6]}-{x[6:8]}')
                    df.insert(loc=0, column='类型', value='商家榜单')
                elif name.endswith('.xlsx') and '批量SKU导出-批量任务' in name:
                    # 京东 sku 导出
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    d_time = datetime.datetime.today().strftime('%Y-%m-%d')
                    df.insert(loc=0, column='日期', value=d_time)
                    df['商品链接'] = df['商品链接'].apply(lambda x: f'https://{x}' if x else x)
                elif name.endswith('.xlsx') and '批量SPU导出-批量任务' in name:
                    # 京东 spu 导出
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    d_time = datetime.datetime.today().strftime('%Y-%m-%d')
                    df.insert(loc=0, column='日期', value=d_time)
                elif name.endswith('.csv') and '万里马箱包推广1_完整点击成交' in name:
                    # 京东推广数据
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df['日期'] = df['日期'].apply(lambda x: f'{str(x)[:4]}-{str(x)[4:6]}-{str(x)[6:8]}')
                elif name.endswith('.csv') and '万里马箱包推广1_京东推广搜索词_pbix同步不要' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df['日期'] = df['日期'].apply(lambda x: f'{str(x)[:4]}-{str(x)[4:6]}-{str(x)[6:8]}')
                    df['是否品牌词'] = df['搜索词'].str.contains('万里马|wanlima', regex=True)
                    df['是否品牌词'] = df['是否品牌词'].apply(lambda x: '品牌词' if x else '')
                elif name.endswith('.xlsx') and '零售明细统计' in name:
                    df = pd.read_excel(os.path.join(root, name), header=0)
                    if len(df) == 0:
                        print(f'{name} 报表数据为空')
                        continue
                    df = df[df['缩略图'] != '合计']
                elif name.endswith('.csv') and '营销概况_全站营销' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=1, na_filter=False)
                    df = df[(df['日期'] != '日期') & (df['日期'] != '汇总') & (df['日期'] != '0') & (df['花费'] != '0') & (df['花费'] != '0.00')]
                    df['日期'] = df['日期'].apply(lambda x: f'{str(x)[:4]}-{str(x)[4:6]}-{str(x)[6:8]}')
                    df.drop("'当前时间'", axis=1, inplace=True)
                    df.rename(columns={'全站ROI': '全站roi'}, inplace=True)
                    df.insert(loc=1, column='产品线', value='全站营销')
                elif name.endswith('.csv') and '关键词点击成交报表_pbix同步_勿删改' in name:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    for col in df.columns.tolist():
                        if '（' in col:
                            new_col = re.sub('[（）]', '_', col)
                            new_col = new_col.strip('_')
                            df.rename(columns={col: new_col}, inplace=True)
                    df['日期'] = df['日期'].apply(lambda x: f'{str(x)[:4]}-{str(x)[4:6]}-{str(x)[6:8]}')
                    df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                    # min_clm = str(df['日期'].min()).split(' ')[0]
                    # max_clm = str(df['日期'].max()).split(' ')[0]

                # 商品素材，必须保持放在最后处理
                elif name.endswith('xlsx'):
                    """从天猫商品素材库中下载的文件，将文件修改日期添加到DF 和文件名中"""
                    if  attrib_pattern:
                        df = pd.read_excel(os.path.join(root, name), header=0, engine='openpyxl')
                        cols = df.columns.tolist()
                        if '商品白底图' in cols and '方版场景图' in cols:
                            f_info = os.stat(os.path.join(root, name))  # 读取文件的 stat 信息
                            mtime = time.strftime('%Y-%m-%d', time.localtime(f_info.st_mtime))  # 读取文件创建日期
                            df['日期'] = mtime
                            df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='ignore')
                            df.rename(columns={'商品ID': '商品id'}, inplace=True)
                            sp_id = df['商品id'].tolist()
                            if 652737455554 in sp_id or 683449516249 in sp_id or 37114359548 in sp_id or 570735930393 in sp_id:
                                df.insert(0, '店铺名称', '万里马官方旗舰店')  # 插入新列
                            elif 704624764420 in sp_id or 701781021639 in sp_id or 520380314717 in sp_id:
                                df.insert(0, '店铺名称', '万里马官方企业店')  # 插入新列
                            else:
                                df.insert(0, '店铺名称', 'coome旗舰店')  # 插入新列
                            db_name = '属性设置2'
                            collection_name = '商品素材导出'
                        else:
                            df = pd.DataFrame()

                if is_move:
                    try:
                        os.remove(os.path.join(root, name))  # 是否移除原文件
                    except Exception as e:
                        print(f'{name},  {e}')
                if len(df) > 0:
                    # 将数据传入 self.datas 等待更新进数据库
                    self.datas.append(
                        {
                            '数据库名': db_name,
                            '集合名称': collection_name,
                            '数据主体': df,
                            '文件名': name,
                        }
                    )

        # 品销宝一个表格里面包含多个 sheet, 最好是单独处理
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                if '~$' in name or '.DS' in name or '.localized' in name or '.jpg' in name or '.png' in name:
                    continue

                db_name = None  # 初始化/重置变量，避免进入下一个循环
                collection_name = None
                for data in datas:  # 根据标题对照表适配 db_name 和 collection_name
                    if data['关键词1'] in name and data['关键词2'] in name:
                        db_name = data['数据库名']
                        collection_name = data['数据表']

                # df = pd.DataFrame()
                if name.endswith('.xlsx') and '明星店铺' in name:
                    # 品销宝
                    pattern = re.findall(r'_(\d{4}-\d{2}-\d{2})_', name)
                    if pattern:
                        continue
                    sheets4 = ['账户', '推广计划', '推广单元', '创意', '品牌流量包', '定向人群']  # 品销宝
                    file_name4 = os.path.splitext(name)[0]  # 明星店铺报表
                    for sheet4 in sheets4:
                        df = pd.read_excel(os.path.join(root, name), sheet_name=sheet4, header=0, engine='openpyxl')
                        df = df[df['搜索量'] > 0]
                        if len(df) < 1:
                            # print(f'{name}/{sheet4} 跳过')
                            continue
                        df.insert(loc=1, column='报表类型', value=sheet4)
                        self.datas.append(
                            {
                                '数据库名': db_name,
                                '集合名称': collection_name,
                                '数据主体': df,
                                '文件名': name,
                            }
                        )
                    if is_move:
                        os.remove(os.path.join(root, name))

        # df = self.date_table()  # 创建一个日期表
        # self.datas.append(
        #     {
        #         '数据库名': '聚合数据',
        #         '集合名称': '日期表',
        #         '数据主体': df,
        #         '文件名': '日期表文件名',
        #     }
        # )

    def upload_df(self, service_databases=[{}], path=None):
        """
        将清洗后的 df 上传数据库, copysh.py 调用
        """
        df_to_json = df_types.DataTypes()  # json 文件, 包含数据的 dtypes 信息
        for service_database in service_databases:
            for service_name, database in service_database.items():
                # print(service_name, database)
                if database == 'mongodb':
                    username, password, host, port = get_myconf.select_config_values(
                        target_service=service_name,
                        database=database,
                    )
                    d = mongo.UploadMongo(
                        username=username,
                        password=password,
                        host=host,
                        port=port,
                        drop_duplicates=False,
                    )
                    for data in self.datas:
                        db_name, collection_name, df = data['数据库名'], data['集合名称'], data['数据主体']
                        df_to_json.get_df_types(
                            df=df,
                            db_name=db_name,
                            collection_name=collection_name,
                            is_file_dtype=True,  # 默认本地文件优先: True
                        )
                        d.df_to_mongo(df=df, db_name=db_name, collection_name=collection_name)
                    if d.client:
                        d.client.close()

                elif database == 'mysql':
                    username, password, host, port = get_myconf.select_config_values(
                        target_service=service_name,
                        database=database,
                    )
                    m = mysql.MysqlUpload(
                        username=username,
                        password=password,
                        host=host,
                        port=port,
                    )
                    for data in self.datas:
                        df, db_name, collection_name, rt_filename = data['数据主体'], data['数据库名'], data['集合名称'], data['文件名']
                        df_to_json.get_df_types(
                            df=df,
                            db_name=db_name,
                            collection_name=collection_name,
                            is_file_dtype=True,  # 默认本地文件优先: True
                        )
                        m.df_to_mysql(
                            df=df,
                            db_name=db_name,
                            table_name=collection_name,
                            move_insert=True,  # 先删除，再插入
                            df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
                            drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
                            filename=rt_filename,  # 用来追踪处理进度
                            service_database=service_database,  # 字典
                        )
                df_to_json.as_json_file()  # 写入 json 文件, 包含数据的 dtypes 信息

    def new_unzip(self, path=None, is_move=None):
        """
        {解压并移除zip文件}
        如果是京东的商品明细，处理过程：
        1. 读取 zip包的文件名
        2. 组合完整路径，判断文件夹下是否已经有同名文件
        3. 如果有，则将该同名文件改名，（从文件名中提取日期，重新拼接文件名）
        4. 然后解压 zip包
        5. 需要用 _jd_rename 继续重命名刚解压的文件
        is_move 参数,  是否移除 下载目录的所有zip 文件
        """
        if not path:
            path = self.path
        res_names = []  # 需要移除的压缩文件
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if '~$' in name or 'DS_Store' in name or 'baidu' in name or 'xunlei' in name:
                    continue
                if name.endswith('.zip'):
                    old_file = os.path.join(root, name)
                    f = zipfile.ZipFile(old_file, 'r')
                    if len(f.namelist()) == 1:  # 压缩包只有一个文件的情况
                        for zip_name in f.namelist():  # 读取zip内的文件名称
                            # zip_name_1 = zip_name.encode('cp437').decode('utf-8')
                            try:
                                zip_name_1 = zip_name.encode('utf-8').decode('utf-8')
                            except:
                                zip_name_1 = zip_name.encode('cp437').decode('utf-8')
                            new_path = os.path.join(root, zip_name_1)  # 拼接解压后的文件路径
                            if os.path.isfile(new_path) and '全部渠道_商品明细' in new_path:  # 是否存在和包内同名的文件
                                # 专门处理京东文件
                                df = pd.read_excel(new_path)
                                try:
                                    pattern1 = re.findall(r'\d{8}_(\d{4})(\d{2})(\d{2})_全部渠道_商品明细',
                                                          name)
                                    pattern2 = re.findall(
                                        r'\d{8}_(\d{4})(\d{2})(\d{2})-(\d{4})(\d{2})(\d{2})_全部渠道_商品明细',
                                        name)
                                    if pattern1:
                                        year_date = '-'.join(list(pattern1[0])) + '_' + '-'.join(list(pattern1[0]))
                                    elif pattern2:
                                        year_date = '-'.join(list(pattern2[0])[0:3]) + '_' + '-'.join(
                                            list(pattern2[0])[3:7])
                                    else:
                                        year_date = '无法提取日期'
                                        print(f'{name} 无法从文件名中提取日期，请检查pattern或文件')
                                    if ('10035975359247' in df['商品ID'].values or '10056642622343' in
                                            df['商品ID'].values):
                                        os.rename(new_path,
                                                  os.path.join(root, 'sku_' + year_date + '_全部渠道_商品明细.xls'))
                                        f.extract(zip_name_1, root)
                                    elif ('10021440233518' in df['商品ID'].values or '10022867813485' in
                                          df['商品ID'].values):
                                        os.rename(new_path,
                                                  os.path.join(root, 'spu_' + year_date + '_全部渠道_商品明细.xls'))
                                        f.extract(zip_name_1, root)
                                    if is_move:
                                        os.remove(os.path.join(root, name))
                                except Exception as e:
                                    print(e)
                                    continue
                            else:
                                f.extract(zip_name, root)
                                if zip_name_1 != zip_name:
                                    os.rename(os.path.join(root, zip_name), os.path.join(root, zip_name_1))
                                if is_move:
                                    res_names.append(name)
                                    # os.remove(os.path.join(root, name))  # 这里不能移除，会提示文件被占用
                        f.close()
                    else:  # 压缩包内包含多个文件的情况
                        f.close()
                        self.unzip_all(path=old_file, save_path=path)

        if is_move:
            for name in res_names:
                os.remove(os.path.join(path, name))
                print(f'移除{os.path.join(path, name)}')

    def unzip_all(self, path, save_path):
        """
        遍历目录， 重命名有乱码的文件
        2. 如果压缩包是文件夹， 则保存到新文件夹，并删除有乱码的文件夹
        3. 删除MAC系统的临时文件夹__MACOSX
        """
        with PyZipFile(path) as _f:
            _f.extractall(save_path)
            _f.close()
        for _root, _dirs, _files in os.walk(save_path, topdown=False):
            for _name in _files:
                if '~$' in _name or 'DS_Store' in _name:
                    continue
                try:
                    _new_root = _root.encode('cp437').decode('utf-8')
                    _new_name = _name.encode('cp437').decode('utf-8')
                except:
                    _new_root = _root.encode('utf-8').decode('utf-8')
                    _new_name = _name.encode('utf-8').decode('utf-8')
                _old = os.path.join(_root, _name)
                _new = os.path.join(_new_root, _new_name)
                if _new_root != _root:  # 目录乱码，创建新目录
                    os.makedirs(_new_root, exist_ok=True)
                os.rename(_old, _new)
            try:
                _new_root = _root.encode('cp437').decode('utf-8')
            except:
                _new_root = _root.encode('utf-8').decode('utf-8')
            if _new_root != _root or '__MACOSX' in _root:
                shutil.rmtree(_root)

    def get_encoding(self, file_path):
        """
        获取文件的编码方式, 读取速度比较慢，非必要不要使用
        """
        with open(file_path, 'rb') as f:
            f1 = f.read()
            encod = chardet.detect(f1).get('encoding')
        return encod

    def date_table(self, service_databases=[{}]):
        """
        生成 pbix使用的日期表
        """
        yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))
        dic = pd.date_range(start=self.start_date, end=yesterday)
        df = pd.DataFrame(dic, columns=['日期'])
        df.sort_values('日期', ascending=True, ignore_index=True, inplace=True)
        df.reset_index(inplace=True)
        # inplace 添加索引到 df
        p = df.pop('index')
        df['月2'] = df['日期']
        df['月2'] = df['月2'].dt.month
        df['日期'] = df['日期'].dt.date  # 日期格式保留年月日，去掉时分秒
        df['年'] = df['日期'].apply(lambda x: str(x).split('-')[0] + '年')
        df['月'] = df['月2'].apply(lambda x: str(x) + '月')
        # df.drop('月2', axis=1, inplace=True)
        mon = df.pop('月2')
        df['日'] = df['日期'].apply(lambda x: str(x).split('-')[2])
        df['年月'] = df.apply(lambda x: x['年'] + x['月'], axis=1)
        df['月日'] = df.apply(lambda x: x['月'] + x['日'] + '日', axis=1)
        df['第n周'] = df['日期'].apply(lambda x: x.strftime('第%W周'))
        df['索引'] = p
        df['月索引'] = mon
        df.sort_values('日期', ascending=False, ignore_index=True, inplace=True)

        for service_database in service_databases:
            for service_name, database in service_database.items():
                username, password, host, port = get_myconf.select_config_values(
                    target_service=service_name,
                    database=database,
                )
                m = mysql.MysqlUpload(
                    username=username,
                    password=password,
                    host=host,
                    port=port,
                )
                m.df_to_mysql(
                    df=df,
                    db_name='聚合数据',
                    table_name='日期表',
                    move_insert=True,  # 先删除，再插入
                    df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
                    drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
                    filename=None,  # 用来追踪处理进度
                    service_database=service_database,  # 用来追踪处理进度
                )
        # return df

    def other_table(self, service_databases=[{'home_lx': 'mysql'}]):
        """ 上传 support 文件夹下的 主推商品.csv """
        support_file = set_support.SetSupport(dirname='support').dirname
        filename = '主推商品.xlsx'
        if not os.path.isfile(os.path.join(support_file, filename)):
            return
        # df = pd.read_csv(os.path.join(support_file, filename), encoding='utf-8_sig', header=0, na_filter=False)
        df = pd.read_excel(os.path.join(support_file, filename), header=0)
        for service_database in service_databases:
            for service_name, database in service_database.items():
                username, password, host, port = get_myconf.select_config_values(
                    target_service=service_name,
                    database=database,
                )
                m = mysql.MysqlUpload(
                    username=username,
                    password=password,
                    host=host,
                    port=port,
                )
                m.df_to_mysql(
                    df=df,
                    db_name='属性设置2',
                    table_name='主推商品',
                    move_insert=False,  # 先删除，再插入
                    df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
                    drop_duplicates=True,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
                    filename=None,  # 用来追踪处理进度
                    service_database=service_database,  # 用来追踪处理进度
                )


def upload_dir(path, db_name, collection_name, dbs={'mysql': True, 'mongodb': True}, json_path=None):
    """ 上传一个文件夹到 mysql 或者 mongodb 数据库 """
    if not os.path.isdir(path):
        print(f'{os.path.splitext(os.path.basename(__file__))[0]}.upload_dir: 函数只接受文件夹路径，不是一个文件夹: {path}')
        return

    if dbs['mongodb']:
        username, password, host, port = get_myconf.select_config_values(
            target_service='home_lx',
            database='mongodb',
        )
        d = mongo.UploadMongo(
            username=username,
            password=password,
            host=host,
            port=port,
            drop_duplicates=False,
        )

    if dbs['mysql']:
        username, password, host, port = get_myconf.select_config_values(
            target_service='company',
            database='mysql',
        )
        m = mysql.MysqlUpload(
            username=username,
            password=password,
            host=host,
            port=port,
        )
        # username, password, host, port = get_myconf.select_config_values(
        #     target_service='nas',
        #     database='mysql',
        # )
        # nas = mysql.MysqlUpload(
        #     username=username,
        #     password=password,
        #     host=host,
        #     port=port,
        # )

    # 从本地 json 文件从读取 df 的数据类型信息
    df_to_json = df_types.DataTypes()
    dtypes = df_to_json.load_dtypes(
        db_name=db_name,
        collection_name=collection_name,
    )

    count = 0
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            count += 1
    i = 0  # 用来统计当前处理文件进度
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if '~$' in name or '.DS' in name or '.localized' in name or 'baidu' in name:
                continue
            if name.endswith('.csv'):
                try:
                    df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                    if len(df) == 0:
                        continue
                    # if '新版' not in name:
                    #     continue
                    cv = converter.DataFrameConverter()
                    df = cv.convert_df_cols(df=df)  # 清理列名和 df 中的非法字符
                    try:
                        df = df.astype(dtypes)  # 按本地文件更新 df 的数据类型, 可能因为字段不同产生异常
                    except Exception as e:
                        print(name, e)
                        # 如果发生异常，这将 df 的数据和 json 中的数据取交集
                        old_dt = df.dtypes.apply(str).to_dict()  # 将 dataframe 数据类型转为字典形式
                        intersection_keys = dtypes.keys() & old_dt.keys()  # 获取两个字典键的交集
                        dtypes = {k: dtypes[k] for k in intersection_keys}  # 使用交集的键创建新字典
                        df = df.astype(dtypes)  # 再次更新 df 的数据类型

                    if dbs['mongodb']:
                        d.df_to_mongo(df=df, db_name=db_name, collection_name=collection_name)
                    if dbs['mysql']:  # drop_duplicates: 值为 True 时检查重复数据再插入
                        m.df_to_mysql(df=df, db_name=db_name, table_name=collection_name,
                                      move_insert=False,  # 先删除，再插入
                                      df_sql = True,
                                      drop_duplicates=False,
                                      filename=name, count=f'{i}/{count}')
                        # nas.df_to_mysql(df=df, db_name=db_name, table_name=collection_name, drop_duplicates=True,)
                except Exception as e:
                    print(name, e)
            i += 1
    if dbs['mongodb']:
        if d.client:
            d.client.close()  # 必须手动关闭数据库连接


def one_file_to_mysql(file, db_name, table_name, target_service, database):
    """ 上传单个文件到 mysql 数据库 file 参数是一个文件 """
    if not os.path.isfile(file):
        print(f'{os.path.splitext(os.path.basename(__file__))[0]}.one_file_to_mysql: 函数只接受文件, 此文件不存在: {file}')
        return
    username, password, host, port = get_myconf.select_config_values(target_service=target_service, database=database)
    filename = os.path.basename(file)
    df = pd.read_csv(file, encoding='utf-8_sig', header=0, na_filter=False, float_precision='high')
    # df.replace(to_replace=[','], value='', regex=True, inplace=True)  # 替换掉特殊字符
    m = mysql.MysqlUpload(username=username, password=password, host=host, port=port)
    m.df_to_mysql(df=df, db_name=db_name, table_name=table_name, filename=filename, move_insert=False,  df_sql=True, drop_duplicates=False,)


def file_dir(one_file=True):
    """
    按照文件记录对照表上传数据
    批量上传数据库
    one_file: 值为 True 时每个文件夹取一个文件上传数据库，反之上传所有文件夹数据
    """
    filename = '文件目录对照表.csv'
    if platform.system() == 'Windows':
        path = 'C:\\同步空间\\BaiduSyncdisk\\原始文件2'
    else:
        path = '/Users/xigua/数据中心/原始文件2'

    support_file = set_support.SetSupport(dirname='support').dirname
    df = pd.read_csv(os.path.join(support_file, filename), encoding='utf-8_sig', header=0, na_filter=False)
    datas = df.to_dict('records')  # 转字典
    for data in datas:
        # print(data)
        if data['入库进度'] == 0:
            sub_path, db_name, table_name = data['子文件夹'], data['数据库名'], data['数据表']
            if platform.system() == 'Windows':
                sub_path = sub_path.replace('/', '\\')
            # print(os.path.join(path, sub_path), db_name, table_name)
            if one_file:  # 从每个文件夹中取出一个文件上传
                real_path_list = []
                for root, dirs, files in os.walk(os.path.join(path, sub_path), topdown=False):
                    for name in files:
                        if name.endswith('.csv') and 'baidu' not in name and '~' not in name:
                            real_path_list.append(os.path.join(root, name))
                            break
                for real_path in real_path_list:
                    one_file_to_mysql(
                        file=real_path,
                        db_name=db_name,
                        table_name=table_name,
                        target_service='home_lx',
                        database='mysql'
                    )
            else:  # 上传全部文件夹
                upload_dir(
                    path=os.path.join(path, sub_path),
                    db_name = db_name,
                    collection_name = table_name,
                    dbs={'mysql': True, 'mongodb': True},
                )
            data.update({'入库进度': 1})  # 更新进度为已上传
    # 将进度信息写回文件
    df = pd.DataFrame.from_dict(datas, orient='columns')
    df.to_csv(os.path.join(support_file, filename), encoding='utf-8_sig', index=False, header=True)


def test():
    path = '/Users/xigua/数据中心/原始文件2/京东报表/JD商品明细spu'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith('.csv') and 'baidu' not in name and '~' not in name:
                df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                df['最近上架时间'].loc[0] = df['最近上架时间'].loc[1]
                # print(df[['日期', '最近上架时间']])
                df.to_csv(os.path.join(root, name), encoding='utf-8_sig', index=False, header=True)
        #         break
        # break


def test2():
    dp = DatabaseUpdate(path='/Users/xigua/Downloads')
    dp.new_unzip(is_move=True)
    dp.cleaning(is_move=False, )  # 清洗数据, 存入 self.datas
    dp.upload_df(service_databases=[
        # {'home_lx': 'mongodb'},
        {'home_lx': 'mysql'},
        # {'nas': 'mysql'}
    ], path=None, service_name=None)


if __name__ == '__main__':
    username, password, host, port = get_myconf.select_config_values(target_service='nas', database='mysql')
    print(username, password, host, port)
    # file_dir(one_file=False)
    # one_file_to_mysql(
    #     file='/Users/xigua/数据中心/原始文件2/京东报表/JD推广_全站营销报表/2024-08/万里马箱包推广1_营销概况_全站营销_2024-08-19_2024-09-02.csv',
    #     db_name='京东数据2',
    #     table_name='推广数据_全站营销',
    #     target_service='company',
    #     database='mysql'
    # )

    db_name = '生意经2'
    table_name = '省份城市分析'
    upload_dir(
        path='/Users/xigua/数据中心/原始文件2/生意经/地域分布',
        db_name=db_name,
        collection_name=table_name,
        dbs={'mysql': True, 'mongodb': False},
    )


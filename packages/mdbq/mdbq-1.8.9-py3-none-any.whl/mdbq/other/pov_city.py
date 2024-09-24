import pandas as pd
import os


def pov():
    """
    :return: 返回一个dataframe, 列名为: 区域, 省份
    如果有疏漏的需要在末尾添加
    """
    pov_ = [['华北', '北京'],
            ['华北', '天津'],
            ['华北', '河北'],
            ['华北', '山西'],
            ['华北', '内蒙古'],
            ['东北', '辽宁'],
            ['东北', '吉林'],
            ['东北', '黑龙江'],
            ['华东', '上海'],
            ['华东', '江苏'],
            ['华东', '浙江'],
            ['华东', '安徽'],
            ['华东', '福建'],
            ['华东', '山东'],
            ['华东', '江西'],
            ['华东', '台湾'],
            ['华中', '河南'],
            ['华中', '湖北'],
            ['华中', '湖南'],
            ['华南', '广东'],
            ['华南', '广西'],
            ['华南', '海南'],
            ['华南', '香港'],
            ['华南', '澳门'],
            ['西南', '重庆'],
            ['西南', '四川'],
            ['西南', '贵州'],
            ['西南', '云南'],
            ['西南', '西藏'],
            ['西北', '陕西'],
            ['西北', '甘肃'],
            ['西北', '青海'],
            ['西北', '宁夏'],
            ['西北', '新疆'],
            ['其他', '其他']]
    pov_ = pd.DataFrame(data=pov_, columns=['地理区域', '省份'])
    return pov_


def city():
    """
    :return: 返回一个dataframe, 列名为: 城市等级, 城市
    如果有疏漏的需要在末尾添加
    """
    city_ = [['一线城市', '北京市', '北京'],
             ['一线城市', '上海市', '上海'],
             ['一线城市', '广州市', '广东'],
             ['一线城市', '深圳市', '广东'],
             ['新一线城市', '成都市', '四川'],
             ['新一线城市', '重庆市', '重庆'],
             ['新一线城市', '杭州市', '浙江'],
             ['新一线城市', '武汉市', '湖北'],
             ['新一线城市', '西安市', '陕西'],
             ['新一线城市', '天津市', '天津'],
             ['新一线城市', '苏州市', '江苏'],
             ['新一线城市', '南京市', '江苏'],
             ['新一线城市', '郑州市', '河南'],
             ['新一线城市', '长沙市', '湖南'],
             ['新一线城市', '东莞市', '广东'],
             ['新一线城市', '青岛市', '山东'],
             ['新一线城市', '合肥市', '安徽'],
             ['新一线城市', '佛山市', '广东'],
             ['新一线城市', '宁波市', '浙江'],
             ['二线城市', '沈阳市', '辽宁'],
             ['二线城市', '无锡市', '江苏'],
             ['二线城市', '大连市', '辽宁'],
             ['二线城市', '福州市', '福建'],
             ['二线城市', '厦门市', '福建'],
             ['二线城市', '哈尔滨市', '黑龙江'],
             ['二线城市', '济南市', '山东'],
             ['二线城市', '温州市', '浙江'],
             ['二线城市', '南宁市', '广西'],
             ['二线城市', '长春市', '吉林'],
             ['二线城市', '泉州市', '福建'],
             ['二线城市', '石家庄市', '河北'],
             ['二线城市', '贵阳市', '贵州'],
             ['二线城市', '南昌市', '江西'],
             ['二线城市', '金华市', '浙江'],
             ['二线城市', '常州市', '江苏'],
             ['二线城市', '南通市', '江苏'],
             ['二线城市', '嘉兴市', '浙江'],
             ['二线城市', '太原市', '山西'],
             ['二线城市', '徐州市', '江苏'],
             ['二线城市', '惠州市', '广东'],
             ['二线城市', '珠海市', '广东'],
             ['二线城市', '中山市', '广东'],
             ['二线城市', '台州市', '浙江'],
             ['二线城市', '烟台市', '山东'],
             ['二线城市', '兰州市', '甘肃'],
             ['二线城市', '绍兴市', '浙江'],
             ['二线城市', '海口市', '海南'],
             ['二线城市', '扬州市', '江苏'],
             ['二线城市', '昆明市', '云南'],
             ['三线城市', '汕头市', '广东'],
             ['三线城市', '揭阳市', '广东'],
             ['三线城市', '江门市', '广东'],
             ['三线城市', '湛江市', '广东'],
             ['三线城市', '潮州市', '广东'],
             ['三线城市', '肇庆市', '广东'],
             ['三线城市', '清远市', '广东'],
             ['三线城市', '梅州市', '广东'],
             ['三线城市', '湖州市', '浙江'],
             ['三线城市', '舟山市', '浙江'],
             ['三线城市', '丽水市', '浙江'],
             ['三线城市', '镇江市', '江苏'],
             ['三线城市', '盐城市', '江苏'],
             ['三线城市', '泰州市', '江苏'],
             ['三线城市', '淮安市', '江苏'],
             ['三线城市', '连云港市', '江苏'],
             ['三线城市', '宿迁市', '江苏'],
             ['三线城市', '潍坊市', '山东'],
             ['三线城市', '临沂市', '山东'],
             ['三线城市', '济宁市', '山东'],
             ['三线城市', '淄博市', '山东'],
             ['三线城市', '威海市', '山东'],
             ['三线城市', '泰安市', '山东'],
             ['三线城市', '保定市', '河北'],
             ['三线城市', '唐山市', '河北'],
             ['三线城市', '廊坊市', '河北'],
             ['三线城市', '邯郸市', '河北'],
             ['三线城市', '沧州市', '河北'],
             ['三线城市', '秦皇岛市', '河北'],
             ['三线城市', '洛阳市', '河南'],
             ['三线城市', '商丘市', '河南'],
             ['三线城市', '南阳市', '河南'],
             ['三线城市', '新乡市', '河南'],
             ['三线城市', '乌鲁木齐市', '新疆'],
             ['三线城市', '漳州市', '福建'],
             ['三线城市', '莆田市', '福建'],
             ['三线城市', '宁德市', '福建'],
             ['三线城市', '龙岩市', '福建'],
             ['三线城市', '三明市', '福建'],
             ['三线城市', '南平市', '福建'],
             ['三线城市', '九江市', '江西'],
             ['三线城市', '赣州市', '江西'],
             ['三线城市', '上饶市', '江西'],
             ['三线城市', '呼和浩特市', '内蒙古'],
             ['三线城市', '包头市', '内蒙古'],
             ['三线城市', '芜湖市', '安徽'],
             ['三线城市', '蚌埠市', '安徽'],
             ['三线城市', '阜阳市', '安徽'],
             ['三线城市', '马鞍山市', '安徽'],
             ['三线城市', '滁州市', '安徽'],
             ['三线城市', '安庆市', '安徽'],
             ['三线城市', '桂林市', '广西'],
             ['三线城市', '柳州市', '广西'],
             ['三线城市', '银川市', '宁夏'],
             ['三线城市', '三亚市', '海南'],
             ['三线城市', '遵义市', '贵州'],
             ['三线城市', '绵阳市', '四川'],
             ['三线城市', '南充市', '四川'],
             ['三线城市', '宜昌市', '湖北'],
             ['三线城市', '襄阳市', '湖北'],
             ['三线城市', '荆州市', '湖北'],
             ['三线城市', '黄冈市', '湖北'],
             ['三线城市', '咸阳市', '陕西'],
             ['三线城市', '衡阳市', '湖南'],
             ['三线城市', '株洲市', '湖南'],
             ['三线城市', '湘潭市', '湖南'],
             ['三线城市', '岳阳市', '湖南'],
             ['三线城市', '郴州市', '湖南'],
             ['三线城市', '大庆市', '黑龙江'],
             ['三线城市', '鞍山市', '辽宁'],
             ['三线城市', '吉林市', '吉林'],
             ['三线城市', '信阳市', '河南'],
             ['四线城市', '韶关市', '广东'],
             ['四线城市', '常德市', '湖南'],
             ['四线城市', '六安市', '安徽'],
             ['四线城市', '汕尾市', '广东'],
             ['四线城市', '西宁市', '青海'],
             ['四线城市', '茂名市', '广东'],
             ['四线城市', '驻马店市', '河南'],
             ['四线城市', '邢台市', '河北'],
             ['四线城市', '宜春市', '江西'],
             ['四线城市', '大理市', '云南'],
             ['四线城市', '大理白族自治州', '云南'],
             ['四线城市', '丽江市', '云南'],
             ['四线城市', '延边朝鲜族自治州', '吉林'],
             ['四线城市', '衢州市', '浙江'],
             ['四线城市', '黔东南苗族侗族自治州', '贵州'],
             ['四线城市', '景德镇市', '江西'],
             ['四线城市', '开封市', '河南'],
             ['四线城市', '红河哈尼族彝族自治州', '云南'],
             ['四线城市', '北海市', '广西'],
             ['四线城市', '东营市', '山东'],
             ['四线城市', '怀化市', '湖南'],
             ['四线城市', '阳江市', '广东'],
             ['四线城市', '菏泽市', '山东'],
             ['四线城市', '黔南布依族苗族自治州', '贵州'],
             ['四线城市', '宿州市', '安徽'],
             ['四线城市', '日照市', '山东'],
             ['四线城市', '黄石市', '湖北'],
             ['四线城市', '周口市', '河南'],
             ['四线城市', '晋中市', '山西'],
             ['四线城市', '许昌市', '河南'],
             ['四线城市', '拉萨市', '西藏'],
             ['四线城市', '锦州市', '辽宁'],
             ['四线城市', '佳木斯市', '黑龙江'],
             ['四线城市', '淮南市', '安徽'],
             ['四线城市', '淮北市', '安徽'],
             ['四线城市', '抚州市', '江西'],
             ['四线城市', '营口市', '辽宁'],
             ['四线城市', '曲靖市', '云南'],
             ['四线城市', '齐齐哈尔市', '黑龙江'],
             ['四线城市', '牡丹江市', '黑龙江'],
             ['四线城市', '河源市', '广东'],
             ['四线城市', '德阳市', '四川'],
             ['四线城市', '邵阳市', '湖南'],
             ['四线城市', '孝感市', '湖北'],
             ['四线城市', '焦作市', '河南'],
             ['四线城市', '益阳市', '湖南'],
             ['四线城市', '张家口市', '河北'],
             ['四线城市', '运城市', '山西'],
             ['四线城市', '大同市', '山西'],
             ['四线城市', '德州市', '山东'],
             ['四线城市', '玉林市', '广西'],
             ['四线城市', '榆林市', '陕西'],
             ['四线城市', '平顶山市', '河南'],
             ['四线城市', '盘锦市', '辽宁'],
             ['四线城市', '渭南市', '陕西'],
             ['四线城市', '安阳市', '河南'],
             ['四线城市', '铜仁市', '贵州'],
             ['四线城市', '宣城市', '安徽'],
             ['四线城市', '永州市', '湖南'],
             ['四线城市', '黄山市', '安徽'],
             ['四线城市', '西双版纳傣族自治州', '云南'],
             ['四线城市', '十堰市', '湖北'],
             ['四线城市', '宜宾市', '四川'],
             ['四线城市', '丹东市', '辽宁'],
             ['四线城市', '乐山市', '四川'],
             ['四线城市', '吉安市', '江西'],
             ['四线城市', '宝鸡市', '陕西'],
             ['四线城市', '鄂尔多斯市', '内蒙古'],
             ['四线城市', '铜陵市', '安徽'],
             ['四线城市', '娄底市', '湖南'],
             ['四线城市', '六盘水市', '贵州'],
             ['四线城市', '承德市', '河北'],
             ['四线城市', '保山市', '云南'],
             ['四线城市', '毕节市', '贵州'],
             ['四线城市', '泸州市', '四川'],
             ['四线城市', '恩施土家族苗族自治州', '湖北'],
             ['四线城市', '安顺市', '贵州'],
             ['四线城市', '枣庄市', '山东'],
             ['四线城市', '聊城市', '山东'],
             ['四线城市', '百色市', '广西'],
             ['四线城市', '临汾市', '山西'],
             ['四线城市', '梧州市', '广西'],
             ['四线城市', '亳州市', '安徽'],
             ['四线城市', '德宏傣族景颇族自治州', '云南'],
             ['四线城市', '鹰潭市', '江西'],
             ['四线城市', '滨州市', '山东'],
             ['四线城市', '绥化市', '黑龙江'],
             ['四线城市', '眉山市', '四川'],
             ['四线城市', '赤峰市', '内蒙古'],
             ['四线城市', '咸宁市', '湖北'],
             ['五线城市', '防城港市', '广西'],
             ['五线城市', '玉溪市', '云南'],
             ['五线城市', '呼伦贝尔市', '内蒙古'],
             ['五线城市', '普洱市', '云南'],
             ['五线城市', '葫芦岛市', '辽宁'],
             ['五线城市', '楚雄彝族自治州', '云南'],
             ['五线城市', '衡水市', '河北'],
             ['五线城市', '抚顺市', '辽宁'],
             ['五线城市', '钦州市', '广西'],
             ['五线城市', '四平市', '吉林'],
             ['五线城市', '汉中市', '陕西'],
             ['五线城市', '黔西南布依族苗族自治州', '贵州'],
             ['五线城市', '内江市', '四川'],
             ['五线城市', '湘西土家族苗族自治州', '湖南'],
             ['五线城市', '漯河市', '河南'],
             ['五线城市', '新余市', '江西'],
             ['五线城市', '延安市', '陕西'],
             ['五线城市', '长治市', '山西'],
             ['五线城市', '文山壮族苗族自治州', '云南'],
             ['五线城市', '云浮市', '广东'],
             ['五线城市', '贵港市', '广西'],
             ['五线城市', '昭通市', '云南'],
             ['五线城市', '河池市', '广西'],
             ['五线城市', '达州市', '四川'],
             ['五线城市', '濮阳市', '河南'],
             ['五线城市', '通化市', '吉林'],
             ['五线城市', '松原市', '吉林'],
             ['五线城市', '通辽市', '内蒙古'],
             ['五线城市', '广元市', '四川'],
             ['五线城市', '鄂州市', '湖北'],
             ['五线城市', '凉山彝族自治州', '四川'],
             ['五线城市', '张家界市', '湖南'],
             ['五线城市', '荆门市', '湖北'],
             ['五线城市', '来宾市', '广西'],
             ['五线城市', '忻州市', '山西'],
             ['五线城市', '克拉玛依市', '新疆'],
             ['五线城市', '遂宁市', '四川'],
             ['五线城市', '朝阳市', '辽宁'],
             ['五线城市', '崇左市', '广西'],
             ['五线城市', '辽阳市', '辽宁'],
             ['五线城市', '广安市', '四川'],
             ['五线城市', '萍乡市', '江西'],
             ['五线城市', '阜新市', '辽宁'],
             ['五线城市', '吕梁市', '山西'],
             ['五线城市', '池州市', '安徽'],
             ['五线城市', '贺州市', '广西'],
             ['五线城市', '本溪市', '辽宁'],
             ['五线城市', '铁岭市', '辽宁'],
             ['五线城市', '自贡市', '四川'],
             ['五线城市', '锡林郭勒盟', '内蒙古'],
             ['五线城市', '白城市', '吉林'],
             ['五线城市', '白山市', '吉林'],
             ['五线城市', '雅安市', '四川'],
             ['五线城市', '酒泉市', '甘肃'],
             ['五线城市', '天水市', '甘肃'],
             ['五线城市', '晋城市', '山西'],
             ['五线城市', '巴彦淖尔市', '内蒙古'],
             ['五线城市', '随州市', '湖北'],
             ['五线城市', '兴安盟', '内蒙古'],
             ['五线城市', '临沧市', '云南'],
             ['五线城市', '鸡西市', '黑龙江'],
             ['五线城市', '迪庆藏族自治州', '云南'],
             ['五线城市', '攀枝花市', '四川'],
             ['五线城市', '鹤壁市', '河南'],
             ['五线城市', '黑河市', '黑龙江'],
             ['五线城市', '双鸭山市', '黑龙江'],
             ['五线城市', '三门峡市', '河南'],
             ['五线城市', '安康市', '陕西'],
             ['五线城市', '乌兰察布市', '内蒙古'],
             ['五线城市', '庆阳市', '甘肃'],
             ['五线城市', '伊犁哈萨克自治州', '新疆'],
             ['五线城市', '儋州市', '海南'],
             ['五线城市', '哈密市', '新疆'],
             ['五线城市', '海西蒙古族藏族自治州', '青海'],
             ['五线城市', '甘孜藏族自治州', '四川'],
             ['五线城市', '伊春市', '黑龙江'],
             ['五线城市', '陇南市', '甘肃'],
             ['五线城市', '乌海市', '内蒙古'],
             ['五线城市', '林芝市', '西藏'],
             ['五线城市', '怒江傈僳族自治州', '云南'],
             ['五线城市', '朔州市', '山西'],
             ['五线城市', '阳泉市', '山西'],
             ['五线城市', '嘉峪关市', '甘肃'],
             ['五线城市', '鹤岗市', '黑龙江'],
             ['五线城市', '张掖市', '甘肃'],
             ['五线城市', '辽源市', '吉林'],
             ['五线城市', '吴忠市', '宁夏'],
             ['五线城市', '昌吉回族自治州', '新疆'],
             ['五线城市', '大兴安岭地区', '黑龙江'],
             ['五线城市', '巴音郭楞蒙古自治州', '新疆'],
             ['五线城市', '阿坝藏族羌族自治州', '四川'],
             ['五线城市', '日喀则市', '西藏'],
             ['五线城市', '阿拉善盟', '内蒙古'],
             ['五线城市', '巴中市', '四川'],
             ['五线城市', '平凉市', '甘肃'],
             ['五线城市', '阿克苏地区', '新疆'],
             ['五线城市', '定西市', '甘肃'],
             ['五线城市', '商洛市', '陕西'],
             ['五线城市', '金昌市', '甘肃'],
             ['五线城市', '七台河市', '黑龙江'],
             ['五线城市', '石嘴山市', '宁夏'],
             ['五线城市', '白银市', '甘肃'],
             ['五线城市', '铜川市', '陕西'],
             ['五线城市', '武威市', '甘肃'],
             ['五线城市', '吐鲁番市', '新疆'],
             ['五线城市', '固原市', '宁夏'],
             ['五线城市', '山南市', '西藏'],
             ['五线城市', '临夏回族自治州', '甘肃'],
             ['五线城市', '海东市', '青海'],
             ['五线城市', '喀什地区', '新疆'],
             ['五线城市', '甘南藏族自治州', '甘肃'],
             ['五线城市', '昌都市', '西藏'],
             ['五线城市', '中卫市', '宁夏'],
             ['五线城市', '资阳市', '四川'],
             ['五线城市', '阿勒泰地区', '新疆'],
             ['五线城市', '塔城地区', '新疆'],
             ['五线城市', '博尔塔拉蒙古自治州', '新疆'],
             ['五线城市', '海南藏族自治州', '青海'],
             ['五线城市', '克孜勒苏柯尔克孜自治州', '新疆'],
             ['五线城市', '阿里地区', '西藏'],
             ['五线城市', '和田地区', '新疆'],
             ['五线城市', '玉树藏族自治州', '青海'],
             ['五线城市', '那曲市', '西藏'],
             ['五线城市', '黄南藏族自治州', '青海'],
             ['五线城市', '海北藏族自治州', '青海'],
             ['五线城市', '果洛藏族自治州', '青海'],
             ['五线城市', '三沙市', '海南']]
    city_ = pd.DataFrame(data=city_, columns=['城市等级', '城市', '省份'])
    return city_


def get_th():
    pass


if __name__ == '__main__':
    c = city()
    d = pov()
    print(len(c))
    c.to_csv(os.path.join('/Users/xigua/Downloads', '城市等级.csv'), encoding='utf-8_sig', index=False, header=True)
    d.to_csv(os.path.join('/Users/xigua/Downloads', '地理区域.csv'), encoding='utf-8_sig', index=False, header=True)

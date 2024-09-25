# encoding: utf-8

from enum import Enum


class ShopTypeModel(str, Enum):
    """
    店铺类型枚举
    """
    # 京东自营
    TYPE_1 = '京东自营'
    # 京东自营旗舰店
    TYPE_2 = '京东自营旗舰店'
    # 京东自营专区
    TYPE_3 = '京东自营专区'
    # 京东自营专卖店
    TYPE_4 = '京东自营专卖店'
    # 旗舰店
    TYPE_5 = '旗舰店'
    # 专营店
    TYPE_6 = '专营店'
    # 卖场店
    TYPE_7 = '卖场店'
    # 天猫超市
    TYPE_8 = '天猫超市'
    # 苏宁自营
    TYPE_9 = '苏宁自营'
    # 苏宁自营旗舰店
    TYPE_10 = '苏宁自营旗舰店'
    # 专卖店
    TYPE_11 = '专卖店'
    # 其他
    TYPE_12 = '其他'


class JdDetailTypeModel(str, Enum):
    """
    京东店铺类型细分
    """
    # 京东自营
    TYPE_1 = '京东自营'
    # 京东自营官方旗舰店
    TYPE_2 = '京东自营官方旗舰店'
    # 海外京东自营旗舰店
    TYPE_3 = '海外京东自营旗舰店'
    # 京东自营旗舰店
    TYPE_4 = '京东自营旗舰店'
    # 京东自营专区
    TYPE_5 = '京东自营专区'
    # 海外京东自营专区
    TYPE_6 = '海外京东自营专区'
    # 京东自营专卖店
    TYPE_7 = '京东自营专卖店'
    # 官方旗舰店
    TYPE_8 = '官方旗舰店'
    # 旗舰店
    TYPE_9 = '旗舰店'
    # 海外专营店
    TYPE_10 = '海外专营店'
    # 专营店
    TYPE_11 = '专营店'
    # 海外卖场店
    TYPE_12 = '海外卖场店'
    # 卖场店
    TYPE_13 = '卖场店'
    # 京东企业自营店
    TYPE_14 = '京东企业自营店'
    # 其他
    TYPE_15 = '其他'


class SnDetailTypeModel(str, Enum):
    """
    苏宁店铺类型细分
    """
    # 苏宁自营
    TYPE_1 = '苏宁自营'
    # 苏宁自营旗舰店
    TYPE_2 = '苏宁自营旗舰店'
    # 官方旗舰店
    TYPE_3 = '官方旗舰店'
    # 旗舰店
    TYPE_4 = '旗舰店'
    # 苏宁专卖店
    TYPE_5 = '苏宁专卖店'
    # 专卖店
    TYPE_6 = '专卖店'
    # 苏宁专营店
    TYPE_7 = '苏宁专营店'
    # 专营店
    TYPE_8 = '专营店'
    # 其他
    TYPE_9 = '其他'


class TmallDetailTypeModel(str, Enum):
    """
    天猫店铺类型细分
    """
    # 天猫超市
    TYPE_1 = '天猫超市'
    # 其他
    TYPE_2 = '其他'

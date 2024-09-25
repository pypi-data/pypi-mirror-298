# encoding: utf-8

import logging

from typing import Union, List, Optional
from ..core.model import ShopModel
from ..zcbot.model import ShopTypeModel, JdDetailTypeModel, SnDetailTypeModel, TmallDetailTypeModel

LOGGER = logging.getLogger(__name__)


class ZcbotShopParser(object):
    def __init__(self):
        pass

    def parse_shop(self, plat_code: str, shop_name: str) -> Optional[ShopModel]:

        if plat_code == "jd":
            result = self.parse_jd(shop_name)
            return result
        elif plat_code == "sn":
            result = self.parse_sn(shop_name)
            return result
        elif plat_code == "tmall":
            result = self.parse_tmall(shop_name)
            return result

        return None

    def parse_jd(self, shop_name: str) -> ShopModel:
        shop_model = ShopModel()
        shop_model.plat_code = "jd"
        shop_model.shop_name = shop_name
        if shop_name == "京东自营":
            shop_model.shop_type_code = ShopTypeModel.TYPE_1.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_1.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_1.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_1.value
        elif shop_name.endswith("京东自营官方旗舰店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_2.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_2.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_2.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_2.value
        elif shop_name.endswith("海外京东自营旗舰店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_2.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_2.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_3.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_3.value
        elif shop_name.endswith("京东自营旗舰店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_2.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_2.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_4.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_4.value
        elif shop_name.endswith("海外京东自营专区") or shop_name.endswith("京东海外自营专区"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_3.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_3.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_6.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_6.value
        elif shop_name.endswith("京东自营专区"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_3.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_3.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_5.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_5.value
        elif shop_name.endswith("京东自营专卖店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_4.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_4.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_7.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_7.value
        elif shop_name.endswith("官方旗舰店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_5.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_5.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_8.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_8.value
        elif shop_name.endswith("旗舰店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_5.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_5.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_9.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_9.value
        elif shop_name.endswith("海外专营店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_6.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_6.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_10.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_10.value
        elif shop_name.endswith("专营店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_6.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_6.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_11.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_11.value
        elif shop_name.endswith("海外卖场店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_7.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_7.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_12.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_12.value
        elif shop_name.endswith("卖场店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_7.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_7.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_13.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_13.value
        elif shop_name.endswith("京东企业自营店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_12.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_12.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_14.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_14.value
        else:
            shop_model.shop_type_code = ShopTypeModel.TYPE_12.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_12.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = JdDetailTypeModel.TYPE_15.name
            shop_model.detail_type_name = JdDetailTypeModel.TYPE_15.value

        return shop_model

    def parse_sn(self, shop_name: str) -> Optional[ShopModel]:
        shop_model = ShopModel()
        shop_model.plat_code = "sn"
        shop_model.shop_name = shop_name

        if shop_name == "苏宁自营":
            shop_model.shop_type_code = ShopTypeModel.TYPE_9.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_9.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = SnDetailTypeModel.TYPE_1.name
            shop_model.detail_type_name = SnDetailTypeModel.TYPE_1.value
        elif shop_name.endswith("苏宁自营旗舰店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_10.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_10.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = SnDetailTypeModel.TYPE_2.name
            shop_model.detail_type_name = SnDetailTypeModel.TYPE_2.value
        elif shop_name.endswith("官方旗舰店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_5.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_5.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = SnDetailTypeModel.TYPE_3.name
            shop_model.detail_type_name = SnDetailTypeModel.TYPE_3.value
        elif shop_name.endswith("旗舰店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_5.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_5.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = SnDetailTypeModel.TYPE_4.name
            shop_model.detail_type_name = SnDetailTypeModel.TYPE_4.value
        elif shop_name.endswith("苏宁专卖店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_11.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_11.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = SnDetailTypeModel.TYPE_5.name
            shop_model.detail_type_name = SnDetailTypeModel.TYPE_5.value
        elif shop_name.endswith("专卖店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_11.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_11.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = SnDetailTypeModel.TYPE_6.name
            shop_model.detail_type_name = SnDetailTypeModel.TYPE_6.value
        elif shop_name.endswith("苏宁专营店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_6.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_6.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = SnDetailTypeModel.TYPE_7.name
            shop_model.detail_type_name = SnDetailTypeModel.TYPE_7.value
        elif shop_name.endswith("专营店"):
            shop_model.shop_type_code = ShopTypeModel.TYPE_6.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_6.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = SnDetailTypeModel.TYPE_8.name
            shop_model.detail_type_name = SnDetailTypeModel.TYPE_8.value
        else:
            shop_model.shop_type_code = ShopTypeModel.TYPE_12.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_12.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = SnDetailTypeModel.TYPE_8.name
            shop_model.detail_type_name = SnDetailTypeModel.TYPE_8.value

        return shop_model

    def parse_tmall(self, shop_name: str) -> Optional[ShopModel]:
        shop_model = ShopModel()
        shop_model.plat_code = "tmall"
        shop_model.shop_name = shop_name

        if shop_name == "天猫超市":
            shop_model.shop_type_code = ShopTypeModel.TYPE_8.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_8.value
            shop_model.is_self = "是"
            shop_model.detail_type_code = TmallDetailTypeModel.TYPE_1.name
            shop_model.detail_type_name = TmallDetailTypeModel.TYPE_1.value

        else:
            shop_model.shop_type_code = ShopTypeModel.TYPE_12.name
            shop_model.shop_type_name = ShopTypeModel.TYPE_12.value
            shop_model.is_self = "否"
            shop_model.detail_type_code = TmallDetailTypeModel.TYPE_2.name
            shop_model.detail_type_name = TmallDetailTypeModel.TYPE_2.value

        return shop_model

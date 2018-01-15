# -*- coding=utf-8 -*-

import copy

from tyframework.context import TyContext


class TuYouPayCatTuyou(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        try:
            del chargeinfo['chargeType']
        except:
            pass
        more_categories = TyContext.Configure.get_global_item_json('more_categories_tuyou')
        charge_cats = copy.deepcopy(more_categories)

        price = chargeinfo['chargeTotal']
        if price > 500:
            for i in xrange(len(charge_cats)):
                if 'CAT_PHONECHARGE_CARD' == charge_cats[i]['category']:
                    del charge_cats[i]
                    break

        for cat in charge_cats:
            # cat['desc'] = ''
            cat['summary'] = chargeinfo['diamondName']
            if 'ali' in cat['paytype']:
                cat['tag'] = 'TAG_CHAOZHI'
        chargeinfo['chargeCategories'] = charge_cats

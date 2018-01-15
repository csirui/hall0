# -*- coding=utf-8 -*-

from tyframework.context import TyContext

from tysdk.configure.game_item import GameItemConfigure


class AccountMomo():
    check_url = 'https://game-api.immomo.com/game/2/server/app/check'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        momo_appid = params.get('momo_appid')
        token = params.get('momo_login_code')
        config = TyContext.Configure.get_global_item_json('momo_paykeys', {})
        momo_secret = config.get(momo_appid, '')
        if not momo_secret:
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('momo', 'momo_appid',
                                                                                                 momo_appid, 'momo')
            momo_secret = config.get('momo_secret', '')
            if not momo_secret:
                return False
        post_params = {
            'appid': momo_appid,
            'app_secret': momo_secret,
            'vtoken': token,
            'userid': snsId.split(':')[1]
        }
        repsonse, _ = TyContext.WebPage.webget(cls.check_url, post_params)
        try:
            import json
            response = json.loads(repsonse)
        except:
            return False
        data = response.get('data', {})
        if data.get('sex') == 'M':
            sex = 0
        else:
            sex = 1
        picdata = data.get('photo', [])
        if len(picdata) > 0:
            pic = picdata[0]
            pic_url = 'https://img.momocdn.com/album/%s/%s/%s_S.jpg' % (pic[0:2], pic[2:4], pic)
            params['purl'] = pic_url
            params['headurl'] = pic_url
        params['sex'] = sex
        params['name'] = data.get('name')
        params['snsinfo'] = data.get('name')
        return True

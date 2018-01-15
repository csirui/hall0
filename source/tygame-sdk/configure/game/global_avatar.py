# -*- coding=utf-8 -*-

from pyscript._helper_config_ import *

photoDownloadHttpDomain = 'http://ddz.image.tuyoo.com'
add_global_item('photo.download.http.domain', photoDownloadHttpDomain)

add_global_item('save_photo_service', 'http://10.3.0.4/pic/upload')



def buildAvatarUrl(avatarFileName):
    return '%s/avatar/%s' % (photoDownloadHttpDomain, avatarFileName)

add_global_item('user.avatar.default', [
                buildAvatarUrl('head_cat.png'),
                buildAvatarUrl('head_china.png'),
                buildAvatarUrl('head_coffee.png'),
                #buildAvatarUrl('head_du.png'),
                
                buildAvatarUrl('head_eagle.png'),
                buildAvatarUrl('head_female_0.png'),
                buildAvatarUrl('head_female_1.png'),
                buildAvatarUrl('head_female_2.png'),
                #buildAvatarUrl('head_hanhou.png'),
                
                buildAvatarUrl('head_horse.png'),
                buildAvatarUrl('head_lotus.png'),
                #buildAvatarUrl('head_male_0.png'),
                buildAvatarUrl('head_male_1.png'),
                buildAvatarUrl('head_male_2.png'),
                
                buildAvatarUrl('head_piano.png'),
                buildAvatarUrl('head_sea.png'),
                buildAvatarUrl('head_suv.png'),
                ])

add_global_item('user.avatar.need.verify', 1)
add_global_item('user.avatar.verifying', buildAvatarUrl('head_verifying.png'))

from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse, urlparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              '/method/account.getInfo',
                              urlencode(OrderedDict(fields=','.join(
                                                    ('bdate', 'sex', 'about', 'user_ids', 'lang')),
                                                    access_token=response['access_token'],
                                                    v='5.92')),
                              None
                              ))

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data['sex'] and not user.shopuserprofile.gender:
            if data['sex'] == 2:
                user.shopuserprofile.gender = 'M'
            else:
                user.shopuserprofile.gender = 'W'

        if data['about'] and not user.shopuserprofile.aboutMe:
            user.shopuserprofile.aboutMe = data['about']

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            else:
                user.age = age

        if data['user_ids']:
            user.shopuserprofile.vk_page = 'https://vk.com/id' + data['user_ids']

        if data['lang']:
            if data['lang'] == 0:
                user.shopuserprofile.lang = 'ru'

    user.save()
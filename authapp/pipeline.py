import datetime
from collections import OrderedDict
from urllib.parse import urlunparse, urlencode
import urllib.request

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from django_project.settings import BASE_DIR


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    # api_url = f"https:/api.vk.com/users.get/fields=bdate,about,sex&access_token={response['access_token']}"

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex',
                                                                 'about', 'photo_max')),
                                                access_token=response['access_token'],
                                                v='5.92')),

                          None
                          ))

    resp = requests.get(api_url)

    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    data['email'] = response['email']

    if data['sex']:
        if data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        elif data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    if data['bdate']:
        bdate = datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().year - bdate.year
        if age < age:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['email']:
        user.shopuserprofile.user.email = data['email']

    if data['photo_max']:
        urllib.request.urlretrieve(data['photo_max'], BASE_DIR + f'/media/users_avatars/{user.pk}.jpg')
        user.avatar = f'users_avatars/{user.pk}.jpg'

    user.save()


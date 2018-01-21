import json
import os

import requests

from auth import read_token


DATA_FOLDER = os.path.abspath(os.path.join(__file__, '..', 'data'))
IMAGE_FOLDER = os.path.abspath(os.path.join(__file__, '..', 'data', 'images'))
TOKEN = read_token()


headers = {
    'User-Agent': 'Happn/19.1.0 AndroidSDK/19',
    'platform': 'android',
    'Host': 'api.happn.fr',
    'connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type' : 'application/json',
    'Authorization': 'OAuth="{}"'.format(TOKEN)
}


def recommendations(limit=100, offset=0):
    endpoint = 'https://api.happn.fr/api/users/me/crossings'
    params = {
        'limit': limit,
        'offset': offset,
        'fields': 'id,nb_times,modification_date,notifier.fields(my_relation,is_charmed,availability.fields(id,availability_type.fields(picto.fields(id,is_default),color,emoji,title,tagline,duration,label,type),time_left),last_invite_received,picture.fields(url,id,is_default).width(585).mode(1).height(927.36),school,is_accepted,profiles.limit(9).fields(url,id,is_default).width(1242).mode(1).height(2208),type,job,id,gender,has_charmed_me,workplace,distance,age,already_charmed,social_synchronization.fields(facebook.fields(id)),first_name,is_invited)',
    }
    response = requests.get(endpoint, headers=headers, params=params).json()
    return response['data']


def view_simple(users):
    return [{
        'id': user['notifier']['id'],
        'first_name': user['notifier']['first_name'],
        'facebook': 'https://www.facebook.com/{}'.format(user['notifier']['fb_id']),
        'age': user['notifier']['age'],
        'job': user['notifier']['job'],
        'workplace': user['notifier']['workplace'],
        'school': user['notifier']['school'],
        'images': [profile['url'] for profile in user['notifier']['profiles']],
    } for user in users]


def view_facebook(users):
    return [{
        'first_name': user['notifier']['first_name'],
        'facebook': 'https://www.facebook.com/{}'.format(user['notifier']['fb_id']),
    } for user in users]
    

def get_images_by_id(users):
    return {'{}-{}'.format(user['notifier']['first_name'], user['notifier']['id']): [profile['url'] for profile in user['notifier']['profiles']]
            for user in users}


def save_minettes(minettes, filename='minettes.json'):
    j = json.dumps(minettes, indent=4)
    path = os.path.join(DATA_FOLDER, filename)
    open(path, 'w').write(j)


def download_image(users, download_path):
    download_path = download_path or IMAGE_FOLDER
    users_images = get_images_by_id(users)
    for key, images in users_images.items():
        for index, image in enumerate(images):
            result = requests.get(image).content
            filename = '{}-{}.jpg'.format(key, index)
            path = os.path.join(IMAGE_FOLDER, filename)
            open(path, 'wb').write(result)

    

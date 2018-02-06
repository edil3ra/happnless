import requests
import logging
import robobrowser
import os.path
import yaml


conf_path = os.path.join(os.path.dirname(__file__), '..', 'conf', 'config.yaml')
token_path = os.path.join(os.path.dirname(__file__), '..', 'conf', 'token.txt')
conf = yaml.load(open(conf_path))


headers = {
    'User-Agent': 'Happn/19.1.0 AndroidSDK/19',
    'platform': 'android',
    'Host': 'api.happn.fr',
    'connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}


def get_fbtoken(email, password):
    rb = robobrowser.RoboBrowser(user_agent=conf['mobile_user_agent'], parser="html5lib")
    rb.open(conf['fb_api_key_url'])
    login_form = rb.get_form()
    login_form["pass"] = password
    login_form["email"] = email
    rb.submit_form(login_form)

    token_url = rb.response.history[-2].url
    fb_token = token_url.split('=')[1].split('&')[0]

    return fb_token


def get_happn_token(fb_token):
    h=headers
    h.update({
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Content-Length': '374'
        })

    payload = {
        'client_id': conf['client_id'],
        'client_secret': conf['client_secret'],
        'grant_type': 'assertion',
        'assertion_type':'facebook_access_token',
        'assertion': fb_token,
        'scope': 'mobile_app'
    }
    url = 'https://api.happn.fr/connect/oauth/token'
    try:
        r = requests.post(url, headers=h, data=payload)
    except Exception as e:
        raise Exception('Error Connecting to Happn Server: {}'.format(e))

    # Check response validity
    if r.status_code == 200:
        logging.debug('Fetched Happn OAuth token:, %s', r.json()['access_token'])
        return r.json()['access_token'], r.json()['user_id']
    else:
        # Error code returned from server (but server was accessible)
        logging.warning('Server denied request for OAuth token. Status: %d', r.status_code)
        raise Exception(r.status_code)


def login(email=None, password=None, fb_token=None):
    '''
    Args:
        email (str): facebook email
        password (str): facebook password
        fb_token (str): fb_token
    Returns:
        (str): acces_token,
    '''

    if fb_token is None:
        if email is None or password is None:
            raise Exception('missing facebook email and password email')
        fb_token = get_fbtoken(email, password)

    if fb_token is None:
        raise Exception('missing fb_token ')

    return get_happn_token(fb_token)[0]


def write_token(token):
    open(token_path, 'w').write(token)


def read_token():
    if not os.path.exists(token_path):
        raise Exception('token does not exist yet')
    return open(token_path, 'r').read()

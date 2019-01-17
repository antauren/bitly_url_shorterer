import os
import sys
import requests
from urllib.parse import urlparse

from dotenv import load_dotenv

BASE_URL = 'https://api-ssl.bitly.com/v4/bitlinks'


def is_correct_link(url):
    try:
        response = requests.get(url)
        return response.ok
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.MissingSchema:
        return False
    except requests.exceptions.InvalidSchema:
        return False


def make_bitlink(url, token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    params = {'long_url': url}

    response = requests.post(BASE_URL,
                             headers=headers,
                             json=params
                             )

    return response.json()['link']


def get_total_clicks(url, token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    params = {'unit': 'day', 'units': -1}
    parsed_url = urlparse(url)

    bitly_URL_ = '{}/{}{}/clicks/summary'.format(BASE_URL, parsed_url.netloc, parsed_url.path)

    response = requests.get(bitly_URL_,
                            headers=headers,
                            params=params
                            )

    return response.json()['total_clicks']


def is_bitly(url):
    netloc = urlparse(url).netloc

    domens = {'bit.ly',
              'bit.com',
              'j.mp'}

    return netloc in domens


def get_link_from_sys_args():
    argv = sys.argv[1:]

    return argv[0] if argv else None


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN')

    url = get_link_from_sys_args()

    if url is None:
        print('Вызов ф-и должен выглядеть так:\n'
              'python main.py https://dvmn.org/')

    elif not is_correct_link(url):
        print('Ваша ссылка не работает')
    elif is_bitly(url):
        total_clicks = get_total_clicks(url, token)
        print('Количество кликов по ссылке {} равно {}.'.format(url, total_clicks))

    else:
        bitlink = make_bitlink(url, token)
        print('Короткая ссылка:', bitlink)

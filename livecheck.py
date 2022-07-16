import requests
import sys
from lxml import etree


def fetch_gh_latest_tag(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Failed to fetch GitHub tag when livechecking {repo}.')
        sys.exit(1)
    if 'tag_name' in response.json():
        return response.json()["tag_name"]
    else:
        print('GitHub tag is not found.')
        return response.json()


def fetch_easyeda_latest_ver(name):
    # https://easyeda.com/api/latestClientVersion
    if name.startswith('easyeda'):
        response = requests.get("https://easyeda.com/page/download")
    if name.startswith('lceda'):
        response = requests.get("https://lceda.cn/page/download")
    if response.status_code != 200:
        print(f'Failed to fetch EasyEDA website when livechecking {name}.')
        sys.exit(1)
    content = etree.HTML(response.text)
    if name.find('pro') == -1:
        x_path = "//table[1]/tr[3]/td[3]/div/div/span[2]/a"
    else:
        x_path = "//table[1]/tr[2]/td[3]/div/div/span[2]/a"
    dl_link = content.xpath(x_path)[0].get('href')
    return '.'.join(dl_link.split('-')[-1].split('.')[:-1])


def fetch_live_ver(name):
    if name == 'anime4k':
        return fetch_gh_latest_tag('bloc97', 'Anime4K')

    if name == 'bbg':
        return fetch_gh_latest_tag('bbg-contributors', 'bbg')

    if name == 'gqrx-scanner':
        return fetch_gh_latest_tag('neural75', 'gqrx-scanner')

    if name == 'docsify-cli':
        return fetch_gh_latest_tag('docsifyjs', 'docsify-cli')

    if name == 'easyeda-bin':
        return fetch_easyeda_latest_ver('easyeda-bin')

    if name == 'easyeda-pro-bin':
        return fetch_easyeda_latest_ver('easyeda-pro-bin')

    if name == 'lceda-bin':
        return fetch_easyeda_latest_ver('lceda-bin')

    if name == 'lceda-pro-bin':
        return fetch_easyeda_latest_ver('lceda-pro-bin')

    return None

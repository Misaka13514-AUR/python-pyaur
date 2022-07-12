import sys
import requests
import pandas as pd
from envconfig import *
from .ArchlinuxUserRepositoryPackage import *


def env_check():
    global github_repo_owner
    global repository_path

    if aur_username == '':
        print('AUR username is not set.')
        sys.exit(1)
    if mirror:
        if github_repo_owner == '':
            if github_username == '':
                print('GitHub username is not set.')
                sys.exit(1)
            else:
                github_repo_owner = github_username
        if repository_path == '':
            repository_path = 'repos'


def fetch_aur(aur_username):
    url = "https://aur.archlinux.org/packages"
    params = {'SeB': 'M', 'K': aur_username, 'SB': 'n', 'SO': 'a', 'PP': 250}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print('Failed to fetch AUR packages.')
        sys.exit(1)
    df = pd.read_html(response.text)[0]
    return df


def parse_df(df):
    packages = {}
    for index, row in df.iterrows():
        packages[row['Name']] = ArchlinuxUserRepositoryPackage(
            row['Name'], row['Version'], row['Description'])
    return packages

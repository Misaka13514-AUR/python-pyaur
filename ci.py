import os
import sys
import requests
import pandas as pd
from pyaur import *
from envconfig import *

if __name__ == '__main__':
    env_check()
    if os.path.exists('packages.csv'):
        df = pd.read_csv('packages.csv')
        packages = parse_df(df)
    else:
        packages = {}

    df_new = fetch_aur(aur_username)
    packages_new = parse_df(df_new)

    for name, package in packages_new.items():
        if name in packages:
            if package.diff(packages[name]):
                print(f"Update package: {package.name}")
                package.sync()
            else:
                print(f"No update: {package.name}")
        else:
            print(f"New package: {package.name}")
            package.create()
            package.sync()

    for name, package in packages.items():
        if name not in packages_new:
            print(f'{package.name} is not in the AUR anymore')
    df_new.to_csv('packages.csv', index=False)

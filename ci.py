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
        packages = []

    df_new = fetch_aur(aur_username)
    packages_new = parse_df(df_new)

    package_dicts = {}
    for package in packages:
        package_dicts[package.name] = package.version
    package_dicts_new = {}
    for package in packages_new:
        package_dicts_new[package.name] = package.version

    for package in packages:
        if package.name not in package_dicts_new:
            print(f'{package.name} is not in the AUR anymore')

    for package in packages_new:
        if package.name not in package_dicts:
            print(f"New package: {package.name}")
            package.create()
            package.sync()
        elif package.version != package_dicts[package.name]:
            print(f"Update package: {package.name}")
            package.sync()
        else:
            print(f"No update: {package.name}")

    df_new.to_csv('packages.csv', index=False)

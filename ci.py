import os
import pandas as pd
from pyaur import *
from envconfig import *

if __name__ == '__main__':
    env_check()
    if os.path.exists('packages.csv'):
        print('Reading old packages.csv...')
        df = pd.read_csv('packages.csv')
        packages = parse_df(df)
    else:
        packages = {}

    print('Fetching AUR packages...')
    df_new = fetch_aur(aur_username)
    packages_new = parse_df(df_new)

    print('Updating packages mirror...')
    mirror_no_update_list = []
    for name, package in packages_new.items():
        if name in packages:
            if package.diff(packages[name]):
                print(f"Update package: {name}")
                package.sync()
            else:
                mirror_no_update_list.append(name)
        else:
            print(f"New package: {name}")
            package.create()
            package.sync()
    if len(mirror_no_update_list) > 0:
        print(f"No update packages: {mirror_no_update_list}")

    mirror_nonexistent_list = []
    for name, package in packages.items():
        if name not in packages_new:
            mirror_nonexistent_list.append(name)
    if len(mirror_nonexistent_list) > 0:
        print(f"Nonexistent packages: {mirror_nonexistent_list}")

    print('Livechecking...')
    livecheck_vcs_list = []
    livecheck_not_checked_list = []
    livecheck_no_update_list = []
    for name, package in packages_new.items():
        if name.endswith('git'):
            livecheck_vcs_list.append(name)
            continue

        package_ver = package.version.split('-')[0]
        livecheck_ver = package.livecheck()

        if livecheck_ver is None:
            livecheck_not_checked_list.append(name)
            continue

        if livecheck_ver.startswith('v') and not package_ver.startswith('v'):
            livecheck_ver = livecheck_ver[1:]
        if package_ver == livecheck_ver:
            livecheck_no_update_list.append(name)
        else:
            print(f"{name} is outdated.", )
            print(f"({package_ver} != {livecheck_ver})")

    if len(livecheck_vcs_list) > 0:
        print(f"Skipped VCS packages: {livecheck_vcs_list}")
    if len(livecheck_not_checked_list) > 0:
        print(f"Packages without livecheck: {livecheck_not_checked_list}")
    if len(livecheck_no_update_list) > 0:
        print(f"Up to date packages: {livecheck_no_update_list}")

    print('Saving packages.csv...')
    df_new.to_csv('packages.csv', index=False)

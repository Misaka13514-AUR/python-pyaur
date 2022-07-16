import os
import sys
import requests
from envconfig import *
from livecheck import fetch_live_ver


class ArchlinuxUserRepositoryPackage:

    def __init__(self, name, version, description=''):
        self.name = name
        self.version = version
        self.description = description
        self.url = f"https://aur.archlinux.org/{name}.git"
        self.pretty_url = f"https://aur.archlinux.org/packages/{name}"
        if mirror:
            if github_username == '' or github_token == '':
                self.mirror_url = \
                    "https://github.com/" \
                    + f"{github_repo_owner}/{name}.git"
            else:
                self.mirror_url = \
                    f"https://{github_username}:{github_token}@github.com/" \
                    + f"{github_repo_owner}/{name}.git"

    def diff(self, package):
        if self.name != package.name \
           or self.version != package.version \
           or self.description != package.description:
            return True
        else:
            return False

    def create(self):
        if not mirror:
            print('Mirror is not enabled.')
            sys.exit(1)
        # use gh api to create repo
        requests.post(f"https://api.github.com/orgs/{github_repo_owner}/repos",
                      headers={
                          "Authorization": f"token {github_token}",
                          "Content-Type": "application/json"
                      },
                      json={"name": self.name})

    def sync(self):
        if not mirror:
            print('Mirror is not enabled.')
            sys.exit(1)
        try:
            if not os.path.isdir(f"{repository_path}/{self.name}.git"):
                os.chdir(f"{repository_path}")
                os.system(f"git clone --mirror {self.url}")
                os.chdir("..")
            os.chdir(f"{repository_path}/{self.name}.git")
            os.system(f"git remote set-url --push origin {self.mirror_url}")
            os.system("git fetch -p origin")
            os.system("git push --mirror")
            os.chdir("../..")
        except Exception as e:
            print(e)
            sys.exit(1)
        # use gh api to update repo
        resp = requests.patch(
            f"https://api.github.com/repos/{github_repo_owner}/{self.name}",
            headers={
                "Authorization": f"token {github_token}",
                "Content-Type": "application/json"
            },
            json={
                "description": self.description,
                "homepage": self.pretty_url
            })

    def livecheck(self):
        return fetch_live_ver(self.name)

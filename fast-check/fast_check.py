#!/usr/local/bin/python3

import os
import base64
import urllib.request
import getpass
import json
from abc import ABC, abstractmethod

LDAP_GROUPS = [
    "ssg-jira-servicedesk-project-FAST",
    "sg-re-jenkins-admins",
]


class Check(ABC):
    def __init__(self, url, name=None):
        self.url = url
        self.name = name or ""

    @abstractmethod
    def process(self, response):
        raise NotImplementedError("Must override process")

    def check(self, usr=None, pwd=None):
        usr = usr or ""
        pwd = pwd or ""
        request = urllib.request.Request(self.url)
        base64string = base64.standard_b64encode(
            f"{usr}:{pwd}".encode("utf-8")
        )
        request.add_header("Authorization", f"Basic {base64string.decode('utf-8')}")
        request.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(request) as data:
                self.process(json.loads(data.read().decode("utf-8")))

        except urllib.error.HTTPError as e:
            print(f"Error checking {self.name}: {e}")


class Bitbucket(Check):
    def __init__(self):
        super().__init__(
            "https://git.splunk.com/rest/api/1.0/logs/rootLogger",
            "bitbucket admin"
        )

    def process(self, response):
        print("You are a bitbucket admin!")


class Ldap(Check):
    def __init__(self):
        super().__init__(
            "https://jenkins-ee.splunkeng.com/whoAmI/api/json", "ldap groups"
        )

    def process(self, response):
        print("You have ldap groups:")
        groups = response["authorities"]
        for g in LDAP_GROUPS:
            if g in groups:
                print(f"Member of {g}")
            else:
                print(f"MISSING {g}")

CHECKS=[
    Bitbucket(),
    Ldap()
]

def main():
    pwd = getpass.getpass(prompt="Enter Password: ", stream=None)
    usr = os.environ["USER"]

    for check in CHECKS:
        check.check(usr,pwd)

if __name__ == "__main__":
    main()

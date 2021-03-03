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
    def __init__(self, url, name=None, usr=None, pwd=None):
        self.url = url
        self.name = name or ""
        self.usr = usr or ""
        self.pwd = pwd or ""

    @abstractmethod
    def process(self, response):
        raise NotImplementedError("Must override process")

    def check(self):
        request = urllib.request.Request(self.url)
        base64string = base64.standard_b64encode(
            f"{self.usr}:{self.pwd}".encode("utf-8")
        )
        request.add_header("Authorization", f"Basic {base64string.decode('utf-8')}")
        request.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(request) as data:
                self.process(json.loads(data.read().decode("utf-8")))

        except urllib.error.HTTPError as e:
            print(f"Error checking {self.name}: {e}")


class Bitbucket(Check):
    def __init__(self, usr, pwd):
        super().__init__(
            "https://git.splunk.com/rest/api/1.0/logs/rootLogger",
            "bitbucket admin",
            usr,
            pwd,
        )

    def process(self, response):
        print("You are a bitbucket admin!")


class Ldap(Check):
    def __init__(self, usr, pwd):
        super().__init__(
            "https://jenkins-ee.splunkeng.com/whoAmI/api/json", "ldap groups", usr, pwd
        )

    def process(self, response):
        print("You have ldap groups:")
        groups = response["authorities"]
        for g in LDAP_GROUPS:
            if g in groups:
                print(f"Member of {g}")
            else:
                print(f"MISSING {g}")


def main():
    pwd = getpass.getpass(prompt="Enter Password: ", stream=None)
    usr = os.environ["USER"]

    bb = Bitbucket(usr, pwd)
    ldap = Ldap(usr, pwd)

    bb.check()
    ldap.check()


if __name__ == "__main__":
    main()
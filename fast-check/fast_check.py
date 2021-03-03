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

pwd = getpass.getpass(prompt="Enter Password: ", stream=None)
usr = os.environ["USER"]


class Check(ABC):
    def __init__(self, url, name):
        self.url = url
        self.name = name

    @abstractmethod
    def process(self, response):
        raise NotImplementedError("Must override check")

    def check(self):
        request = urllib.request.Request(self.url)
        base64string = base64.standard_b64encode(f"{usr}:{pwd}".encode("utf-8"))
        request.add_header("Authorization", f"Basic {base64string.decode('utf-8')}")
        request.add_header("Content-Type", "application/json")

        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print(f"Error checking {self.name}: {e}")
        else:
            self.process(response)


class Bitbucket(Check):
    def __init__(self):
        super().__init__(
            "https://git.splunk.com/rest/api/1.0/logs/rootLogger", "bitbucket admin"
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
        data = response.read()
        encoding = response.info().get_content_charset("utf-8")
        whoami = json.loads(data.decode(encoding))
        groups = whoami["authorities"]
        for g in LDAP_GROUPS:
            if g in groups:
                print(f"member of {g}")
            else:
                print(f"MISSING {g}")


bb = Bitbucket()
ldap = Ldap()

bb.check()
ldap.check()
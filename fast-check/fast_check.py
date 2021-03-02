import os
import base64
import urllib.request
import getpass

pwd = getpass.getpass(prompt="Enter Password: ", stream=None)
usr = os.environ["USER"]

request = urllib.request.Request("https://git.splunk.com/rest/api/1.0/admin/cluster")
str = f"{usr}:{pwd}"
base64string = base64.standard_b64encode(str.encode("utf-8"))
request.add_header("Authorization", f"Basic {base64string.decode('utf-8')}")
request.add_header("Content-Type", "application/json")

try:
    result = urllib.request.urlopen(request)
except urllib.error.HTTPError as e:
    print(f"You are not a bitbucket sys admin!")
    print(e)
else:
    print("You are a bitbucket sys admin!")
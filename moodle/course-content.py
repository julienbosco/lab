import os
import json
import requests
from bs4 import BeautifulSoup
import http.cookiejar
import execjs
import re

MOODLE_BASE_URL = "https://moodle.cegepsherbrooke.qc.ca"

# Retrieve environment variables
username = os.environ["MOODLE_USER"]
password = os.environ["MOODLE_PASS"]
course_id = os.environ["MOODLE_COURSE"]

# Moodle login URL and course URL
login_url = f"{MOODLE_BASE_URL}/login/index.php"
course_url = f"{MOODLE_BASE_URL}/course/view.php?id={course_id}"

# Create a session to maintain cookies
session = requests.Session()

# Create a CookieJar to store cookies
session.cookies = http.cookiejar.CookieJar()

# Login to Moodle
login_data = {
    "username": username,
    "password": password
}
response = session.post(login_url, data=login_data)

# Check for anti-bot cookie mechanism
if "Antibot-cookie" in response.text:
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script")
    js_code = script_tag.string
    
    # Custom implementation of the document object
    custom_document = """
    var document = {
        _cookie: '',
        get cookie() {
            return this._cookie;
        },
        set cookie(value) {
            this._cookie = value;
        },
        location: {
            reload() {}
        }
    };
    """
    
    js_code = custom_document + js_code
    
    ctx = execjs.compile(js_code)
    ctx.call("go")
    cookie_value = ctx.eval("document.cookie")
    
    # Set the Antibot-cookie
    cookie = http.cookiejar.Cookie(version=0, name="Antibot-cookie", value=cookie_value,
                                   port=None, port_specified=False,
                                   domain="moodle.cegepsherbrooke.qc.ca", domain_specified=True, domain_initial_dot=False,
                                   path="/", path_specified=True,
                                   secure=False, expires=None, discard=True, comment=None, comment_url=None, rest=None)
    session.cookies.set_cookie(cookie)

    # Retry login
    response = session.post(login_url, data=login_data)

    # Check if login was successful
    if response.status_code != 200:
        print("Error: Unable to bypass the anti-bot cookie.")
        exit(1)

# Get the course content
response = session.get(course_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all activity instances and extract information
activity_instances = soup.find_all("div", class_="activityinstance")
items = []

for instance in activity_instances:
    item_info = {
        "id": instance.find("a")["id"],
        "title": instance.find("span", class_="instancename").get_text(strip=True).rsplit(" ", 1)[0],
        "type": instance.find("img")["alt"]
    }
    items.append(item_info)

# Generate JSON output
output = json.dumps(items, indent=2)
print(output)


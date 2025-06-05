# This example fetches GitHub profile details and shows them on Badger 2040 W.
# Fill in your GitHub username in the USERNAME constant.

import badger2040
from badger2040 import WIDTH
import urequests
import qrcode

# GitHub API requires a User-Agent header
HEADERS = {"User-Agent": "Badger2040"}

# Replace this with your GitHub username
USERNAME = "Julian-Elliott"

USER_URL = "https://api.github.com/users/" + USERNAME
REPO_URL = (
    "https://api.github.com/users/" + USERNAME + "/repos?per_page=1&sort=pushed"
)

# URL used for the QR code
GITHUB_URL = "https://github.com/" + USERNAME

# QR code setup
code = qrcode.QRCode()


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(15)
    display.rectangle(ox, oy, size, size)
    display.set_pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(
                    ox + x * module_size,
                    oy + y * module_size,
                    module_size,
                    module_size,
                )


# Display Setup
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(2)

display.connect()


def get_data():
    global login, repos, followers, latest_repo, pushed
    try:
        r = urequests.get(USER_URL, headers=HEADERS)
        user = r.json()
        login = user.get("login", USERNAME)
        repos = user.get("public_repos", 0)
        followers = user.get("followers", 0)
    except Exception as e:
        print(f"Failed to fetch user info: {e}")
        login = USERNAME
        repos = 0
        followers = 0
    finally:
        try:
            r.close()
        except Exception:
            pass

    try:
        r = urequests.get(REPO_URL, headers=HEADERS)
        repo_list = r.json()
        if repo_list and isinstance(repo_list, list):
            repo = repo_list[0]
            latest_repo = repo.get("name", "")
            pushed = repo.get("pushed_at", "").split("T")[0]
        else:
            latest_repo = ""
            pushed = ""
    except Exception as e:
        print(f"Failed to fetch repo info: {e}")
        latest_repo = ""
        pushed = ""
    finally:
        try:
            r.close()
        except Exception:
            pass


def draw_page():
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    display.set_font("bitmap6")
    display.rectangle(0, 0, WIDTH, 20)
    display.set_pen(15)
    display.text("GitHub Badge", 3, 4)
    display.set_pen(0)

    display.set_font("bitmap8")

    code.set_text(GITHUB_URL)
    draw_qr_code(WIDTH - 100, 25, 100, code)

    text_width = WIDTH - 105

    display.text(f"User: {login}", 0, 30, text_width, 2)
    display.text(f"Repos: {repos}", 0, 50, text_width, 2)
    display.text(f"Followers: {followers}", 0, 70, text_width, 2)
    display.text(f"Latest: {latest_repo}", 0, 90, text_width, 2)
    display.text(f"Pushed: {pushed}", 0, 110, text_width, 2)

    display.update()


def main():
    get_data()
    draw_page()
    while True:
        display.keepalive()
        display.halt()


if __name__ == "__main__":
    main()

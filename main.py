import cqhttp_helper as cq
from bot_context import *
from const import SUPPORT_LANGUAGES, HEADER
import hashlib
import requests
from html import unescape
from config import group_id, bot_host, bot_port
bot = cq.CQHttp(api_root='http://127.0.0.1:5700/')


@bot.on_message(ContextMessage.GROUP)
def handle_group_msg(context):
    c = ContextMessage.Group(context)
    if c.group_id not in group_id:
        return
    message = c.message
    try:
        if message[: 4] == "运行代码":
            message = print_code(message)
            bot.send_group_msg(group_id=c.group_id, message=f"{CqCode.atQQ(c.message)}\n{message}")

    except Exception as e:
        bot.send_group_msg(group_id=c.group_id,
                           message=CqCode.atQQ(c.user_id) + "\n" + "error" + str(e))


def print_code(data):
    language, code = get_code(data)
    if language not in SUPPORT_LANGUAGES:
        return "暂不支持此语言"
    result, data = run_code(language.lower(), code, stdin="")
    line = data.count("\n")
    length = len(data)
    if line >= 15:
        data = "\n".join(data.split("\n")[:15]) + f"\n共{line}行, 仅显示前15行"
    if length > 400:
        data = data[:400] + f"\n长度{length}, 仅显示前400"
    return_data = f"{'stdout:' if result else 'stderr:'}\n{data}"
    return return_data


def get_code(message):
    language_index = str(message[4:]).find("\n")
    language = ""
    code = ""
    if language_index != -1:
        language = message[5: language_index + 4].strip()
        code = unescape(message[language_index + 5:])
    return language, code


def run_code(language: str, code: str, stdin: str):
    try:
        if language not in SUPPORT_LANGUAGES:
            return False, "暂不支持此语言"
        url = SUPPORT_LANGUAGES[language]["url"]
        data = {
            "command": "",
            "stdin": stdin,
            "files": [
                {
                    "name": f"Main{SUPPORT_LANGUAGES[language]['name']}",
                    "content": code
                }
            ]
        }
        response = requests.post(url=url, json=data, headers=HEADER, timeout=30).text
        response = json.loads(response)
        if response["error"] == "" and response["stderr"] == "":
            return True, response["stdout"]
        return False, f"{response['error']}\n{response['stderr']}"
    except Exception as e:
        return False, str(e)


def get_md5(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()


bot.run(host=bot_host, port=bot_port)


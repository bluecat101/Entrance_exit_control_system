"""
######################## README ########################
文字形式で送るようと文字形式＋画像で送るようです。

envファイルには以下のように記述してください。

# SlackのAPIキー
SLACK_API_TOKEN = 
# Slackのチャンネル
SLACK_CHANNEL_ID = "" # Slackのチャンネルのリンクをコピーの一番後ろのIDです。
# https://xxx.slack.com/yyyy/zzzz この場合は zzzz の部分です。
########################################################
"""


import config
import yaml
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_API_TOKEN  = config.SLACK_API_TOKEN
NAME_TO_SLACK_ID_FILE = "name_to_slack_id.yml"

# SlackBot用のトークンとチャンネル
def get_slack_id_from_name(name):
  with open(NAME_TO_SLACK_ID_FILE, 'r') as yml: # name_list, envファイルに追加する
    name_to_slack_id = yaml.safe_load(yml)
  return config.getenv(name_to_slack_id[name])

def add_users_list_for_message(message, users):
  if len(users) == 0:
    return f"{message}\n=====研究室にいるメンバー=====\nいません。\n=============================="
  return f"{message}\n=====研究室にいるメンバー=====\n{"\n".join(users)}\n=============================="
  

def send_message_with_users_list(name, message, users, status):
  SLACK_MEMBER_ID = get_slack_id_from_name(name)
  client = WebClient(token=SLACK_API_TOKEN)
  try:
    response = client.chat_postMessage(
      channel=SLACK_MEMBER_ID,
      text=message,
    )
    # 特定の人に送る
    if status == "in":
      response = client.chat_postMessage(
      channel=get_slack_id_from_name("橋山"),
      text=add_users_list_for_message(f"+{name}さんが研究室に来ました。", users),
    )
    elif status == "out":
      response = client.chat_postMessage(
      channel=get_slack_id_from_name("橋山"),
      text=add_users_list_for_message(f"-{name}さんが帰りました。", users),
    )
    
  except SlackApiError as e:
    print(f"Got an error: {e.response['error']}")
  except Exception as e:
    print(e)
if __name__ == "__main__":
  send_message_with_users_list("name","test message",["tset1","test2"],"in")

# if __name__ == "__main__":
#   send_slack_message("test")
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
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# SlackBot用のトークンとチャンネル
SLACK_API_TOKEN  = config.SLACK_API_TOKEN
SLACK_CHANNEL_ID  = config.SLACK_CHANNEL_ID

"""
画像と文字を一緒に送ります。
message: メッセージ
file1_path: 画像1のパス
file2_path: 画像2のパス
"""
def send_slack_message_with_picture(message, file1_path,file2_path):
  client = WebClient(token=SLACK_API_TOKEN)
  try:
    response = client.files_upload_v2(
      channel=SLACK_CHANNEL_ID,
      initial_comment=message,
      file_uploads=[
        {"file": file1_path,},
        {"file": file2_path,},
      ],
      
    )
  except SlackApiError as e:
    print(f"Got an error: {e.response['error']}")

"""
文字のみで送ります
text: メッセージ
"""
def send_slack_message(text):
  client = WebClient(token=SLACK_API_TOKEN)
  
  try:
    # chat.postMessage API を呼び出します
    response = client.chat_postMessage(
      channel = SLACK_CHANNEL_ID,
      text = text,
    )
  except SlackApiError as e:
    assert e.response["error"]
    print(e)

if __name__ == "__main__":
  send_slack_message("test")
import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime


# 認証情報の設定
GOOGLE_APPLICATION_CREDENTIALS_PATH = config.GOOGLE_APPLICATION_CREDENTIALS_PATH
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_APPLICATION_CREDENTIALS_PATH, scope)
# クライアントの作成
client = gspread.authorize(creds)

# スプレッドシートの取得
SPREADSHEET_NAME = config.SPREADSHEET_NAME
spreadsheet = client.open(SPREADSHEET_NAME)
# シートの取得
MAX_LEN = 19
ALL_USER_COLUMN = f"A2:C{MAX_LEN+1}"
IN_USER_COLUMN = 1
OUT_USER_COLUMN = 3
OCCUPANCY_STATUS_SHEET_NAME = "在室状況"
OCCUPANCY_STATUS_WORKSHEET = spreadsheet.worksheet(OCCUPANCY_STATUS_SHEET_NAME)

# ログを書く用
def write_log(name, status):
  log_sheet_name = "ログ"
  log_worksheet = spreadsheet.worksheet(log_sheet_name)
  dt = datetime.datetime.now()
  str_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
  log_worksheet.append_row([str_dt, name, status])


def in_out_user(name, status):  
  # 名前の取得
  users_in, users_out = get_user_status()
  if status == "in":
    users_to_add = users_in
    users_to_delete = users_out
  elif status == "out":
    users_to_add = users_out
    users_to_delete = users_in
  # 名前を削除,追加
  if name not in users_to_delete:
    return _, False
  users_to_delete.remove(name)
  users_to_add += [name] 
  # ダミーデータの追加(users_in,users_outも変更されるので注意)
  users_to_add += [""] * (MAX_LEN - len(users_to_add))
  users_to_delete +=  [""] * (MAX_LEN - len(users_to_delete))
  # 1度のスプレッドシートへの通信で済ませるようにまとめる
  users_to_write = []
  for i in range(MAX_LEN):
    if status == "in":
      users_to_write.append([users_to_add[i], "", users_to_delete[i]])
    elif status == "out":
      users_to_write.append([users_to_delete[i],"",users_to_add[i]])
  OCCUPANCY_STATUS_WORKSHEET.update(ALL_USER_COLUMN, users_to_write)
  
  if status == "in":
    write_log(name, "不在→在室")
  elif status == "out":
    write_log(name, "在室→不在")
  return list(filter(lambda name: name != "", users_in)), True

# userの状態を全て取得
def get_user_status():
  users = OCCUPANCY_STATUS_WORKSHEET.get(ALL_USER_COLUMN)
  users_in = []
  users_out = []
  for user in users:
    if len(user) == 3:
      if user[0] != "":
        users_in.append(user[0])
      if user[2] != "":
        users_out.append(user[2])
    if len(user) < 3:
      users_in.append(user[0])
  return users_in, users_out
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
  if status == "in": # inになったのでinに書き込み、outから取り除く
    column_to_add = IN_USER_COLUMN
    column_name_to_add = "A"
    column_to_delete = OUT_USER_COLUMN
    column_name_to_delete = "C"
    
  elif status == "out": # outになったのでoutに書き込み、inから取り除く
    column_to_add = OUT_USER_COLUMN
    column_name_to_add = "C"
    column_to_delete = IN_USER_COLUMN
    column_name_to_delete = "A"
  else:
    return
  
  # 名前を削除
  users_to_delete = OCCUPANCY_STATUS_WORKSHEET.col_values(column_to_delete)[1:]
  if name not in users_to_delete:
    return False
  OCCUPANCY_STATUS_WORKSHEET.update(f'{column_name_to_delete}{2}:{column_name_to_delete}{len(users_to_delete)+1}', [[""] for user in users_to_delete]) # 初期化
  users_to_delete.remove(name)
  OCCUPANCY_STATUS_WORKSHEET.update(f'{column_name_to_delete}{2}:{column_name_to_delete}{len(users_to_delete)+1}', [[user] for user in users_to_delete])
  
  # 名前を追加
  num_in_user = len(OCCUPANCY_STATUS_WORKSHEET.col_values(column_to_add)[1:])
  OCCUPANCY_STATUS_WORKSHEET.update_acell(f'{column_name_to_add}{num_in_user+2}', name)

  if status == "in":
    write_log(name, "不在→在室")
  elif status == "out":
    write_log(name, "在室→不在")

# userの状態を全て取得
def get_user_status():
  users_in = OCCUPANCY_STATUS_WORKSHEET.col_values(IN_USER_COLUMN)[1:]
  users_out = OCCUPANCY_STATUS_WORKSHEET.col_values(OUT_USER_COLUMN)[1:]
  return users_in, users_out
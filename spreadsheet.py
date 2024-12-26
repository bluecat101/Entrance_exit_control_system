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

# ログを書く用
def write_log(name, status):
  log_sheet_name = "ログ"
  log_worksheet = spreadsheet.worksheet(log_sheet_name)
  dt = datetime.datetime.now()
  str_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
  log_worksheet.append_row([str_dt, name, status])


def in_out_user(name, status):
  # 設定
  IN_USER_COLUMN = "A2:A100"
  OUT_USER_COLUMN = "C2:C100"
  
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
  
  occupancy_status_sheet_name = "在室状況"
  occupancy_status_worksheet = spreadsheet.worksheet(occupancy_status_sheet_name)
  # 名前を削除
  users_to_delete = occupancy_status_worksheet.get(column_to_delete)[0]
  users_to_delete.remove(name)
  occupancy_status_worksheet.update(column_to_delete, [[users_to_delete]])
  
  # 名前を追加
  num_in_user = len(occupancy_status_worksheet.get(column_to_add)[0])
  out_users.remove(name)
  occupancy_status_worksheet.update_acell(f'{column_name_to_add}{num_in_user+2}', name)

  if status == "in":
    write_log(name, "不在→在室")
  elif status == "out":
    write_log(name, "在室→不在")
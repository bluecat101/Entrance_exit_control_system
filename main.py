from flask import Flask, render_template, redirect, request, jsonify
import os
import config
import spreadsheet
import slack
import datetime 

name_replace_from_nickname={
  "ウッディ":"細川",
  "かんちゃん":"菅野",
  "YANG":"杨",
  "けんさん":"田中",
  "たーさん":"小原",
  "そらっち":"柳谷",
	"天国":"武田",
	"ひろむさん":"新妻",
	"なとりく":"名執",
	"でぐっち":"出口",
	"よしのりさん":"東川",
	"しょうごくん":"斉藤",
	"けいちゃん":"中田",
}

START_TIME = datetime.datetime(2024, 12, 28, 22, 00, 00)
END_TIME = datetime.datetime(2025, 1, 4, 7, 00, 00)
app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/')
def main():
  return app.send_static_file('main.html')

@app.route('/arrive_at_work', methods=['POST'])
def post_arrive_at_work():
  if "user_out" not in request.form: # outの状態のuserが選択されるためuser_outとなる
    return redirect('/')
  user = request.form['user_out']
  users_in, is_ok = spreadsheet.in_out_user(user, "in")
  if is_ok and START_TIME < datetime.datetime.now() < END_TIME:
    slack.send_message_with_users_list(name_replace_from_nickname[user], f"[在室]{user} 本日も研究頑張っていきましょう！", list(map(lambda nickname: name_replace_from_nickname[nickname],users_in)), "in")
  return redirect('/')


@app.route('/clock_out', methods=['POST'])
def post_clock_out():
  if "user_in" not in request.form: # inの状態のuserが選択されるためuser_inとなる
    return redirect('/')
  user = request.form['user_in']
  users_in, is_ok = spreadsheet.in_out_user(user, "out")
  if is_ok and START_TIME < datetime.datetime.now() < END_TIME:
    slack.send_message_with_users_list(name_replace_from_nickname[user], f"[帰宅]{user} 研究お疲れ様です！", list(map(lambda nickname: name_replace_from_nickname[nickname], users_in)), "out")
  return redirect('/')

# userの状態を取得する
@app.route('/get_in_out_name')
def get_in_out_name():
  users_in, users_out = spreadsheet.get_user_status()
  return jsonify({'users_in': users_in, 'users_out': users_out})

# userの名前一覧を取得する
@app.route('/get_name_list')
def get_name_list():
  name_list = config.get_name_list()
  if len(name_list) != 0:
    return jsonify({'name_list': name_list})
  else:
    return jsonify({'error': 'File not found'}), 404

app.run(host='0.0.0.0', port=8000, debug=True)  
from flask import Flask, render_template, redirect, request, jsonify
import os
import config
import spreadsheet

  
app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/')
def main():
  return app.send_static_file('main.html')

@app.route('/arrive_at_work', methods=['POST'])
def post_arrive_at_work():
  if "user_out" not in request.form: # outの状態のuserが選択されるためuser_outとなる
    return redirect('/')
  user = request.form['user_out']
  spreadsheet.in_out_user(user, "in")
  return redirect('/')


@app.route('/clock_out', methods=['POST'])
def post_clock_out():
  if "user_in" not in request.form: # inの状態のuserが選択されるためuser_inとなる
    return redirect('/')
  user = request.form['user_in']
  spreadsheet.in_out_user(user, "out")
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

app.run(port=8000, debug=True)  
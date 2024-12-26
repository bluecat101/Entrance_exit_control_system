from flask import Flask, render_template, redirect, request, jsonify
import os
import datetime
import config

TIME_FILE = "in_out_name.txt"
TIME_LOG_FILE = "in_out_time.log"
def write_log(user, action):
  with open(TIME_LOG_FILE, 'a') as f:
    dt= datetime.datetime.now()
    str_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    f.write(f"{action}:({user}):{str_dt} \n")
  
app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/')
def main():
  return app.send_static_file('main.html')

@app.route('/arrive_at_work', methods=['POST'])
def post_arrive_at_work():
  if "user_out" not in request.form:
    return redirect('/')
  user = request.form['user_out']
  with open(TIME_FILE, 'r') as f:
    name_list = [s.rstrip() for s in f.readlines()]
  if user not in name_list:
    with open(TIME_FILE, 'a') as f:
      f.write(user+'\n')
  write_log(user, "arrive_at_work")
  return redirect('/')


@app.route('/clock_out', methods=['POST'])
def post_clock_out():
  if "user_in" not in request.form:
    return redirect('/')
  user = request.form['user_in']
  with open(TIME_FILE, 'r') as f:
    name_list = [s.rstrip() for s in f.readlines()]
  if user in name_list:
    name_list.remove(user)
  with open(TIME_FILE, 'w') as f:
    for name in name_list:
      f.write(name + '\n')
  write_log(user, "clock_out")
  return redirect('/')

@app.route('/get_in_out_name')
def get_in_out_name():
  file_path = os.path.join(os.getcwd(), TIME_FILE)
  if os.path.exists(file_path):
    with open(TIME_FILE, 'r') as f:
      name_list = [s.rstrip() for s in f.readlines()]
    return jsonify({'name': name_list})
  else:
      return jsonify({'error': 'File not found'}), 404

@app.route('/get_name_list')
def get_name_list():
  name_list = config.get_name_list()
  if len(name_list) != 0:
    return jsonify({'name_list': name_list})
  else:
      return jsonify({'error': 'File not found'}), 404

app.run(port=8000, debug=True)  
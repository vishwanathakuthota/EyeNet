import time
from flask import Flask, request, jsonify, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# User session tracking dictionary
user_sessions = {}
INACTIVITY_TIMEOUT = 600  # 10 minutes

def get_user_id():
    return request.remote_addr  # Using IP address as a simple identifier

def start_or_update_session(user_id):
    now = time.time()
    if user_id in user_sessions:
        user_sessions[user_id]['last_active'] = now
    else:
        user_sessions[user_id] = {'start_time': now, 'last_active': now, 'total_active_time': 0}

def check_and_update_session(user_id):
    now = time.time()
    if user_id in user_sessions:
        session_data = user_sessions[user_id]
        if now - session_data['last_active'] > INACTIVITY_TIMEOUT:
            session_data['total_active_time'] += session_data['last_active'] - session_data['start_time']
            session_data['start_time'] = now  # Restart session
        session_data['last_active'] = now

def end_session(user_id):
    if user_id in user_sessions:
        session_data = user_sessions[user_id]
        session_data['total_active_time'] += session_data['last_active'] - session_data['start_time']
        session_data['start_time'] = None

@app.route('/interact', methods=['POST'])
def interact():
    user_id = get_user_id()
    check_and_update_session(user_id)
    return jsonify({"message": "User interaction recorded."})

@app.route('/session_time', methods=['GET'])
def get_session_time():
    user_id = get_user_id()
    if user_id in user_sessions:
        session_data = user_sessions[user_id]
        active_time = session_data['total_active_time']
        return jsonify({"user_id": user_id, "total_active_time": active_time})
    return jsonify({"error": "No active session found."})

if __name__ == '__main__':
    app.run(debug=True)

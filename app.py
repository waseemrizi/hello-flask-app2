from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"<h2>Hello from Flask App 2!</h2><p>🕒 Current server time: {current_time}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


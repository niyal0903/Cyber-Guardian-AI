from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# Futuristic UI
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS SECURITY ACCESS</title>
    <style>
        body { background: #000; color: #00f2ff; font-family: 'Segoe UI', sans-serif; text-align: center; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .glass { background: rgba(0, 242, 255, 0.1); backdrop-filter: blur(15px); border: 1px solid #00f2ff; padding: 50px; border-radius: 20px; box-shadow: 0 0 40px #00f2ff; width: 450px; }
        .warning { color: #ff0000; font-weight: bold; text-transform: uppercase; margin-bottom: 20px; animation: blink 0.8s infinite; }
        @keyframes blink { 0% {opacity: 1;} 50% {opacity: 0;} 100% {opacity: 1;} }
        input { width: 100%; padding: 12px; margin: 10px 0; background: transparent; border: 1px solid #00f2ff; color: white; border-radius: 5px; }
        button { width: 100%; padding: 15px; background: #00f2ff; color: black; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="glass">
        <h1>JARVIS PROTOCOL</h1>
        <div class="warning">Unauthorized Intrusion Detected</div>
        <p>This network is secured by AI. Provide your details to request access or you will be disconnected in 60 seconds.</p>
        <form method="POST" action="/submit">
            <input type="text" name="name" placeholder="Enter Your Name" required>
            <input type="text" name="reason" placeholder="Reason for connecting" required>
            <button type="submit">SUBMIT IDENTITY</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_UI)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    reason = request.form.get('reason')
    # Save for Jarvis to read
    with open("intruder_log.txt", "w") as f:
        f.write(f"{name}|{reason}")
    return "<h1>Identity Logged. Jarvis is verifying... Do not close this page.</h1>"

def start_portal():
    app.run(host='0.0.0.0', port=80)
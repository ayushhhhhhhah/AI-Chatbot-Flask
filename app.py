from flask import Flask, request, redirect, session, send_file
import sqlite3
from main import ask_ai
from captcha.image import ImageCaptcha
import random
import string

app = Flask(__name__)

# Secret Key For Session
app.secret_key = "super_secret_key_123"

# Store Chat Messages
chat_history = []


# =========================
# CAPTCHA ROUTE
# =========================
@app.route('/captcha')
def captcha():

    image = ImageCaptcha()

    captcha_text = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=5
        )
    )

    session['captcha'] = captcha_text

    data = image.generate(captcha_text)

    return send_file(data, mimetype='image/png')


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():

    return open("templates/INDEX100.html").read()


# =========================
# LOGIN FUNCTION
# =========================
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]
    captcha_input = request.form["captcha"]

    # CAPTCHA CHECK
    if captcha_input != session.get("captcha"):

        return """
        <h1 style='color:red;text-align:center;margin-top:50px;'>
        Wrong Captcha ❌
        </h1>
        """

    # DATABASE CONNECTION
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # CHECK USER
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    # LOGIN SUCCESS
    if user:

        session["user"] = username

        return redirect("/dashboard")

    # LOGIN FAILED
    else:

        return """
        <h1 style='color:red;text-align:center;margin-top:50px;'>
        Invalid Username or Password ❌
        </h1>
        """


# =========================
# SIGNUP PAGE
# =========================
@app.route("/signup")
def signup_page():

    return open("templates/signup.html").read()


# =========================
# SIGNUP FUNCTION
# =========================
@app.route("/signin", methods=["POST"])
def signin():

    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username, password, email) VALUES(?, ?, ?)",
        (username, password, email)
    )

    conn.commit()
    conn.close()

    session["user"] = username

    return redirect("/dashboard")


# =========================
# DASHBOARD PAGE
# =========================
@app.route("/dashboard")
def dashboard():

    # BLOCK DIRECT ACCESS
    if "user" not in session:

        return redirect("/")

    username = session["user"]

    return f"""
    <!DOCTYPE html>
    <html>

    <head>

    <title>Dashboard</title>

    <style>

    *{{
        margin:0;
        padding:0;
        box-sizing:border-box;
    }}

    body{{
        font-family:Arial;
        background:linear-gradient(135deg,#0f172a,#111827,#1e1b4b);
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
        color:white;
    }}

    .dashboard{{
        width:700px;
        background:rgba(255,255,255,0.08);
        backdrop-filter:blur(20px);
        padding:40px;
        border-radius:25px;
        border:1px solid rgba(255,255,255,0.1);
        box-shadow:0px 8px 32px rgba(0,0,0,0.3);
        text-align:center;
    }}

    h1{{
        margin-bottom:10px;
        font-size:38px;
    }}

    p{{
        color:#cbd5e1;
        margin-bottom:30px;
    }}

    .cards{{
        display:grid;
        grid-template-columns:1fr 1fr;
        gap:20px;
        margin-bottom:30px;
    }}

    .card{{
        background:#1e293b;
        padding:25px;
        border-radius:20px;
    }}

    .card h2{{
        margin-bottom:10px;
        color:#60a5fa;
    }}

    .btn{{
        display:inline-block;
        padding:15px 30px;
        background:linear-gradient(135deg,#2563eb,#7c3aed);
        color:white;
        text-decoration:none;
        border-radius:15px;
        font-weight:bold;
        transition:0.3s;
    }}

    .btn:hover{{
        transform:scale(1.05);
    }}

    </style>

    </head>

    <body>

    <div class="dashboard">

        <h1>Welcome, {username} 👋</h1>

        <p>AI Assistant Dashboard</p>

        <div class="cards">

            <div class="card">
                <h2>AI Chat</h2>
                <p>Talk with AI instantly.</p>
            </div>

            <div class="card">
                <h2>Ticketing System</h2>
                <p>Coming Soon 🚀</p>
            </div>

            <div class="card">
                <h2>Security</h2>
                <p>Captcha Protected Login</p>
            </div>

            <div class="card">
                <h2>Status</h2>
                <p>System Online ✅</p>
            </div>

        </div>

        <a href="/chat" class="btn">
            Open Chatbot
        </a>

    </div>

    </body>

    </html>
    """


# =========================
# CHATBOT PAGE
# =========================
@app.route("/chat", methods=["GET", "POST"])
def chat():

    # BLOCK DIRECT ACCESS
    if "user" not in session:

        return redirect("/")

    global chat_history

    if request.method == "POST":

        user_msg = request.form["message"]

        chat_history.append(f"You: {user_msg}")

        # AI RESPONSE
        bot_reply = ask_ai(user_msg)

        chat_history.append(f"Bot: {bot_reply}")

    html = """
<!DOCTYPE html>
<html>

<head>

<title>AI Chatbot</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    font-family:'Segoe UI', sans-serif;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(135deg,#0f172a,#111827,#1e1b4b);
    overflow:hidden;
}

.chat-container{
    width:600px;
    height:750px;
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(20px);
    border-radius:25px;
    padding:25px;
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0px 8px 32px rgba(0,0,0,0.3);
    display:flex;
    flex-direction:column;
}

.chat-header{
    text-align:center;
    margin-bottom:20px;
}

.chat-header h2{
    color:white;
    font-size:32px;
}

.chat-box{
    flex:1;
    overflow-y:auto;
    padding:20px;
    border-radius:20px;
    background:#0f172a;
    margin-bottom:20px;
}

.user{
    text-align:right;
    margin-bottom:15px;
}

.user span{
    background:#2563eb;
    color:white;
    padding:14px 18px;
    border-radius:18px;
    display:inline-block;
}

.bot{
    text-align:left;
    margin-bottom:15px;
}

.bot span{
    background:#10b981;
    color:white;
    padding:14px 18px;
    border-radius:18px;
    display:inline-block;
}

.chat-form{
    display:flex;
    gap:12px;
}

.chat-form input{
    flex:1;
    padding:16px;
    border:none;
    outline:none;
    border-radius:16px;
    background:#1e293b;
    color:white;
}

.chat-form button{
    padding:0px 28px;
    border:none;
    border-radius:16px;
    background:linear-gradient(135deg,#2563eb,#7c3aed);
    color:white;
    cursor:pointer;
}

</style>

</head>

<body>

<div class="chat-container">

<div class="chat-header">
    <h2>AI Chatbot 🤖</h2>
</div>

<div class="chat-box">
"""

    # SHOW MESSAGES
    for msg in chat_history:

        if "You:" in msg:

            html += f'<div class="user"><span>{msg}</span></div>'

        else:

            html += f'<div class="bot"><span>{msg}</span></div>'

    html += """

</div>

<form method="POST" class="chat-form">

<input type="text" name="message" placeholder="Type your message..." required>

<button type="submit">Send</button>

</form>

</div>

</body>
</html>
"""

    return html


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


# =========================
# RUN APP
# =========================
if __name__ == "__main__":

    app.run(debug=True)
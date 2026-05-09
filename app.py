from flask import Flask, request, redirect
import sqlite3
from main import ask_ai

app = Flask(__name__)

chat_history = []


# =========================
# LOGIN PAGE
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

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return redirect("/chat")

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

    return redirect("/chat")


# =========================
# CHATBOT PAGE
# =========================
@app.route("/chat", methods=["GET", "POST"])
def chat():

    global chat_history

    if request.method == "POST":

        user_msg = request.form["message"]

        chat_history.append(f"You: {user_msg}")

        # AI reply
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

/* Glow Effects */
body::before{
    content:"";
    position:absolute;
    width:450px;
    height:450px;
    background:#06b6d4;
    border-radius:50%;
    filter:blur(150px);
    top:-120px;
    left:-120px;
    opacity:0.3;
}

body::after{
    content:"";
    position:absolute;
    width:450px;
    height:450px;
    background:#7c3aed;
    border-radius:50%;
    filter:blur(150px);
    bottom:-120px;
    right:-120px;
    opacity:0.3;
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
    z-index:10;
    display:flex;
    flex-direction:column;
}

/* Header */
.chat-header{
    text-align:center;
    margin-bottom:20px;
}

.chat-header h2{
    color:white;
    font-size:32px;
    margin-bottom:5px;
}

.chat-header p{
    color:#cbd5e1;
    font-size:14px;
}

/* Chat Box */
.chat-box{
    flex:1;
    overflow-y:auto;
    padding:20px;
    border-radius:20px;
    background:#0f172a;
    border:1px solid rgba(255,255,255,0.08);
    margin-bottom:20px;
}

/* Scrollbar */
.chat-box::-webkit-scrollbar{
    width:6px;
}

.chat-box::-webkit-scrollbar-thumb{
    background:#64748b;
    border-radius:10px;
}

/* User Message */
.user{
    display:flex;
    justify-content:flex-end;
    margin-bottom:15px;
}

.user span{
    background:#2563eb;
    color:white;
    padding:14px 18px;
    border-radius:18px 18px 0px 18px;
    max-width:75%;
    font-size:15px;
    line-height:1.5;
    word-wrap:break-word;
    box-shadow:0px 4px 10px rgba(37,99,235,0.3);
}

/* Bot Message */
.bot{
    display:flex;
    justify-content:flex-start;
    margin-bottom:15px;
}

.bot span{
    background:#10b981;
    color:white;
    padding:14px 18px;
    border-radius:18px 18px 18px 0px;
    max-width:75%;
    font-size:15px;
    line-height:1.5;
    word-wrap:break-word;
    box-shadow:0px 4px 10px rgba(16,185,129,0.3);
}

/* Input Area */
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
    font-size:15px;
}

.chat-form input::placeholder{
    color:#94a3b8;
}

.chat-form button{
    padding:0px 28px;
    border:none;
    border-radius:16px;
    background:linear-gradient(135deg,#2563eb,#7c3aed);
    color:white;
    font-size:15px;
    font-weight:bold;
    cursor:pointer;
    transition:0.3s;
}

.chat-form button:hover{
    transform:scale(1.05);
    opacity:0.9;
}
.support-email{
    position:fixed;
    bottom:20px;
    right:20px;
    background:rgba(255,255,255,0.1);
    backdrop-filter:blur(10px);
    padding:10px 16px;
    border-radius:15px;
    color:white;
    font-size:14px;
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0px 4px 12px rgba(0,0,0,0.2);
    z-index:999;
}

.support-email a{
    color:#60a5fa;
    text-decoration:none;
    font-weight:bold;
}

.support-email a:hover{
    text-decoration:underline;
}

</style>

</head>

<body>

<div class="chat-container">

<div class="chat-header">
    <h2>AI Chatbot 🤖</h2>
    <p>Powered by Artificial Intelligence</p>
</div>

<div class="chat-box">
"""

    # Show Messages
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
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)
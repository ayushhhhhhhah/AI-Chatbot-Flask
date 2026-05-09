import requests

API_KEY = "AIzaSyAwXTZmQ0AeDwnmoHY11heDqP63p7UQ-oQ"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={"AIzaSyAwXTZmQ0AeDwnmoHY11heDqP63p7UQ-oQ"}"

def ask_ai(user_input):
    response = requests.post(
        url,
        json={
            "contents": [
                {
                    "parts": [{"text": user_input}]
                }
            ]
        }
    )

    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Error: " + str(data)


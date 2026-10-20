from flask import Flask, request
import os, requests

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "docconvert_verify_2026")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.route('/')
def home():
    return "DocConvert Bot Live ✅"

@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    print(f"Verify attempt: {token} vs {VERIFY_TOKEN}")
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("WEBHOOK RECEIVED:", data)
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            from_num = msg['from']
            print(f"Message from {from_num}: {msg}")
            
            # Send reply
            if WHATSAPP_TOKEN and PHONE_NUMBER_ID:
                url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
                headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
                body = {
                    "messaging_product": "whatsapp",
                    "to": from_num,
                    "type": "text",
                    "text": {"body": "👋 Hi! I'm DocConvert Bot LIVE!\n\nYour connection works ✅\n\nNow send me any file to convert."}
                }
                r = requests.post(url, headers=headers, json=body)
                print("Send response:", r.text)
    except Exception as e:
        print("Error:", e)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

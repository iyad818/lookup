from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

# تحميل الـ BINs المخزنة في Bin.txt
def load_bins():
    try:
        with open("Bin.txt", "r") as file:
            return set(line.strip() for line in file if line.strip().isdigit())
    except FileNotFoundError:
        return set()

# قراءة الـ BINs عند تشغيل الخادم
valid_bins = load_bins()

@app.route('/<card>', methods=['GET'])
def check_card(card):
    parts = card.split('|')
    
    if len(parts) < 1 or not parts[0].isdigit() or len(parts[0]) != 16:
        return jsonify({"error": "Invalid card format! ❌"}), 400

    cc_number = parts[0]  # رقم البطاقة الكامل
    bin_number = cc_number[:6]  # استخراج أول 6 أرقام (BIN)

    if bin_number in valid_bins:
        return jsonify({"status": "Challenge Required ✅"})
    else:
        return jsonify({"status": "Card_declined (LookUP_error)! ❌"})

if __name__ == '__main__':
    ip_address = socket.gethostbyname(socket.gethostname())
    port = 5000  # يمكنك تغييره إذا أردت

    print(f"🔹 خادم يعمل على: http://{ip_address}:{port}/<CARD>")
    app.run(host='0.0.0.0', port=port, debug=True)

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # ফ্রন্টএন্ড থেকে সিকিউর কানেকশন পারমিট করার জন্য

# তোমার দেওয়া গেমস কিনবো প্রিমিয়াম API Key
API_KEY = "VJjAaQFwrzagWcB1R2tYr33ScuJBTQ18OyxP9aI4lEc"
BASE_URL = "https://api.gameskinbo.com/ff-info/get"

@app.route('/check-uid', methods=['GET'])
def check_uid():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({'success': False, 'message': 'UID field is empty!'}), 400

    # ডকুমেন্টেশন অনুযায়ী হেডার এবং প্যারামিটার সেটআপ
    headers = {
        "x-api-key": API_KEY
    }
    params = {
        "uid": uid,
        "region": "BD" # BD রিজিয়ন আগে ট্রাই করবে, ফলে পলকের মধ্যে নাম চলে আসবে
    }

    try:
        # গেমস কিনবো অফিশিয়াল সার্ভারে GET রিকোয়েস্ট পাঠানো হচ্ছে
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=6)
        data = response.json()

        if response.status_code == 200:
            # ডকুমেন্টেশন স্ট্রাকচার অনুযায়ী নাম ফিল্টার করা হচ্ছে (AccountInfo -> AccountName)
            account_info = data.get("AccountInfo", {})
            player_name = account_info.get("AccountName")
            
            if player_name:
                return jsonify({'success': True, 'name': player_name})
            else:
                return jsonify({'success': False, 'message': 'UID সঠিক কিন্তু প্লেয়ারের নাম পাওয়া যায়নি।'})
        else:
            # ডকুমেন্টেশনে উল্লেখিত রেট লিমিট বা অন্যান্য এরর মেসেজ হ্যান্ডেলিং
            error_msg = data.get("error", "সার্ভার গেটওয়ে এরর। আবার চেষ্টা করো।")
            return jsonify({'success': False, 'message': error_msg})

    except requests.exceptions.RequestException:
        return jsonify({'success': False, 'message': 'কানেকشن টাইমআউট! গেমস কিনবো সার্ভার রেসপন্স করছে না।'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
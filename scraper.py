# تاریخ ایجاد: ۱۴۰۴/۱۰/۱۲ - ۰۵:۰۱ صبح
# نام فایل: scraper.py
# هدف: اصلاح مسیر استخراج از نقطه استیبل

import requests
import json
import os

os.makedirs('fa', exist_ok=True)
os.makedirs('en', exist_ok=True)

def get_stable_data():
    url = "https://raw.githubusercontent.com/kayvan-sylvan/work-day-calendar/master/iranian-holidays.json"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            data = response.json()
            # چاپ برای دیباگ در کنسول گیت‌هاب
            print(f"Data received. Type: {type(data)}")
            return data
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def translate_event(text):
    subs = {"عید": "Eid", "نوروز": "Nowruz", "وفات": "Martyrdom", "ولادت": "Birthday"}
    for fa, en in subs.items():
        text = text.replace(fa, en)
    return text

def run():
    raw_data = get_stable_data()
    if not raw_data:
        return

    # نکته حیاتی: اگر دیتا به صورت لیست مستقیم است یا داخل کلید events
    events = raw_data if isinstance(raw_data, list) else raw_data.get('events', [])
    
    if not events:
        print("No events found in the JSON!")
        return

    calendar_fa = {m: [] for m in range(1, 13)}
    calendar_en = {m: [] for m in range(1, 13)}

    for event in events:
        try:
            # ساختار فایل Kayvan: "date": "1404/01/01"
            date_str = event.get('date', '')
            if not date_str: continue
            
            parts = date_str.split('/')
            month = int(parts[1])
            day = int(parts[2])
            title = event.get('title', '')
            is_holiday = event.get('is_holiday', False)

            calendar_fa[month].append({"d": day, "t": title, "h": is_holiday})
            calendar_en[month].append({"d": day, "t": translate_event(title), "h": is_holiday})
        except:
            continue

    info_header = "Stable Sync: 1404/10/12"
    for m in range(1, 13):
        # ذخیره فایل‌ها (حتی اگر خالی باشند تا زمان ویرایش عوض شود)
        with open(f'fa/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"month": m, "events": calendar_fa[m], "info": info_header}, f, ensure_ascii=False, indent=2)
        with open(f'en/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"month": m, "events": calendar_en[m], "info": info_header}, f, ensure_ascii=False, indent=2)

    print("Process Finished Successfully.")

if __name__ == "__main__":
    run()

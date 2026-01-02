# تاریخ ایجاد: ۱۴۰۴/۱۰/۱۲ - ۰۵:۱۵ صبح
# اصلاح: تغییر منبع به API جایگزین و رفع خطای Fetch

import requests
import json
import os

os.makedirs('fa', exist_ok=True)
os.makedirs('en', exist_ok=True)

def translate_event(text):
    # ترجمه پایه برای نمایشگر TFT
    subs = {"عید": "Eid", "نوروز": "Nowruz", "شهادت": "Martyr", "ولادت": "Birth"}
    for fa, en in subs.items():
        text = text.replace(fa, en)
    return text

def run():
    # استفاده از یک منبع جایگزین برای تقویم
    url = "https://raw.githubusercontent.com/pajacyk/calendar-iran/master/holidays.json"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            events = response.json()
        else:
            print(f"Server error: {response.status_code}")
            return
    except Exception as e:
        print(f"Connection error: {e}")
        return

    # اسکلت‌بندی ماه‌ها
    calendar_fa = {m: [] for m in range(1, 13)}
    calendar_en = {m: [] for m in range(1, 13)}

    # پردازش داده‌ها (تطبیق با ساختار جدید منبع)
    for event in events:
        try:
            # استخراج ماه و روز از ساختار جدید
            month = int(event.get('month'))
            day = int(event.get('day'))
            title = event.get('title', 'مناسبت')
            is_holiday = event.get('is_holiday', False)

            calendar_fa[month].append({"d": day, "t": title, "h": is_holiday})
            calendar_en[month].append({"d": day, "t": translate_event(title), "h": is_holiday})
        except:
            continue

    # ذخیره فایل‌ها - نقطه استیبل
    for m in range(1, 13):
        with open(f'fa/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"m": m, "events": calendar_fa[m]}, f, ensure_ascii=False, indent=2)
        with open(f'en/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"m": m, "events": calendar_en[m]}, f, ensure_ascii=False, indent=2)
    
    print("Files successfully generated.")

if __name__ == "__main__":
    run()

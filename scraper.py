# تاریخ ایجاد: ۱۴۰۴/۱۰/۱۲ - ۰۵:۰۸ صبح
# اصلاحیه: حذف فیلتر سال برای اطمینان از خروجی دیتای استیبل

import requests
import json
import os

os.makedirs('fa', exist_ok=True)
os.makedirs('en', exist_ok=True)

def translate_event(text):
    subs = {"عید": "Eid", "نوروز": "Nowruz", "وفات": "Martyrdom", "ولادت": "Birthday", "شهادت": "Martyrdom"}
    for fa, en in subs.items():
        text = text.replace(fa, en)
    return text

def run():
    url = "https://raw.githubusercontent.com/kayvan-sylvan/work-day-calendar/master/iranian-holidays.json"
    response = requests.get(url, timeout=20)
    
    if response.status_code != 200:
        print("Failed to fetch source")
        return

    events = response.json()
    # اگر فایل به صورت دیکشنری بود و کلید events داشت
    if isinstance(events, dict):
        events = events.get('events', [])

    calendar_fa = {m: [] for m in range(1, 13)}
    calendar_en = {m: [] for m in range(1, 13)}

    for event in events:
        try:
            date_str = event.get('date', '') # فرمت: "1403/01/01"
            parts = date_str.split('/')
            
            # ما فقط ماه و روز را می‌خواهیم، سال فعلاً مهم نیست برای تست
            month = int(parts[1])
            day = int(parts[2])
            title = event.get('title', '')
            is_holiday = event.get('is_holiday', False)

            calendar_fa[month].append({"d": day, "t": title, "h": is_holiday})
            calendar_en[month].append({"d": day, "t": translate_event(title), "h": is_holiday})
        except:
            continue

    # ذخیره اجباری ۱۲ فایل
    for m in range(1, 13):
        with open(f'fa/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"m": m, "events": calendar_fa[m]}, f, ensure_ascii=False)
        with open(f'en/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"m": m, "events": calendar_en[m]}, f, ensure_ascii=False)
    
    print("Files forced to update.")

if __name__ == "__main__":
    run()

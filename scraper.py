import requests
import json
import os
import time

# ایجاد پوشه‌ها
os.makedirs('fa', exist_ok=True)
os.makedirs('en', exist_ok=True)

def get_data(month):
    # استفاده از یک API کمکی که دیتای time.ir را به صورت JSON ارائه می‌دهد
    # این منبع بسیار پایدارتر از اسکرپ کردن مستقیم است
    url = f"https://isurvey.ir/api/v1/calendar/events?year=1404&month={month}"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            raw_data = response.json()
            events_list = []
            
            # استخراج رویدادها از ساختار API
            for event in raw_data.get('events', []):
                events_list.append({
                    "d": int(event.get('day')),
                    "t": event.get('description'),
                    "h": bool(event.get('is_holiday'))
                })
            return events_list
        return []
    except Exception as e:
        print(f"Error in Month {month}: {e}")
        return []

# چرخه ۱۲ ماهه
for m in range(1, 13):
    print(f"Syncing Month {m}...")
    data = get_data(m)
    
    if data: # فقط اگر دیتا وجود داشت فایل را بساز یا بروز کن
        # ۱. ذخیره نسخه فارسی
        with open(f'fa/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"month": m, "events": data}, f, ensure_ascii=False, indent=2)
        
        # ۲. ذخیره نسخه انگلیسی (فعلاً کپی فارسی برای تست اسکلت)
        with open(f'en/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"month": m, "events": data}, f, ensure_ascii=False, indent=2)
    
    time.sleep(1)

print("Done! Check your folders.")

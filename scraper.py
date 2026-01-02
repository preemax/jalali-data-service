import requests
from bs4 import BeautifulSoup
import json
import os
import time

os.makedirs('fa', exist_ok=True)
os.makedirs('en', exist_ok=True)

def get_events_from_time_ir(month):
    # آدرس مستقیم و رسمی سایت time.ir برای سال 1404
    url = f"https://www.time.ir/fa/event/list/0/1404/{month}"
    
    # این بخش حیاتی است؛ وانمود می‌کنیم که یک آدم هستیم نه ربات
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        events_list = []
        
        # پیدا کردن لیست مناسبت‌ها در ساختار جدید سایت
        # مناسبت‌ها معمولاً در تگ‌های <li> با کلاس event-item هستند
        items = soup.find_all('li', class_='event-item')
        
        for item in items:
            day_element = item.find('span', class_='event-day')
            title_element = item.find('div', class_='event-title')
            
            if day_element and title_element:
                # تبدیل اعداد فارسی به انگلیسی برای ذخیره در JSON
                raw_day = day_element.text.strip()
                day_en = "".join([c for c in raw_day if c.isdigit()])
                
                # تشخیص تعطیلی (معمولاً متن قرمز یا کلاس خاص)
                is_holiday = "holiday" in str(item).lower() or "text-danger" in str(item).lower()
                
                events_list.append({
                    "d": int(day_en),
                    "t": title_element.text.strip(),
                    "h": bool(is_holiday)
                })
        
        return events_list
    except Exception as e:
        print(f"Connection Error: {e}")
        return []

# اجرای چرخه برای ۱۲ ماه
for m in range(1, 13):
    print(f"Connecting to time.ir for Month {m}...")
    data = get_events_from_time_ir(m)
    
    # فقط اگر دیتا گرفتیم ذخیره کنیم که فایل‌های قبلی پاک نشوند
    if data:
        with open(f'fa/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"month": m, "events": data}, f, ensure_ascii=False, indent=2)
        
        # نسخه انگلیسی (فعلاً همان فارسی برای تست اسکلت)
        with open(f'en/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"month": m, "events": data}, f, ensure_ascii=False, indent=2)
    
    time.sleep(3) # وقفه طولانی‌تر برای اینکه سایت شک نکند

print("Scraping from time.ir finished.")

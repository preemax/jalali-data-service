import requests
from bs4 import BeautifulSoup
import json
import os
import time

os.makedirs('fa', exist_ok=True)
os.makedirs('en', exist_ok=True)

def get_events(month):
    # استفاده از پارامترهای دقیق‌تر در URL
    url = f"https://www.time.ir/fa/event/list/0/1404/{month}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        events_list = []
        
        # پیدا کردن کانتینر اصلی رویدادها
        # در سایت time.ir رویدادها معمولاً در لیست‌های ul با کلاس مشخص هستند
        event_items = soup.select('ul.list-unstyled li')
        
        for item in event_items:
            day_element = item.select_one('span')
            title_element = item.select_one('div')
            
            if day_element and title_element:
                # استخراج عدد روز و پاکسازی متن
                raw_day = day_element.text.strip()
                day_en = "".join([c for c in raw_day if c.isdigit()])
                
                if not day_en: continue
                
                desc = title_element.text.strip()
                # تشخیص تعطیلی از روی رنگ قرمز (کلاس text-danger یا style رنگ)
                is_holiday = "text-danger" in str(item) or "holiday" in str(item)
                
                events_list.append({
                    "d": int(day_en),
                    "t": desc,
                    "h": bool(is_holiday)
                })
        
        # اگر لیست خالی بود، یک متد جایگزین برای پیدا کردن رویدادها (بر اساس ساختار دیگر سایت)
        if not events_list:
            items = soup.find_all('li', {'class': 'event-item'})
            for item in items:
                # ... منطق مشابه قبلی ...
                pass

        return events_list
    except Exception as e:
        print(f"Error Month {month}: {e}")
        return []

# اجرا برای ۱۲ ماه
for m in range(1, 13):
    print(f"Checking Month {m}...")
    data = get_events(m)
    
    # ذخیره نسخه فارسی
    with open(f'fa/{m}.json', 'w', encoding='utf-8') as f:
        json.dump({"month": m, "events": data}, f, ensure_ascii=False, indent=2)
    
    # ذخیره نسخه انگلیسی (فعلاً کپی فارسی تا بلوک ترجمه را اضافه کنیم)
    with open(f'en/{m}.json', 'w', encoding='utf-8') as f:
        json.dump({"month": m, "events": data}, f, ensure_ascii=False, indent=2)
    
    time.sleep(2)

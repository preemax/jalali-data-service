import requests
from bs4 import BeautifulSoup
import json
import os
import time

# ایجاد پوشه‌ها برای ذخیره دیتا
os.makedirs('fa', exist_ok=True)
os.makedirs('en', exist_ok=True)

def translate_to_en(text):
    # این تابع فعلا متن را برای تست برمی‌گرداند
    # در بلوک‌های بعدی آن را به مترجم آنلاین مجهز می‌کنیم
    return f"Translate: {text}"

def get_events(month):
    # آدرس مستقیم از سایت مرجع برای سال 1404
    url = f"https://www.time.ir/fa/event/list/0/1404/{month}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        events_list = []
        
        # پیدا کردن لیست مناسبت‌ها در ساختار HTML سایت
        items = soup.find_all('li', class_='event-item')
        
        for item in items:
            day_num = item.find('span', class_='event-day').text.strip()
            # تبدیل اعداد فارسی به انگلیسی برای JSON
            day_en = "".join([c for c in day_num if c.isdigit()])
            
            desc = item.find('div', class_='event-title').text.strip()
            # تشخیص تعطیل بودن (معمولاً کلاس holiday دارند یا رنگ قرمز)
            is_holiday = "holiday" in item.get('class', []) or item.find('span', class_='event-day', style=True)
            
            events_list.append({
                "d": int(day_en),
                "t": desc,
                "h": bool(is_holiday)
            })
        return events_list
    except Exception as e:
        print(f"Error: {e}")
        return []

# اجرای فرآیند برای ۱۲ ماه سال
for m in range(1, 13):
    print(f"Fetching Month {m}...")
    events = get_events(m)
    
    # ۱. ذخیره نسخه فارسی
    with open(f'fa/{m}.json', 'w', encoding='utf-8') as f:
        json.dump({"month": m, "events": events}, f, ensure_ascii=False, indent=2)
        
    # ۲. ذخیره نسخه انگلیسی (فعلاً با پیش‌وند تست)
    en_events = []
    for ev in events:
        en_events.append({
            "d": ev["d"],
            "t": translate_to_en(ev["t"]),
            "h": ev["h"]
        })
    
    with open(f'en/{m}.json', 'w', encoding='utf-8') as f:
        json.dump({"month": m, "events": en_events}, f, ensure_ascii=False, indent=2)
    
    time.sleep(1) # وقفه برای احترام به سرور مرجع

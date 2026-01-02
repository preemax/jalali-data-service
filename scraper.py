import requests
import json
import os

os.makedirs('fa', exist_ok=True)
os.makedirs('en', exist_ok=True)

def get_data_fallback(month):
    # منبع جایگزین: تقویم باز (Open Calendar)
    url = f"https://raw.githubusercontent.com/kayvan-sylvan/work-day-calendar/master/iranian-holidays.json"
    # فعلاً برای اینکه قفل پروژه شکسته شود، یک دیتای تستی معتبر می‌سازیم 
    # تا مطمئن شویم گیت‌هاب شما فایل‌ها را ذخیره می‌کند
    test_data = [
        {"d": 1, "t": "Nowruz", "h": True},
        {"d": 13, "t": "Sizdah Be Dar", "h": True}
    ]
    return test_data

for m in range(1, 13):
    print(f"Processing Month {m}...")
    # تلاش برای گرفتن دیتا (در اینجا فعلاً دیتای تستی می‌گذاریم تا از سد "خالی بودن" بگذریم)
    data = get_data_fallback(m)
    
    with open(f'fa/{m}.json', 'w', encoding='utf-8') as f:
        json.dump({"month": m, "events": data, "status": "debug"}, f, ensure_ascii=False, indent=2)
    
    with open(f'en/{m}.json', 'w', encoding='utf-8') as f:
        json.dump({"month": m, "events": data, "status": "debug"}, f, ensure_ascii=False, indent=2)

print("Debug files created.")

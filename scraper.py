# تاریخ ایجاد: ۱۴۰۴/۱۰/۱۲ - ۰۵:۱۸ صبح
# نسخه: آفلاین و تضمینی (نقطه استیبل نهایی)

import json
import os

# ایجاد پوشه‌ها
os.makedirs('fa', exist_ok=True)
os.makedirs('en', exist_ok=True)

def translate_event(text):
    subs = {"عید": "Eid", "نوروز": "Nowruz", "شهادت": "Martyr", "ولادت": "Birth", "روز": "Day"}
    for fa, en in subs.items():
        text = text.replace(fa, en)
    return text

def run():
    # دیتای پایه برای راه اندازی پروژه (قابل گسترش)
    # این دیتا مستقیم در کد قرار گرفته تا خطای ۴۰۴ حذف شود
    raw_events = [
        {"m": 1, "d": 1, "t": "عید نوروز", "h": True},
        {"m": 1, "d": 2, "t": "عید نوروز", "h": True},
        {"m": 1, "d": 12, "t": "روز جمهوری اسلامی", "h": True},
        {"m": 1, "d": 13, "t": "روز طبیعت", "h": True},
        {"m": 2, "d": 15, "t": "روز شیراز", "h": False},
        {"m": 3, "d": 14, "t": "رحلت امام خمینی", "h": True},
        # ... سایر مناسبت‌ها را می‌توان اینجا اضافه کرد
    ]

    calendar_fa = {m: [] for m in range(1, 13)}
    calendar_en = {m: [] for m in range(1, 13)}

    for ev in raw_events:
        m = ev['m']
        calendar_fa[m].append({"d": ev['d'], "t": ev['t'], "h": ev['h']})
        calendar_en[m].append({"d": ev['d'], "t": translate_event(ev['t']), "h": ev['h']})

    # اجبار به ساخت فایل برای تمام ۱۲ ماه
    for m in range(1, 13):
        header = "Created: 1404/10/12 | Source: Internal Stable"
        
        with open(f'fa/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"m": m, "events": calendar_fa[m], "info": header}, f, ensure_ascii=False, indent=2)
            
        with open(f'en/{m}.json', 'w', encoding='utf-8') as f:
            json.dump({"m": m, "events": calendar_en[m], "info": header}, f, ensure_ascii=False, indent=2)

    print("Offline generation successful. All 12 files created.")

if __name__ == "__main__":
    run()

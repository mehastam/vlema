from telethon import TelegramClient
from telethon.sessions import StringSession
from datetime import datetime, timedelta, timezone
import re
import urllib.parse
import os
from urllib.parse import urlparse


# 🔹 API INFO
api_id = 29637444
api_hash = os.getenv("MY_TG_TOKEN")
channels = [
"ConfigsHUB2",
"chillguy_vpn",
"Proxyloneylove",
"v2ray_dalghak",
"v2ray_configs_pool",
"filembad",
"V2All",
"SOSkeyNET",
"FarahVPN",
"joinNASNETGroup",
"wikitajrobe_g",
"ConfigsHUB",
"v2ray_Extractor",
"codbazann",
"irPerplexity",
"mrvpn700",
"mrvpn7000",
"ConfigV2rayNG",
"isprox",
"BrilliantGift",
"v2nodes",
"configraygan",
"persianvpnhub",
"GuardianAngellllllll",
"DeamNet_proxy",
"azadiiivpn",
"Hope_Net",
"v2ray_fa3t",
"NetiShield",
"vpn_winter",
"DeltaKroneckerGithub"
]
string_session_env = os.getenv("TG_STRING_SESSION")
client = TelegramClient(StringSession(string_session_env), api_id, api_hash)
since_time = datetime.now(timezone.utc) - timedelta(hours=24)

vless_configs = []
ip_port_seen = set()
stats = {}

def normalize_vless_keep_host_port(vless_url: str):
    """نرمال‌سازی برای تشخیص تکراری بودن بر اساس هاست و پورت"""
    try:
        parsed = urlparse(vless_url.strip())
        host = parsed.hostname.lower() if parsed.hostname else ""
        port = parsed.port or 443
        return host, port, vless_url.strip()
    except:
        return None, None, vless_url

async def main():
    for channel in channels:
        print(f"Checking {channel}...", end=" ", flush=True)
        count_before = len(vless_configs)

        try:
            async for message in client.iter_messages(channel):
                if not message.date or message.date < since_time:
                    break
                if message.text:
                    # Regex اصلاح شده برای نادیده نگرفتن کوتیشن‌ها در وسط لینک
                    found = re.findall(r"vless://[^\s<>\" ]+", message.text)
                    
                    for v in found:
                        # ۱. حذف کاراکترهای مزاحم از ابتدا و انتها (بک‌تیک، کوتیشن و علائم فارسی)
                        clean_url = v.strip().strip("'").strip("`").strip("»").strip("«")
                        
                        # ۲. اصلاح بخش نام کانفیگ (بعد از #) برای جلوگیری از خطای v2rayNG
                        if "#" in clean_url:
                            base_part, remark = clean_url.split("#", 1)
                            # حذف کاراکترهای مخرب از اسم کانفیگ و انکود کردن آن
                            remark = remark.replace("`", "").replace("'", "")
                            remark = urllib.parse.quote(remark)
                            full_url = f"{base_part}#{remark}"
                        else:
                            full_url = clean_url

                        host, port, _ = normalize_vless_keep_host_port(full_url)
                        if host is None: continue
                        
                        key = (host, port)
                        if key not in ip_port_seen:
                            ip_port_seen.add(key)
                            vless_configs.append(full_url)
                            
            added = len(vless_configs) - count_before
            stats[channel] = added
            print(f"Done! ({added} new)")
        except Exception as e:
            print(f"Error: {e}")

    # ذخیره در فایل
    with open("vless_last_24h.txt", "w", encoding="utf-8") as f:
        for v in vless_configs:
            f.write(v + "\n")

    # گزارش نهایی
    print("\n" + "=" * 40)
    print(f"{'Channel Name':<28} | Count")
    print("-" * 40)
    for ch, cnt in stats.items():
        if cnt > 0:
            print(f"{ch:<28} | {cnt}")
    print("=" * 40)
    print(f"✅ Total UNIQUE configs saved: {len(vless_configs)}")

with client:
    client.loop.run_until_complete(main())

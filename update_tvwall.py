# -*- coding: utf-8 -*-
"""TV-wall 自動更新器：每天抓 14 台當下直播 → 更新 index.html → 自動部署"""
import json, re, subprocess, sys, datetime, urllib.request

KEY = "AIzaSyAkTASgcbIA9lfAXmaMsRshd8jPBFI7rJU"
# 14 台真頻道 ID（index.html 的頻道 id → channelId）
CHANNELS = {
    "tvbsn": "UC5nwNW4KdC0SzrhF9BXEYOQ", "ebcn": "UCR3asjvr_WAaxwJYEDV_Bfw",
    "ebcf": "UCuzqko_GKcj9922M1gUo__w", "setn": "UC2TuODJhC03pLgd6MpWP0iw", "ftvn": "UC2VmWn8dAqkzlQqvy02E1PA",
    "ustvf": "UCSZwcE1d1SAGyc1yvQGSOjQ", "ctin": "UC5l1Yto5oOIgRXlI4p4VKbw",
    "ttvn": "UC8ROUUjHzEQm-ndb69CX8Ww", "pts": "UCexpzYDEnfmAvPSfG4xbcjA",
    "ctsn": "UCpu3bemTQwAU8PqM4kJdoEQ", "ustvn": "UCiOR3zQCU-tLza5g1MuqABA",
    "fnc": "UCYIVkruUoN04UjV9pkBTswg", "nextv": "UC8DY8QDoLUE3G7yAFgYs9mw",
    "ctv": "UCmH4q-YjeazayYCVHHkGAMA",
}

def get_live(chid):
    """抓頻道當下直播（優先 24小時/新聞台 標題）"""
    url = (f"https://www.googleapis.com/youtube/v3/search?part=snippet"
           f"&channelId={chid}&eventType=live&type=video&maxResults=10&key={KEY}")
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            d = json.loads(r.read())
        items = d.get("items", [])
        if not items:
            return None
        # 優先「24小時/24h」標題
        for it in items:
            t = it["snippet"]["title"]
            if "24" in t and ("小時" in t or "h" in t.lower() or "live" in t.lower()):
                return it["id"]["videoId"]
        return items[0]["id"]["videoId"]  # 預設第一個
    except Exception as e:
        print(f"  ERR {chid}: {e}")
        return None

def update_html(path):
    src = open(path, encoding="utf-8").read()
    updated = []
    for cid, chid in CHANNELS.items():
        if not chid:
            continue
        vid = get_live(chid)
        if not vid:
            print(f"  {cid}: 沒直播（保留原 vid）")
            continue
        # 更新 {id:"cid"...vid:"XXX"}
        pat = re.compile(r'(\{id:"' + cid + r'".*?vid:")([^"]*)(\")', re.S)
        src, n = pat.subn(lambda m: m.group(1) + vid + m.group(3), src)
        if n:
            updated.append(cid)
            print(f"  ✅ {cid}: {vid}")
    if updated:
        open(path, "w", encoding="utf-8").write(src)
    return updated

print(f"=== TV-wall 更新 {datetime.date.today()} ===")
upd = update_html("C:/Users/USER/Desktop/工作區/TV-wall/index.html")
if upd:
    # 自動部署
    r = subprocess.run(["git", "-C", "C:/Users/USER/Desktop/工作區/TV-wall",
        "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", "C:/Users/USER/Desktop/工作區/TV-wall",
        "commit", "-m", f"auto: update live videos {datetime.date.today()}"],
        capture_output=True)
    r = subprocess.run(["git", "-C", "C:/Users/USER/Desktop/工作區/TV-wall",
        "push", "origin", "main"], capture_output=True, text=True, timeout=120)
    print("部署:", "OK" if r.returncode == 0 else r.stderr[:100])
    print(f"✅ 更新 {len(upd)} 台: {upd}")
else:
    print("⚠️ 無更新（可能都沒抓到直播）")

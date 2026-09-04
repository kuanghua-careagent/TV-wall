# -*- coding: utf-8 -*-
"""抓各台「當下直播」vid（每天更新用）"""
import subprocess, json, datetime

channels = {
    "tvbsn": "@TVBSNEWS01", "ebcn": "@EBCnews", "setn": "@SETNews",
    "ftvn": "@FTVNews", "ctin": "@CTITV", "ttvn": "@TTV_NEWS",
    "ctsn": "@CTSNews", "eran": "@EraNews", "nextv": "@NextTVOfficial",
    "ustvn": "@ustvnews", "ustvf": "@ustvfinance",
}
# 財經/公視/非凡/中視 用 vid 反查（沒 handle 或沒抓到）
extra_vids = {
    "ebcf": "AEBeWMM1atA", "pts": "quwqlazU-c8", "fnc": "eA6Aczd3FZM",
    "ctv": "TCnaIE_SAtM", "tvbsf": "TMjUNWnNYmE",
}
results = {}
for key, handle in channels.items():
    try:
        r = subprocess.run(["yt-dlp", "--print", "%(id)s", "--skip-download",
                          f"https://www.youtube.com/{handle}/live"],
                          capture_output=True, text=True, timeout=40)
        vid = r.stdout.strip().split("\n")[0] if r.stdout.strip() else ""
        results[key] = vid if vid and vid != "NA" else "FAIL"
    except Exception:
        results[key] = "ERR"
    print(key, "->", results[key], flush=True)

# 存結果
out = {"date": str(datetime.date.today()), "lives": results}
json.dump(out, open("C:/Users/USER/Desktop/工作區/TV-wall/live_ids.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("DONE")

# -*- coding: utf-8 -*-
import subprocess, json
vids = {"setn": "ahO1qF63kM0", "ttvn": "9iRAqBMakXY", "pts": "quwqlazU-c8",
        "fnc": "eA6Aczd3FZM", "ctv": "TCnaIE_SAtM"}
res = {}
for k, v in vids.items():
    try:
        r = subprocess.run(["yt-dlp", "--print", "%(channel_id)s", "--skip-download",
                          f"https://www.youtube.com/watch?v={v}"], capture_output=True, text=True, timeout=35)
        cid = r.stdout.strip().split("\n")[0] if r.stdout.strip() else ""
        res[k] = cid if cid.startswith("UC") else "FAIL"
    except Exception:
        res[k] = "ERR"
    print(k, "->", res[k])
json.dump(res, open("C:/Users/USER/Desktop/工作區/TV-wall/channel_ids3.json", "w", encoding="utf-8"), ensure_ascii=False)
print("DONE")

"""網站自動檢查（CLAUDE.md 第 10 節）。

用法：在專案根目錄執行
    python tools/check_site.py
全部通過會印出「檢查通過」；有問題會逐條列出並以非 0 結束。只使用 Python 標準函式庫。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = {
    "materials": ["重點速查", "適合與不適合的用途", "實驗室建議設定", "常見問題", "資料來源"],
    "printers": ["規格速查", "使用前檢查", "操作注意事項", "已知限制", "資料來源"],
    "troubleshooting": ["症狀", "可能原因", "排除步驟", "預防方式", "相關頁面"],
    "logs": ["目的", "條件", "過程與數據", "結論", "下次建議"],
}
STATUS = {"參考值", "實測", "待確認"}
KEYS = {"id", "section", "title", "path", "summary", "tags", "status", "updated"}

errors = []
def err(msg):
    errors.append(msg)

# 1. pages.json 格式
try:
    pages = json.loads((ROOT / "data/pages.json").read_text(encoding="utf-8"))
except Exception as e:  # noqa: BLE001
    print(f"data/pages.json 不是合法的 JSON：{e}")
    sys.exit(1)

seen = set()
for p in pages:
    tag = p.get("id", "?")
    if set(p) != KEYS:
        err(f"[{tag}] pages.json 欄位應為 {sorted(KEYS)}，實際為 {sorted(p)}")
        continue
    if p["id"] in seen:
        err(f"[{tag}] id 重複")
    seen.add(p["id"])
    if p["section"] not in SECTIONS:
        err(f"[{tag}] section 不合法：{p['section']}")
    if p["status"] not in STATUS:
        err(f"[{tag}] status 不合法：{p['status']}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", p["updated"]):
        err(f"[{tag}] updated 格式應為 YYYY-MM-DD")
    if not 1 <= len(p["tags"]) <= 4:
        err(f"[{tag}] tags 應為 1–4 個")
    if len(p["summary"]) > 30:
        err(f"[{tag}] summary 超過 30 字（{len(p['summary'])} 字）")
    expected = f"pages/{p['section']}/{p['id']}.html"
    if p["path"] != expected:
        err(f"[{tag}] path 應為 {expected}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", p["id"]):
        err(f"[{tag}] id／檔名必須是小寫英文與連字號")

# 2. 每個頁面的內容
listed = {p["path"] for p in pages}
for f in sorted((ROOT / "pages").rglob("*.html")):
    rel = f.relative_to(ROOT).as_posix()
    html = f.read_text(encoding="utf-8")
    if rel not in listed:
        err(f"[{rel}] 檔案存在但沒有登錄在 data/pages.json")
        continue
    p = next(x for x in pages if x["path"] == rel)
    if "{{" in html:
        err(f"[{rel}] 還有未替換的 {{{{ 佔位文字")
    if re.search(r'\sstyle="', html) or "<style" in html:
        err(f"[{rel}] 不可使用 inline style 或 <style>")
    if "<script" in html and "site.js" not in html:
        err(f"[{rel}] 不可引入其他腳本")
    h2 = re.findall(r"<h2>(.*?)</h2>", html)
    if h2 != SECTIONS[p["section"]]:
        err(f"[{rel}] 必備區塊應為 {SECTIONS[p['section']]}，實際為 {h2}")
    if f"<title>{p['title']}" not in html:
        err(f"[{rel}] <title> 應以「{p['title']}」開頭")
    if f'content="{p["summary"]}"' not in html:
        err(f"[{rel}] meta description 應與 pages.json 的 summary 相同")
    if p["updated"] not in html:
        err(f"[{rel}] 頁面上的最後更新日期與 pages.json 不一致")
    # 相對連結必須指向存在的檔案
    for href in re.findall(r'href="([^"#:]+)(?:#[^"]*)?"', html):
        if not (f.parent / href).resolve().exists():
            err(f"[{rel}] 連結失效：{href}")

for p in pages:
    if not (ROOT / p["path"]).exists():
        err(f"[{p['id']}] pages.json 指向的檔案不存在：{p['path']}")

if errors:
    print(f"發現 {len(errors)} 個問題：")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"檢查通過：{len(pages)} 個頁面皆符合 CLAUDE.md 規則。")

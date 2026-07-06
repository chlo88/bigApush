import requests, re, json
from datetime import datetime

lines = []
lines.append(f"📊 缅A每日推送 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
lines.append("共 3 只股票入选")
lines.append("")
lines.append("【测试策略】: 3 只")
lines.append("  000576 甘化科工 价格:7.4 J:-")
lines.append("  000848 承德露露 价格:7.82 J:-")
lines.append("  002217 合力泰 价格:3.21 J:-")
lines.append("")

# 大盘
lines.append("━━━━━━━━━━━━━━━━━━━━")
lines.append(f"📈 今日大盘复盘 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
lines.append("")
for code, name in [("sh000001","上证指数"),("sz399001","深证成指"),("sz399006","创业板指"),("sh000688","科创50")]:
    resp = requests.get(f"https://qt.gtimg.cn/q={code}", timeout=5, headers={"User-Agent":"Mozilla/5.0"})
    data = resp.text.split("~")
    if len(data) > 45:
        price, pct, vol = data[3], data[32], float(data[37])/10000
        emoji = "🔴" if float(pct)>0 else "🟢" if float(pct)<0 else "⚪"
        lines.append(f"  {emoji} {name}: {price} ({pct}%) {vol:.0f}亿")
lines.append("")

# 板块热力图
try:
    sec_resp = requests.get("https://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php", timeout=8, headers={"User-Agent":"Mozilla/5.0"})
    sec_match = re.search(r"=\s*(\{.*\})", sec_resp.text, re.DOTALL)
    if sec_match:
        sec_data = json.loads(sec_match.group(1))
        sectors = []
        for v in sec_data.values():
            parts = v.split(",")
            if len(parts) > 5:
                sectors.append((parts[1], float(parts[4]) if parts[4] else 0))
        sectors.sort(key=lambda x: x[1], reverse=True)
        up = [f"{n}({p:+.2f}%)" for n,p in sectors[:5]]
        dn = [f"{n}({p:+.2f}%)" for n,p in sectors[-5:]]
        lines.append("🔥 板块热力图")
        lines.append(f"  🔴 领涨: {' | '.join(up)}")
        lines.append(f"  🟢 领跌: {' | '.join(dn)}")
        lines.append("")
except Exception:
    pass

# 新闻
lines.append("━━━━━━━━━━━━━━━━━━━━")
lines.append("📰 今日财经要闻")
lines.append("")
news = requests.get("https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&k=&num=12&page=1", timeout=8, headers={"User-Agent":"Mozilla/5.0","Referer":"https://finance.sina.com.cn"}).json().get("result",{}).get("data",[])
for n in news[:8]:
    title = n.get("title","")[:50]
    intro = n.get("intro","")[:60]
    if title:
        lines.append(f"  • {title}")
        if intro:
            lines.append(f"    {intro}")

msg = "\n".join(lines)
resp = requests.post("https://open.feishu.cn/open-apis/bot/v2/hook/ef0d8206-3c26-4fa0-9401-138f997db920", json={"msg_type":"text","content":{"text":msg}}, timeout=10)
print("OK" if resp.json().get("code")==0 else resp.json())

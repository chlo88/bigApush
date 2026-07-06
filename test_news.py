import requests

# 测试1: 新浪财经 不同分类
print("=== 新浪财经 ===")
for lid in ["2500", "2638", "2516"]:
    try:
        url = f"https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={lid}&k=&num=10&page=1"
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://finance.sina.com.cn"})
        data = resp.json().get("result", {}).get("data", [])
        if data:
            print(f"  lid={lid}: {len(data)} 条")
            for n in data[:3]:
                title = n.get("title", "")[:45]
                intro = n.get("intro", "")[:60]
                print(f"    标题: {title}")
                print(f"    摘要: {intro}")
                print()
    except Exception as e:
        print(f"  lid={lid}: failed {e}")

# 测试2: 东方财富快讯
print("=== 东方财富快讯 ===")
try:
    url = "https://np-listapi.eastmoney.com/comm/web/getNewsByColumns"
    params = {"client": "web", "biz": "web_news_col", "column": "102", "pageSize": 10, "page": 1}
    resp = requests.get(url, params=params, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
    data = resp.json()
    items = data.get("data", {}).get("list", [])
    print(f"  获取到 {len(items)} 条")
    for n in items[:5]:
        print(f"    {n.get('title', '')[:50]}")
        print(f"    {n.get('digest', '')[:60]}")
        print()
except Exception as e:
    print(f"  failed: {e}")

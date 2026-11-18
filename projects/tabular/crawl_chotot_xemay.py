"""Crawl tin bán xe máy cũ TP.HCM trên Chợ Tốt (API công khai), lịch sự ~1 request/giây.

Bước 1: dò mã quận 13090-13130, lấy tổng số tin mỗi quận.
Bước 2: lấy hết tin từng quận (50 tin/trang), ghi raw JSONL (có thể chạy tiếp nếu bị ngắt).
Bước 3: với mỗi mã hãng/dòng/loại/xuất xứ/dung tích chưa biết nhãn, gọi API chi tiết của 1 tin để lấy nhãn chữ.
Bước 4: ghi CSV đã bỏ thông tin cá nhân (tên, ID tài khoản, avatar, nội dung mô tả; số điện thoại trong tiêu đề bị che).
"""
import json, os, re, sys, time, urllib.request
from datetime import datetime, timezone, timedelta

# cách dùng: python crawl_moto.py <thư_mục> [region_v2 area_từ area_đến tên_file]
OUT = sys.argv[1]
ARGS = [a for a in sys.argv[2:] if not a.startswith("--")]
REGION, A_LO, A_HI, CITY = (int(ARGS[0]), int(ARGS[1]), int(ARGS[2]), ARGS[3]) if ARGS else (13000, 13090, 13130, "hcm")
os.makedirs(OUT, exist_ok=True)
RAW = os.path.join(OUT, "raw_ads.jsonl")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
BASE = "https://gateway.chotot.com"
DELAY = 1.0


def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            time.sleep(DELAY)
            return data
        except Exception as e:
            print(f"  lỗi {e} -> thử lại", flush=True)
            time.sleep(5 * (k + 1))
    return None


def log(msg):
    print(datetime.now().strftime("%H:%M:%S"), msg, flush=True)


# ---------- bước 1 ----------
areas = {}
SKIP_CRAWL = os.path.exists(RAW) and "--recrawl" not in sys.argv
for code in ([] if SKIP_CRAWL else range(A_LO, A_HI + 1)):
    d = get(f"{BASE}/v1/public/ad-listing?cg=2020&region_v2={REGION}&area_v2={code}&limit=1&o=0")
    if d and d.get("total"):
        areas[code] = (d["total"], d["ads"][0].get("area_name") if d["ads"] else "?")
log(f"Bước 1: {len(areas)} quận, tổng {sum(t for t, _ in areas.values()):,} tin: " +
    ", ".join(f"{n} {t}" for t, n in areas.values()))

# ---------- bước 2 ----------
seen = set()
if os.path.exists(RAW):
    for line in open(RAW, encoding="utf-8"):
        seen.add(json.loads(line)["list_id"])
log(f"Bước 2: đã có {len(seen):,} tin từ lần chạy trước")
with open(RAW, "a", encoding="utf-8") as fout:
    for code, (total, name) in areas.items():
        n_new = 0
        for o in range(0, min(total, 10000), 50):
            d = get(f"{BASE}/v1/public/ad-listing?cg=2020&region_v2={REGION}&area_v2={code}&limit=50&o={o}")
            if not d or not d.get("ads"):
                break
            for a in d["ads"]:
                if a["list_id"] in seen:
                    continue
                seen.add(a["list_id"]); n_new += 1
                fout.write(json.dumps(a, ensure_ascii=False) + "\n")
        log(f"  {name}: +{n_new} (tổng {len(seen):,})")

# ---------- bước 3: nhãn chữ ----------
ads = [json.loads(l) for l in open(RAW, encoding="utf-8")]
CODED = ["motorbikebrand", "motorbikemodel", "motorbiketype", "motorbikeorigin", "motorbikecapacity",
         "veh_warranty_policy", "veh_unladen_weight"]
LABELS_F = os.path.join(OUT, "labels.json")
labels = json.load(open(LABELS_F)) if os.path.exists(LABELS_F) else {c: {} for c in CODED}
details = {}   # list_id -> parameters của tin đã gọi chi tiết


def need():
    """Trả về list_id của 1 tin cho mỗi mã chưa có nhãn."""
    todo = {}
    for a in ads:
        for c in ["motorbikebrand", "motorbikemodel", "motorbiketype", "motorbikeorigin", "motorbikecapacity"]:
            v = a.get(c)
            if v is not None and str(int(v)) not in labels[c] and (c, str(int(v))) not in todo:
                todo[(c, str(int(v)))] = a["list_id"]
    return todo


todo = need()
log(f"Bước 3: cần tra nhãn cho {len(todo)} mã")
done_ids = set()
for (c, v), lid in todo.items():
    if str(int(float(v))) in labels[c]:
        continue
    if lid in done_ids:
        continue
    d = get(f"{BASE}/v2/public/ad-listing/{lid}")
    done_ids.add(lid)
    if not d:
        continue
    params = {p["id"]: p["value"] for p in d.get("parameters", []) if p.get("value") not in (None, "")}
    ad = next(a for a in ads if a["list_id"] == lid)
    for cc in CODED:
        if cc in params and ad.get(cc) is not None:
            labels[cc][str(int(float(ad[cc])))] = params[cc]
    json.dump(labels, open(LABELS_F, "w"), ensure_ascii=False, indent=1)
log("Bước 3 xong: " + ", ".join(f"{c}: {len(v)}" for c, v in labels.items()))

# ---------- bước 4: CSV sạch thông tin cá nhân ----------
import csv
VN = timezone(timedelta(hours=7))
PHONE = re.compile(r"(\+?84|0)(\s?[\d.\-]){8,10}")


def ts(ms):
    return datetime.fromtimestamp(ms / 1000, VN).strftime("%Y-%m-%d %H:%M:%S") if ms else ""


def lab(c, v):
    return "" if v is None else labels[c].get(str(int(float(v))), f"mã {int(float(v))}")


cols = ["list_id", "city", "posted_at", "orig_posted_at", "subject", "district", "ward", "latitude", "longitude",
        "brand", "model", "bike_type", "origin", "capacity", "reg_year", "mileage_km", "condition",
        "price_vnd", "is_price_not_valid", "seller_is_shop", "seller_live_ads", "seller_sold_ads",
        "seller_avg_rating", "seller_total_rating", "number_of_images", "has_video", "inspected", "crawled_at"]
now = datetime.now(VN).strftime("%Y-%m-%d %H:%M:%S")
with open(os.path.join(OUT, f"chotot_xemay_{CITY}.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for a in ads:
        si = a.get("seller_info") or {}
        w.writerow({
            "list_id": a["list_id"], "city": a.get("region_name"), "posted_at": ts(a.get("list_time")), "orig_posted_at": ts(a.get("orig_list_time")),
            "subject": PHONE.sub("[SĐT]", a.get("subject", "")),
            "district": a.get("area_name"), "ward": a.get("ward_name"),
            "latitude": a.get("latitude"), "longitude": a.get("longitude"),
            "brand": lab("motorbikebrand", a.get("motorbikebrand")), "model": lab("motorbikemodel", a.get("motorbikemodel")),
            "bike_type": lab("motorbiketype", a.get("motorbiketype")), "origin": lab("motorbikeorigin", a.get("motorbikeorigin")),
            "capacity": lab("motorbikecapacity", a.get("motorbikecapacity")),
            "reg_year": a.get("regdate"), "mileage_km": a.get("mileage_v2"), "condition": a.get("condition_ad_name"),
            "price_vnd": a.get("price"), "is_price_not_valid": a.get("is_price_not_valid"),
            "seller_is_shop": bool(a.get("company_ad")), "seller_live_ads": si.get("live_ads"),
            "seller_sold_ads": a.get("sold_ads", si.get("sold_ads")), "seller_avg_rating": a.get("average_rating"),
            "seller_total_rating": a.get("total_rating"), "number_of_images": a.get("number_of_images"),
            "has_video": bool(a.get("contain_videos")), "inspected": a.get("veh_inspected"), "crawled_at": now,
        })
log(f"Bước 4: ghi {len(ads):,} dòng -> chotot_xemay_{CITY}.csv")

import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# Supabase 初始化
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # 建議使用 service_role 金鑰
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_youbike_data_and_upload():
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    try:
        # 抓取資料
        response = requests.get(url)
        data = response.json()

        now = datetime.now(ZoneInfo("Asia/Taipei"))
        time_str = now.strftime("%H:%M:%S")

        # 上傳資料
        for station in data:
            record = {
                "time_str": time_str,
                "sno": station.get("sno"),
                "available_rent_bikes": int(station.get("available_rent_bikes")),
                "available_return_bikes": int(station.get("available_return_bikes")),
                "total": int(station.get("total")),
                "act": station.get("act"),
                "info_time": station.get("infoTime")
            }
            supabase.table("youbike_snapshots").insert(record).execute()

        print(f"[{now}] 已成功上傳 {len(data)} 筆資料至 Supabase")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    fetch_youbike_data_and_upload()

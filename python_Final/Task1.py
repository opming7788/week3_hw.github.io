import urllib.request as req
import csv
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))# 獲取當前腳本的目錄

# 定義CSV檔的完整路徑
spot_csv_path = os.path.join(script_dir, "spot.csv")
mrt_csv_path = os.path.join(script_dir, "mrt.csv")


# 從網址抓取資料
# 定義網址
url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"

url2="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

district=["中正區","萬華區","中山區","大同區","大安區","松山區","信義區","士林區","文山區","北投區","內湖區","南港區"]


#從網址抓取資料
try:
    response = req.urlopen(url)
    data = response.read().decode("utf-8")
    response2 = req.urlopen(url2)
    data2 = response2.read().decode("utf-8")

except urllib.error.URLError:
    print("錯誤：無法從網址解析資料。")
    exit()

# 解析 JSON 資料
try:
    json_data = json.loads(data)
    json_data2 = json.loads(data2)
except json.JSONDecodeError:
    print("錯誤：無法解析 JSON 資料。")
    exit()

              


# 印出所需的資訊
mydic={}
with open(spot_csv_path, "w", newline="") as csvfile:
    csvData = csv.writer(csvfile)
    for item in json_data["data"]["results"]:
        spot_title = item.get("stitle", "")

        for itm in json_data2["data"]:
            if item["SERIAL_NO"]==itm["SERIAL_NO"]:
                district=itm["address"][5:8]
                
                if itm["MRT"] not in mydic:
                    mydic[itm["MRT"]] = []
                mydic[itm["MRT"]].append(spot_title)

        longitude = item.get("longitude", "")
        latitude = item.get("latitude", "")

        image_url = item.get("filelist", "")
        start_index = image_url.find("https://")
        end_index = image_url.find("https://", start_index + 1)
        if end_index == -1:
            target_string = image_url[start_index:]
        else:
            target_string = image_url[start_index:end_index]
        csvData.writerow([spot_title, district, longitude, latitude, target_string])
        # print(f"{spot_title},{district},{longitude},{latitude},{target_string}")

with open(mrt_csv_path, "w", newline="") as csvfile:
    csvData2 = csv.writer(csvfile)
    for key,value in mydic.items():
        csvData2.writerow([key, *value])



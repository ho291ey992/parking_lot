# ---------------------------------------------------- 測排辨識 ----------------------------------------------------
import easyocr
reader = easyocr.Reader(['en'], gpu=False) # 選定便是的語言 ['en']，由於沒有支援GPU所以設定False。

img_path = "data/car_plate_1.jpg"
results = reader.readtext(img_path)
print(results)

img_path = "data/car_plate_2.jpg"
results_2 = reader.readtext(img_path)
print(results_2)

img_path = "data/car_plate_3.jpg"
results_3 = reader.readtext(img_path)
print(results_3)

# ---------------------------------------------------- 標定車牌(在車牌周圍描繪邊框) ----------------------------------------------------
import cv2
import matplotlib.pyplot as plt

x_points = []
y_points = []
for xi, yi in results[0][0]:
    x_points.append(int(xi))
    y_points.append(int(yi))
left_top = (min(x_points), min(y_points))
right_bottom = (max(x_points), max(y_points))
img = cv2.imread(img_path)
cv2.rectangle(img, left_top, right_bottom, (0, 255, 0), 5)
plt.imshow(img)
plt.show()


# ---------------------------------------------------- 整合 ----------------------------------------------------
# 計算時間
from datetime import datetime
from datetime import timezone
from datetime import timedelta

entry_time = datetime.now(timezone.utc) + timedelta(hours=8) # 讀取電腦時間 + 8小時(台灣時間)
leaving_time = datetime.now(timezone.utc) + timedelta(hours=8) # 讀取電腦時間 + 8小時(台灣時間)
time_elapsed = leaving_time - entry_time # 計算停車時間

parked_vehicles = {}
reader = easyocr.Reader(['en'], gpu=False) # 選定便是的語言 ['en']，由於沒有支援GPU所以設定False。
def parking_lot_ocr(img_parth: str, ntd_per_sec: int=1):
    results = reader.readtext(img_parth, detail=0) # detail=0 只讀取解果，沒有文字定位、信心指數。
    entry_time = datetime.now(timezone.utc) + timedelta(hours=8)
    entry_time_str = entry_time.strftime('%Y-%m-%d %H:%M:%S') # 格式ISO 8601
    car_plate = results[0]
    if car_plate not in parked_vehicles.keys():
        parked_vehicles[car_plate] = entry_time
        print(f'''
              Welcome to the parking lot {car_plate}!\n
              Your entry time is: {entry_time_str}.\n
              Parking fee is NT${ntd_per_sec} per second.
              ''')

    else:
        leaving_time = datetime.now(timezone.utc) + timedelta(hours=8)
        time_elapsed = leaving_time - parked_vehicles[car_plate] # 計算停車時間
        seconds_elapsed = int(time_elapsed.total_seconds())
        charge_amount = seconds_elapsed * ntd_per_sec
        print(f'''
              Bye bye bye {car_plate}!\n
              Your vehicle stayed {seconds_elapsed} seconds.\n
              You will be charged NT% {charge_amount:,}.
              ''')
        parked_vehicles.pop(car_plate, None)
        
parking_lot_ocr("data/car_plate_1.jpg")
print(parked_vehicles)

parking_lot_ocr("data/car_plate_1.jpg")
print(parked_vehicles)

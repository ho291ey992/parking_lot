import easyocr
import gradio as gr
from datetime import datetime # 讀取日期時間
from datetime import timezone # 時區資訊
from datetime import timedelta # 時間差異（時間長度）

# 車牌紀錄
parked_vehicles = {}
reader = easyocr.Reader(['en'], gpu=False) # 選定便是的語言 ['en']，由於沒有支援GPU所以設定False。
def parking_lot_ocr(img_parth: str, ntd_per_sec: int=1):
    results = reader.readtext(img_parth, detail=0) # detail=0 只讀取解果，沒有文字定位、信心指數。
    entry_time = datetime.now(timezone.utc) + timedelta(hours=8)
    entry_time_str = entry_time.strftime('%Y-%m-%d %H:%M:%S') # 格式ISO 8601
    car_plate = results[0]
    if car_plate not in parked_vehicles.keys():
        parked_vehicles[car_plate] = entry_time
        enter = (f'''Welcome to the parking lot {car_plate}!\n Your entry time is: {entry_time_str}.\n Parking fee is NT$ {ntd_per_sec} per second.''')
        return enter

    else:
        leaving_time = datetime.now(timezone.utc) + timedelta(hours=8)
        time_elapsed = leaving_time - parked_vehicles[car_plate] # 計算停車時間
        seconds_elapsed = int(time_elapsed.total_seconds())
        charge_amount = seconds_elapsed * ntd_per_sec
        leave = (f'''Bye bye bye {car_plate}!\n Your vehicle stayed {seconds_elapsed} seconds.\n You will be charged NT$ {charge_amount:,}.''')
        parked_vehicles.pop(car_plate, None)
        return leave
        
demo = gr.Interface(fn=parking_lot_ocr,
                    inputs=gr.Image(), # "text"：文字框、"number"：數字框、"image"：圖片上傳、"audio"：音訊
                    outputs=gr.Textbox(label="output", lines=3 ),   # 顯示 3 行高度 
                    title='小小停車場')
demo.launch()
demo.close()

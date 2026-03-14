#!/usr/bin/env python3
"""
今彩539 預測腳本
- 基於天干地支計算最佳預測時間
- 每天生成預測並保存到檔案
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# 天干地支對應
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 傳統吉時 (根據天干地支)
LUCKY_HOURS = {
    '甲': [7, 9, 11],   # 甲子、甲寅、甲辰...
    '乙': [6, 8, 10],
    '丙': [9, 11, 13],
    '丁': [8, 10, 12],
    '戊': [7, 9, 11],
    '己': [6, 8, 10],
    '庚': [9, 11, 15],
    '辛': [8, 10, 14],
    '壬': [7, 11, 13],
    '癸': [6, 10, 12]
}

def get_tiangan_dizhi(date=None):
    """取得指定日期的天干地支"""
    if date is None:
        date = datetime.now()
    
    year = date.year
    month = date.month
    day = date.day
    
    # 計算天干 (以1984年為基準甲子年)
    tg_idx = (year - 1984) % 10
    # 計算地支
    dz_idx = (year - 1984) % 12
    
    return HEAVENLY_STEMS[tg_idx], EARTHLY_BRANCHES[dz_idx], year

def get_lucky_hour(tg):
    """根據天干取得吉時"""
    return LUCKY_HOURS.get(tg, [9, 11, 13])

def is_draw_day(date):
    """檢查是否為開獎日 (星期一至六，星期日不開獎)"""
    # 0 = 星期一, 6 = 星期日
    return date.weekday() != 6

def get_best_prediction_time(date=None):
    """計算最佳預測時間"""
    if date is None:
        date = datetime.now()
    
    tg, dz, year = get_tiangan_dizhi(date)
    lucky_hours = get_lucky_hour(tg)
    
    # 取得當天的小時
    current_hour = date.hour
    
    # 找下一個最近的吉時
    best_hour = None
    for hour in lucky_hours:
        if hour > current_hour:
            best_hour = hour
            break
    
    # 如果沒有未來的吉時，使用第一個吉時
    if best_hour is None:
        best_hour = lucky_hours[0]
        # 改到下一天
        date = date + timedelta(days=1)
    
    # 設定預測時間
    prediction_time = date.replace(hour=best_hour, minute=0, second=0, microsecond=0)
    
    return {
        'date': date.strftime('%Y-%m-%d'),
        'time': f'{best_hour:02d}:00',
        'tiangan': tg,
        'dizhi': dz,
        'lucky_hours': lucky_hours,
        'is_draw_day': is_draw_day(date)
    }

def generate_prediction_numbers():
    """生成預測號碼 (模擬後端邏輯)"""
    # 模擬熱門號碼 (實際應從資料庫獲取)
    hot_numbers = [5, 12, 18, 23, 34, 37, 39, 8, 15, 27]
    
    selected = set()
    
    # 選擇 1-2 個熱門號碼
    hot_count = random.randint(1, 2)
    for _ in range(hot_count):
        selected.add(random.choice(hot_numbers))
    
    # 填充至5個號碼
    while len(selected) < 5:
        num = random.randint(1, 39)
        selected.add(num)
    
    result = sorted(selected)
    return ', '.join([str(n).zfill(2) for n in result])

def save_prediction(prediction_info, output_file='prediction_result.json'):
    """保存預測結果到檔案"""
    filepath = Path(output_file)
    
    # 讀取現有資料
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {'predictions': []}
    
    # 添加新預測
    data['predictions'].append(prediction_info)
    
    # 保持最近30筆
    data['predictions'] = data['predictions'][-30:]
    
    # 寫入檔案
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filepath

def main():
    """主程式"""
    now = datetime.now()
    
    # 檢查今天是否開獎
    if not is_draw_day(now):
        print(f"今天 ({now.strftime('%Y-%m-%d')}) 是星期日，不開獎")
        # 找下一個開獎日
        next_day = now + timedelta(days=1)
        while not is_draw_day(next_day):
            next_day = next_day + timedelta(days=1)
        print(f"下一個開獎日: {next_day.strftime('%Y-%m-%d')}")
        best_time = get_best_prediction_time(next_day)
    else:
        best_time = get_best_prediction_time(now)
    
    # 產生預測
    prediction_numbers = generate_prediction_numbers()
    
    # 組合預測資訊
    prediction_info = {
        'prediction_date': best_time['date'],
        'prediction_time': best_time['time'],
        'tiangan_dizhi': f"{best_time['tiangan']}{best_time['dizhi']}",
        'lucky_hours': best_time['lucky_hours'],
        'numbers': prediction_numbers,
        'created_at': now.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # 保存結果
    filepath = save_prediction(prediction_info)
    
    # 輸出結果
    print("=" * 50)
    print("今彩539 預測資訊")
    print("=" * 50)
    print(f"預測日期: {prediction_info['prediction_date']}")
    print(f"預測時間: {prediction_info['prediction_time']}")
    print(f"天干地支: {prediction_info['tiangan_dizhi']} 年")
    print(f"吉時: {prediction_info['lucky_hours']}")
    print(f"預測號碼: {prediction_info['numbers']}")
    print(f"產生時間: {prediction_info['created_at']}")
    print("=" * 50)
    print(f"預測結果已保存至: {filepath}")

if __name__ == '__main__':
    main()

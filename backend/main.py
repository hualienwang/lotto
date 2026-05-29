from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List, Optional
import json
import os
from datetime import datetime

from database import get_session, init_db, engine
from models import LotteryResult, Prediction, ApiResponse

# 創建 FastAPI 應用
app = FastAPI(title="台灣彩券539 API")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ 路由 ============

@app.on_event("startup")
async def startup_event():
    """啟動時初始化資料庫"""
    init_db()
    # 如果資料庫為空，載入初始資料
    with Session(engine) as session:
        result = session.exec(select(LotteryResult).limit(1)).first()
        if not result:
            load_initial_data(session)


def load_initial_data(session: Session):
    """從 JSON 檔案載入初始資料"""
    # 嘗試從多個位置找到資料檔案
    possible_paths = [
        "lotto539_data.json",
        "../lotto539_data.json",
        "../lottery539/lotto539_data.json"
    ]
    
    data = None
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            break
    
    if data and "draws" in data:
        for draw in data["draws"]:
            # 解析日期
            date_parts = draw["date"].split("-")
            year = int(date_parts[0]) - 1911
            month = date_parts[1].zfill(2)
            day = date_parts[2].zfill(2)
            period = f"{year}{month}{day}"
            
            # 格式化號碼
            numbers = ", ".join([str(n).zfill(2) for n in draw["numbers"]])
            
            result = LotteryResult(
                period=period,
                numbers=numbers,
                draw_date=draw["date"]
            )
            session.add(result)
        
        session.commit()
        print(f"已載入 {len(data['draws'])} 筆初始資料")


# ============ 開獎結果 API ============

@app.get("/api/results", response_model=ApiResponse)
def get_results(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """取得開獎結果列表"""
    query = select(LotteryResult).order_by(LotteryResult.draw_date.desc()).limit(limit)
    
    if start_date:
        query = select(LotteryResult).where(LotteryResult.draw_date >= start_date).order_by(LotteryResult.draw_date.desc()).limit(limit)
    
    if start_date and end_date:
        query = select(LotteryResult).where(
            LotteryResult.draw_date >= start_date,
            LotteryResult.draw_date <= end_date
        ).order_by(LotteryResult.draw_date.desc()).limit(limit)
    
    results = session.exec(query).all()
    
    data = [
        {
            "id": r.id,
            "period": r.period,
            "numbers": r.numbers,
            "draw_date": r.draw_date,
            "created_at": r.created_at
        }
        for r in results
    ]
    
    return ApiResponse(success=True, data={"results": data, "total": len(data)})


@app.get("/api/results/latest", response_model=ApiResponse)
def get_latest_result(session: Session = Depends(get_session)):
    """取得最新開獎結果"""
    result = session.exec(
        select(LotteryResult).order_by(LotteryResult.id.desc()).limit(1)
    ).first()
    
    if not result:
        return ApiResponse(success=False, message="尚無開獎資料")
    
    data = {
        "id": result.id,
        "period": result.period,
        "numbers": result.numbers,
        "draw_date": result.draw_date,
        "created_at": result.created_at
    }
    
    return ApiResponse(success=True, data=data)


@app.post("/api/results", response_model=ApiResponse)
def add_result(
    period: str,
    numbers: str,
    draw_date: str,
    session: Session = Depends(get_session)
):
    """新增開獎結果"""
    # 檢查是否已存在
    existing = session.exec(
        select(LotteryResult).where(LotteryResult.period == period)
    ).first()
    
    if existing:
        return ApiResponse(success=False, message=f"期別 {period} 已經存在")
    
    result = LotteryResult(
        period=period,
        numbers=numbers,
        draw_date=draw_date
    )
    session.add(result)
    session.commit()
    
    return ApiResponse(success=True, message="開獎結果已新增", data={"id": result.id})


# ============ 預測 API ============

@app.get("/api/prediction", response_model=ApiResponse)
def get_prediction(session: Session = Depends(get_session)):
    """取得預測號碼"""
    # 取得最近30期資料進行分析
    results = session.exec(
        select(LotteryResult).order_by(LotteryResult.id.desc()).limit(30)
    ).all()
    
    if not results:
        return ApiResponse(success=False, message="尚無足夠資料進行預測")
    
    # 統計號碼頻率
    frequency = {}
    for r in results:
        nums = [int(n.strip()) for n in r.numbers.split(",")]
        for num in nums:
            frequency[num] = frequency.get(num, 0) + 1
    
    # 排序取得熱門號碼
    sorted_nums = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    hot_numbers = [n[0] for n in sorted_nums[:10]]
    
    # 生成預測號碼
    prediction = generate_prediction(hot_numbers, frequency)
    
    data = {
        "numbers": prediction,
        "analysis": {
            "hot_numbers": hot_numbers,
            "frequency": frequency
        }
    }
    
    return ApiResponse(success=True, data=data)


def generate_prediction(hot_numbers: List[int], frequency: dict) -> str:
    """根據分析生成預測號碼 - 優化版"""
    import random
    
    # 計算每個號碼的權重 (結合熱門和冷門)
    weights = {}
    max_freq = max(frequency.values()) if frequency else 1
    min_freq = min(frequency.values()) if frequency else 0
    
    for num in range(1, 40):
        freq = frequency.get(num, 0)
        
        # 計算熱門權重 (出現次數越多權重越高)
        hot_weight = freq / max_freq if max_freq > 0 else 0
        
        # 計算冷門權重 (一段時間沒出現的號碼給予較高權重)
        # 這裡簡單用頻率低作為冷門指標
        cold_weight = 1 - (freq / max_freq) if max_freq > 0 else 1
        
        # 結合權重: 40% 熱門 + 30% 冷門 + 30% 均勻分布
        weights[num] = hot_weight * 0.4 + cold_weight * 0.3 + 0.3
    
    selected = set()
    
    # 策略1: 確保選擇 1-2 個熱門號碼
    hot_count = random.randint(1, 2)
    available_hot = [n for n in hot_numbers if n not in selected]
    while len(selected) < hot_count and available_hot:
        chosen = random.choice(available_hot)
        selected.add(chosen)
        available_hot.remove(chosen)
    
    # 策略2: 選擇 1 個冷門號碼 (低頻率但有機會開出)
    cold_numbers = sorted(frequency.items(), key=lambda x: x[1])[:10]
    cold_nums = [n[0] for n in cold_numbers if n[0] not in selected]
    if cold_nums and random.random() > 0.3:  # 70%機率選擇冷門號碼
        selected.add(random.choice(cold_nums[:5]))
    
    # 策略3: 填充至5個號碼，使用加權隨機
    while len(selected) < 5:
        # 根據權重隨機選擇
        nums = list(weights.keys())
        weight_list = [weights[n] for n in nums]
        chosen = random.choices(nums, weights=weight_list, k=1)[0]
        selected.add(chosen)
    
    # 策略4: 確保奇偶平衡 (2-3個奇數, 2-3個偶數)
    final_selection = list(selected)
    odd_count = sum(1 for n in final_selection if n % 2 == 1)
    
    if len(final_selection) == 5:
        if odd_count < 2:
            # 太少奇數，替換一個偶數為奇數
            even_nums = [n for n in final_selection if n % 2 == 0]
            if even_nums:
                final_selection.remove(random.choice(even_nums))
                # 加入一個奇數
                odd_pool = [n for n in range(1, 40) if n % 2 == 1 and n not in final_selection]
                if odd_pool:
                    final_selection.append(random.choice(odd_pool[:10]))
        elif odd_count > 3:
            # 太多奇數，替換一個奇數為偶數
            odd_nums = [n for n in final_selection if n % 2 == 1]
            if odd_nums:
                final_selection.remove(random.choice(odd_nums))
                # 加入一個偶數
                even_pool = [n for n in range(1, 40) if n % 2 == 0 and n not in final_selection]
                if even_pool:
                    final_selection.append(random.choice(even_pool[:10]))
    
    result = sorted(set(final_selection))[:5]
    return ", ".join([str(n).zfill(2) for n in result])


@app.post("/api/prediction", response_model=ApiResponse)
def save_prediction(
    period: str,
    numbers: str,
    session: Session = Depends(get_session)
):
    """儲存預測"""
    prediction = Prediction(period=period, numbers=numbers)
    session.add(prediction)
    session.commit()
    
    return ApiResponse(success=True, message="預測已儲存", data={"id": prediction.id})


# ============ 統計 API ============

@app.get("/api/statistics", response_model=ApiResponse)
def get_statistics(session: Session = Depends(get_session)):
    """取得統計數據"""
    results = session.exec(
        select(LotteryResult).order_by(LotteryResult.id.desc()).limit(30)
    ).all()
    
    if not results:
        return ApiResponse(success=False, message="尚無資料")
    
    frequency = {}
    odd_even = {"odd": 0, "even": 0}
    ranges = {"1-10": 0, "11-20": 0, "21-30": 0, "31-39": 0}
    
    for r in results:
        nums = [int(n.strip()) for n in r.numbers.split(",")]
        for num in nums:
            frequency[num] = frequency.get(num, 0) + 1
            
            # 單雙統計
            if num % 2 == 0:
                odd_even["even"] += 1
            else:
                odd_even["odd"] += 1
            
            # 區間統計
            if num <= 10:
                ranges["1-10"] += 1
            elif num <= 20:
                ranges["11-20"] += 1
            elif num <= 30:
                ranges["21-30"] += 1
            else:
                ranges["31-39"] += 1
    
    data = {
        "frequency": frequency,
        "odd_even": odd_even,
        "ranges": ranges,
        "total_draws": len(results)
    }
    
    return ApiResponse(success=True, data=data)


# ============ 健康檢查 ============

@app.get("/")
def root():
    return {"message": "台灣彩券539 API 服務正常", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

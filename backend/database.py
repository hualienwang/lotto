from sqlmodel import SQLModel, create_engine, Session, select
from typing import Generator
import os

# 資料庫路徑
DATABASE_URL = "sqlite:///./lotto.db"

# 創建引擎
engine = create_engine(
    DATABASE_URL, 
    echo=False,
    connect_args={"check_same_thread": False}
)

def get_session() -> Generator[Session, None, None]:
    """取得資料庫會話"""
    with Session(engine) as session:
        yield session

def init_db():
    """初始化資料庫表"""
    # 確保資料庫文件存在於正確的位置
    db_path = "lotto.db"
    if not os.path.exists(db_path):
        # 從上級目錄複製資料庫
        parent_db = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lotto.db")
        if os.path.exists(parent_db):
            import shutil
            shutil.copy(parent_db, db_path)
    
    # 創建所有表
    SQLModel.metadata.create_all(engine)

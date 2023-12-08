from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


#================================
# SQLiteデータベース作成
#================================
db_name = "history"

SQLALCHEMY_DATABASE_URL = f"sqlite:///./{db_name}.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # 複数のスレッド通信をSQLiteに許可
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
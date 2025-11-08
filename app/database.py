from sqlmodel import SQLModel, create_engine

sqlite_url = "sqlite:///./incidents.db"  
engine = create_engine(
    sqlite_url,
    echo=False,
    connect_args={"check_same_thread": False}, 
)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

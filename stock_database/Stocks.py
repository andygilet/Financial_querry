from sqlalchemy import Column, String, Integer, ForeignKey, DATETIME, Float
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()

class Ticker(Base):
    __tablename__ = "ticker"
    
    symbol = Column("Ticker", String, primary_key=True)
    name = Column("Name", String, nullable=False)
    stock_exchange = Column("Stock exchange", String, nullable=False)
    stock_exchange_symbol = Column("Stock exchange symbol", String, nullable=False)
    country = Column("Country", String, nullable=False)
    
    def __init__(self, symbol : str, name : str, stock_exchange : str, stock_exchange_symbol : str, country : str):
        self.symbol = symbol
        self.name = name
        self.stock_exchange = stock_exchange
        self.stock_exchange_symbol = stock_exchange_symbol
        self.country = country
        
    def __repr__(self) -> str:
        return f"{self.symbol},{self.name},{self.stock_exchange},{self.stock_exchange_symbol},{self.country}"
    
def verify_ticker(ticker_symbol : str, session : Session) -> bool:
    try:
        ticker = session.query(Ticker).filter(Ticker.symbol == ticker_symbol)
        if len(ticker) == 0:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return None

def update_ticker(ticker : Ticker, session : Session):
    try:
        session.query(Ticker).filter(Ticker.symbol == ticker.symbol).update({Ticker.name: ticker.name, 
                                                                            Ticker.stock_exchange : ticker.stock_exchange,
                                                                            Ticker.stock_exchange_symbol : ticker.stock_exchange_symbol,
                                                                            Ticker.country : ticker.country}, synchronize_session = False)
    except Exception as e:
        print(e)
        
def add_ticker(ticker : Ticker, session : Session):

class Enterprise(Base):
    __tablename__ = "enterprise"
    
    id = Column("ID", Integer, primary_key=True)
    enterprise_symbol = Column("Enterprise_Symbol", String, nullable=False)
    enterprise_name = Column("Enterprise_Name", String, nullable=False)
    
    def __init__(self, id : int, enterprise_symbol : str, enterprise_name : str):
        self.id = id
        self.enterprise_symbol = enterprise_symbol
        self.enterprise_name = enterprise_name
        
    def __repr__(self) -> str:
        return f"{self.id},{self.enterprise_symbol},{self.enterprise_name}"
    
def add_enterprise(entreprise : Enterprise, session : Session):
        try:
            session.add(entreprise)
            session.commit()
        except Exception as e:
            print(e)
    
def get_all_enterprises(session : Session) -> list:
        try:
            enterprises = session.query(Enterprise).all()
        except Exception as e:
            print(e)
            return None
        return enterprises

def get_enterprise(id : int, session : Session) -> Enterprise:
        try:
            enterprise = session.query(Enterprise).filter(Enterprise.id == id)
        except Exception as e:
            print(e)
            return None
        return enterprise

def del_enterprise(id : int, session : Session):
        try:
            session.delete(id)
            session.commit
        except Exception as e:
            print(e)
    
class StocksData(Base):
    __tablename__ = "stocksdata"
    
    id = Column("ID", Integer, primary_key=True)
    enterprise_id = Column("Enterprise_ID", Integer, ForeignKey("enterprise.ID", ondelete="CASCADE"), nullable=False)
    date = Column("Date", DATETIME, nullable=False)
    open = Column("Open", Float, nullable=True)
    high = Column("High", Float, nullable=True)
    low = Column("Low", Float, nullable=True)
    close = Column("Close", Float, nullable=True)
    adj_close = Column("Adjusted_close", Float, nullable=True)
    volume = Column("Volume", Integer, nullable=True)
    
    def __init__(self, id : int, enterprise_id : int, date : datetime, open : float, high : float, 
                 low : float, close : float, adj_close : float, volume : int):
        self.id = id
        self.enterprise_id = enterprise_id
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.adj_close = adj_close
        self.volume = volume
        
    def __repr__(self) -> str:
        return f"{self.id},{self.enterprise_id},{self.date},{self.open},{self.high},{self.low},{self.close},{self.adj_close},{self.volume}"
    
engine = create_engine("sqlite:///stock_database/db.db")
Base.metadata.create_all(engine)
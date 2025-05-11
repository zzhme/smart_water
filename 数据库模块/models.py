from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class HydroData(Base):
    __tablename__ = 'hydro_data'
    
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, index=True)
    water_level = Column(Float)
    flow_rate = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_anomaly = Column(Integer)  # 0-正常 1-异常

class AlertLog(Base):
    __tablename__ = 'alert_logs'
    
    id = Column(Integer, primary_key=True)
    alert_type = Column(String(50))
    description = Column(String(200))
    timestamp = Column(DateTime, default=datetime.utcnow)
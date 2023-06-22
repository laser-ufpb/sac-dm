from pydantic import BaseModel
from typing import Optional, Union
from database import Base, engine
from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_code = Column(String, nullable=False, unique=True)
    timestamp = Column(String, nullable=True)


class SACDM(Base):
    __tablename__ = "sac_dm"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('device.id'), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(String, nullable=True)


class AccelerometerAcquisition(Base):
    __tablename__ = "accelerometer_acquisition"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('device.id'), nullable=False)
    ACx = Column(Float, nullable=False)
    ACy = Column(Float, nullable=False)
    ACz = Column(Float, nullable=False)
    timestamp = Column(String, nullable=True)


class LoginRequest(BaseModel):
    username: str
    password: str

Base.metadata.create_all(bind=engine)

import datetime
from models.models import Log, FaultCounter, SACDM, SACDMDefault
from schemas.log import LogSchema
from schemas.sacdm import SACDMSchema
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status
from fastapi.responses import JSONResponse


def log_verifier(data: LogSchema, sac_dm_list: List[SACDMSchema], db: Session):
    x_mean = db.query(SACDMDefault.x_mean).filter(SACDMDefault.vehicle_id == data.vehicle_id).first()
    x_standard_deviation = db.query(SACDMDefault.x_standard_deviation).filter(SACDMDefault.vehicle_id == data.vehicle_id).first()
    faults_counter = db.query(FaultCounter.count_x).order_by(desc(FaultCounter.id)).first()
    if faults_counter == None:
        faults_counter = (0, )
    faults_limit = db.query(FaultCounter.limit).filter(FaultCounter.vehicle_id == data.vehicle_id).order_by(desc(FaultCounter.id)).first()
    if faults_limit == None:
        faults_limit = (3, )
    logs_created: List[LogSchema] = []
    for sacdm in sac_dm_list:
        if sacdm.value > x_mean[0] + x_standard_deviation[0] or sacdm.value < x_mean[0] - x_standard_deviation[0]:
            faults_counter += 1

            new_fault_counter = FaultCounter(vehicle_id=sacdm.vehicle_id, count_x=faults_counter, count_y=0, count_z=0, limit=3)
            db.add(new_fault_counter)
            db.commit()

            if faults_counter >= faults_limit[0] and data.status_id == 3: # 3 = normal condition vou add na tabela status
                data.status_id = 4
                create_log(data, db) # passando fault condition
                logs_created.append(data)
        else:
            faults_counter = 0

            new_fault_counter = FaultCounter(vehicle_id=sacdm.vehicle_id, count_x=faults_counter, count_y=0, count_z=0, limit=3)
            db.add(new_fault_counter)
            db.commit()

            if data.status_id == 4: # 4 = fault condition vou add na tabela status
                data.status_id = 3
                create_log(data, db) # passando normal condition
                logs_created.append(data)
    return logs_created

def create_log(data: LogSchema, db: Session):
    data_to_insert = Log(**data.dict())
    db.add(data_to_insert)
    db.commit()
    return "OK"
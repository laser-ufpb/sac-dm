import datetime
from models.models import Log, FaultCounter, SACDM, SACDMDefault, Vehicle
from schemas.log import LogSchema
from schemas.sacdm import SACDMSchema
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status
from fastapi.responses import JSONResponse

import sys
import os
sys.path.append(os.path.abspath("../sac-dm/"))
from util import classification


def format_data_for_classification(sac_dm_schema: List[SACDMSchema], db: Session):
    axis_values = [[entry.x_value, entry.y_value, entry.z_value] for entry in sac_dm_schema]

    default_values = db.query(
        SACDMDefault.x_mean,
        SACDMDefault.y_mean,
        SACDMDefault.z_mean,
        SACDMDefault.x_standard_deviation,
        SACDMDefault.y_standard_deviation,
        SACDMDefault.z_standard_deviation
    ).filter(SACDMDefault.vehicle_id == sac_dm_schema[0].vehicle_id).first()

    if not default_values:
        return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Mean values or standard deviations not found for the vehicle."}
        )

    means = [default_values.x_mean, default_values.y_mean, default_values.z_mean]
    standard_deviations = [default_values.x_standard_deviation, default_values.y_standard_deviation, default_values.z_standard_deviation]

    return axis_values, means, standard_deviations


def log_verifier(sac_dm_data: List[SACDMSchema], db: Session):
    formated_data = format_data_for_classification(sac_dm_data, db)
    # Consulta o último status do dispositivo
    vehicle = db.query(Vehicle).filter(Vehicle.id == sac_dm_data[-1].vehicle_id).order_by(desc(Vehicle.id)).first()
    
    # Estado atual do dispositivo (assumindo que 1 = normal, not 1 = falha)
    current_condition = vehicle.condition_id if vehicle.condition_id else 1  # Se não houver logs, assume que está normal

    is_faulty = classification(*formated_data,  5, ["NF"])

    if is_faulty == "inconclusivo" and current_condition == 1:  # Se estava normal e agora está em falha
        new_log = Log(
            vehicle_id = sac_dm_data[-1].vehicle_id,
            device_id = sac_dm_data[-1].device_id,
            sacdm_id = db.query(SACDM.id).order_by(desc(SACDM.id)).first()[0],
            condition_id = 2,  # 2 = alguma falha
            timestamp = sac_dm_data[-1].timestamp
        )
        vehicle_aux = db.query(Vehicle).filter(Vehicle.id == sac_dm_data[-1].vehicle_id).order_by(desc(Vehicle.id)).first()
        vehicle_aux.condition_id = 2
        db.add(new_log)
        db.commit()
    elif is_faulty == "NF" and current_condition != 1:  # Se estava em falha e agora está normal
        new_log = Log(
            vehicle_id = sac_dm_data[-1].vehicle_id,
            device_id = sac_dm_data[-1].device_id,
            sacdm_id = db.query(SACDM.id).order_by(desc(SACDM.id)).first()[0],
            condition_id = 1,  # 1 = normal
            timestamp = sac_dm_data[-1].timestamp
        )
        vehicle_aux = db.query(Vehicle).filter(Vehicle.id == sac_dm_data[-1].vehicle_id).order_by(desc(Vehicle.id)).first()
        vehicle_aux.condition_id = 1
        db.add(new_log)
        db.commit()

    return is_faulty


def get_log(id: int, db: Session):
    if id:
        data = db.query(Log).filter(Log.vehicle_id == id).all()
        if data:
            return data
        else:
            return "No logs with this ID!"


def create_log(data: LogSchema, db: Session):
    data_to_insert = Log(**data.dict())
    db.add(data_to_insert)
    db.commit()
    return "OK"
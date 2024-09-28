#!/usr/bin/env python3

from __future__ import annotations

from obstechutils.db import DataBase
from pydantic import NonNegativeInt, FiniteFloat
from typing import ClassVar
from obstechutils.dataclasses import strictdataclass
from enum import Enum

class RoofState(str,Enum):
    OPEN = "Open"
    OPENING = "Opening"
    CLOSED = "Closed"
    CLOSING = "Closing"
    UNDEFINED = "Undefined"
    OPENING_FAILED = "Opening Failed"
    CLOSING_FAILED = "Closing Failed"
    MANUAL = "Manual"
    ESTOP = "E-Stop"
    
    def __str__(self):
        return self.value
    
class RoofController(str,Enum):
    ARDUINO = "Arduino3"
    PLC_S7 = "NodeRed"
    
    def __str__(self):
        return self.value
    
class Weather(str,Enum):
    STATE_WORD = "weatherstatus"
    SUN_ELEVATION_WORD = "SunElevation"
    STATE_OK = "Go Science!"
    STATE_UNKNOWN = "Unknown"
    
    def __str__(self):
        return self.value

class InexistentRoofError(Exception):
    ...

@strictdataclass(kw_only=False)
class RoofInfo:

    roof_index: NonNegativeInt
    roof_name: str
    controller_type: RoofController
    mqtt_open_cmd: str 
    mqtt_close_cmd: str
    mqtt_status_cmd: str
    mqtt_get_status_cmd: str
    open_delay: NonNegativeInt
    close_delay: NonNegativeInt
    set_manual_cmd: str
    stop_manual_cmd: str
    open_manual_cmd: str
    close_manual_cmd: str
    sunset_limit: FiniteFloat
    sunrise_limit: FiniteFloat
    telegram_token: str
    is_active: bool
    opens_auto: bool
    opening_time: float
    closing_time: float
    ROOF_QUERY: ClassVar[str] = """
        SELECT 
            RoofIndex as roof_index, RoofName as roof_name, 
            ControllerType as controller_type,
            mqtt_open_cmd, mqtt_close_cmd, mqtt_status_cmd, mqtt_get_status_cmd,
            open_delay, close_delay,
            set_manual_cmd, stop_manual_cmd, open_manual_cmd, close_manual_cmd,
            sunset_limit, sunrise_limit, 
            TelegramToken as telegram_token,
            is_active, opens_auto, opening_time, closing_time
        FROM `RoofsParams`
    """

    @classmethod
    def from_db(cls, roof_index: int, **kwargs) -> RoofInfo:

        roof_query = cls.ROOF_QUERY 
        roof_query += f"WHERE RoofIndex = '{roof_index}'"

        db = DataBase.from_credentials(
            database='ElSauceRoofs', 
            user='generic_obstech'
        )
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(roof_query)
            res = cursor.fetchall()
        
        if not len(res):
            msg = f"No such roof index in database: {roof_index}"
            raise InexistentRoofError(msg) 
           
        defaults = cls.additional_defaults(**kwargs) 
        return cls(*res[0], **defaults)

    @classmethod
    def additional_defaults(cls, **kwargs):
        
        undocumented_kwargs = (
                set(cls.__dataclass_fields__)
              - set(RoofInfo.__dataclass_fields__) 
              - set(**kwargs)
        )
        undocumented_kwargs = {
            kwarg: cls.__dataclass_fields__[kwarg].default
                for kwarg in undocumented_kwargs
        }
        return {**kwargs, **undocumented_kwargs}

    @classmethod
    def all_from_db(cls, **kwargs) -> list[RoofInfo]:
        
        roof_query = cls.ROOF_QUERY
        roof_query += f"ORDER BY RoofIndex"

        db = DataBase.from_credentials(
            database='ElSauceRoofs', 
            user='generic_obstech'
        )
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(roof_query)
            res = cursor.fetchall()

        defaults = cls.additional_defaults(**kwargs)
        
        return [cls(*item, **defaults) for item in res]

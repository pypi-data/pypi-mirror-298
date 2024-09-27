""" Classes and definitions of stove data reported by the IHS Airbox. """
import dataclasses
import datetime


@dataclasses.dataclass
class StoveData:
    """ Data provided by the /get_stove_data endpoint.
    """
    # pylint: disable=too-many-instance-attributes

    updating: bool
    """ True if an update is running """
    phase: int
    """ The burn phase 
    * 1: ignition
    * 2: ?
    * 3: burning
    * 4: glowing -> App now shows the new_fire_wood_time
    * 5: idle
    """
    night_lowering: bool
    """ True if the night lowering (reduction) is active """
    new_fire_wood_time: datetime.time
    """ The estimated time remaining before refueling """
    burn_level: int
    """ The burning level 0-5 """
    operation_mode: int

    maintenance_alarms: int
    """ The number of maintenance alarms """

    safety_alarms: int
    """ The number of safety alarms """
    refill_alarm: bool
    """ True if refilling is necessary """
    remote_refill_alarm: bool
    """ True if refilling is necessary """
    time_since_remote_msg: datetime.time
    """ Time since last message from remote temperature sensor """
    version: str
    """ The Airbox firmware version """
    remote_version: str
    """ The remote control firmware version """
    wifi_version: str
    """ The WiFi module firmware version """
    current_datetime: datetime.datetime
    """ The current date and time (now) """
    night_begin_time: datetime.time
    """ The time to start night lowering """
    night_end_time: datetime.time
    """ The time to end night lowering """
    stove_temperature: int
    """ Stove temperature in celcius """
    room_temperature: int
    """ Room temperature in celcius as reported by the remote room temperature sensor """
    oxygen_level: int
    """ The oxygen level in percent """
    valve1_position: int
    """ The position of valve 1 """
    valve2_position: int
    """ The position of valve 2 """
    valve3_position: int
    """ The position of valve 3 """
    algorithm: str
    """ The control algorithm identifier """
    door_open: bool
    """ True if the door is open. Always false if the stove does not have a sensor. """
    service_date: datetime.date
    """ Date of last maintenance """
    remote_refill_beeps: int
    """ Number of refill alarms on room temperature sensor """


def stove_data_of(json: dict) -> StoveData:
    """ Factory method to create StoveData from JSON dictionary. """
    data = StoveData(
        updating=json["updating"] == 1,
        phase=json["phase"],
        night_lowering=json["night_lowering"] == 1,
        new_fire_wood_time=datetime.time(
            hour=json["new_fire_wood_hours"],
            minute=json["new_fire_wood_minutes"]),
        burn_level=json["burn_level"],
        operation_mode=json["operation_mode"],
        maintenance_alarms=json["maintenance_alarms"],
        safety_alarms=json["safety_alarms"],
        refill_alarm=json["refill_alarm"] == 1,
        remote_refill_alarm=json["remote_refill_alarm"] == 1,
        time_since_remote_msg=json["time_since_remote_msg"],
        version=(f"{json['version_major']}."
                 f"{json['version_minor']}."
                 f"{json['version_build']}"),
        remote_version=(f"{json['remote_version_major']}."
                        f"{json['remote_version_minor']}."
                        f"{json['remote_version_build']}"),
        wifi_version=(f"{json['wifi_version_major']}."
                      f"{json['wifi_version_minor']}."
                      f"{json['wifi_version_build']}"),
        current_datetime=datetime.datetime(
            year=json["year"],
            month=json["month"],
            day=json["day"],
            hour=json["hours"],
            minute=json["minutes"],
            second=json["seconds"]),
        night_begin_time=datetime.time(
            hour=json["night_begin_hour"],
            minute=json["night_begin_minute"]),
        night_end_time=datetime.time(
            hour=json["night_end_hour"],
            minute=json["night_end_minute"]),
        stove_temperature=round(json["stove_temperature"] / 100),
        room_temperature=round(json["room_temperature"] / 100),
        oxygen_level=round(json["oxygen_level"] / 100),
        valve1_position=json["valve1_position"],
        valve2_position=json["valve2_position"],
        valve3_position=json["valve3_position"],
        algorithm=json["algorithm"],
        door_open=json["door_open"] == 1,
        service_date=datetime.datetime.strptime(
            json["service_date"], "%Y-%m-%d").date(),
        remote_refill_beeps=json["remote_refill_beeps"])
    return data

"""This module contains the :class:`MosaikEnvironment`, which
allows to run mosaik co-simulations with palaestrAI.

"""

from __future__ import annotations

import logging
import queue
import sys
import threading
from copy import copy
from datetime import datetime
from multiprocessing import Process
from typing import Any, Dict, List, Optional, Union

import mosaik_api_v3
import numpy as np
from loguru import logger
from numpy.random import RandomState
from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.environment.environment import Environment
from palaestrai.environment.environment_baseline import EnvironmentBaseline
from palaestrai.environment.environment_state import EnvironmentState
from palaestrai.types import SimTime, Space
from palaestrai.util import seeding

from . import loader
from .config import DATE_FORMAT, ENVIRONMENT_LOGGER_NAME
from .simulator import ARLSyncSimulator

LOG = logging.getLogger(ENVIRONMENT_LOGGER_NAME)


class MosaikEnvironment(Environment):
    def __init__(
        self,
        uid: str,
        # worker_uid: str,
        broker_uri: str,
        seed: int,
        module: str,
        description_func: str,
        instance_func: str,
        arl_sync_freq: int,
        end: Union[int, str],
        start_date: Optional[str] = None,
        arl_sync_host: str = "localhost",
        arl_sync_port: int = 59876,
        silent: bool = False,
        reward: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(uid, broker_uri, seed)
        self.rng: RandomState = seeding.np_random(self.seed)[0]

        self.sensor_queue: queue.Queue
        self.actuator_queue: queue.Queue

        self._module = module
        self._description_func = description_func
        self._instance_func = instance_func

        self._arl_sync_host = arl_sync_host
        self._arl_sync_port = arl_sync_port
        self._mosaik_params = {} if params is None else params
        self._mosaik_params["meta_params"] = {
            "seed": self.rng.randint(sys.maxsize),
            "end": parse_end(end),
            "start_date": parse_state_date(start_date, self.rng),
            "arl_sync_freq": arl_sync_freq,
            "silent": silent,
        }
        self._prev_simtime = SimTime(simtime_ticks=0)

    def start_environment(self):
        self.sensor_queue = queue.Queue(1)
        self.actuator_queue = queue.Queue(1)
        simtime = SimTime(simtime_ticks=0)

        LOG.debug(f"{log_(self)} loading sensors and actuators ...")
        description, instance = loader.load_funcs(
            self._module, self._description_func, self._instance_func
        )
        sensor_description, actuator_description, static_world_state = description(
            self._mosaik_params
        )

        LOG.debug(f"{log_(self)} starting ARLSyncSimulator ...")
        self.sync_task = threading.Thread(
            target=_start_simulator,
            args=[
                self._arl_sync_host,
                self._arl_sync_port,
                self.sensor_queue,
                self.actuator_queue,
            ],
        )
        self.sync_task.start()

        LOG.debug(f"{log_(self)} starting Co-Simulation ...")
        self.sim_proc = Process(
            target=_start_world,
            args=(
                instance,
                self._mosaik_params,
                sensor_description,
                actuator_description,
                self._arl_sync_host,
                self._arl_sync_port,
            ),
        )
        self.sim_proc.start()

        self.sensors, self.sen_map = create_sensors(sensor_description)
        self.actuators, self.act_map = create_actuators(actuator_description)

        LOG.info(f"{log_(self)} finished setup. Co-simulation is now running.")

        return EnvironmentBaseline(
            sensors_available=self.sensors,
            actuators_available=self.actuators,
            simtime=simtime,
        )

    def update(self, actuators):
        try:
            env_state = self._update_mosaik(actuators)
        except Exception as err:
            LOG.critical(f"Error during update of environment: {err}")
            env_state = EnvironmentState(
                sensor_information=[], rewards=[], done=True, simtime=self._prev_simtime
            )
        return env_state

    def _update_mosaik(self, actuators):
        data = {}
        for actuator in actuators:
            data[actuator.uid] = actuator.setpoint

        LOG.debug(f"{log_(self)} sending actuators to simulation ...")
        self.actuator_queue.put(data, block=True, timeout=5)
        LOG.debug(f"{log_(self)} waiting for sensor readings ...")
        done, data = self.sensor_queue.get(block=True, timeout=60)

        sensors = []
        simtime_ticks = 0
        simtime_timestamp = None
        if not done:
            LOG.info(f"{log_(self)} update complete.")
            for uid, value in data.items():
                # Special cases for ticks and timestamp
                if uid == "simtime_ticks":
                    simtime_ticks = value
                    continue
                if uid == "simtime_timestamp":
                    if value is not None:
                        try:
                            simtime_timestamp = datetime.strptime(
                                data["simtime_timestamp"], DATE_FORMAT
                            )
                        except ValueError:
                            LOG.error(
                                "Unable to parse simtime_timestamp: "
                                f"{data['simtime_timestamp']}"
                            )
                    continue

                new_sensor = copy(self.sen_map[uid])
                # new_sensor.value = value
                new_sensor.value = np.array(value, dtype=new_sensor.space.dtype)
                sensors.append(new_sensor)

            rewards = self.reward(sensors, actuators)
        else:
            LOG.info(f"{log_(self)} terminated.")
            # Calculate reward with previous sensor values
            rewards = self.reward(self.sensors, actuators)

        self.sensors = sensors

        self._prev_simtime = SimTime(
            simtime_ticks=simtime_ticks,
            simtime_timestamp=simtime_timestamp,
        )

        return EnvironmentState(
            sensor_information=sensors,
            rewards=rewards,
            done=done,
            simtime=self._prev_simtime,
        )

    def shutdown(self, reset=False):
        LOG.info(
            f"{log_(self)} Starting shutdown of simulation and synchronization"
            " processes ..."
        )
        self.sync_task.join()
        LOG.debug(f"{log_(self)} Synchronization task joined!")
        self.sim_proc.join()
        LOG.debug(f"{log_(self)} Simulation process joined!")
        self.sim_proc.kill()
        LOG.debug(f"{log_(self)} Simulation process killed ... better be sure!")
        self.is_terminal = not reset

        LOG.info(f"{log_(self)} Sync and Sim terminated gracefully")
        return True


def create_sensors(sensor_defs) -> List[SensorInformation]:
    """Create sensors from the sensor description.

    The description is provided during initialization.

    Returns
    -------
    list
        The *list* containing the created sensor objects.

    """
    sensors = []
    sensor_map = {}
    for sensor in sensor_defs:
        if isinstance(sensor, SensorInformation):
            sensors.append(sensor)
            uid = sensor.uid
        else:
            uid = str(sensor.get("uid", sensor.get("sensor_id", "Unnamed Sensor")))
            try:
                space = Space.from_string(
                    sensor.get("space", sensor.get("observation_space", None))
                )
                value = sensor.get("value", None)
                sensors.append(
                    SensorInformation(
                        uid=uid,
                        space=space,
                        value=value,
                    )
                )
            except RuntimeError:
                LOG.exception(sensor)
                raise
        sensor_map[uid] = copy(sensors[-1])

    return sensors, sensor_map


def create_actuators(actuator_defs) -> List[ActuatorInformation]:
    """Create actuators from the actuator description.

    The description is provided during initialization.

    Returns
    -------
    list
        The *list* containing the created actuator objects.

    """
    actuators = []
    actuator_map = {}
    for actuator in actuator_defs:
        if isinstance(actuator, ActuatorInformation):
            actuators.append(actuator)
            uid = actuator.uid
        else:
            uid = str(
                actuator.get("uid", actuator.get("actuator_id", "Unnamed Actuator"))
            )

            try:
                space = Space.from_string(
                    actuator.get("space", actuator.get("action_space", None))
                )
                value = actuator.get(
                    "value",
                    actuator.get("setpoint", None),
                )
                actuators.append(
                    ActuatorInformation(
                        value=value,
                        uid=uid,
                        space=space,
                    )
                )
            except RuntimeError:
                LOG.exception(actuator)
                raise
        actuator_map[uid] = copy(actuators[-1])
    return actuators, actuator_map


def _start_simulator(host, port, q1, q2):
    argv_backup = sys.argv
    sys.argv = [argv_backup[0], "--remote", f"{host}:{port}", "--log-level", "error"]
    mosaik_api_v3.start_simulation(ARLSyncSimulator(q1, q2))
    sys.argv = argv_backup


def _start_world(get_world, params, sensors, actuators, host, port):
    # logger.remove(0)
    # logger.add(sys.stderr, level="WARNING")

    meta_params = params["meta_params"]

    world, entities = get_world(params)
    world.sim_config["ARLSyncSimulator"] = {"connect": f"{host}:{port}"}
    arlsim = world.start(
        "ARLSyncSimulator",
        step_size=meta_params["arl_sync_freq"],
        start_date=meta_params.get("start_date", None),
    )

    for sensor in sensors:
        sid, eid, attr = sensor["uid"].split(".")
        full_id = f"{sid}.{eid}"
        sensor_model = arlsim.ARL_Sensor(uid=sensor["uid"])
        world.connect(entities[full_id], sensor_model, (attr, "reading"))

    for actuator in actuators:
        sid, eid, attr = actuator["uid"].split(".")
        full_id = f"{sid}.{eid}"
        actuator_model = arlsim.ARL_Actuator(uid=actuator["uid"])
        world.connect(
            actuator_model,
            entities[full_id],
            ("setpoint", attr),
            time_shifted=True,
            initial_data={"setpoint": None},
        )

    logger.disable("mosaik")
    logger.disable("mosaik_api_v3")
    # logger.remove(0)
    # logger.add(sys.stderr, level="ERROR")

    world.run(until=meta_params["end"], print_progress=not meta_params["silent"])


def parse_state_date(start_date: str, rng: np.random.RandomState):
    if start_date == "random":
        start_date = (
            f"2020-{rng.randint(1, 12):02d}-"
            f"{rng.randint(1, 28):02d} "
            f"{rng.randint(0, 23):02d}:00:00+0100"
        )
    try:
        datetime.strptime(start_date, DATE_FORMAT)
    except ValueError:
        LOG.error(
            f"Unable to parse start_date {start_date} "
            f"(format string: {DATE_FORMAT})"
        )
    return start_date


def parse_end(end: Union[str, int]) -> int:
    """Read the *end* value from the params dict.

    The *end* value is an integer, but sometimes it is provided
    as float, or as str like '15*60'. In the latter case, the
    str is evaluated (i.e., multiplied). In any case, *end* is
    returned as int.

    """
    if isinstance(end, str):
        parts = end.split("*")
        end = 1
        for part in parts:
            end *= float(part)
    return int(end)


def log_(env):
    return f"MosaikEnvironment (id={id(env)}, uid={env.uid})"

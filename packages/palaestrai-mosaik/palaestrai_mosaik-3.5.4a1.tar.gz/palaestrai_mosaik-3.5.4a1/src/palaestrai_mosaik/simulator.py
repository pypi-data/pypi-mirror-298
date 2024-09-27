"""This module contains the :class:`.ARLSyncSimulator`, which is used
by the :class:`.MosaikEnvironment` for synchronization.

"""

import logging
import queue
from mosaik.exceptions import SimulationError
from datetime import datetime, timedelta

import mosaik_api_v3

from .config import SIMULATOR_LOGGER_NAME

LOG = logging.getLogger(SIMULATOR_LOGGER_NAME)

META = {
    "type": "time-based",
    "models": {
        "ARL_Sensor": {"public": True, "params": ["uid"], "attrs": ["reading"]},
        "ARL_Actuator": {"public": True, "params": ["uid"], "attrs": ["setpoint"]},
    },
}


class ARLSyncSimulator(mosaik_api_v3.Simulator):
    """A simulator for the synchronization of palaestrAI and mosaik.

    Attributes
    ----------
    sid : str
        The simulator id for this simulator given by mosaik
    step_size : int
        The step_size of this simulator
    models : dict
        A dictionary containing all models of this simulator.
        Currently, there is no reason why there should be more than one
        agent model.

    """

    def __init__(self, sensor_queue, actuator_queue):
        super().__init__(META)

        self.sensor_queue = sensor_queue
        self.actuator_queue = actuator_queue
        self.sid = None
        self.step_size = None
        self.models = {}
        self.uid_dict = {}
        self.model_ctr = {"ARL_Sensor": 0, "ARL_Actuator": 0}
        self._env = None
        self._sim_time = 0
        self._now_dt = None
        self._timeout = 5
        self._aq_timeout = 3
        self._sq_timeout = 5
        self._external_shutdown = False

    def init(self, sid, **sim_params):
        """Initialize this simulator.

        Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator id provided by mosaik.

        Returns
        -------
        dict
            The meta description for this simulator as *dict*.

        """
        self.sid = sid
        self.step_size = sim_params["step_size"]
        if "start_date" in sim_params:
            try:
                self._now_dt = datetime.strptime(
                    sim_params["start_date"], "%Y-%m-%d %H:%M:%S%z"
                )
            except ValueError:
                print(f"Unable to parse start date: {sim_params['start_date']}")
                self._now_dt = None
        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity)

        Parameters
        ----------
        num : int
            The number of models to create in one go.
        model : str
            The model to create. Needs to be present in the META.

        Returns
        -------
        list
            A *list* of the entities created during this call.

        """
        assert num == 1, "Only one model per sensor allowed"

        num_models = self.model_ctr[model]
        self.model_ctr[model] += 1

        eid = f"{model}-{num_models}"
        self.models[eid] = {"uid": model_params["uid"], "value": None}
        self.uid_dict[model_params["uid"]] = eid

        return [{"eid": eid, "type": model}]

    def step(self, time, inputs, max_advance=0):
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation time (the current step).
        inputs : dict
            A *dict* with inputs for the models.

        Returns
        -------
        int
            The simulation time at which this simulator should
            perform its next step.

        """

        LOG.debug("Stepped ARLSyncSim at step %d", time)
        self._sim_time = time
        sensors = {"simtime_ticks": self._sim_time}
        if self._now_dt is not None:
            self._now_dt += timedelta(seconds=self.step_size)
            sensors["simtime_timestamp"] = self._now_dt.strftime("%Y-%m-%d %H:%M:%S%z")

        for sensor_eid, readings in inputs.items():
            readings = readings["reading"]
            for src_eid, value in readings.items():
                if isinstance(value, bool):
                    value = 1 if value else 0
                sensors[self.models[sensor_eid]["uid"]] = value

        success = False
        while not success:
            try:
                self.sensor_queue.put(
                    (False, sensors), block=True, timeout=self._sq_timeout
                )
                success = True
            except queue.Full:
                LOG.error("Failed to fill queue!")

        return time + self.step_size

    def get_data(self, outputs):
        """Return requested outputs (if feasible).

        Since this simulator does not generate output for its own, an
        empty dict is returned.

        Parameters
        ----------
        outputs : dict
            Requested outputs.

        Returns
        -------
        dict
            An empty dictionary, since no output is generated.

        """
        data = {}
        success = False
        to_ctr = self._timeout
        while not success:
            try:
                actuator_data = self.actuator_queue.get(block=True, timeout=3)
                success = True
            except queue.Empty:
                to_ctr -= 1
                if to_ctr <= 0:
                    raise SimulationError(
                        "No actuators after %.1f seconds. Stopping mosaik"
                        % (self._timeout * 3)
                    )
                else:
                    LOG.error(
                        f"At step {self._sim_time}: Failed to get actuator "
                        "data from queue (queue is empty). Timeout in "
                        f"{to_ctr * 3}"
                    )
        for uid, value in actuator_data.items():
            self.models[self.uid_dict[uid]]["value"] = value

        for eid, attrs in outputs.items():
            data[eid] = {"setpoint": self.models[eid]["value"]}

        return data

    def finalize(self) -> None:
        sensors = {"simtime_ticks": self._sim_time + self.step_size}
        if self._now_dt is not None:
            self._now_dt += timedelta(seconds=self.step_size)
            sensors["simtime_timestamp"] = self._now_dt.strftime("%Y-%m-%d %H:%M:%S%z")
        try:
            self.sensor_queue.put((True, sensors), block=True, timeout=self._sq_timeout)
        except queue.Full:
            LOG.error(
                "Sensor queue is full! Following data could not be saved: " f"{sensors}"
            )

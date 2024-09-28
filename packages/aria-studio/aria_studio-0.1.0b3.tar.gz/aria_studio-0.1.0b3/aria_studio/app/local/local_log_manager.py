# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import asyncio
import csv
import platform
import shutil
from dataclasses import dataclass
from datetime import datetime
from enum import auto, Enum, unique
from inspect import currentframe, getframeinfo, Traceback
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Final, List, Optional

from aria_studio.app.common.types import DeviceStatus
from aria_studio.app.device.device_manager import AriaException, DeviceManager
from aria_studio.app.local.app_info import get_app_version
from aria_studio.app.singleton_base import SingletonBase
from aria_studio.app.utils import CliAuthHelper, CliHttpHelper, login_required
from projectaria_tools.aria_mps_cli.cli_lib.types import MpsFeature


@unique
class LocalLogSurface(str, Enum):
    """
    The surface, where the event originated
    """

    def _generate_next_value_(name, start, count, last_values):  # noqa: B902
        return name.upper()

    FRONT_END = auto()
    BACK_END = auto()

    def __str__(self):
        return self.name


@unique
class LogLevel(str, Enum):
    """
    The importance of event to log
    """

    def _generate_next_value_(name, start, count, last_values):  # noqa: B902
        return name.upper()

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()

    def __str__(self):
        return self.name


@unique
class LocalLogEvent(str, Enum):
    """
    The event's type to log.

    WARNING:
    keep in sync with AriaStudioLogEvent in loggerTypes.js
    """

    def _generate_next_value_(name, start, count, last_values):  # noqa: B902
        return name.upper()

    APP_DOWNLOAD = auto()
    APP_INSTALL = auto()

    LOGIN = auto()
    SEE_DOCS = auto()

    SESSION = auto()
    CRASH = auto()

    NAVIGATE = auto()
    CONNECT_GLASSES = auto()
    IMPORT_RECORDING = auto()
    CREATE_GROUP = auto()

    MPS_REQUEST = auto()
    MPS_STATUS = auto()
    MPS_UPLOAD = auto()
    MPS_DOWNLOAD = auto()
    VISUALIZATION = auto()

    def __str__(self):
        return self.name


@unique
class LocalLogScreen(str, Enum):
    """
    The screen, where the event originated.


    WARNING:
    Keep in sync with AriaStudioRoutes in commonTypes.js
    """

    def _generate_next_value_(name, start, count, last_values):  # noqa: B902
        return name.upper()

    HOME = auto()

    LOGIN = auto()
    FORGOT_PASSWORD = auto()

    GLASSES = auto()
    FILES = auto()
    GROUPS = auto()
    SERVICES = auto()
    SETTINGS = auto()

    SIDEBAR = auto()
    HEADER = auto()
    CRASH = auto()

    def __str__(self):
        return self.name


@unique
class LocalLogDeviceConnectionState(str, Enum):
    """
    The device's connection state to user's local machine
    """

    def _generate_next_value_(name, start, count, last_values):  # noqa: B902
        return name.upper()

    CONNECTED = auto()
    DISCONNECTED = auto()

    def __str__(self):
        return self.name


@dataclass
class LocalLogEntry:
    """
    The log entry to be logged to the local log file.
    """

    timestamp: int
    surface: LocalLogSurface
    event: LocalLogEvent
    screen: LocalLogScreen
    message: str

    source: Optional[str] = None
    duration: float = 0.0
    file_size: int = 0

    navigate_from: Optional[LocalLogScreen] = None
    navigate_to: Optional[LocalLogScreen] = None

    device_serial: Optional[str] = None
    device_model: Optional[str] = None
    device_connection_state: Optional[LocalLogDeviceConnectionState] = None

    session_id: Optional[str] = None
    mps_features: Optional[List[MpsFeature]] = None
    is_forced: Optional[bool] = None

    is_logged: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """
        Gets the dictionary representation of the log entry.
        Used for sending data to the Meta's back-end,
        hence dict's keys must match expected by the endpoint.
        """

        data = dict(vars(self))
        data.pop(LocalLogManager.KEY_IS_LOGGED, None)
        return data

    def to_list(self) -> List[Any]:
        """
        Gets the list representation of the log entry.
        Used for writing data to the local log file.
        """

        data = list(vars(self).values())
        # MpsFeature doesn't have automatic conversion to string, so we need to convert it manually
        data[14] = [feature.value for feature in data[14]] if data[14] else None
        return data

    @classmethod
    def from_list(cls, row: List[str]) -> "LocalLogEntry":
        """
        Creates a new instance of the log entry from the list representation.
        """

        return LocalLogEntry(
            timestamp=int(row[0]),
            surface=LocalLogSurface(row[1]),
            event=LocalLogEvent(row[2]),
            screen=LocalLogScreen(row[3]),
            message=row[4],
            source=row[5],
            duration=float(row[6]) if row[6] else 0.0,
            file_size=int(row[7]),
            navigate_from=LocalLogScreen(row[8]) if row[8] else None,
            navigate_to=LocalLogScreen(row[9]) if row[9] else None,
            device_serial=row[10],
            device_model=row[11],
            device_connection_state=(
                LocalLogDeviceConnectionState(row[12]) if row[12] else None
            ),
            session_id=row[13],
            mps_features=(
                [MpsFeature(feature) for feature in row[14].split(",")]
                if row[14]
                else None
            ),
            is_forced=row[15] == LocalLogManager.ENTRY_TRUE,
            is_logged=row[16] == LocalLogManager.ENTRY_TRUE,
        )

    @classmethod
    def get_caller(cls) -> str:
        """
        Gets the caller's file name and line number.
        """

        frameinfo: Traceback = getframeinfo(currentframe().f_back)
        return f"{frameinfo.filename}:{frameinfo.lineno}"


class LocalLogManager(metaclass=SingletonBase):
    """
    The class to manage the local logging operations.
    """

    KEY_IS_LOGGED: Final[str] = "is_logged"
    ENTRY_TRUE: Final[str] = "True"
    __FILE_PATH: Final[Path] = Path("/tmp/logs/projectaria")
    __DOC_ID_SEND_LOGS: Final[int] = 26511009311880320
    __KEY_DATA: Final[str] = "data"

    __DATA_KEY_APP_VERSION: Final[str] = "app_version"
    __DATA_KEY_MACHINE_HOST_NAME: Final[str] = "machine_host_name"
    __DATA_KEY_CPU_ARCHITECTURE: Final[str] = "cpu_architecture"
    __DATA_KEY_HOST_OS_PRODUCT_TYPE: Final[str] = "host_os_product_type"
    __DATA_KEY_HOST_OS_PRODUCT_VERSION: Final[str] = "host_os_product_version"
    __DATA_KEY_PRETTY_HOST_OS_PRODUCT_NAME: Final[str] = "pretty_host_os_product_name"

    __DATA_ENTRY_OS_DARWIN: Final[str] = "Darwin"

    __filename: Path
    __device_manager: DeviceManager

    __is_sync_required: bool = False

    __session_id: Optional[str] = None
    __session_timestamp: int = 0

    def __init__(self):
        """
        Creates a new instance of the local log manager.
        Sets the log file name for duration of the session.

        WARNING:
        This class is a singleton. Each call to create a new instance will
        return the first created during given session. This method is thread-safe.
        """

        self.__filename = self.__FILE_PATH / datetime.now().strftime(
            "log_%Y%m%d_%H%M%S.log"
        )
        self.__device_manager: DeviceManager = DeviceManager.get_instance()

    @classmethod
    async def log(
        cls,
        event: LocalLogEvent,
        screen: LocalLogScreen,
        message: str,
    ) -> None:
        """
        Logs the back-end event to the local log file.

        Assumes:
        - timestamp is set to current time,
        - surface is set to BACK_END,
        - source is set to the caller's file name and line number.

        Args:
        - event: the event's type,
        - screen: the screen, where the event originated,
        - message: the message with detailed description of the event.
        """

        frameinfo: Traceback = getframeinfo(currentframe().f_back)
        entry: LocalLogEntry = LocalLogEntry(
            timestamp=int(datetime.now().timestamp()),
            surface=LocalLogSurface.BACK_END,
            event=event,
            screen=screen,
            source=f"{frameinfo.filename}:{frameinfo.lineno}",
            message=message,
        )

        await cls.log_event(entry)

    @classmethod
    async def log_event(cls, entry: LocalLogEntry) -> None:
        """
        Logs the front-end event to the local log file.

        Args:
        - entry: the entry to add for logged event.
        """

        instance = LocalLogManager()
        await instance.__log(entry)

    @classmethod
    async def sync(cls) -> None:
        """
        Synchronizes unpublished entries to Meta's back-end.
        """

        tempfile = NamedTemporaryFile(mode="w", delete=False)

        instance = LocalLogManager()
        with open(instance.__filename) as csvfile, tempfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(tempfile)
            for row in reader:
                try:
                    entry: LocalLogEntry = LocalLogEntry.from_list(row)
                    if not entry.is_logged:
                        await instance.__submit_entry(entry)
                        entry.is_logged = True
                        writer.writerow(entry.to_list())
                    else:
                        # entry was already logged, keep it as is
                        writer.writerow(row)
                except Exception:
                    instance.__is_sync_required = True
                    # submit failed, keep the entry in the local file
                    writer.writerow(row)

            shutil.move(tempfile.name, instance.__filename)

    async def __log(self, entry: LocalLogEntry) -> None:
        entry = await self.__get_device_info(entry)
        entry = self.__get_session_info(entry)

        try:
            if not CliAuthHelper.get().is_logged_in():
                # endpoint allows only logged in users
                raise Exception("User is not logged in")

            await self.__submit_entry(entry)
            entry.is_logged = True

            if self.__is_sync_required:
                self.__is_sync_required = False
                asyncio.create_task(self.sync())
        except Exception:
            self.__is_sync_required = True
            entry.is_logged = False

        with open(self.__filename, "a") as f:
            writer = csv.writer(f)
            writer.writerow(entry.to_list())

    async def __get_device_info(self, entry: LocalLogEntry) -> LocalLogEntry:
        """
        Adds device info to the log entry.
        """

        try:
            await self.__device_manager.check_device_connected()
            device_status: DeviceStatus = await self.__device_manager.get_status()

            entry.device_connection_state = LocalLogDeviceConnectionState.CONNECTED
            entry.device_serial = device_status.serial_number
            entry.device_model = device_status.model
        except AriaException:
            entry.device_connection_state = LocalLogDeviceConnectionState.DISCONNECTED
            entry.device_serial = None
            entry.device_model = None

        return entry

    def __get_session_info(self, entry: LocalLogEntry) -> LocalLogEntry:
        """
        Adds session info to the log entry.
        If entry is of type SESSION, then store the session_id and it's timestamp.
        """
        # store session id when it is created
        if entry.event == LocalLogEvent.SESSION:
            if entry.timestamp > self.__session_timestamp:
                self.__session_timestamp = entry.timestamp
                self.__session_id = entry.session_id
            # else - old value, ignore
        else:
            entry.session_id = self.__session_id

        return entry

    @login_required
    async def __submit_entry(self, entry: LocalLogEntry) -> None:
        """
        Fills in host information in log entry and submits it to the server.
        """

        data = entry.to_dict()

        data[self.__DATA_KEY_APP_VERSION] = await get_app_version()
        # eg. brzyski-mbp
        data[self.__DATA_KEY_MACHINE_HOST_NAME] = platform.node()
        # eg. x86_64-i386
        data[self.__DATA_KEY_CPU_ARCHITECTURE] = (
            f"{platform.machine()}-{platform.processor()}"
        )
        # eg. Darwin
        data[self.__DATA_KEY_HOST_OS_PRODUCT_TYPE] = platform.system()
        data[self.__DATA_KEY_HOST_OS_PRODUCT_VERSION] = (
            # eg. 14.6.1
            platform.mac_ver()[0]
            if data[self.__DATA_KEY_HOST_OS_PRODUCT_TYPE] == self.__DATA_ENTRY_OS_DARWIN
            # eg 23.6.0 for MacOS 14.6.1
            else platform.release()
        )
        # eg. macOS-14.6.1-x86_64-i386-64bit
        data[self.__DATA_KEY_PRETTY_HOST_OS_PRODUCT_NAME] = platform.platform()

        _ = await CliHttpHelper.get().query_graph(
            doc_id=self.__DOC_ID_SEND_LOGS,
            variables={self.__KEY_DATA: data},
        )

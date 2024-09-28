# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import logging
import os
import shutil
from datetime import datetime
from enum import auto, Enum, unique
from pathlib import Path
from typing import Final, Optional

from aria_studio.app.constants import CACHE_DIR
from aria_studio.app.local.app_info import get_app_version
from aria_studio.app.local.local_log_manager import (
    LocalLogEntry,
    LocalLogEvent,
    LocalLogManager,
    LocalLogScreen,
    LocalLogSurface,
    LogLevel,
)
from aria_studio.app.utils import CliHttpHelper, login_required

from fastapi import APIRouter, status
from pydantic import BaseModel, Field


_VERSION_FILE: Final[Path] = Path("VERSION")

_PREFIX_VERSION: Final[str] = "Version: "
_SUFFIX_DEVELOPMENT: Final[str] = "-development"
_DEFAULT_VERSION: Final[str] = "unknown"

_VERSION_QUERY_ID: Final[int] = 8637461982965576
_KEY_DATA: Final[str] = "data"
_KEY_APP_VERSION: Final[str] = "app_version"
_KEY_RESPONSE_QUERY_VERSION: Final[str] = "query_version"
_KEY_RESPONSE_TITLE: Final[str] = "title"
_KEY_RESPONSE_MESSAGE: Final[str] = "message"
_KEY_RESPONSE_MODE: Final[str] = "mode"
_KEY_RESPONSE_INSTRUCTION: Final[str] = "instruction"
_KEY_RESPONSE_LEARN_MORE: Final[str] = "learn_more_link"
_KEY_RESPONSE_READ_INSTRUCTION: Final[str] = "read_instruction_link"

logger = logging.getLogger(__name__)

router = APIRouter()


class AriaStudioVersion(BaseModel):
    """Response from the application endpoint for application's version request"""

    version: str = Field(..., description="The current version of the Aria Studio")


class CacheClearResponse(BaseModel):
    """Response from the cache clear endpoint"""

    message: str = Field(..., description="Cache clear message")


@router.get(
    "/version",
    status_code=status.HTTP_200_OK,
    response_model=AriaStudioVersion,
    summary="Gets the Aria Studio Version",
)
async def check_version() -> AriaStudioVersion:
    """
    Gets the Aria Studio Version
    """
    version = await get_app_version()
    return AriaStudioVersion(version=version)


@unique
class UpdateMode(str, Enum):
    """
    The importance of the update
    """

    def _generate_next_value_(name, start, count, last_values):  # noqa: B902
        return name.upper()

    BLOCK = auto()
    HIGH = auto()

    def __str__(self):
        return self.name

    @classmethod
    def from_name(cls, name: str) -> "UpdateMode":
        for mode in cls:
            if mode.name == name:
                return mode
        raise ValueError(f"Unknown update mode: {name}")


class AriaStudioVersionUpdateResponse(BaseModel):
    """Response for query, if Aria Studio's update is available"""

    title: Optional[str] = Field(
        None, description="The title of the update", nullable=True
    )
    message: Optional[str] = Field(
        None, description="Details of the update", nullable=True
    )
    mode: Optional[UpdateMode] = Field(
        None, description="Importance of the update", nullable=True
    )
    learn_more_link: Optional[str] = Field(
        None,
        description="The link with more information about the update",
        nullable=True,
    )
    read_instruction_link: Optional[str] = Field(
        None,
        description="The link with detailed update instructions for Aria Studio",
        nullable=True,
    )
    instruction: Optional[str] = Field(
        None, description="Installation instructions for the update", nullable=True
    )


@login_required
@router.get(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=AriaStudioVersionUpdateResponse,
    summary="Gets the information, if Aria Studio's update is available",
)
async def check_update() -> AriaStudioVersionUpdateResponse:
    """
    Gets the information, if Aria Studio's update is available
    """
    version = await get_app_version()
    response = await CliHttpHelper.get().query_graph(
        doc_id=_VERSION_QUERY_ID,
        variables={_KEY_DATA: {_KEY_APP_VERSION: version}},
    )

    if response[_KEY_DATA][_KEY_RESPONSE_QUERY_VERSION] is None:
        return AriaStudioVersionUpdateResponse()

    return AriaStudioVersionUpdateResponse(
        title=response[_KEY_DATA][_KEY_RESPONSE_QUERY_VERSION][_KEY_RESPONSE_TITLE],
        message=response[_KEY_DATA][_KEY_RESPONSE_QUERY_VERSION][_KEY_RESPONSE_MESSAGE],
        mode=UpdateMode.from_name(
            response[_KEY_DATA][_KEY_RESPONSE_QUERY_VERSION][_KEY_RESPONSE_MODE],
        ),
        learn_more_link=response[_KEY_DATA][_KEY_RESPONSE_QUERY_VERSION][
            _KEY_RESPONSE_LEARN_MORE
        ],
        read_instruction_link=response[_KEY_DATA][_KEY_RESPONSE_QUERY_VERSION][
            _KEY_RESPONSE_READ_INSTRUCTION
        ],
        instruction=response[_KEY_DATA][_KEY_RESPONSE_QUERY_VERSION][
            _KEY_RESPONSE_INSTRUCTION
        ],
    )


@router.get("/clear_cache", status_code=status.HTTP_200_OK, summary="Clears the cache")
async def clear_cache() -> None:
    """
    Clears the cache
    """
    try:
        logger.info("Clearing cache")
        if os.path.exists(CACHE_DIR):
            shutil.rmtree(CACHE_DIR)
            logger.info("Cache cleared")
        else:
            logger.info(f"Cache directory '{CACHE_DIR}' does not exist")
        return CacheClearResponse(message="Cache cleared")
    except PermissionError as e:
        logger.error(f"Error deleting cache directory: {e}")
        return CacheClearResponse(message=f"Error deleting cache directory: {e}")


class LogMessageRequest(BaseModel):
    """Logging request"""

    message: str = Field(..., description="A message to be logged")
    log_level: Optional[LogLevel] = Field(
        LogLevel.INFO, description="The log level to be used for logging"
    )


@router.post(
    "/log",
    status_code=status.HTTP_200_OK,
    summary="Puts provided message in persistent log",
)
def log_message(request: LogMessageRequest) -> None:
    """
    Puts provided message in persistent log.
    """
    if request.log_level == LogLevel.DEBUG:
        logger.debug(request.message)
    elif request.log_level == LogLevel.WARNING:
        logger.warning(request.message)
    elif request.log_level == LogLevel.ERROR:
        logger.error(request.message)
    else:
        logger.info(request.message)


class LogEventRequest(BaseModel):
    """The request to persistently log a specific event"""

    event: LocalLogEvent = Field(..., description="The event to be logged")
    screen: LocalLogScreen = Field(
        ..., description="The screen, where the event originated"
    )
    message: str = Field(..., description="A message to be logged")

    source: Optional[str] = Field(
        None, description="A place in code, where the event is logged"
    )
    duration: float = Field(
        0.0, description="The time between previous and current event of the same type"
    )

    navigate_from: Optional[LocalLogScreen] = Field(
        None, description="The screen, where user was before the event"
    )
    navigate_to: Optional[LocalLogScreen] = Field(
        None, description="The screen, where user is going to after serving the event"
    )

    session_id: Optional[str] = Field(
        None, description="The ID of the active session, if any"
    )


@router.post(
    "/log_event",
    status_code=status.HTTP_200_OK,
    summary="Puts provided message in persistent log",
)
async def log_event(request: LogEventRequest) -> None:
    """
    Puts provided message in persistent log.
    """
    await LocalLogManager.log_event(
        LocalLogEntry(
            timestamp=int(datetime.now().timestamp()),
            surface=LocalLogSurface.FRONT_END,
            event=request.event,
            screen=request.screen,
            message=request.message,
            source=request.source,
            duration=request.duration,
            navigate_from=request.navigate_from,
            navigate_to=request.navigate_to,
            session_id=request.session_id,
        )
    )

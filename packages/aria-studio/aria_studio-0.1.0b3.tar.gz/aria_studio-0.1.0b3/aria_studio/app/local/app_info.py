# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Final


_VERSION_FILE: Final[Path] = Path("VERSION")

_PREFIX_VERSION: Final[str] = "Version: "
_SUFFIX_DEVELOPMENT: Final[str] = "-development"
_DEFAULT_VERSION: Final[str] = "unknown"

logger = logging.getLogger(__name__)


async def get_app_version() -> str:
    """
    Gets the Aria Studio Version
    """

    version = _DEFAULT_VERSION
    if _VERSION_FILE.is_file():
        with open(_VERSION_FILE, "r") as fp:
            version = f"{fp.read().strip()}{_SUFFIX_DEVELOPMENT}"
            logger.info(f"Read version from file {version}")
    else:
        process = await asyncio.create_subprocess_exec(
            *["pip3", "show", "aria_studio"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logger.error(f'"pip3 show aria_studio" failed with {process.returncode}')
            logger.error(f"Read package version failed {stderr.decode()}")
        else:
            """
            Sample output of "pip3 show aria_studio" command:

            Name: aria_studio
            Version: 0.1.0b1
            Summary: Aria Studio
            Home-page:
            Author: Meta Reality Labs Research
            Author-email:
            License: Apache-2.0
            Location: /Users/brzyski/venv/aria_studio/lib/python3.11/site-packages
            Requires: aiofiles, aiohttp, aioredis, aiosqlite, annotated-types, anyio, async-timeout, attrs, certifi, charset-normalizer, click, dataclasses, dnspython, email-validator, exceptiongroup, fastapi, fastapi-cache, fastapi-cli, h11, hiredis, httpcore, httptools, httpx, idna, imageio, iniconfig, Jinja2, jsons, markdown-it-py, MarkupSafe, mdurl, numpy, orjson, packaging, pillow, pluggy, projectaria-tools, pyarrow, pycryptodome, pydantic, pydantic-core, Pygments, pytest, python-dotenv, python-multipart, PyYAML, requests, rerun-sdk, rich, shellingham, sniffio, soupsieve, starlette, textual, tomli, tqdm, transitions, typer, typing, typing-extensions, typish, ujson, urllib3, uvicorn, uvloop, vrs, watchfiles, websockets, xxhash
            Required-by:
            """

            output = stdout.decode()
            try:
                version = next(
                    x[len(_PREFIX_VERSION) :]
                    for x in output.splitlines()
                    if x.startswith(_PREFIX_VERSION)
                )
                logger.info(f"Read version from package {version}")
            except StopIteration:
                logger.error("Read package version failed")

    return version

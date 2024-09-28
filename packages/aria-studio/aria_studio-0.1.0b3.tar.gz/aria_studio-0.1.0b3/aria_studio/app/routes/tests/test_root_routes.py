# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

from pathlib import Path
from unittest.mock import patch

from aria_studio.app.routes.root_routes import router as app
from fastapi import status
from fastapi.testclient import TestClient


class MockFileResponse:
    def __init__(
        self, path, filename=None, media_type=None, headers=None, stat_result=None
    ):
        self.status_code = status.HTTP_200_OK

    async def __call__(self, scope, receive, send):
        pass


client = TestClient(app)


@patch("aria_studio.app.routes.root_routes.FileResponse", new=MockFileResponse)
def test_serve_react_app_exists(monkeypatch):
    monkeypatch.setattr(Path, "is_file", lambda self: True)
    client = TestClient(app)
    response = client.get("/some_path")
    assert response.status_code == status.HTTP_200_OK


def test_serve_react_app_fallback_to_index(monkeypatch):
    monkeypatch.setattr(Path, "is_file", lambda self: False)
    response = client.get("/nonexistentpath")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"].startswith("text/html")


def test_serve_react_app_api_path(monkeypatch):
    monkeypatch.setattr(Path, "is_file", lambda self: True)
    response = client.get("/api/some_path")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Not Found"}

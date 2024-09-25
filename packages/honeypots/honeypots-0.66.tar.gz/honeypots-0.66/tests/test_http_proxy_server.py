from __future__ import annotations

from pathlib import Path

import pytest
import requests

from honeypots import QHTTPProxyServer
from .utils import (
    assert_connect_is_logged,
    IP,
    load_logs_from_file,
    wait_for_server,
)

PORT = "58080"
PORT_2 = "58081"
SERVER_CONFIG = {
    "honeypots": {
        "httpproxy": {
            "options": ["capture_commands"],
        },
    }
}


@pytest.mark.parametrize(
    "server_logs",
    [{"server": QHTTPProxyServer, "port": PORT, "custom_config": SERVER_CONFIG}],
    indirect=True,
)
def test_http_proxy_server(server_logs):
    with wait_for_server(PORT):
        response = requests.get(
            "http://example.com/",
            proxies={"http": f"http://{IP}:{PORT}"},
            timeout=2,
        )

    logs = load_logs_from_file(server_logs)

    assert len(logs) == 2
    connect, query = logs
    assert_connect_is_logged(connect, PORT)

    assert query["data"] == "example.com"
    assert query["action"] == "query"

    assert response.ok
    assert "Example Website" in response.text, "dummy response is missing"


CUSTOM_TEMPLATE = Path(__file__).parent / "data" / "test_template.html"
CUSTOM_TEMPLATE_CONFIG = {
    "honeypots": {
        "httpproxy": {
            "template": str(CUSTOM_TEMPLATE.absolute()),
        },
    }
}


@pytest.mark.parametrize(
    "server_logs",
    [
        {
            "server": QHTTPProxyServer,
            "port": PORT_2,
            "custom_config": CUSTOM_TEMPLATE_CONFIG,
        }
    ],
    indirect=True,
)
def test_custom_template(server_logs):  # noqa: ARG001
    with wait_for_server(PORT_2):
        response = requests.get(
            "http://example.com/",
            proxies={"http": f"http://{IP}:{PORT_2}"},
            timeout=2,
        )

    assert response.ok
    assert "This is a template for testing!" in response.text, "custom template is missing"

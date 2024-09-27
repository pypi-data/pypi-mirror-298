"""
Unit tests for the splunk returner
"""

import json
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from salt.modules import config

from saltext.splunk.returners import splunk


@pytest.fixture
def configure_loader_modules():
    opts = {
        "splunk_http_forwarder": {
            "token": "TheToken",
            "indexer": "the.splunk.domain",
            "index": "TheIndex",
            "sourcetype": "TheSourceType",
        }
    }
    return {
        splunk: {"__opts__": opts, "__salt__": {"config.get": config.get}},
        config: {"__opts__": opts},
    }


def test_verify_ssl_defaults_to_true():
    payload = {"some": "payload"}
    requests_post = MagicMock()
    ts = 1234565789
    host = "TheHostName"
    data = {
        "time": str(ts),
        "index": "TheIndex",
        "sourcetype": "TheSourceType",
        "event": payload,
        "host": host,
    }
    with patch("saltext.splunk.returners.splunk.time.time", MagicMock(return_value=ts)), patch(
        "saltext.splunk.returners.splunk.socket.gethostname", MagicMock(return_value=host)
    ), patch("requests.post", requests_post):
        splunk.returner(payload.copy())
    assert json.loads(requests_post.call_args_list[0][1]["data"]) == data
    assert requests_post.call_args_list[0][1]["verify"]
    assert requests_post.call_args_list[0][1]["headers"] == {"Authorization": "Splunk TheToken"}
    assert (
        requests_post.call_args_list[0][0][0]
        == "https://the.splunk.domain:8088/services/collector/event"
    )


def test_verify_ssl():
    payload = {"some": "payload"}
    verify_ssl_values = [True, False, None]
    payload = {"some": "payload"}
    ts = 1234565789
    host = "TheHostName"
    data = {
        "time": str(ts),
        "index": "TheIndex",
        "sourcetype": "TheSourceType",
        "event": payload,
        "host": host,
    }
    for verify_ssl in verify_ssl_values:
        requests_post = MagicMock()
        with patch("saltext.splunk.returners.splunk.time.time", MagicMock(return_value=ts)), patch(
            "saltext.splunk.returners.splunk.socket.gethostname", MagicMock(return_value=host)
        ), patch("requests.post", requests_post), patch.dict(
            splunk.__opts__["splunk_http_forwarder"], verify_ssl=verify_ssl
        ):
            splunk.returner(payload.copy())
            assert json.loads(requests_post.call_args_list[0][1]["data"]) == data
            assert requests_post.call_args_list[0][1]["verify"] == verify_ssl
            assert requests_post.call_args_list[0][1]["headers"] == {
                "Authorization": "Splunk TheToken"
            }
            assert (
                requests_post.call_args_list[0][0][0]
                == "https://the.splunk.domain:8088/services/collector/event"
            )


def test_verify_event_returner():
    payload = [{"some": "payload"}, {"another": "event"}]
    ts = 1234565789
    host = "TheHostName"
    verify_ssl = True

    requests_post = MagicMock()
    with patch("saltext.splunk.returners.splunk.time.time", MagicMock(return_value=ts)), patch(
        "saltext.splunk.returners.splunk.socket.gethostname", MagicMock(return_value=host)
    ), patch("requests.post", requests_post), patch.dict(
        splunk.__opts__["splunk_http_forwarder"], verify_ssl=verify_ssl
    ):
        splunk.event_return(payload)
        for _ in range(len(payload)):
            assert json.loads(requests_post.call_args_list[0][1]["data"])["event"] in payload
            assert requests_post.call_args_list[0][1]["verify"] == verify_ssl
            assert requests_post.call_args_list[0][1]["headers"] == {
                "Authorization": "Splunk TheToken"
            }
            assert (
                requests_post.call_args_list[0][0][0]
                == "https://the.splunk.domain:8088/services/collector/event"
            )

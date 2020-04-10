# -*- coding: utf-8 -*-
"""Conftest: fixtures used by multiple tests."""
from unittest.mock import Mock

from pytest import fixture


@fixture
def get_res_with_values(monkeypatch):
    """Mock get_res_with_values."""
    mock_res = Mock()
    monkeypatch.setattr("dsdkexample.cli.get_res_with_values", mock_res)
    return mock_res

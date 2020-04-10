# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel

"""Tests."""
from contextlib import contextmanager
from unittest.mock import Mock

from dsdk import Service
from pandas import DataFrame

from dsdkexample.cli import Cohort


class _MockMssqlService(Service):
    @contextmanager
    def open_mssql(self):  # pylint: disable=no-self-use
        """I am a docstring."""
        yield Mock()


def test_cohort(get_res_with_values):
    """Test the Cohort Block."""
    get_res_with_values.return_value = [{"CSN": 123.0, "HAR": 42.0}]

    c = Cohort("")
    service = _MockMssqlService(pipeline=(c,))
    batch = service()
    print(batch.evidence["cohort"])
    assert batch.csns == [123]
    assert batch.hars == [42]
    assert batch.evidence["cohort"].equals(
        DataFrame(get_res_with_values.return_value)
    )

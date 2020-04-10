# -*- coding: utf-8 -*-
# pylint: disable=no-member,too-few-public-methods
"""Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will
  cause problems: the code will get executed twice:

  - When you run `python -mdsdkexample` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``dsdkexample.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``dsdkexample.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
from abc import ABC
from contextlib import contextmanager
from logging import INFO, basicConfig, getLogger
from sys import stdout
from typing import TYPE_CHECKING, Generator, Optional, cast

from configargparse import ArgParser as ArgumentParser
from dsdk import (
    ModelMixin,
    Service,
    Task,
)
from dsdk.utils import get_res_with_values
from dsdk.mongo import EvidenceMixin as MongoEvidenceMixin
from pandas import DataFrame

try:
    # Since not everyone will use sqlalchemy
    from sqlalchemy import create_engine
except ImportError:
    create_engine = None


if TYPE_CHECKING:
    BaseMixin = Service
else:
    BaseMixin = ABC

# Simple way to import sql queries a better approach would be to have these
# In .sql files and build utilities for loading them.

# from .sql import (
#     COHORT_QUERY,
#     DRG_QUERY,
#     NOTES_QUERY,
#     PAT_INFO_QUERY,
#     QUERIES_QUERY,
# )

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=stdout,
)
logger = getLogger(__name__)


class SQLiteMixin(BaseMixin):
    """SQLLiteMixin.

     This could be added to dsdk but for now put this here."""

    def __init__(self, *, sqlite_uri: Optional[str] = None, **kwargs):
        """__init__."""
        # inferred type of self._sqlite_uri must not be optional...
        self._sqlite_uri = cast(str, sqlite_uri)
        super().__init__(**kwargs)

        # ... because self._sqlite_uri is not optional
        assert self._sqlite_uri is not None
        self._sqlite = create_engine(self._sqlite_uri)

    def inject_arguments(self, parser: ArgumentParser) -> None:
        """Inject arguments."""
        super().inject_arguments(parser)

        def _inject_sqlite_uri(sqlite_uri: str) -> str:
            self._sqlite_uri = sqlite_uri
            return sqlite_uri

        parser.add(
            "--sqlite-uri",
            required=True,
            help=(
                "SQLITE URI used to connect to a SQLITE database: "
                "sqlite:///file_path"
            ),
            env_var="SQLITE_URI",
            type=_inject_sqlite_uri,
        )

    @contextmanager
    def open_sqlite(self) -> Generator:
        """Open sqlite."""
        with self._sqlite.connect() as con:
            yield con


class LoadData(Task):
    """Load iris dataset into sqllite.

    This step is for demonstration purposes only. In a real ETL pipeline this
    would not be here.
    """

    def __call__(self, batch, service):
        with service.open_sqlite() as sqlite:
            # TODO: Load fake data from iris dataset into sqlite
            pass
        logger.info(self.__class__.__name__)


class Cohort(Task):
    """Pull down the iris dataset for our 'cohort'."""

    def __call__(self, batch, service):
        with service.open_sqlite() as sqlite:
            cohort = DataFrame(
                data={'a': [1], 'b': [2]}
                # TODO replace data with 'real' loaded iris data
                # get_res_with_values(COHORT_QUERY, params, sqlite)
            )
        logger.info(self.__class__.__name__)
        service.store_evidence(batch, "cohort", cohort)


class Transform(Task):
    """Scale dataset to prepare it for predict."""

    def __call__(self, batch, service):
        logger.info(self.__class__.__name__)
        scaler = service.model['scaler']
        cohort = batch.evidence['cohort']
        # TODO: use scaler to scale data for predict
        # scaled = scaler.transform(cohort)

        scaled = cohort
        service.store_evidence(batch, "scaled", scaled)



class Predict(Task):
    """Run predictions."""

    def __call__(self, batch, service):
        logger.info(self.__class__.__name__)
        clf = service.model['knn']
        scaled = batch.evidence['scaled']
        # TODO: use clf to predict
        # predictions = clf.predict(scaled)

        predictions = scaled
        service.store_evidence(batch, "predictions", predictions)


class DSDKExample(MongoEvidenceMixin, SQLiteMixin, ModelMixin, Service):
    """Batch class for DSDKExample."""
    def __init__(self, parser):
        super().__init__(
            parser=parser,
            pipeline=[LoadData(), Cohort(), Transform(), Predict()]
        )


def main(args=None):  # pylint: disable=unused-argument
    """Main."""
    parser = ArgumentParser()
    service = DSDKExample(parser=parser)
    batch = service()
    logger.info("len(batch.evidence): %s", len(batch.evidence))
    logger.info("batch.evidence.keys(): %s", batch.evidence.keys())

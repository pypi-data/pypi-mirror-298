""" Dataset stores including utility methods. 

The end goal is to allow users to freely register their own benchmarks
for retrieval by their peers while also providing some basic benchmarks
for immediate testing.

Currently supported:
- OpenML AutoML regression
- OpenML AutoML classification
- OpenML CC18
- CatBoost (regression/classification for <50k instances)
- PMLB

Near future support:
- Ikonomovska regression datasets
- scikit-learn associated datasets

# TODO(nopdive): Review how seq_num (integrity) are done with measure outcomes.
"""

import pytz
import base64
from dataclasses import dataclass
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Type, Mapping
import random
from powerlift.db.actions import drop_tables, create_db, create_tables
from powerlift.measures import class_stats, data_stats, regression_stats
from sqlalchemy.exc import IntegrityError
from tqdm import tqdm
from itertools import chain
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import create_engine
import io
import os
from powerlift.db import schema as db
import numbers
from datetime import datetime
import pathlib
import numpy as np
import pandas as pd
import ast
import time
import traceback as tb
import json


MIMETYPE_DF = "application/vnd.interpretml/parquet-df"
MIMETYPE_SERIES = "application/vnd.interpretml/parquet-series"
MIMETYPE_JSON = "application/json"


class BytesParser:
    @classmethod
    def deserialize(cls, mimetype, bytes):
        import io
        import json
        import pandas as pd

        if not isinstance(bytes, io.BytesIO):
            bstream = io.BytesIO(bytes)
        else:
            bstream = bytes

        if mimetype == MIMETYPE_JSON:
            return json.load(bstream)
        elif mimetype == MIMETYPE_DF:
            return pd.read_parquet(bstream)
        elif mimetype == MIMETYPE_SERIES:
            return pd.read_parquet(bstream)["Target"]
        else:
            return None

    @classmethod
    def serialize(cls, obj):
        import io
        import json
        import pandas as pd
        from types import FunctionType
        import inspect

        bstream = io.BytesIO()
        mimetype = None
        if isinstance(obj, pd.Series):
            orig_close = bstream.close
            bstream.close = lambda: None
            try:
                obj.to_frame(name="Target").to_parquet(
                    bstream, compression="Brotli", index=False
                )
            finally:
                bstream.close = orig_close
            mimetype = MIMETYPE_SERIES
        elif isinstance(obj, pd.DataFrame):
            orig_close = bstream.close
            bstream.close = lambda: None
            try:
                obj.to_parquet(bstream, compression="Brotli", index=False)
            finally:
                bstream.close = orig_close
            mimetype = MIMETYPE_DF
        elif isinstance(obj, dict):
            bstream.write(json.dumps(obj).encode())
            mimetype = MIMETYPE_JSON
        else:
            return None, None

        return mimetype, bstream


class Store:
    """Store that represents persistent state for experiments.

    Apart from initialization, the user should not be using its methods normally.
    """

    def __init__(
        self,
        uri: str,
        force_recreate: bool = False,
        print_exceptions=False,
        max_attempts=3,
        wait_secs=30.0,
        wait_lengthing=1.1,
        **create_engine_kwargs,
    ):
        """Initializes.

        Args:
            uri (str): Database URI to connect store to.
            force_recreate (bool, optional): This will delete and create the database associated with the uri if set to true. Defaults to False.
        """

        # TODO: include support for Azure passwordless credentials:
        # https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/connect-python?tabs=cmd%2Cpasswordless

        if wait_lengthing < 1.0:
            raise Exception("wait_lengthing must be equal to or above 1.0")

        self._create_engine_kwargs = create_engine_kwargs
        attempts = 0
        while True:
            try:
                self._engine = create_db(uri, **create_engine_kwargs)
                if force_recreate:
                    drop_tables(self._engine)
                create_tables(self._engine)
                break
            except Exception as e:
                if print_exceptions:
                    try:
                        print(str(e))
                    except Exception:
                        pass
                attempts += 1
                if max_attempts is not None and max_attempts <= attempts:
                    raise
                sleep_time = (
                    wait_secs * (wait_lengthing**attempts) * random.uniform(0.5, 2.0)
                )
                time.sleep(sleep_time)

        self._conn = None
        self._session = None

        self._uri = uri

        self._print_exceptions = print_exceptions
        self._max_attempts = max_attempts
        self._wait_secs = wait_secs
        self._wait_lengthing = wait_lengthing

        self._in_context = False
        self._attempts = 0
        self._reset = False

    @property
    def uri(self):
        return self._uri

    def __del__(self):
        if self._session is not None:
            try:
                self._session.close()
            except:
                pass
            self._session = None
        if self._conn is not None:
            try:
                self._conn.close()
            except:
                pass
            self._conn = None
        if self._engine is not None:
            try:
                self._engine.dispose()
            except:
                pass
            self._engine = None

    def __enter__(self):
        if self._in_context:
            raise Exception("Already inside a database transaction.")

        if not self._reset and self._attempts == 0:
            raise Exception("Must reset before entering the Store context.")

        # on first re-attempt, do not sleep
        if 2 <= self._attempts:
            sleep_time = (
                self._wait_secs
                * (self._wait_lengthing**self._attempts)
                * random.uniform(0.5, 2.0)
            )
            if self._print_exceptions:
                try:
                    print(
                        f"Sleeping: {sleep_time} seconds on attempt {self._attempts}."
                    )
                except Exception:
                    pass

            time.sleep(sleep_time)

        self._in_context = True
        self._reset = False

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._in_context:
            raise Exception("Not in Store context.")
        self._in_context = False

        if exc_type is None:
            if self._session is not None:
                try:
                    # check if the user handled an error already
                    if self._session.is_active:
                        self._session.commit()
                    else:
                        self._session.rollback()
                except Exception as e:

                    if self._print_exceptions:
                        try:
                            print(str(e))
                        except Exception:
                            pass

                    try:
                        self._session.close()
                    except Exception as e:
                        if self._print_exceptions:
                            try:
                                print(str(e))
                            except Exception:
                                pass
                    self._session = None

                    if self._conn is not None:
                        try:
                            self._conn.close()
                        except Exception as e:
                            if self._print_exceptions:
                                try:
                                    print(str(e))
                                except Exception:
                                    pass
                        self._conn = None

                    if self._engine is not None:
                        try:
                            self._engine.dispose()
                        except Exception as e:
                            if self._print_exceptions:
                                try:
                                    print(str(e))
                                except Exception:
                                    pass
                        self._engine = None

                    self._attempts += 1
                    if (
                        self._max_attempts is not None
                        and self._max_attempts <= self._attempts
                    ):
                        raise

                    # swallow the exception and any exception inside the
                    # with block if we haven't reached max_attempts
                    return False

                try:
                    self._session.close()
                except Exception as e:
                    if self._print_exceptions:
                        try:
                            print(str(e))
                        except Exception:
                            pass
                self._session = None

            self._attempts = 0
            return False

        if self._print_exceptions:
            try:
                print("".join(tb.format_exception(exc_type, exc_value, traceback)))
            except Exception:
                pass

        if self._session is not None:
            try:
                self._session.close()
            except Exception as e:
                if self._print_exceptions:
                    try:
                        print(str(e))
                    except Exception:
                        pass
            self._session = None

        if self._conn is not None:
            try:
                self._conn.close()
            except Exception as e:
                if self._print_exceptions:
                    try:
                        print(str(e))
                    except Exception:
                        pass
            self._conn = None

        if self._engine is not None:
            try:
                self._engine.dispose()
            except Exception as e:
                if self._print_exceptions:
                    try:
                        print(str(e))
                    except Exception:
                        pass
            self._engine = None

        self._attempts += 1
        return self._max_attempts is None or self._attempts < self._max_attempts

    def reset(self):
        if self._in_context:
            raise Exception("Cannot reset while inside a Store context.")
        self._reset = True
        self._attempts = 0

    @property
    def do(self):
        if self._in_context:
            raise Exception("Must exit a Store context for do to be valid")
        return self._reset or self._attempts != 0

    @property
    def connection(self):
        if not self._in_context:
            raise Exception("Must be inside a Store context to get a connection.")

        if self._conn is None:
            if self._engine is None:
                self._engine = create_engine(self._uri, **self._create_engine_kwargs)

            self._conn = self._engine.connect()

        return self._conn

    @property
    def session(self):
        if not self._in_context:
            raise Exception("Must be inside a Store context to get a session.")

        if self._session is None:
            self._session = Session(bind=self.connection)

        return self._session

    def end_trial(self, trial_id, errmsg=None):
        sql_text = text(
            """
UPDATE trial
SET end_time = CURRENT_TIMESTAMP,
  errmsg = :errmsg,
  runner_id = -2
WHERE id = :trial_id
"""
        )

        params = {
            "errmsg": errmsg,
            "trial_id": trial_id,
        }

        self.reset()
        while self.do:
            with self:
                self.session.execute(sql_text, params)

    def from_db_task(self, task_orm):
        from powerlift.bench.experiment import Task

        return Task(
            self,
            task_orm.id,
            task_orm.name,
            task_orm.problem,
            task_orm.origin,
            task_orm.n_samples,
            task_orm.n_features,
            task_orm.n_classes,
            task_orm.max_unique_continuous,
            task_orm.max_categories,
            task_orm.total_categories,
            task_orm.percent_categorical,
            task_orm.percent_special_values,
            json.loads(task_orm.meta),
        )

    def from_db_wheel(self, wheel_orm):
        from powerlift.bench.experiment import Wheel

        return Wheel(
            wheel_orm.experiment_id,
            wheel_orm.name,
            wheel_orm.embedded,
        )

    def from_db_experiment(self, experiment_orm):
        from powerlift.bench.experiment import Experiment

        wheels = [self.from_db_wheel(wheel) for wheel in experiment_orm.wheels]
        trials = list(self.iter_experiment_trials(experiment_orm.id))
        return Experiment(
            experiment_orm.id,
            experiment_orm.name,
            experiment_orm.description,
            experiment_orm.shell_install,
            experiment_orm.pip_install,
            experiment_orm.script,
            experiment_orm.trial_fn,
            wheels,
            trials,
        )

    def from_db_trial(self, trial_orm):
        from powerlift.bench.experiment import Trial

        task = self.from_db_task(trial_orm.task)
        return Trial(
            trial_orm.id,
            self,
            task,
            trial_orm.method,
            trial_orm.replicate_num,
            json.loads(trial_orm.meta),
        )

    def find_experiment_by_id(self, _id: int):
        experiment_orm = (
            self.session.query(db.Experiment).filter_by(id=_id).one_or_none()
        )
        if experiment_orm is None:
            return None
        return self.from_db_experiment(experiment_orm)

    def find_task_by_id(self, _id: int):
        task_orm = self.session.query(db.Task).filter_by(id=_id).one_or_none()
        if task_orm is None:
            return None
        return self.from_db_task(task_orm)

    def get_trial_fn(self, experiment_id) -> str:
        sql_text = text(f"SELECT trial_fn FROM experiment WHERE id = :experiment_id")
        params = {"experiment_id": experiment_id}

        self.reset()
        while self.do:
            with self:
                trial_fn = self.session.execute(sql_text, params).scalar()
        return trial_fn

    def pick_trial(self, experiment_id, runner_id):
        from powerlift.bench.experiment import Task
        from powerlift.bench.experiment import Trial

        # trials are inserted in the order we want them processed
        # (biggest to smallest) so ordering by ascending "id"
        # orders the work in our desired processing order.
        #
        # It is possible for the DB to successfully commit the
        # transaction, but then subsequently have the network
        # communication fail, which puts us in a state where
        # the DB thinks this runner is assigned some work
        # but the runner does not know this. When retrying
        # we include our runner id, and select any trials that
        # the DB believes are already assigned to us, thus we eventually
        # re-aquire orphaned work provided the runners do not fail.
        #
        # The UPDATE is not atomic from the inner query, so we need to
        # re-check that the runner_id has not been updated in the update.
        # If there are no results it might mean that there is no work
        # or it could mean another runner stole our tentatively taken trial
        # so we need to recheck if all trials are taken to exit
        sql_assign = text(
            f"""
UPDATE trial
SET runner_id = :runner_id, start_time = CURRENT_TIMESTAMP
WHERE id = (
  SELECT id
  FROM trial
  WHERE experiment_id = :experiment_id
    AND (runner_id = :runner_id OR runner_id = -1)
  ORDER BY experiment_id, runner_id DESC, id
  LIMIT 1
) 
AND experiment_id = :experiment_id 
AND (runner_id = :runner_id OR runner_id = -1)
"""
        )

        # If runner_id was a match then the above would not fail to take it, so we
        # only have to worry about the scenario where an open trial was taken.
        sql_check = text(
            "SELECT EXISTS(SELECT 1 FROM trial WHERE experiment_id = :experiment_id AND runner_id = -1)"
        )
        params_check = {"experiment_id": experiment_id}

        sql_query = text(
            f"""
SELECT
  ta.id AS task_id,
  ta.name AS name,
  ta.problem AS problem,
  ta.origin AS origin,
  ta.n_samples AS n_samples,
  ta.n_features AS n_features,
  ta.n_classes AS n_classes,
  ta.max_unique_continuous AS max_unique_continuous,
  ta.max_categories AS max_categories,
  ta.total_categories AS total_categories,
  ta.percent_categorical AS percent_categorical,
  ta.percent_special_values AS percent_special_values,
  ta.meta AS task_meta,
  t.id AS trial_id,
  t.method AS method,
  t.replicate_num AS replicate_num,
  t.meta AS trial_meta
FROM
  trial t
JOIN
  task ta ON t.task_id = ta.id
WHERE
  t.experiment_id = :experiment_id AND t.runner_id = :runner_id
LIMIT 1
"""
        )

        params = {"experiment_id": experiment_id, "runner_id": runner_id}

        self.reset()
        while self.do:
            with self:
                while True:
                    result = self.session.execute(sql_assign, params)
                    if 0 < result.rowcount:
                        break
                    result = self.session.execute(sql_check, params_check)
                    if not result.scalar():
                        # work is all done
                        return None
                result = self.session.execute(sql_query, params).fetchone()

        task = Task(
            self,
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            result[6],
            result[7],
            result[8],
            result[9],
            result[10],
            result[11],
            json.loads(result[12]),
        )
        return Trial(
            result[13],
            self,
            task,
            result[14],
            result[15],
            json.loads(result[16]),
        )

    def get_experiment(self, name: str) -> Optional[int]:
        exp_orm = self.session.query(db.Experiment).filter_by(name=name).one_or_none()
        if exp_orm is None:
            return None
        else:
            return exp_orm.id

    def create_experiment(
        self,
        name: str,
        description: str,
        shell_install: str = None,
        pip_install: str = None,
        script: str = None,
        trial_fn: str = None,
        wheels=None,
    ) -> Tuple[int, bool]:
        """Create experiment keyed by name."""

        exp_orm = db.Experiment(
            name=name,
            description=description,
            shell_install=shell_install,
            pip_install=pip_install,
            script=script,
            trial_fn=trial_fn,
        )

        if wheels is not None:
            for wheel in wheels:
                exp_orm.wheels.append(wheel)

        self.reset()
        while self.do:
            with self:
                self.session.add(exp_orm)
                self.session.flush()
                experiment_id = exp_orm.id
        return experiment_id

    def create_trials(self, trial_params: List[Dict[str, Any]]):
        trial_orms = []
        for trial_param in trial_params:
            trial_orm = db.Trial(
                experiment_id=trial_param["experiment_id"],
                task_id=trial_param["task_id"],
                method=trial_param["method"],
                replicate_num=trial_param["replicate_num"],
                meta=json.dumps(trial_param["meta"]),
            )
            trial_orms.append(trial_orm)

        self.reset()
        while self.do:
            with self:
                self.session.bulk_save_objects(trial_orms)

    def create_trial(
        self,
        experiment_id: int,
        task_id: int,
        method: str,
        replicate_num: int,
        meta: dict,
    ):
        trial_orm = db.Trial(
            experiment_id=experiment_id,
            task_id=task_id,
            method=method,
            replicate_num=replicate_num,
            meta=json.dumps(meta),
        )
        self.session.add(trial_orm)
        self.session.flush()
        return trial_orm.id

    def iter_experiment_trials(self, experiment_id: int):
        trial_orms = self.session.query(db.Trial).filter_by(experiment_id=experiment_id)
        for trial_orm in trial_orms:
            trial = self.from_db_trial(trial_orm)
            yield trial

    def get_status(self, experiment_name: str):
        sql_text = text(
            f"""
SELECT
  t.id AS trial_id,
  ta.name AS task,
  t.method AS method,
  t.meta AS meta,
  t.replicate_num AS replicate_num,
  t.errmsg AS errmsg,
  t.create_time AS create_time,
  t.start_time AS start_time,
  t.end_time AS end_time,
  t.runner_id AS runner_id,
  ta.n_samples AS n_samples,
  ta.n_features AS n_features,
  ta.n_classes AS n_classes,
  ta.total_categories as total_categories
FROM
  experiment e
JOIN
  trial t on e.id = t.experiment_id
JOIN
  task ta ON t.task_id = ta.id
WHERE
  e.name = :experiment_name
"""
        )

        params = {"experiment_name": experiment_name}

        self.reset()
        while self.do:
            with self:
                result = self.session.execute(sql_text, params)
                records = result.all()
                columns = result.keys()
        df = pd.DataFrame.from_records(records, columns=columns)

        df["runner_id"] = df["runner_id"].astype(int)
        df["create_time"] = pd.to_datetime(df["create_time"])
        df["start_time"] = pd.to_datetime(df["start_time"])
        df["end_time"] = pd.to_datetime(df["end_time"])

        df["status"] = df.apply(
            lambda row: (
                db.StatusEnum.ERROR.name
                if row["errmsg"] is not None
                else (
                    db.StatusEnum.COMPLETE.name
                    if pd.notna(row["end_time"])
                    else (
                        db.StatusEnum.RUNNING.name
                        if pd.notna(row["start_time"])
                        else db.StatusEnum.READY.name
                    )
                )
            ),
            axis=1,
        )

        return df

    def get_results(self, experiment_name: str):
        sql_text = text(
            f"""
SELECT
  mo.id AS id,
  ta.name AS task,
  t.method AS method,
  t.meta AS meta,
  t.replicate_num AS replicate_num,
  mo.name AS name,
  mo.seq_num AS seq_num,
  mo.type AS type,
  mo.val AS val
FROM
  experiment e
JOIN
  trial t ON e.id = t.experiment_id
JOIN
  task ta ON t.task_id = ta.id
JOIN
  measure_outcome mo ON t.id = mo.trial_id
WHERE
  e.name = :experiment_name
"""
        )

        params = {"experiment_name": experiment_name}

        self.reset()
        while self.do:
            with self:
                result = self.session.execute(sql_text, params)
                records = result.all()
                columns = result.keys()
        df = pd.DataFrame.from_records(records, columns=columns)

        df["num_val"] = np.nan
        df["str_val"] = None
        df["json_val"] = None

        for index, row in df.iterrows():
            if row["type"] == db.TypeEnum.NUMBER.value:
                df.at[index, "num_val"] = float(row["val"])
            elif row["type"] == db.TypeEnum.STR.value:
                df.at[index, "str_val"] = row["val"]
            elif row["type"] == db.TypeEnum.JSON.value:
                df.at[index, "json_val"] = row["val"]
            else:
                raise Exception(f"Bad DB type {row['type']}")

        df = df.drop(columns=["val"])
        df["type"] = df["type"].apply(lambda x: db.TypeEnum(x).name)

        return df

    def get_assets(self, task_id: int):
        sql_text = text(f"SELECT x, y FROM task WHERE id = :task_id")

        params = {"task_id": task_id}

        self.reset()
        while self.do:
            with self:
                result = self.session.execute(sql_text, params).fetchone()
        return tuple(result)

    def iter_available_tasks(
        self, include_measures: bool = False
    ) -> Iterable[Mapping[str, object]]:
        # WARNING: obsolete
        task_orms = self.session.query(db.Task)
        for task_orm in task_orms:
            record = {
                "task_id": task_orm.id,
                "name": task_orm.name,
                "version": task_orm.version,
                "problem": task_orm.problem,
                "origin": task_orm.origin,
                "config": task_orm.config,
            }
            if include_measures:
                for measure_outcome in task_orm.measure_outcomes:
                    record.update(
                        {
                            "measure_name": measure_outcome.measure_description.name,
                            "seq_num": measure_outcome.seq_num,
                            "type": measure_outcome.measure_description.type.name,
                            "num_val": measure_outcome.num_val,
                            "str_val": measure_outcome.str_val,
                            "json_val": measure_outcome.json_val,
                        }
                    )
            yield record

    def get_tasks(self):
        from powerlift.bench.experiment import Task

        sql_text = text(
            f"""
SELECT
  ta.id as id,
  ta.name as name,
  ta.problem as problem,
  ta.origin as origin,
  ta.n_samples AS n_samples,
  ta.n_features AS n_features,
  ta.n_classes AS n_classes,
  ta.max_unique_continuous AS max_unique_continuous,
  ta.max_categories AS max_categories,
  ta.total_categories AS total_categories,
  ta.percent_categorical AS percent_categorical,
  ta.percent_special_values AS percent_special_values,
  ta.meta as meta
FROM
  task ta
"""
        )

        self.reset()
        while self.do:
            with self:
                results = self.session.execute(sql_text).all()
        return [
            Task(
                self,
                r[0],
                r[1],
                r[2],
                r[3],
                r[4],
                r[5],
                r[6],
                r[7],
                r[8],
                r[9],
                r[10],
                r[11],
                json.loads(r[12]),
            )
            for r in results
        ]

    def add_measure(
        self,
        trial_id: int,
        name,
        value,
        seq_num,
    ):
        if isinstance(value, str):
            type_ = db.TypeEnum.STR.value
        elif isinstance(value, dict):
            type_ = db.TypeEnum.JSON.value
            value = json.dumps(value)
        elif isinstance(value, numbers.Number):
            type_ = db.TypeEnum.NUMBER.value
            value = repr(float(value))
        else:
            raise RuntimeError(f"Value type {type(value)} is not supported for measure")

        sql_text = text(
            "INSERT INTO measure_outcome (name, type, seq_num, val, trial_id) VALUES (:name, :type, :seq_num, :val, :trial_id)"
        )

        params = {
            "name": name,
            "type": type_,
            "seq_num": seq_num,
            "val": value,
            "trial_id": trial_id,
        }

        self.reset()
        while self.do:
            with self:
                self.session.execute(sql_text, params)

    def create_task_with_data(self, data, exist_ok):
        if isinstance(data, SupervisedDataset):
            return self._create_task_with_supervised(data, exist_ok)
        elif isinstance(data, DataFrameDataset):
            return self._create_task_with_dataframe(data, exist_ok)
        else:  # pragma: no cover
            raise ValueError(f"Does not support {type(data)}")

    def _create_task_with_supervised(self, supervised, exist_ok):
        X_bstream, y_bstream, _ = SupervisedDataset.serialize(supervised)

        meta = supervised.meta.copy()

        name = meta["name"]
        del meta["name"]

        problem = meta["problem"]
        del meta["problem"]

        origin = meta["origin"]
        del meta["origin"]

        n_samples = meta["n_samples"]
        del meta["n_samples"]

        n_features = meta["n_features"]
        del meta["n_features"]

        n_classes = meta["n_classes"]
        del meta["n_classes"]

        max_unique_continuous = meta["max_unique_continuous"]
        del meta["max_unique_continuous"]

        max_categories = meta["max_categories"]
        del meta["max_categories"]

        total_categories = meta["total_categories"]
        del meta["total_categories"]

        percent_categorical = meta["percent_categorical"]
        del meta["percent_categorical"]

        percent_special_values = meta["percent_special_values"]
        del meta["percent_special_values"]

        task_orm = db.Task(
            name=name,
            problem=problem,
            origin=origin,
            n_samples=n_samples,
            n_features=n_features,
            n_classes=n_classes,
            max_unique_continuous=max_unique_continuous,
            max_categories=max_categories,
            total_categories=total_categories,
            percent_categorical=percent_categorical,
            percent_special_values=percent_special_values,
            meta=json.dumps(meta),
            x=X_bstream.getvalue(),
            y=y_bstream.getvalue(),
        )

        self.reset()
        while self.do:
            with self:
                try:
                    self.session.add(task_orm)
                    # we need to flush here to get the exception if it exists
                    self.session.flush()
                    ret = True
                except IntegrityError as e:
                    ret = False

        if ret is False and not exist_ok:
            raise DatasetAlreadyExistsError("Dataset already in store") from e

        return ret

    def _create_task_with_dataframe(self, data, version):
        # WARNING: obsolete
        inputs_bstream, outputs_bstream, _ = DataFrameDataset.serialize(data)

        meta = data.meta
        task_orm = db.Task(
            name=meta["name"],
            description=f"Dataset {meta['name']} for {meta['problem']}",
            version=version,
            problem=meta["problem"],
            origin=meta["origin"],
            config={
                "type": "data_dataframe",
            },
            x=inputs_bstream.getvalue(),
            y=outputs_bstream.getvalue(),
            meta=data.meta,
        )

        self.session.add(task_orm)
        self.session.flush()
        return task_orm.id


def retrieve_cache(
    cache_dir: Optional[str], names: List[str]
) -> Optional[List[io.BytesIO]]:
    if cache_dir is None:
        return None

    cache_dir = pathlib.Path(os.path.expanduser(cache_dir))
    cache_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for name in names:
        filepath = pathlib.Path(cache_dir, name)
        if filepath.exists():
            with open(filepath, "rb") as f:
                outputs.append(io.BytesIO(f.read()))
        else:
            return None
    return outputs


def update_cache(cache_dir, names: List[str], bytes_io: List[io.BytesIO]):
    cache_dir = pathlib.Path(os.path.expanduser(cache_dir))
    for name, a_bytes_io in zip(names, bytes_io):
        filepath = pathlib.Path(cache_dir, name)
        with open(filepath, "wb") as f:
            b = a_bytes_io.getvalue()
            f.write(b)


class Dataset:
    pass


@dataclass
class DataFrameDataset(Dataset):
    inputs: pd.DataFrame
    outputs: pd.DataFrame
    meta: dict

    @classmethod
    def serialize(cls, obj):
        _, inputs_bstream = BytesParser.serialize(obj.inputs)
        _, outputs_bstream = BytesParser.serialize(obj.outputs)
        _, meta_bstream = BytesParser.serialize(obj.meta)
        return inputs_bstream, outputs_bstream, meta_bstream

    @classmethod
    def deserialize(
        cls,
        inputs_bstream: io.BytesIO,
        outputs_bstream: io.BytesIO,
        meta_bstream: io.BytesIO,
    ):
        inputs = BytesParser.deserialize(MIMETYPE_DF, inputs_bstream)
        outputs = BytesParser.deserialize(MIMETYPE_DF, outputs_bstream)
        meta = BytesParser.deserialize(MIMETYPE_JSON, meta_bstream)
        return cls(inputs, outputs, meta)

    def asset_names(self):
        inputs_name = f"{self.meta['name']}.inputs.parquet"
        outputs_name = f"{self.meta['name']}.outputs.parquet"
        meta_name = f"{self.meta['name']}.meta.json"
        return inputs_name, outputs_name, meta_name

    def mimetypes(self):
        inputs_metadata = MIMETYPE_DF
        outputs_metadata = MIMETYPE_DF
        meta_metadata = MIMETYPE_JSON
        return inputs_metadata, outputs_metadata, meta_metadata

    def name(self):
        return self.meta["name"]


@dataclass
class SupervisedDataset(Dataset):
    X: pd.DataFrame
    y: pd.Series
    meta: dict

    @classmethod
    def serialize(cls, obj):
        _, X_bstream = BytesParser.serialize(obj.X)
        _, y_bstream = BytesParser.serialize(obj.y)
        _, meta_bstream = BytesParser.serialize(obj.meta)
        return X_bstream, y_bstream, meta_bstream

    @classmethod
    def deserialize(
        cls, X_bstream: io.BytesIO, y_bstream: io.BytesIO, meta_bstream: io.BytesIO
    ):
        X = BytesParser.deserialize(MIMETYPE_DF, X_bstream)
        y = BytesParser.deserialize(MIMETYPE_SERIES, y_bstream)
        meta = BytesParser.deserialize(MIMETYPE_JSON, meta_bstream)
        return cls(X, y, meta)

    def asset_names(self):
        X_name = f"{self.meta['name']}.X.parquet"
        y_name = f"{self.meta['name']}.y.parquet"
        meta_name = f"{self.meta['name']}.meta.json"
        return X_name, y_name, meta_name

    def mimetypes(self):
        X_metadata = MIMETYPE_DF
        y_metadata = MIMETYPE_SERIES
        meta_metadata = MIMETYPE_JSON
        return X_metadata, y_metadata, meta_metadata

    def name(self):
        return self.meta["name"]


class DatasetAlreadyExistsError(Exception):
    """Raised when dataset already exists in store."""

    pass


def populate_with_datasets(
    store: Store,
    dataset_iter: Iterable[Dataset] = None,
    cache_dir: str = None,
    exist_ok: bool = False,
) -> bool:
    """Populates store with datasets.

    Attempts to add datasets to store from iterable.
    This can be made idempotent by setting `exist_ok` to true.

    Args:
        store (Store): Store for experiment.
        dataset_iter (Iterable[Dataset], optional): Iterable of supervised datasets. Defaults to None, which populates with OpenML and PMLB.
        cache_dir (str, optional): If dataset_iter is None, use this cache directory across calls. Defaults to None.
        exist_ok (bool, optional): Do not raise exception if a dataset already exist.
    Returns:
        bool: True if datasets were created, False otherwise
    """

    if dataset_iter is None:
        dataset_iter = chain(
            retrieve_openml_cc18(cache_dir=cache_dir),
            retrieve_openml_automl_regression(cache_dir=cache_dir),
        )

    for dataset in dataset_iter:
        if not store.create_task_with_data(dataset, exist_ok):
            return False
    return True


def retrieve_openml(
    cache_dir: str = None, suite_id: int | str = 99, origin: str = "openml"
) -> Generator[SupervisedDataset, None, None]:
    """Retrives OpenML datasets.

    Args:
        cache_dir (str, optional): Use this cache directory across calls. Defaults to None.
        suite_id (int | str): OpenML suite_id
        origin (str): name for the dataset within powerlift

    Yields:
        Generator[SupervisedDataset]: Yields datasets.
    """
    import openml

    if cache_dir is not None:
        cache_dir = pathlib.Path(cache_dir, origin)

    dataset_names_filename = "dataset_names.json"
    dataset_names_stream = retrieve_cache(cache_dir, [dataset_names_filename])
    if dataset_names_stream is None:
        dataset_names = []
        suite = openml.study.get_suite(suite_id)
        tasks = suite.tasks.copy()
        random.Random(1337).shuffle(tasks)
        cat_type = pd.CategoricalDtype(ordered=False)
        for task_id in tqdm(tasks, desc=origin):
            task = openml.tasks.get_task(
                task_id,
                download_splits=False,
                download_data=False,
                download_qualities=False,
                download_features_meta_data=False,
            )
            dataset = openml.datasets.get_dataset(
                task.dataset_id,
                download_data=True,
                download_qualities=True,
                download_features_meta_data=True,
            )
            name = dataset.name
            dataset_names.append(name)

            X_name = f"{name}.X.parquet"
            y_name = f"{name}.y.parquet"
            meta_name = f"{name}.meta.json"

            X, y, categorical_mask, feature_names = dataset.get_data(
                target=task.target_name, dataset_format="dataframe"
            )

            if task.task_type_id == openml.tasks.TaskType.SUPERVISED_CLASSIFICATION:
                classes, y = np.unique(y.values, return_inverse=True)
                problem = "binary" if len(classes) == 2 else "multiclass"

                # for benchmarking we do not care about the original target strings
                y = pd.Series(y, dtype=np.int16)
            elif task.task_type_id == openml.tasks.TaskType.SUPERVISED_REGRESSION:
                problem = "regression"
                y = pd.Series(y, dtype=np.float64)
            else:
                raise Exception(f"Unrecognized task_type_id {task.task_type_id}.")

            for col_name, cat in zip(X.columns, categorical_mask):
                col = X[col_name]
                if cat:
                    X[col_name] = pd.Series(col, dtype=cat_type, name=col.name)
                else:
                    X[col_name] = pd.Series(col, dtype=np.float64, name=col.name)

            meta = {
                "name": name,
                "problem": problem,
                "origin": origin,
                "categorical_mask": categorical_mask,
                "feature_names": feature_names,
            }

            if problem == "regression":
                regression_stats(y, meta)
            elif problem in ["binary", "multiclass"]:
                class_stats(y, meta)
            data_stats(X, categorical_mask, meta)

            supervised = SupervisedDataset(X, y, meta)
            if cache_dir is not None:
                serialized = SupervisedDataset.serialize(supervised)
                update_cache(cache_dir, [X_name, y_name, meta_name], serialized)
            yield supervised

        if cache_dir is not None:
            _, dataset_names_stream = BytesParser.serialize(
                {"dataset_names": dataset_names}
            )
            update_cache(cache_dir, [dataset_names_filename], [dataset_names_stream])
    else:
        dataset_names_stream = dataset_names_stream[0]
        dataset_names = BytesParser.deserialize(MIMETYPE_JSON, dataset_names_stream)[
            "dataset_names"
        ]
        for name in tqdm(dataset_names, desc=origin):
            X_name = f"{name}.X.parquet"
            y_name = f"{name}.y.parquet"
            meta_name = f"{name}.meta.json"
            cached = retrieve_cache(cache_dir, [X_name, y_name, meta_name])
            supervised = SupervisedDataset.deserialize(*cached)
            yield supervised


def retrieve_openml_automl_regression(
    cache_dir: str = None,
) -> Generator[SupervisedDataset, None, None]:
    """Retrives OpenML AutoML regression datasets.

    Args:
        cache_dir (str, optional): Use this cache directory across calls. Defaults to None.

    Yields:
        Generator[SupervisedDataset]: Yields datasets.
    """

    return retrieve_openml(cache_dir, 269, "openml_automl_regression")


def retrieve_openml_automl_classification(
    cache_dir: str = None,
) -> Generator[SupervisedDataset, None, None]:
    """Retrives OpenML AutoML classification datasets.

    Args:
        cache_dir (str, optional): Use this cache directory across calls. Defaults to None.

    Yields:
        Generator[SupervisedDataset]: Yields datasets.
    """

    return retrieve_openml(cache_dir, 271, "openml_automl_classification")


def retrieve_openml_cc18(
    cache_dir: str = None,
) -> Generator[SupervisedDataset, None, None]:
    """Retrives OpenML CC18 datasets.

    Args:
        cache_dir (str, optional): Use this cache directory across calls. Defaults to None.

    Yields:
        Generator[SupervisedDataset]: Yields datasets.
    """

    return retrieve_openml(cache_dir, 99, "openml_cc18")


def retrieve_catboost_50k(
    cache_dir: str = None,
) -> Generator[SupervisedDataset, None, None]:
    """Retrieves catboost regression and classification datasets that have less than 50k training instances.

    Does not download adult dataset as currently there some download issues.

    Args:
        cache_dir (str, optional): Use this cache directory across calls. Defaults to None.

    Yields:
        Generator[SupervisedDataset]: Yields datasets.
    """
    from catboost.datasets import amazon, msrank_10k, titanic

    datasets = [
        # NOTE: CatBoost uses an internal dev link for first attempt, slowing the system to a halt - ignoring adult dataset.
        # {
        #     "name": "adult",
        #     "data_fn": adult,
        #     "problem": "classification",
        #     "target": "income",
        # },
        {
            "name": "amazon",
            "data_fn": amazon,
            "problem": "classification",
            "target": "ACTION",
        },
        {
            "name": "msrank_10k",
            "data_fn": msrank_10k,
            "problem": "regression",
            "target": 0,
        },
        {
            "name": "titanic",
            "data_fn": titanic,
            "problem": "classification",
            "target": "Survived",
        },
    ]

    if cache_dir is not None:
        cache_dir = pathlib.Path(cache_dir, "catboost_50k")

    cat_type = pd.CategoricalDtype(ordered=False)
    for dataset in tqdm(datasets, desc="catboost_50k"):
        name = dataset["name"]
        X_name = f"{name}.X.parquet"
        y_name = f"{name}.y.parquet"
        meta_name = f"{name}.meta.json"

        cached = retrieve_cache(cache_dir, [X_name, y_name, meta_name])
        if cached is None:
            df = dataset["data_fn"]()[0]
            target = dataset["target"]
            X = df.drop(target, axis=1)
            y = df[target]
            problem_type = dataset["problem"]

            if problem_type == "classification":
                classes, y = np.unique(y.values, return_inverse=True)
                problem = "binary" if len(classes) == 2 else "multiclass"

                # for benchmarking we do not care about the original target strings
                y = pd.Series(y, dtype=np.int16)
            elif problem_type == "regression":
                problem = "regression"
                y = pd.Series(y, dtype=np.float64)
            else:
                raise Exception(f"Unrecognized problem {problem_type}.")

            categorical_mask = [dt.kind == "O" for dt in X.dtypes]

            for col_name, cat in zip(X.columns, categorical_mask):
                col = X[col_name]
                if cat:
                    X[col_name] = pd.Series(col, dtype=cat_type, name=col.name)
                else:
                    X[col_name] = pd.Series(col, dtype=np.float64, name=col.name)

            meta = {
                "name": name,
                "problem": problem,
                "origin": "catboost_50k",
                "categorical_mask": categorical_mask,
                "feature_names": list(X.columns),
            }
            if problem == "regression":
                regression_stats(y, meta)
            elif problem in ["binary", "multiclass"]:
                class_stats(y, meta)
            data_stats(X, categorical_mask, meta)

            supervised = SupervisedDataset(X, y, meta)
            if cache_dir is not None:
                serialized = SupervisedDataset.serialize(supervised)
                update_cache(cache_dir, [X_name, y_name, meta_name], serialized)
        else:
            supervised = SupervisedDataset.deserialize(*cached)
        yield supervised


def retrieve_pmlb(cache_dir: str = None) -> Generator[SupervisedDataset, None, None]:
    """Retrieves PMLB regression and classification datasets.

    Args:
        cache_dir (str, optional): Use this cache directory across calls. Defaults to None.

    Yields:
        Generator[SupervisedDataset]: Yields datasets.
    """
    from pmlb import fetch_data, classification_dataset_names, regression_dataset_names

    if cache_dir is not None:
        cache_dir = pathlib.Path(cache_dir, "pmlb")

    dataset_names = []
    dataset_names.extend(
        [("classification", name) for name in classification_dataset_names]
    )
    dataset_names.extend([("regression", name) for name in regression_dataset_names])

    cat_type = pd.CategoricalDtype(ordered=False)
    for problem_type, dataset_name in tqdm(dataset_names, desc="pmlb"):
        name = dataset_name
        X_name = f"{name}.X.parquet"
        y_name = f"{name}.y.parquet"
        meta_name = f"{name}.meta.json"

        cached = retrieve_cache(cache_dir, [X_name, y_name, meta_name])
        if cached is None:
            df = fetch_data(dataset_name)
            X = df.drop("target", axis=1)
            y = df["target"]
            if problem_type == "classification":
                classes, y = np.unique(y.values, return_inverse=True)
                problem = "binary" if len(classes) == 2 else "multiclass"

                # for benchmarking we do not care about the original target strings
                y = pd.Series(y, dtype=np.int16)
            elif problem_type == "regression":
                problem = "regression"
                y = pd.Series(y, dtype=np.float64)
            else:
                raise Exception(f"Unrecognized problem_type {problem_type}.")

            categorical_mask = [dt.kind == "O" for dt in X.dtypes]

            for col_name, cat in zip(X.columns, categorical_mask):
                col = X[col_name]
                if cat:
                    X[col_name] = pd.Series(col, dtype=cat_type, name=col.name)
                else:
                    X[col_name] = pd.Series(col, dtype=np.float64, name=col.name)

            meta = {
                "name": name,
                "problem": problem,
                "origin": "pmlb",
                "categorical_mask": categorical_mask,
                "feature_names": list(X.columns),
            }
            if problem == "regression":
                regression_stats(y, meta)
            elif problem in ["binary", "multiclass"]:
                class_stats(y, meta)
            data_stats(X, categorical_mask, meta)

            supervised = SupervisedDataset(X, y, meta)
            if cache_dir is not None:
                serialized = SupervisedDataset.serialize(supervised)
                update_cache(cache_dir, [X_name, y_name, meta_name], serialized)
        else:
            supervised = SupervisedDataset.deserialize(*cached)
        yield supervised

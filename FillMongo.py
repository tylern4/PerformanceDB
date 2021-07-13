#!/usr/bin/env python3

from typing import Dict
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime, timedelta
from random import choice
import numpy as np
import logging
from random import getrandbits
import hashlib
from time import sleep

try:
    from tqdm import trange as range
except Exception:
    pass


class performanceMetrics:
    metrics: Dict = {}
    client: MongoClient = None
    collation: Collection = None

    def __init__(self,
                 collection: Collection = None,
                 client: MongoClient = None,
                 startData: Dict = None) -> None:
        """
        Performance Metrics

        Parameters
        ----------
        collection : Collection
            The collection to put performance data into.
        client : MongoClient
            Client to connect to mongodb, ignored of collection is present.
        startData : Dict
            Initial data to store
        """

        if collection is not None:
            self.collation = collection
        elif client is not None:
            self.client = client
            # Get default performance collection from client
            self.collation = self.client["performance"].get_collection("perf")
        else:
            raise

        if startData is not None:
            self.addDataDict(startData)

    def __del__(self):
        if self.metrics:
            self.insert()

    def insert(self):
        if self.collation is not None:
            try:
                self.collation.insert_one(self.metrics)
            except Exception as e:
                logging.error(f"Insert {e}")
        self.metrics = {}

    def addDataDict(self, data: Dict = None) -> bool:
        try:
            for key, value in data.items():
                self.metrics[key] = value
        except Exception as e:
            logging.error(f"addDataDict {e}")
            return False
        return True

    def addDataKeyVal(self, key: str = None, value=None) -> bool:
        try:
            self.metrics[key] = value
        except Exception as e:
            logging.error(e)
            return False
        return True

    def getMetricDict(self) -> Dict:
        return self.metrics

    @classmethod
    def createRandomData(cls) -> Dict:
        """
        For testing purposes only
        """
        # This can probbaly be found from WDL file and jaws at start
        output = {
            "_id": getrandbits(32),
            "submit_time": datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f"),
            "compute_platform": choice(['cori', 'jgi', 'aws', 'pnnl']),
            "requested_cpu": np.random.binomial(n=48, p=0.5),
            "requested_mem": np.random.binomial(n=10, p=0.75),
            "requested_disk": np.random.binomial(n=5, p=0.75),
            "input_file_size": np.random.binomial(n=5, p=0.25),
            "input_file_compression": choice([True, False]),
            "input_file_time": timedelta(minutes=np.random.binomial(n=240, p=0.5)).total_seconds(),
            "pipeline": f"pipeline_{choice([1,2,3,4])}",
        }

        # Needs to be updated at start of running later on
        output["start_time"] = (datetime.strptime(output["submit_time"], "%m-%d-%Y %H:%M:%S.%f") +
                                timedelta(minutes=np.random.binomial(n=240, p=0.5))).strftime("%m-%d-%Y %H:%M:%S.%f")

        # Needs to updated at the end
        output["output_file_size"] = timedelta(
            minutes=np.random.binomial(n=5, p=0.25)).total_seconds()
        output["output_file_compression"] = choice([True, False])
        output["output_file_time"] = timedelta(
            minutes=np.random.binomial(n=240, p=0.5)).total_seconds()
        output["end_time"] = (datetime.strptime(output['start_time'], "%m-%d-%Y %H:%M:%S.%f")
                              + timedelta(minutes=np.random.binomial(n=240, p=0.5))).strftime("%m-%d-%Y %H:%M:%S.%f")
        return output


# TODO:
#   Properly setup mongo with good username/password
#   Probably even better to have an api key?
client = MongoClient('127.0.0.1',
                     username="root",
                     password="rootpassword")
# TODO:
#   Do checks to make sure database is setup and collection is setup
try:
    collection = client['performance'].get_collection("perf")
except Exception as e:
    print(e)
    exit(1)


for num in range(200):
    perf = performanceMetrics(collection=collection)
    # TODO: Put data into the performance object
    perf.addDataDict(performanceMetrics.createRandomData())
    perf.addDataKeyVal("event", num)
    # Insert into mongodb
    perf.insert()

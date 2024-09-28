from typing import List
import unittest
from unittest.mock import MagicMock, Mock

import pandas as pd
from mantlebio.core.dataset.mantle_dataset import MantleDataset
from mantlebio.types.response.list_reponse import ListResponse
from mantlebio.types.response.response_item import ResponseItem
from proto import common_pb2, entity_pb2

class TestListResponse(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.storage_client = MagicMock()
        self.datasets= self.setupMantleDatasetList(5)
        self.items = [self.datasets[0], self.datasets[1], self.datasets[2]]
        self.list_response = ListResponse(self.items)

    def setupMantleDatasetList(self, num_datasets: int) -> List[MantleDataset]:
        datasets = []
        for i in range(num_datasets):
            proto_entity = entity_pb2.Entity(
                        unique_id=f"E00000{i}",
                        created_by=common_pb2.User(
                            name=f"test_user_{i}",
                        ),
                        updated_by=common_pb2.User(
                            name=f"test_user_{i}",
                        ),
                        props={
                            "test_string": entity_pb2.EntityDataValue(
                                string="test"
                            ),
                            "test_int": entity_pb2.EntityDataValue(
                                int=i
                            ),
                            "test_float": entity_pb2.EntityDataValue(
                                double=1.0*i
                            ),
                            "test_bool": entity_pb2.EntityDataValue(
                                boolean=True
                            ),
                            "test_object": entity_pb2.EntityDataValue(
                                object=entity_pb2.EntityDataValue.DataObject(values = {})
                            ),
                            "test_dataset": entity_pb2.EntityDataValue(
                                entity=entity_pb2.Entity(
                                    unique_id=f"123{i}"
                                )
                            )
                        }
                    )   
            dataset = MantleDataset(entity_pb2.Entity(),self.session, self.storage_client)
            datasets.append(dataset)
        
        return datasets

    def test_len(self):
        self.assertEqual(len(self.list_response), 3)

    def test_getitem(self):
        self.assertEqual(self.list_response[0], self.datasets[0])
        self.assertEqual(self.list_response[1], self.datasets[1])
        self.assertEqual(self.list_response[2], self.datasets[2])

    def test_iter(self):
        items = list(self.list_response)
        self.assertEqual(items, self.items)

    def test_append(self):
        item4 = self.datasets[3]
        self.list_response.append(item4)
        self.assertEqual(len(self.list_response), 4)
        self.assertEqual(self.list_response[3], item4)

    def test_extend(self):
        items = [self.datasets[3],self.datasets[4]]
        self.list_response.extend(items)
        self.assertEqual(len(self.list_response), 5)
        self.assertEqual(self.list_response[3], items[0])
        self.assertEqual(self.list_response[4], items[1])

    def test_to_dataframe(self):
        # Assuming ResponseItem has a `to_series` method that returns a pandas Series
        dataframe = self.list_response.to_dataframe()
        expected_dataframe = pd.DataFrame([item.to_series() for item in self.items])
        pd.testing.assert_frame_equal(dataframe, expected_dataframe, check_like=True)
        self.assertEqual(len(dataframe), 3)

    def test_get_item_type(self):
        item_type = self.list_response._get_item_type()
        self.assertEqual(item_type, MantleDataset)

if __name__ == "__main__":
    unittest.main()
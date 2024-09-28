import unittest
from unittest.mock import MagicMock
from mantlebio.core.dataset.client import DatasetClient
from mantlebio.core.dataset.mantle_dataset import MantleDataset
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleApiError
from mantlebio.types.response.list_reponse import ListResponse
from proto import entity_pb2


class TestDatasetClient(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=_ISession)
        self.storage_client = MagicMock(spec=_IStorageClient)
        self.client = DatasetClient(self.session, self.storage_client)

    def test_get(self):
        id = "test_id"
        dataset_resp = MagicMock()
        entity_pb2_obj = entity_pb2.Entity()
        self.session.make_request.return_value = dataset_resp
        dataset_resp.ok = True
        dataset_resp.content = entity_pb2_obj.SerializeToString()

        result = self.client.get(id)

        self.assertIsInstance(result, MantleDataset)
        self.assertEqual(result.to_proto(), entity_pb2_obj)

    def test_get_error(self):
        id = "test_id"
        dataset_resp = MagicMock()
        self.session.make_request.return_value = dataset_resp
        dataset_resp.ok = False
        dataset_resp.raise_for_status.side_effect = MantleApiError

        with self.assertRaises(MantleApiError):
            self.client.get(id)

    def test_create_cloud_dataset_error(self):
        dataset_type = "test_dataset_type"
        properties = {"prop1": {"string": "value1"},
                      "prop2": {"string": "value2"}}
        origin = entity_pb2.Origin()

        dataset_resp = MagicMock()
        dataset_resp.ok = False
        dataset_resp.raise_for_status.side_effect = MantleApiError
        self.session.make_request.return_value = dataset_resp

        with self.assertRaises(MantleApiError):
            self.client._create_cloud_dataset(dataset_type, properties, origin)

    def test_create_local_dataset_no_properties(self):
        dataset_type = "test_dataset_type"

        result = self.client._create_local_dataset(dataset_type=dataset_type)

        self.assertIsInstance(result, MantleDataset)
        self.assertEqual(result.to_proto().data_type.unique_id, dataset_type)

    def test_create(self):
        dataset_type = "test_dataset_type"
        properties = {"prop1": {"string": "value1"},
                      "prop2": {"string": "value2"}}
        local = True
        origin = entity_pb2.Origin()

        result = self.client.create(
            dataset_type=dataset_type, properties=properties, local=local, origin=origin)

        self.assertIsInstance(result, MantleDataset)
        self.assertEqual(result.to_proto().data_type.unique_id, dataset_type)

    def test_list(self):
        query_params = {"param1": "value1", "param2": "value2"}
        dataset_list_resp = MagicMock()
        dataset_list_pb2 = entity_pb2.EntitiesResponse()
        self.session.make_request.return_value = dataset_list_resp
        dataset_list_resp.ok = True
        dataset_list_resp.content = dataset_list_pb2.SerializeToString()
        result = self.client.list(query_params)
        self.assertIsInstance(result, ListResponse)
        self.assertEqual(len(list(result)), len(dataset_list_pb2.entities))

    def test_list_error(self):
        query_params = {"param1": "value1", "param2": "value2"}
        dataset_list_resp = MagicMock()
        self.session.make_request.return_value = dataset_list_resp
        dataset_list_resp.ok = False
        dataset_list_resp.raise_for_status.side_effect = MantleApiError
        with self.assertRaises(MantleApiError):
            self.client.list(query_params)


if __name__ == '__main__':
    unittest.main()

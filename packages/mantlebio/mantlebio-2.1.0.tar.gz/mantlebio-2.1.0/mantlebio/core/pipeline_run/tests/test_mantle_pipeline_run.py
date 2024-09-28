import unittest
from unittest.mock import patch, MagicMock
from mantlebio.core.dataset.client import _IDatasetClient
from mantlebio.core.dataset.mantle_dataset import _IDataset, MantleDataset
from mantlebio.core.pipeline_run import mantle_pipeline_run
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleResourceNotFoundError
from proto import entity_pb2, pipeline_pb2, pipeline_run_pb2

class TestMantlePipelineRun(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(_ISession)
        self.storage_client = MagicMock(_IStorageClient)
        self.dataset_client = MagicMock(_IDatasetClient)
        self.pipeline_run = mantle_pipeline_run.MantlePipelineRun(
            pipeline_run_pb2.PipelineRun(unique_id="P0000001"), self.session, self.storage_client, self.dataset_client
        )

    def test_add_input(self):
        key = "input_key"
        value = "input_value"
        self.session.make_request.return_value.ok = True

        test_prv = pipeline_pb2.PipelineRunValue(string=value)
        test_inputs = pipeline_run_pb2.PipelineInputs(data={key: test_prv})

        test_pipeline_run_add_input_response = pipeline_run_pb2.PipelineRun(id="test_id", inputs=test_inputs, outputs={})
        self.session.make_request.return_value.content = test_pipeline_run_add_input_response.SerializeToString()

        self.pipeline_run.add_input(key, value)

        self.session.make_request.assert_called_once_with(
            "POST", f"/pipeline_run/{self.pipeline_run.unique_id}/input/{key}", data=test_prv
        )
        self.storage_client.download.assert_not_called()

    def test_add_input_dataset(self):
        key = "input_key"
        self.session.make_request.return_value.ok = True

        test_dataset = MantleDataset(dataset_input=entity_pb2.Entity(unique_id="test_id"),session=self.session,storage_client=self.storage_client)
        test_prv = pipeline_pb2.PipelineRunValue(entity=test_dataset.to_proto())

        test_inputs = pipeline_run_pb2.PipelineInputs(data={key: test_prv})

        test_pipeline_run_add_input_response = pipeline_run_pb2.PipelineRun(id="test_id", inputs=test_inputs, outputs={})
        self.session.make_request.return_value.content = test_pipeline_run_add_input_response.SerializeToString()

        self.pipeline_run.add_input(key, test_dataset)

        self.session.make_request.assert_called_once_with(
            "POST", f"/pipeline_run/{self.pipeline_run.unique_id}/input/{key}", data=test_prv
        )
        self.storage_client.download.assert_not_called()

    def test_add_output(self):
        key = "output_key"
        value = "output_value"
        self.session.make_request.return_value.ok = True

        test_prv = pipeline_pb2.PipelineRunValue(string=value)
        test_outputs = pipeline_run_pb2.PipelineOutputs(data={key: test_prv})

        test_pipeline_run_add_input_response = pipeline_run_pb2.PipelineRun(id="test_id", inputs={}, outputs=test_outputs)
        self.session.make_request.return_value.content = test_pipeline_run_add_input_response.SerializeToString()

        self.pipeline_run.add_output(key, value)

        self.session.make_request.assert_called_once_with(
            "POST", f"/pipeline_run/{self.pipeline_run.unique_id}/output/{key}", data=test_prv
        )
        self.storage_client.download.assert_not_called()

    def test_add_output_dataset(self):
        key = "input_key"
        self.session.make_request.return_value.ok = True

        test_dataset = MantleDataset(dataset_input=entity_pb2.Entity(unique_id="test_id"),session=self.session,storage_client=self.storage_client)
        test_prv = pipeline_pb2.PipelineRunValue(entity=test_dataset.to_proto())

        test_inputs = pipeline_run_pb2.PipelineInputs(data={key: test_prv})

        test_pipeline_run_add_input_response = pipeline_run_pb2.PipelineRun(id="test_id", inputs=test_inputs, outputs={})
        self.session.make_request.return_value.content = test_pipeline_run_add_input_response.SerializeToString()

        self.pipeline_run.add_output(key, test_dataset)

        self.session.make_request.assert_called_once_with(
            "POST", f"/pipeline_run/{self.pipeline_run.unique_id}/output/{key}", data=test_prv
        )
        self.storage_client.download.assert_not_called()  

    def test_update_status(self):
        status = "RUNNING"
        self.session.make_request.return_value.ok = True

        test_pipeline_run_update_status_response = pipeline_run_pb2.PipelineRun(id="test_id", status=status)
        self.session.make_request.return_value.content = test_pipeline_run_update_status_response.SerializeToString()
        test_update_status_request = pipeline_run_pb2.PipelineStatusUpdateRequest(status=status)

        self.pipeline_run.update_status(status)

        self.session.make_request.assert_called_once_with(
            "PATCH", f"/pipeline_run/{self.pipeline_run.unique_id}/status", data=test_update_status_request
        )
        self.storage_client.download.assert_not_called()

    def test_get_input(self):
        key = "input_key"
        expected_value = "input_value"
        test_prv = pipeline_pb2.PipelineRunValue(string=expected_value)
        test_inputs = pipeline_run_pb2.PipelineInputs(data={key: test_prv})
        self.pipeline_run._pipeline_run_instance = pipeline_run_pb2.PipelineRun(inputs=test_inputs)

        value = self.pipeline_run.get_input(key)

        self.assertEqual(value, test_prv)
        self.storage_client.download.assert_not_called()

    def test_get_input_dataset(self):
        key = "input_key"
        dataset_id = "dataset_id"
        test_dataset = MantleDataset(dataset_input=entity_pb2.Entity(unique_id="test_id"),session=self.session,storage_client=self.storage_client)
        test_prv = pipeline_pb2.PipelineRunValue(entity=test_dataset.to_proto())
        self.pipeline_run._pipeline_run_instance = pipeline_run_pb2.PipelineRun(inputs=pipeline_run_pb2.PipelineInputs(data={key: test_prv}))

        dataset = self.pipeline_run.get_input(key)

        self.assertEqual(dataset.to_proto(), test_dataset.to_proto())
        self.storage_client.download.assert_not_called()

    def test_get_output(self):
        key = "output_key"
        expected_value = "output_value"
        test_prv = pipeline_pb2.PipelineRunValue(string=expected_value)
        test_outputs = pipeline_run_pb2.PipelineOutputs(data={key: test_prv})
        self.pipeline_run._pipeline_run_instance = pipeline_run_pb2.PipelineRun(outputs=test_outputs)

        value = self.pipeline_run.get_output(key)

        self.assertEqual(value, test_prv)
        self.storage_client.download.assert_not_called()

    def test_get_output_dataset(self):
        key = "output_key"
        test_dataset = MantleDataset(dataset_input=entity_pb2.Entity(unique_id="test_id"),session=self.session,storage_client=self.storage_client)
        test_prv = pipeline_pb2.PipelineRunValue(entity=test_dataset.to_proto())
        self.pipeline_run._pipeline_run_instance = pipeline_run_pb2.PipelineRun(outputs=pipeline_run_pb2.PipelineOutputs(data={key: test_prv}))

        dataset = self.pipeline_run.get_output(key)

        self.assertEqual(dataset.to_proto(), test_dataset.to_proto())
        self.storage_client.download.assert_not_called()

    def test_get_input_dataset_list(self):
        key = "input_key"
        dataset_id = "dataset_id"
        dataset = MagicMock()
        self.pipeline_run._pipeline_run_instance.inputs.data[key].entity.unique_id = dataset_id
        self.dataset_client.get.return_value = dataset

        datasets = self.pipeline_run.get_input_dataset_list(key)

        self.assertEqual(datasets, [dataset])
        self.dataset_client.get.assert_called_once_with(id=dataset_id)
        self.storage_client.download.assert_not_called()

    def test_get_output_dataset_list(self):
        key = "output_key"
        dataset_id = "dataset_id"
        dataset = MagicMock()
        self.pipeline_run._pipeline_run_instance.outputs.data[key].entity.unique_id = dataset_id
        self.dataset_client.get.return_value = dataset

        datasets = self.pipeline_run.get_output_dataset_list(key)

        self.assertEqual(datasets, [dataset])
        self.dataset_client.get.assert_called_once_with(id=dataset_id)
        self.storage_client.download.assert_not_called()

if __name__ == '__main__':
    unittest.main()
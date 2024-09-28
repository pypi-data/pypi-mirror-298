import unittest
from unittest.mock import MagicMock
from typing import Dict, Any, Optional
from mantlebio.core.pipeline_run.client import PipelineRunClient
from mantlebio.core.pipeline_run.mantle_pipeline_run import MantlePipelineRun
from mantlebio.core.dataset.client import _IDatasetClient
from mantlebio.core.session.mantle_session import _ISession
from mantlebio.core.storage.client import _IStorageClient
from mantlebio.exceptions import MantleConfigurationError
from proto import pipeline_run_pb2, data_type_pb2

class TestPipelineRunClient(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=_ISession)
        self.storage_client = MagicMock(spec=_IStorageClient)
        self.entity_client = MagicMock(spec=_IDatasetClient)
        self.client = PipelineRunClient(self.session, self.storage_client, self.entity_client)

    def test_kickoff_run_without_input(self):
        pipeline_id = "test_pipeline_id"
        version = "test_version"
        input = None
        external = False

        pipeline_run_resp = MagicMock()
        pipeline_run_obj_pb2 = pipeline_run_pb2.PipelineRun()
        self.session.make_request.return_value = pipeline_run_resp
        pipeline_run_resp.content = pipeline_run_obj_pb2.SerializeToString()

        result = self.client.kickoff(pipeline_id, version, input, external)

        self.assertEqual(result._pipeline_run_instance ,pipeline_run_obj_pb2)

    def test_kickoff_run_with_input(self):
        pipeline_id = "test_pipeline_id"
        version = "test_version"
        input = {"input1": "value1", "input2": "value2"}
        external = False

        pipeline_run_resp = MagicMock()
        pipeline_run_obj_pb2 = pipeline_run_pb2.PipelineRun()
        self.session.make_request.return_value = pipeline_run_resp
        pipeline_run_resp.content = pipeline_run_obj_pb2.SerializeToString()


        result = self.client.kickoff(pipeline_id, version, input, external)

        self.assertEqual(result._pipeline_run_instance, pipeline_run_obj_pb2)

    def test_kickoff_run_without_pipeline_id_and_version(self):
        pipeline_id = ""
        version = "test_version"
        input = {"input1": "value1", "input2": "value2"}
        external = False

        with self.assertRaises(MantleConfigurationError):
            self.client.kickoff(pipeline_id, version, input, external)

    def test_get(self):
        pipeline_id = "test_pipeline_id"

        pipeline_run_resp = MagicMock()
        pipeline_run_obj_pb2 = pipeline_run_pb2.PipelineRun()
        self.session.make_request.return_value = pipeline_run_resp
        pipeline_run_resp.content = pipeline_run_obj_pb2.SerializeToString()

        result = self.client.get(pipeline_id)

        self.assertEqual(result._pipeline_run_instance, pipeline_run_obj_pb2)

if __name__ == '__main__':
    unittest.main()
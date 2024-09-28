import os
import unittest
from mantlebio.core.pipeline_run.helpers import MantlePipelineRunKickoff, validate_pipeline_run_value
from mantlebio.exceptions import MantleTypeError
from proto import data_type_pb2, entity_pb2, pipeline_pb2

class TestMantlePipelineRunKickoff(unittest.TestCase):

    def test_init(self):
        pipeline_id = "test_pipeline"
        pipeline_version = "1.0"
        external = True
        inputs = {"input1": "value1", "input2": "value2"}

        kickoff = MantlePipelineRunKickoff(pipeline_id, pipeline_version, external, inputs)

        self.assertEqual(kickoff.pipeline_id, pipeline_id)
        self.assertEqual(kickoff.pipeline_version, pipeline_version)
        self.assertEqual(kickoff.external, external)
        self.assertEqual(kickoff.inputs, inputs)

    def test_init_with_default_inputs(self):
        pipeline_id = "test_pipeline"
        pipeline_version = "1.0"
        external = True

        kickoff = MantlePipelineRunKickoff(pipeline_id, pipeline_version, external)

        self.assertEqual(kickoff.pipeline_id, pipeline_id)
        self.assertEqual(kickoff.pipeline_version, pipeline_version)
        self.assertEqual(kickoff.external, external)
        self.assertEqual(kickoff.inputs, {})

class TestValidatePipelineRunValue(unittest.TestCase):
    def setUp(self):
        os.mkdir(f"{os.getcwd()}/test_folder")
        with open(f"{os.getcwd()}/test_folder/test_upload.txt", "w") as f:
            f.write("test content")
    
    def tearDown(self):
        os.remove(f"{os.getcwd()}/test_folder/test_upload.txt")
        os.rmdir(f"{os.getcwd()}/test_folder")


    def test_validate_pipeline_run_value_with_entity(self):
        value = entity_pb2.Entity()
        result = validate_pipeline_run_value(value)
        self.assertEqual(result, {"entity": value})

    def test_validate_pipeline_run_value_with_entity_list(self):
        value = entity_pb2.EntityList()
        result = validate_pipeline_run_value(value)
        self.assertEqual(result, {"entities": value})

    def test_validate_pipeline_run_value_with_s3_file(self):
        value = data_type_pb2.S3File()
        result = validate_pipeline_run_value(value)
        self.assertEqual(result, {"s3_file": value})

    def test_validate_pipeline_run_value_with_file_upload(self):
        value = data_type_pb2.FileUpload(
            filename="test_folder",
        )

        expected_value = data_type_pb2.FileUpload(
            filename="test_folder/",
        )
        result = validate_pipeline_run_value(value)
        self.assertEqual(result, {"file_upload": expected_value})

    def test_validate_pipeline_run_value_with_bool(self):
        value = True
        result = validate_pipeline_run_value(value)
        self.assertEqual(result, {"boolean": value})

    def test_validate_pipeline_run_value_with_string(self):
        value = "test_string"
        result = validate_pipeline_run_value(value)
        self.assertEqual(result, {"string": value})

    def test_validate_pipeline_run_value_with_invalid_type(self):
        value = {"key": "value"}
        with self.assertRaises(MantleTypeError):
            validate_pipeline_run_value(value)

if __name__ == '__main__':
    unittest.main()

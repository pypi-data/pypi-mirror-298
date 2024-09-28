from mantlebio.core.analysis.client import AnalysisClient
from mantlebio.core.dataset.client import DatasetClient
from mantlebio.core.pipeline.client import PipelineClient
from mantlebio.core.pipeline_run.client import PipelineRunClient
from mantlebio.core.session.mantle_session import MantleSession
from mantlebio.core.auth.creds import AuthMethod
from mantlebio.core.storage.client import StorageClient
from typing import Optional, Dict


class MantleClient:
    """
      Client to interact with MantleBio.
    """

    def __init__(self, tenant_id: Optional[str] = None, env: str = "PROD", credentials: Optional[AuthMethod] = None):
        """
        Initalize MantleClient class object.
        Args:
            tenant_id (optional, str): Tenant ID
            env (optional, str): Environment
        """

        self.session = MantleSession()
        self.session.authenticate(tenant_id, env, creds=credentials)
        self._storage = StorageClient(self.session)
        self._dataset = DatasetClient(self.session, self._storage)
        self._analysis = AnalysisClient(
            self.session, self._storage,  self._dataset)
        self._pipeline_run = PipelineRunClient(
            self.session, self._storage, self._dataset)
        self._pipeline = PipelineClient(self.session)

        pass

    @property
    def dataset(self) -> DatasetClient:
        """
        A property that provides access to the dataset object.

        Returns:
            object: The dataset object associated with the instance, typically providing 
            access to dataset-related functionalities or data.

        Note:
            This property encapsulates the internal _dataset attribute, ensuring controlled
            access and potential for additional logic in future updates.
        """
        return self._dataset

    @property
    def analysis(self) -> AnalysisClient:
        """
        A property that provides access to the analysis object.

        Returns:
            object: The analysis object used for performing or managing various analysis tasks.

        Note:
            This property encapsulates the internal _analysis attribute, ensuring controlled
            access and potential for additional logic in future updates.
        """
        return self._analysis

    @property
    def pipeline(self) -> PipelineClient:
        """
        A property that provides access to the pipeline object.

        Returns:
            object: The pipeline object associated with the instance, used for managing pipelines.

        Note:
            This property encapsulates the internal _pipeline attribute, ensuring controlled
            access and potential for additional logic in future updates.
        """
        return self._pipeline

    @property
    def pipeline_run(self) -> PipelineRunClient:
        """
        A property that provides access to the pipeline run object.

        Returns:
            object: The pipeline run object associated with the instance, used for 
            managing or monitoring pipeline runs.

        Note:
            This property encapsulates the internal _pipeline_run attribute, ensuring 
            controlled access and potential for additional logic in future updates.
        """
        return self._pipeline_run

    @property
    def storage(self):
        """
        A property that provides access to the storage client.

        Returns:
            object: The storage client object for this instance, generally used for 
            interacting with storage services (like databases or cloud storage).

        Note:
            This property encapsulates the internal _storage attribute, ensuring controlled
            access and potential for additional logic in future updates.
        """
        return self._storage
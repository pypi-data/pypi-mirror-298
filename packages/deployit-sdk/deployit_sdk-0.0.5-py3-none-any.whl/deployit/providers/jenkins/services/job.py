"""
This module provides a service for interacting with Jenkins jobs.
"""
import time
from typing import Dict

from deployit.providers.jenkins.endpoints.job import JobEndpoints
from deployit.providers.jenkins.models.build import Build
from deployit.providers.jenkins.models.job import Job
from deployit.providers.jenkins.parameters.base import DeployParameters
from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.services.base import JenkinsApiService
from deployit.providers.jenkins.services.build import JenkinsBuildApiService
from deployit.providers.jenkins.utils.errors import JenkinsAPIError
from deployit.providers.jenkins.utils.filter import matches_filter


class JenkinsJobApiService(JenkinsApiService):
    """
    A service class for interacting with Jenkins jobs.
    """

    def __init__(self, jenkins_client, build_service: JenkinsBuildApiService = None):
        super().__init__(jenkins_client)
        self.build_service = build_service or JenkinsBuildApiService(jenkins_client)
        self.presenter = RichPresenter()

    def get_all(self, tree: str) -> Dict:
        """
        Retrieve all jobs information with a specific tree structure.

        Parameters
        ----------
        tree : str
            The tree structure for retrieving job information.

        Returns
        -------
        dict
            Information about all jobs.
        """
        self.presenter.info(f"Retrieving all jobs with tree structure: {tree}")
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.JOBS_QUERY, method="GET", tree=tree
            )
            self.presenter.info("Successfully retrieved all jobs.")
            return response
        except Exception as e:
            self.presenter.error(f"Error retrieving all jobs: {e}")
            raise

    def get_info(self, base_url: str, depth: int = 1) -> Job:
        """
        Retrieve information about a specific job.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.
        depth : int, optional
            The depth of the information retrieval (default is 1).

        Returns
        -------
        dict
            The job information.
        """
        self.presenter.info(
            f"Retrieving job info for {base_url} with depth {depth}"
        )
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.JOB_INFO,
                method="GET",
                base_url=base_url,
                depth=depth,
            )
            job = Job({**response, "urlPath": base_url})
            self.presenter.info("Successfully retrieved job info.")
            return job
        except Exception as e:
            self.presenter.error(f"Error retrieving job info: {e}")
            raise

    def wait_for_build(
        self, build_obj: Build, timeout: int = 120, interval: int = 10
    ) -> bool:
        """
        Wait for a build to start and return the Build object.

        Parameters
        ----------
        queue_id : int
            The queue ID of the enqueued build.
        timeout : int
            The maximum time to wait for the build to start, in seconds.
        interval : int
            The interval between checks, in seconds.

        Returns
        -------
        Build
            The Build object once the build starts.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                build_obj = self.build_service.refresh_build(build_obj)
                if build_obj.number:
                    self.presenter.info(f"Build {build_obj.number} started.")
                    return build_obj
            except Exception as e:
                self.presenter.error(f"Error checking queue item: {e}")
            time.sleep(interval)
        raise TimeoutError(f"Build did not start within {timeout} seconds.")

    def build(self, base_url: str, wait_until_start=False, timeout: int = 120, interval: int = 10) -> Build:
        """
        Trigger a build for a specific job.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.

        Returns
        -------
        dict
            The response from triggering the build.
        """
        self.presenter.info(f"Triggering build for job {base_url}")
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.BUILD_JOB,
                method="POST",
                base_url=base_url,
            )
            self.presenter.info("Successfully triggered build.")
            if "Location" in response and "queue" in response["Location"]:
                queue_id = int(response["Location"].split("/")[-2])
                response["queueId"] = queue_id
            build_obj = Build({**response, "urlPath": base_url})
            if wait_until_start:
                build_obj = self.wait_for_build(build_obj, timeout, interval)
            return build_obj
        except Exception as e:
            self.presenter.error(f"Error triggering build: {e}")
            raise

    def build_with_params(self, base_url: str, params: Dict) -> Dict:
        """
        Trigger a build for a specific job with parameters.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.
        params : dict
            The parameters to pass to the job.

        Returns
        -------
        dict
            The response from triggering the build with parameters.
        """
        self.presenter.info(
            f"Triggering build with parameters for job {base_url} with params {params}"
        )
        try:
            request_query = DeployParameters(**params).to_url_query()
            response = self.jenkins_client.make_request(
                JobEndpoints.BUILD_WITH_PARAMETERS,
                method="POST",
                query=request_query,
                base_url=base_url,
            )
            self.presenter.info("Successfully triggered build with parameters.")
            return response
        except Exception as e:
            self.presenter.error(f"Error triggering build with parameters: {e}")
            raise

    def get_all_builds(self, base_url: str) -> Dict:
        """
        Retrieve all builds information for a specific job with a specific tree structure.

        Parameters
        ----------
        base_url : str
            The URL of the folder containing the job.
        tree : str
            The tree structure for retrieving build information.

        Returns
        -------
        dict
            Information about all builds for the job.
        """
        self.presenter.info(
            f"Retrieving all builds for job {base_url}."
        )
        try:
            response = self.jenkins_client.make_request(
                JobEndpoints.ALL_BUILDS,
                method="GET",
                base_url=base_url,
            )
            self.presenter.info("Successfully retrieved all builds.")
            return response
        except Exception as e:
            self.presenter.error(f"Error retrieving all builds: {e}")
            raise

    def fetch_job_details(self, job: Job) -> Job:
        """
        Fetch details for a given job and update the job instance.

        Parameters
        ----------
        job : Job
            The job for which to fetch details.

        Returns
        -------
        Job
            The updated job instance.
        """
        self.presenter.info(
            f"Fetching details for job '{job.name}' with URL '{job.url}'"
        )
        try:
            job_info = self.get_info(base_url=job.full_name)
            self.presenter.debug(f"Job info received: {job_info}")
            job = Job(job_info)
            job.build_history = self.fetch_builds(job)
            self.presenter.info(f"Successfully fetched details for job '{job.name}'")
        except Exception as e:
            raise JenkinsAPIError(f"Error fetching job details: {e}") from e
        return job

    def fetch_builds(self, job: Job, filter_by: dict = {}) -> list:
        """
        Fetch all builds for a given job.

        Parameters
        ----------
        job : Job
            The job for which to fetch builds.
        filter_by : dict
            A dictionary of filters to apply to the builds. 
            The key is the field to filter by, and the value is the value to filter for.

        Returns
        -------
        list
            A list of builds associated with the job.
        """
        self.presenter.info(
            f"Fetching all builds for job '{job.name}' with URL '{job.url}'"
        )
        try:
            builds_data = self.get_all_builds(
                base_url=job.url_path
            ).get("allBuilds", [])
            filtered_builds = []
            for build_response in builds_data:
                if matches_filter(build_response, filter_by):
                    filtered_builds.append(Build(build_response))
            self.presenter.info(f"Fetched {len(filtered_builds)} builds for job '{job.name}'")
            return filtered_builds
        except Exception as e:
            raise JenkinsAPIError(
                f"Error fetching builds for job '{job.name}': {e}"
            ) from e

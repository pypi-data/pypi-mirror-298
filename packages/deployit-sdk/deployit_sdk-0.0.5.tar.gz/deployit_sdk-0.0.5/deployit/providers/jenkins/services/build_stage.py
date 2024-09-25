import json
from typing import Dict, Optional

from deployit.providers.jenkins.models.build_stage import JenkinsBuildStage
from deployit.providers.jenkins.presentation.rich import RichPresenter
from deployit.providers.jenkins.services.base import JenkinsApiService
from deployit.providers.jenkins.utils.errors import JenkinsError


class JenkinsBuildStageService(JenkinsApiService):
    def __init__(self, jenkins_client):
        super().__init__(jenkins_client)
        self.presenter = RichPresenter()

    def handle_input(
        self,
        base_url: str,
        build_stage: JenkinsBuildStage,
        action: str,
        proceed_caption: Optional[str] = None,
        parameters: Optional[Dict] = None,
    ):
        """
        Handle input stages in a Jenkins build.

        Parameters
        ----------
        folder_url : str
            The base URL of the Jenkins server with path to the folder.
        short_name : str
            The last path to the job.
        build_stage : JenkinsBuildStage
            The build stage to handle.
        action : str
            The action to perform ('abort', 'proceedEmpty', 'submit', 'wfapi/inputSubmit').
        proceed_caption : str, optional
            The caption of the 'Proceed' button, required for 'submit' action.
        parameters : dict, optional
            The parameters to send with the 'submit' or 'wfapi/inputSubmit' actions.

        Returns
        -------
        dict
            The response from the Jenkins server.
        """
        formatted_base_url = "/job/".join(base_url.split("/"))
        self.presenter.info(
            f"Handling input action '{action}' for input ID '{build_stage.id}' in build {build_stage.build_id} of project {formatted_base_url}."
        )
        try:
            if action not in ["abort", "proceedEmpty", "submit", "wfapi/inputSubmit"]:
                raise ValueError("Invalid action specified")
            url = f"{formatted_base_url}/{build_stage.build_id}/input/{build_stage.id}/{action}"

            if action in ["submit", "wfapi/inputSubmit"]:
                if not proceed_caption:
                    raise ValueError(
                        "'proceed_caption' is required for 'submit' action"
                    )

                data = {
                    "proceed": proceed_caption,
                    "json": json.dumps({"parameter": parameters}) if parameters else "",
                }
            else:
                data = None

            response = self.jenkins_client.make_request(url, method="POST", data=data)
            self.presenter.info(
                f"Successfully performed '{action}' for input ID '{build_stage.id}'."
            )
            return response.json() if hasattr(response, "content") else {}
        except JenkinsError as e:
            self.presenter.error(
                f"Jenkins error during input handling for input ID '{build_stage.id}': {e}"
            )
            raise
        except Exception as e:
            self.presenter.error(
                f"Unexpected error during input handling for input ID '{build_stage.id}': {e}"
            )
            raise

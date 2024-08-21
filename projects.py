# Copyright 2020 Alvin Chen sonoma001@gmail.com
# SPDX-License-Identifier: GPL-2.0+
import io
import logging

from exceptions import DependencyTrackApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Projects:
    """Class dedicated to all "projects" related endpoints"""

    def __init__(self):
        self.session = None
        self.paginated_param_payload = None
        self.api = None

    def list_projects(self):
        """List all projects accessible to the authenticated user

        API Endpoint: GET /project

        :return: a list of projects
        :rtype: list()
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + "/project", params=self.paginated_param_payload)

        if response.status_code == 200:
            return response.json()
        else:
            description = f"Unable to get a list of projects"
            raise DependencyTrackApiError(description, response)

    def get_project_property(self, uuid):
        """Get details of project.

        API Endpoint: GET /project/{uuid}/property

        :param uuid: the ID of the project to be analysed
        :type uuid: uuid string
        :return: the requested project property
        :rtype: list()
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/project/{uuid}/property", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Error while getting property for project {uuid}"
            raise DependencyTrackApiError(description, response)

    def get_project_dependency(self, uuid):
        """Get details of project dependency.

        API Endpoint: GET /dependency/project/{uuid}

        :param uuid: the ID of the project to be analysed
        :type uuid: uuid string
        :return: the requested project
        :rtype: project dependency dict
        :raises DependencyTrackApiError: if the REST call failed
        """

        response = self.session.get(self.api + f"/dependency/project/{uuid}", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Error while getting dependency for project {uuid}"
            raise DependencyTrackApiError(description, response)

    def get_project(self, uuid):
        """Get details of project.

        API Endpoint: GET /project/{uuid}/property

        :param uuid: the ID of the project to be analysed
        :type uuid: uuid string
        :return: the requested project property
        :rtype: list()
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/project/{uuid}/", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Error while getting project {uuid}"
            raise DependencyTrackApiError(description, response)

    def get_project_vdr(self, uuid, name, version):
        """Get VDR file of project.

        API Endpoint: GET /v1/bom/cyclonedx/project/{project_uuid}

        :param uuid: the ID of the project to be analysed
        :param name: the name of the Project for which a VDR is requested
        :param version: the version of the Project for which a VDR is requested
        :return: the requested VDR data
        :rtype: a file
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/bom/cyclonedx/project/{uuid}" + "?variant=vdr",
                                    params=self.paginated_param_payload)
        with io.open((name + "_" + version + "_VDR.json"), "w", encoding='utf-8') as output_file_handle:
            print(response.text, file=output_file_handle)

        if response.status_code != 200:
            description = f"Error while getting project {uuid}"
            raise DependencyTrackApiError(description, response)

    def get_product_policy_violations(self, uuid, name, version):
        """
        Get the list of policy violations for a specific product at a named version.
        REQUIRES the Administrator team has the following capabilities in the Dependency Track Team -> Permission
            POLICY_MANAGEMENT
            POLICY_VIOLATION_ANALYSIS
            VIEW_POLICY_VIOLATION

        "/v1/violation/project/{uuid}"
        :param uuid: the ID of the project to be analysed
        :param name: the name of the Project for which a VDR is requested
        :param version: the version of the Project for which a VDR is requested
        :return: the requested policy violation data
        :rtype: a file
        :raises DependencyTrackApiError: if the REST call failed
        """
        response_API = self.session.get(self.api + f"/violation/project/{uuid}")
        if response_API.status_code != 200:
            description = f"Error while getting project {uuid}"
            raise DependencyTrackApiError(description, response_API)

        import json

        json_object = json.loads(response_API.text)
        json_formatted_str = json.dumps(json_object, indent=2)
        with io.open((name + "_" + version + "_policy_violations.json"), "w", encoding='utf-8') as output_file_handle:
            print(json_formatted_str, file=output_file_handle)

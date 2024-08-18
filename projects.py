# Copyright 2020 Alvin Chen sonoma001@gmail.com
# SPDX-License-Identifier: GPL-2.0+
import io
import logging

import requests

from exceptions import DependencyTrackApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Projects:
    """Class dedicated to all "projects" related endpoints"""

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
        print(response.url)
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
        """Get vdr file of project.

        example command line method:
        curl -H
            'X-Api-Key: XrnGcCSFoCzhHFX7vWu0hD4IisDeFrQl'
            -H 'Accept application/vnd.cyclonedx+xml'
            'http://192.168.1.24:8081/api/v1/bom/cyclonedx/project/b9213f2b-c073-4b24-b03e-30ea4e65664f?variant=vdr'
        API Endpoint: GET /v1/bom/cyclonedx/project/{project_uuid}

        :param uuid: the ID of the project to be analysed
        :type uuid: uuid string
        :return: the requested VDR data
        :rtype: a file
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/bom/cyclonedx/project/{uuid}" + "?variant=vdr", \
                                    params=self.paginated_param_payload)
        with io.open((name + "_" + version + "_VDR.json"), "w", encoding='utf-8') as output_file_handle:
            print(response.text, file=output_file_handle)

        if response.status_code == 200:
            print("VDR response content", response.content)
            return response.json()
        else:
            description = f"Error while getting project {uuid}"
            raise DependencyTrackApiError(description, response)

    def get_product_policy_violations(self, uuid, name, version):
        """
        Get the list of policy violations for a specific product at a named version.
        "/v1/violation/project/{uuid}"
        :param uuid: the ID of the project to be analysed
        :type uuid: uuid string
        :return: the requested policy violation VDR data
        :rtype: a file
        :raises DependencyTrackApiError: if the REST call failed
        """

        """
        response = self.session.get(self.api + f"/violation/project/{uuid}", params=self.paginated_param_payload)
        """
        response_API = requests.get(self.api + f"/violation/project/{uuid}")
        if response_API.status_code == 200:
            print("Violation response content for project ", {uuid}, response_API.content)

        else:
            description = f"Error while getting project {uuid}"
            raise DependencyTrackApiError(description, response_API)

        """
        TODO 
        with io.open((name + "_" + version + "_policy_violations.json"), "w", encoding='utf-8') as output_file_handle:
            print(response.text, file=output_file_handle)
        """

# Copyright 2019 AT&T Intellectual Property. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from robot import utils
from robot.api.deco import keyword
import os.path
import json


class ServiceMappingKeywords(object):
    """ServiceMapping is used for loading data for services into the robot framework in a structured decentralized way
    that lets vnfs be added without code change to testuite"""

    def __init__(self):
        super(ServiceMappingKeywords, self).__init__()
        self._cache = utils.ConnectionCache('No Service Mappings directories loaded')

    @keyword
    def set_directory(self, alias, service_mappings_directory):
        self._cache.register(service_mappings_directory, alias=alias)

    @keyword
    def get_service_folder_mapping(self, alias, service):
        """returns an array of strings with metadata that identifies the folders to be zipped and
        uploaded to SDC for model distribution for a given Service """
        return self._service_mapping(alias, service)['GLOBAL_SERVICE_FOLDER_MAPPING'][service]

    @keyword
    def get_service_vnf_mapping(self, alias, service):
        """returns an array of strings that is the vnfs in this service """
        return self._service_mapping(alias, service)['GLOBAL_SERVICE_VNF_MAPPING'][service]

    @keyword
    def get_service_neutron_mapping(self, alias, service):
        """returns an array of strings that lists the neutron networks needed in this service.
        Map the service to the list of Generic Neutron Networks to be orchestrated """
        return self._service_mapping(alias, service)['GLOBAL_SERVICE_GEN_NEUTRON_NETWORK_MAPPING'][service]

    @keyword
    def get_service_deployment_artifact_mapping(self, alias, service):
        """returns an array of strings that is the extra deployment artifacts needed with this service """
        return self._service_mapping(alias, service)['GLOBAL_SERVICE_DEPLOYMENT_ARTIFACT_MAPPING'][service]

    @keyword
    def get_service_template_mapping(self, alias, service, vnf):
        """returns an array of strings that are the heat templates for this vnf. This metadata identifes the preloads
        that need to be done for a VNF as there may be more than one (vLB) "template" maps to the parameters
        in the preload_paramenters.py """
        return self._service_mapping(alias, service)['GLOBAL_SERVICE_TEMPLATE_MAPPING'][vnf]

    """@PendingDeprecationWarning"""
    @keyword
    def get_validate_name_mapping(self, alias, service, vnf):
        """returns an array of strings that are the names to validate in heatbridge for the vnf.
         Used by the Heatbridge Validate Query to A&AI to locate the vserver name"""
        return self._service_mapping(alias, service)['GLOBAL_VALIDATE_NAME_MAPPING'][vnf]

    def _service_mapping(self, alias, service):
        filepath = os.path.join(self._cache.switch(alias), service, 'service_mapping.json')
        with open(filepath, 'r') as f:
            return json.load(f)

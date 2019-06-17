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

import robot.utils
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import json

from ONAPLibrary.Utilities import Utilities


class BaseOpenstackKeywords(object):
    """SO is an ONAP testing library for Robot Framework that provides functionality for interacting with the serivce
    orchestrator. """

    def __init__(self):
        super(BaseOpenstackKeywords, self).__init__()
        self._cache = robot.utils.ConnectionCache('No connections created')
        self.application_id = "robot-ete"
        self.uuid = Utilities()
        self.builtin = BuiltIn()

    @keyword
    def save_openstack_auth(self, alias, response, token, version='v2.0'):
        """Save Openstack Auth takes in an openstack auth response and saves it to allow easy retrival of token
        and service catalog"""
        self.builtin.log('Creating connection: %s' % alias, 'DEBUG')
        json_response = json.loads(response)
        json_response['auth_token'] = token
        json_response['keystone_api_version'] = version
        self._cache.register(json_response, alias=alias)

    @keyword
    def get_openstack_token(self, alias):
        """Get Openstack auth token from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            json_response = json.loads(response)
        else:
            json_response = response
        if json_response['keystone_api_version'] == 'v2.0':
            return json_response['access']['token']['id']
        else:
            return json_response['auth_token']

    @keyword
    def get_openstack_catalog(self, alias):
        """Get Openstack service catalog from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            json_response = json.loads(response)
        else:
            json_response = response
        if json_response['keystone_api_version'] == 'v2.0':
            return json_response['access']['serviceCatalog']
        else:
            return json_response['token']['catalog']

    @keyword
    def get_current_openstack_tenant(self, alias):
        """Get Openstack tenant from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            json_response = json.loads(response)
        else:
            json_response = response
        if json_response['keystone_api_version'] == 'v2.0':
            return json_response['access']['token']['tenant']
        else:
            return json_response['token']['project']

    @keyword
    def get_current_openstack_tenant_id(self, alias):
        """Get Openstack tenant id from the current alias"""
        tenant = self.get_current_openstack_tenant(alias)
        return tenant['id']

    @keyword
    def get_openstack_regions(self, alias):
        """Get all Openstack regions from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            json_response = json.loads(response)
        else:
            json_response = response
        regions = []
        if json_response['keystone_api_version'] == 'v2.0':
            resp = json_response['access']['serviceCatalog']
        else:
            resp = json_response['token']['catalog']
        for catalogEntry in resp:
            list_of_endpoints = catalogEntry['endpoints']
            for endpoint in list_of_endpoints:
                if 'region' in endpoint:
                    if endpoint['region'] not in regions:
                        regions.append(endpoint['region'])
        return regions

    @keyword
    def get_openstack_service_url(self, alias, servicetype, region=None, tenant_id=None):
        """Get Openstack service catalog from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            json_response = json.loads(response)
        else:
            json_response = response
        endpoint = None
        if json_response['keystone_api_version'] == 'v2.0':
            resp = json_response['access']['serviceCatalog']
        else:
            resp = json_response['token']['catalog']
        for catalogEntry in resp:
            if self.__determine_match(catalogEntry['type'], servicetype):
                list_of_endpoints = catalogEntry['endpoints']
                # filter out non matching regions if provided
                list_of_endpoints[:] = [x for x in list_of_endpoints if self.__determine_match(x['region'], region)]
                # filter out non matching tenants if provided
                # Only provide tenant id when authorizing without qualifying with tenant id
                # WindRiver does not return the tenantId on the endpoint in this case.
                if tenant_id is not None:
                    list_of_endpoints[:] = [y for y in list_of_endpoints if
                                            self.__determine_match(y['tenantId'], tenant_id)]
                if json_response['keystone_api_version'] == 'v3':
                    list_of_endpoints[:] = [z for z in list_of_endpoints if
                                            self.__determine_match(z['interface'], 'public')]
                if len(list_of_endpoints) > 0:
                    if json_response['keystone_api_version'] == 'v2.0':
                        endpoint = list_of_endpoints[0]['publicURL']
                    else:
                        endpoint = list_of_endpoints[0]['url']
        if endpoint is None:
            self.builtin.should_not_be_empty("", "Service Endpoint Url should not be empty")
        return endpoint

    @staticmethod
    def __determine_match(list_item, item):
        if item is None:
            return True
        elif list_item == item:
            return True
        else:
            return False

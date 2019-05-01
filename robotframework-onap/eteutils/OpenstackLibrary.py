from robot.libraries.BuiltIn import BuiltIn
import robot.utils
import json

class OpenstackLibrary:
    """OpenstackLibrary manages the connection state and service catalog of an openstack instance."""

    ROBOT_LIBRARY_SCOPE = 'Global'


    def __init__(self):
        self._cache = robot.utils.ConnectionCache('No connections created')
        self.builtin = BuiltIn()

    def save_openstack_auth(self, alias, response,token, version='v2.0'):
        """Save Openstack Auth takes in an openstack auth response and saves it to allow easy retrival of token and service catalog"""
        self.builtin.log('Creating connection: %s' % alias, 'DEBUG')
        jsonResponse = json.loads(response);
        jsonResponse['auth_token'] = token
        jsonResponse['keystone_api_version'] = version
        self._cache.register(jsonResponse, alias=alias)

    def get_openstack_token(self, alias):
        """Get Openstack auth token from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        if jsonResponse['keystone_api_version'] == 'v2.0':
            return  jsonResponse['access']['token']['id']
        else:
            return  jsonResponse['auth_token']

    def get_openstack_catalog(self, alias):
        """Get Openstack service catalog from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        if jsonResponse['keystone_api_version'] == 'v2.0':
            return  jsonResponse['access']['serviceCatalog']
        else:
            return  jsonResponse['token']['catalog']
 

    def get_current_openstack_tenant(self, alias):
        """Get Openstack tenant from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        if jsonResponse['keystone_api_version'] == 'v2.0':
            return  jsonResponse['access']['token']['tenant']
        else:
            return  jsonResponse['token']['project']

    def get_current_openstack_tenant_id(self, alias):
        """Get Openstack tenant id from the current alias"""
        tenant = self.get_current_openstack_tenant(alias);
        return  tenant['id']

    def get_openstack_regions(self, alias):
        """Get all Openstack regions from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        regions = [];
        if jsonResponse['keystone_api_version'] == 'v2.0':
            resp = jsonResponse['access']['serviceCatalog']
        else:
            resp = jsonResponse['token']['catalog']
        for catalogEntry in resp:
            listOfEndpoints = catalogEntry['endpoints'];
            for endpoint in listOfEndpoints:
                if 'region'in endpoint:
                    if endpoint['region'] not in regions:
                        regions.append(endpoint['region'])
        return regions;

    def get_openstack_service_url(self, alias, servicetype, region =  None, tenant_id = None):
        """Get Openstack service catalog from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, str):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        endPoint = None;
        if jsonResponse['keystone_api_version'] == 'v2.0':
            resp = jsonResponse['access']['serviceCatalog']
        else:
            resp = jsonResponse['token']['catalog']
        for catalogEntry in resp:    
            if self.__determine_match(catalogEntry['type'], servicetype):
                listOfEndpoints = catalogEntry['endpoints'];
                # filter out non matching regions if provided
                listOfEndpoints[:] = [x for x in listOfEndpoints if self.__determine_match(x['region'], region)];
                # filter out non matching tenants if provided
                # Only provide tenant id when authorizing without qualifying with tenant id
                # WindRiver does not return the tenantId on the endpoint in this case.
                if tenant_id is not None:
                    listOfEndpoints[:] = [y for y in listOfEndpoints if self.__determine_match(y['tenantId'], tenant_id)];
                if jsonResponse['keystone_api_version'] == 'v3':
                        listOfEndpoints[:] = [z for z in listOfEndpoints if self.__determine_match(z['interface'], 'public')];
                if len(listOfEndpoints) > 0:
                    if jsonResponse['keystone_api_version'] == 'v2.0':
                        endPoint = listOfEndpoints[0]['publicURL'];
                    else:
                        endPoint = listOfEndpoints[0]['url'];
        if endPoint == None:
            self.builtin.should_not_be_empty("", "Service Endpoint Url should not be empty")
        return endPoint;

    def __determine_match(self, listItem, item):
        if item is None:
            return True;
        elif listItem == item:
            return True;
        else:
            return False;
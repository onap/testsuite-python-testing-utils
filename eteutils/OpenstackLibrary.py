from robot.libraries.BuiltIn import BuiltIn
import robot.utils
import json

class OpenstackLibrary:
    """OpenstackLibrary manages the connection state and service catalog of an openstack instance."""
    
    ROBOT_LIBRARY_SCOPE = 'Global'
    
    
    def __init__(self):
        self._cache = robot.utils.ConnectionCache('No connections created')
        self.builtin = BuiltIn()

    def save_openstack_auth(self, alias, response):
        """Save Openstack Auth takes in an openstack auth response and saves it to allow easy retrival of token and service catalog"""
        self.builtin.log('Creating connection: %s' % alias, 'DEBUG')
        self._cache.register(response, alias=alias)
        
    def get_openstack_token(self, alias):
        """Get Openstack auth token from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, basestring):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        return  jsonResponse['access']['token']['id']
    
    def get_openstack_catalog(self, alias):
        """Get Openstack service catalog from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, basestring):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        return  jsonResponse['access']['serviceCatalog']
    
    def get_current_openstack_tenant(self, alias):
        """Get Openstack tenant from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, basestring):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        return  jsonResponse['access']['token']['tenant']
    
    def get_current_openstack_tenant_id(self, alias):
        """Get Openstack tenant id from the current alias"""
        tenant = self.get_current_openstack_tenant(alias);
        return  tenant['id']
    
    def get_openstack_regions(self, alias):
        """Get all Openstack regions from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, basestring):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        regions = [];
        for catalogEntry in jsonResponse['access']['serviceCatalog']:
            listOfEndpoints = catalogEntry['endpoints'];
            for endpoint in listOfEndpoints:
                if 'region'in endpoint:
                    if endpoint['region'] not in regions:
                        regions.append(endpoint['region'])
        return regions;
    
    def get_openstack_service_url(self, alias, servicetype, region =  None, tenant_id = None):
        """Get Openstack service catalog from the current alias"""
        response = self._cache.switch(alias)
        if isinstance(response, basestring):
            jsonResponse = json.loads(response);
        else:
            jsonResponse = response;
        endPoint = None;
        for catalogEntry in jsonResponse['access']['serviceCatalog']:
            if self.__determine_match(catalogEntry['type'], servicetype):
                listOfEndpoints = catalogEntry['endpoints'];
                # filter out non matching regions if provided
                listOfEndpoints[:] = [x for x in listOfEndpoints if self.__determine_match(x['region'], region)];
                # filter out non matching tenants if provided
                listOfEndpoints[:] = [y for y in listOfEndpoints if self.__determine_match(y['tenantId'], tenant_id)];
                if len(listOfEndpoints) > 0:
                    endPoint = listOfEndpoints[0]['publicURL'];
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
import logging
import os


class VcpeCommon:
    # set the openstack cloud access credentials here
    cloud = {
        '--os-auth-url': 'http://10.12.25.2:5000',
        '--os-username': 'kxi',
        '--os-user-domain-id': 'default',
        '--os-project-domain-id': 'default',
        '--os-tenant-id': '09d8566ea45e43aa974cf447ed591d77',
        '--os-region-name': 'RegionOne',
        '--os-password': 'n3JhGMGuDzD8',
        '--os-project-domain-name': 'Integration-SB-03',
        '--os-identity-api-version': '3'
    }

    #############################################################################################

    template_variable_symbol = '${'
    cpe_vm_prefix = 'zdcpe'

    dcae_ves_collector_name = 'dcae-bootstrap'
    global_subscriber_id = 'Demonstration'
    project_name = 'Project-Demonstration'
    owning_entity_id = '520cc603-a3c4-4ec2-9ef4-ca70facd79c0'
    owning_entity_name = 'OE-Demonstration1'

    def __init__(self, extra_host_names=None):
        rootlogger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s.%(funcName)s(): %(message)s')
        handler.setFormatter(formatter)
        rootlogger.addHandler(handler)
        rootlogger.setLevel(logging.INFO)

        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info('Initializing configuration')

        # CHANGEME: vgw_VfModuleModelInvariantUuid is in rescust service csar,
        # look in service-VcpesvcRescust1118-template.yml for groups vgw module metadata.
        # TODO: read this value automcatically
        self.vgw_VfModuleModelInvariantUuid = '26d6a718-17b2-4ba8-8691-c44343b2ecd2'
        self.sdnc_preloading_port = '8282'

        self.host_names = ['so', 'sdnc', 'robot', 'aai', self.dcae_ves_collector_name]
        if extra_host_names:
            self.host_names.extend(extra_host_names)
        # get IP addresses
        self.hosts = {'so': 'so.onap', 'sdnc': 'sdnc.onap', 'robot': 'robot.onap', 'aai': 'aai.onap'}
        self.os_tenant_id = self.cloud['--os-tenant-id']
        self.os_region_name = self.cloud['--os-region-name']

        #############################################################################################
        # SDNC urls
        self.sdnc_db_name = 'sdnctl'
        self.sdnc_db_user = 'sdnctl'
        self.sdnc_db_pass = 'gamma'
        self.sdnc_db_port = '32774'
        self.sdnc_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.sdnc_preload_network_url = 'http://' + self.hosts['sdnc'] + \
                                        ':' + self.sdnc_preloading_port + '/restconf/operations/VNF-API:preload-network-topology-operation'
        self.sdnc_preload_vnf_url = 'http://' + self.hosts['sdnc'] + \
                                    ':' + self.sdnc_preloading_port + '/restconf/operations/VNF-API:preload-vnf-topology-operation'
        self.sdnc_preload_gra_url = 'http://' + self.hosts['sdnc'] + \
                                    ':' + self.sdnc_preloading_port + '/restconf/operations/GENERIC-RESOURCE-API:preload-vf-module-topology-operation'
        self.sdnc_ar_cleanup_url = 'http://' + self.hosts['sdnc'] + ':' + self.sdnc_preloading_port + \
                                   '/restconf/config/GENERIC-RESOURCE-API:'

        self.vpp_inf_url = 'http://{0}:8183/restconf/config/ietf-interfaces:interfaces'
        self.vpp_api_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.vpp_api_userpass = ('admin', 'admin')
        self.vpp_ves_url = 'http://{0}:8183/restconf/config/vesagent:vesagent'

    @staticmethod
    def network_name_to_subnet_name(network_name):
        """
        :param network_name: example: vcpe_net_cpe_signal_201711281221
        :return: vcpe_net_cpe_signal_subnet_201711281221
        """
        fields = network_name.split('_')
        fields.insert(-1, 'subnet')
        return '_'.join(fields)

    def set_network_name(self, network_name):
        param = ' '.join([k + ' ' + v for k, v in list(self.cloud.items())])
        openstackcmd = 'openstack ' + param
        cmd = ' '.join([openstackcmd, 'network set --name', network_name, 'ONAP-NW1'])
        os.popen(cmd)

    def set_subnet_name(self, network_name):
        """
        Example: network_name =  vcpe_net_cpe_signal_201711281221
        set subnet name to vcpe_net_cpe_signal_subnet_201711281221
        :return:
        """
        param = ' '.join([k + ' ' + v for k, v in list(self.cloud.items())])
        openstackcmd = 'openstack ' + param

        # expected results: | subnets | subnet_id |
        subnet_info = os.popen(openstackcmd + ' network show ' + network_name + ' |grep subnets').read().split('|')
        if len(subnet_info) > 2 and subnet_info[1].strip() == 'subnets':
            subnet_id = subnet_info[2].strip()
            subnet_name = self.network_name_to_subnet_name(network_name)
            cmd = ' '.join([openstackcmd, 'subnet set --name', subnet_name, subnet_id])
            os.popen(cmd)
            self.logger.info("Subnet name set to: " + subnet_name)
            return True
        else:
            self.logger.error("Can't get subnet info from network name: " + network_name)
            return False

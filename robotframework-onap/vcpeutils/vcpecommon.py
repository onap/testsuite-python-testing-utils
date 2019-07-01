import json
import logging
import os
import sys
import requests


class VcpeCommon:
    #############################################################################################
    #     Start: configurations that you must change for a new ONAP installation
    external_net_addr = '10.12.0.0'
    external_net_prefix_len = 16
    #############################################################################################
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

    common_preload_config = {
        'oam_onap_net': 'oam_network_2No2',
        'oam_onap_subnet': 'oam_network_2No2',
        'public_net': 'external',
        'public_net_id': '971040b2-7059-49dc-b220-4fab50cb2ad4'
    }
    sdnc_controller_pod = 'dev-sdnc-sdnc-0'

    #############################################################################################

    template_variable_symbol = '${'
    cpe_vm_prefix = 'zdcpe'
    #############################################################################################
    # preloading network config
    #  key=network role
    #  value = [subnet_start_ip, subnet_gateway_ip]
    preload_network_config = {
        'cpe_public': ['10.2.0.2', '10.2.0.1'],
        'cpe_signal': ['10.4.0.2', '10.4.0.1'],
        'brg_bng': ['10.3.0.2', '10.3.0.1'],
        'bng_mux': ['10.1.0.10', '10.1.0.1'],
        'mux_gw': ['10.5.0.10', '10.5.0.1']
    }

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

        # CHANGEME: vgw_VfModuleModelInvariantUuid is in rescust service csar, look in service-VcpesvcRescust1118-template.yml for groups vgw module metadata. TODO: read this value automcatically
        self.vgw_VfModuleModelInvariantUuid = '26d6a718-17b2-4ba8-8691-c44343b2ecd2'
        # CHANGEME: OOM: this is the address that the brg and bng will nat for sdnc access - 10.0.0.x address of k8 host for sdnc-0 container
        #self.sdnc_oam_ip = self.get_pod_node_oam_ip('sdnc-sdnc-0')
        self.sdnc_oam_ip = 'sdnc.onap'
        # CHANGEME: OOM: this is a k8s host external IP, e.g. oom-k8s-01 IP 
        #self.oom_so_sdnc_aai_ip = self.get_pod_node_public_ip('sdnc-sdnc-0')
        #self.oom_so_sdnc_aai_ip = self.get_pod_node_public_ip('sdnc-sdnc-0')
        # CHANGEME: OOM: this is a k8s host external IP, e.g. oom-k8s-01 IP
        #self.oom_dcae_ves_collector = self.oom_so_sdnc_aai_ip
        # CHANGEME: OOM: this is a k8s host external IP, e.g. oom-k8s-01 IP
        #self.mr_ip_addr = self.oom_so_sdnc_aai_ip
        self.mr_ip_addr = 'mr.onap'
        #self.mr_ip_port = '30227'
        self.mr_ip_port = '3904'
        #self.so_nbi_port = '30277' if self.oom_mode else '8080'

        #self.sdnc_preloading_port = '30202' if self.oom_mode else '8282'
        self.sdnc_preloading_port = '8282'
        #self.aai_query_port = '30233' if self.oom_mode else '8443'
        self.aai_query_port = '8443' 
        #self.sniro_port = '30288' if self.oom_mode else '8080'
        self.sniro_port = '8080' 

        self.host_names = ['so', 'sdnc', 'robot', 'aai', self.dcae_ves_collector_name]
        if extra_host_names:
            self.host_names.extend(extra_host_names)
        # get IP addresses
        #self.hosts = self.get_vm_ip(self.host_names, self.external_net_addr, self.external_net_prefix_len)
        self.hosts = { 'so': 'so.onap', 'sdnc': 'sdnc.onap', 'robot': 'robot.onap', 'aai': 'aai.onap' }
        # this is the keyword used to name vgw stack, must not be used in other stacks
        self.vgw_name_keyword = 'base_vcpe_vgw'
        # this is the file that will keep the index of last assigned SO name
        self.vgw_vfmod_name_index_file= '__var/vgw_vfmod_name_index'
        self.svc_instance_uuid_file = '__var/svc_instance_uuid'
        self.preload_dict_file = '__var/preload_dict'
        self.vgmux_vnf_name_file = '__var/vgmux_vnf_name'
        self.product_family_id = 'f9457e8c-4afd-45da-9389-46acd9bf5116'
        self.custom_product_family_id = 'a9a77d5a-123e-4ca2-9eb9-0b015d2ee0fb'
        self.instance_name_prefix = {
            'service': 'svc',
            'network': 'net',
            'vnf': 'vnf',
            'vfmodule': 'vf'
        }
        self.aai_userpass = 'AAI', 'AAI'
        self.pub_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKXDgoo3+WOqcUG8/5uUbk81+yczgwC4Y8ywTmuQqbNxlY1oQ0YxdMUqUnhitSXs5S/yRuAVOYHwGg2mCs20oAINrP+mxBI544AMIb9itPjCtgqtE2EWo6MmnFGbHB4Sx3XioE7F4VPsh7japsIwzOjbrQe+Mua1TGQ5d4nfEOQaaglXLLPFfuc7WbhbJbK6Q7rHqZfRcOwAMXgDoBqlyqKeiKwnumddo2RyNT8ljYmvB6buz7KnMinzo7qB0uktVT05FH9Rg0CTWH5norlG5qXgP2aukL0gk1ph8iAt7uYLf1ktp+LJI2gaF6L0/qli9EmVCSLr1uJ38Q8CBflhkh'
        self.os_tenant_id = self.cloud['--os-tenant-id']
        self.os_region_name = self.cloud['--os-region-name']
        self.common_preload_config['pub_key'] = self.pub_key
        self.sniro_url = 'http://' + self.hosts['robot'] + ':' + self.sniro_port + '/__admin/mappings'
        self.sniro_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.homing_solution = 'sniro'  # value is either 'sniro' or 'oof'
#        self.homing_solution = 'oof'
        self.customer_location_used_by_oof = {
            "customerLatitude": "32.897480",
            "customerLongitude": "-97.040443",
            "customerName": "some_company"
        }

        #############################################################################################
        # SDNC urls
        self.sdnc_userpass = 'admin', 'Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U'
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
        self.vpp_ves_url= 'http://{0}:8183/restconf/config/vesagent:vesagent'



    def find_file(self, file_name_keyword, file_ext, search_dir):
        """
        :param file_name_keyword:  keyword used to look for the csar file, case insensitive matching, e.g, infra
        :param file_ext: e.g., csar, json
        :param search_dir path to search
        :return: path name of the file
        """
        file_name_keyword = file_name_keyword.lower()
        file_ext = file_ext.lower()
        if not file_ext.startswith('.'):
            file_ext = '.' + file_ext

        filenamepath = None
        for file_name in os.listdir(search_dir):
            file_name_lower = file_name.lower()
            if file_name_keyword in file_name_lower and file_name_lower.endswith(file_ext):
                if filenamepath:
                    self.logger.error('Multiple files found for *{0}*.{1} in '
                                      'directory {2}'.format(file_name_keyword, file_ext, search_dir))
                    sys.exit()
                filenamepath = os.path.abspath(os.path.join(search_dir, file_name))

        if filenamepath:
            return filenamepath
        else:
            self.logger.error("Cannot find *{0}*{1} in directory {2}".format(file_name_keyword, file_ext, search_dir))
            sys.exit()

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

    def is_node_in_aai(self, node_type, node_uuid):
        key = None
        search_node_type = None
        if node_type == 'service':
            search_node_type = 'service-instance'
            key = 'service-instance-id'
        elif node_type == 'vnf':
            search_node_type = 'generic-vnf'
            key = 'vnf-id'
        else:
            logging.error('Invalid node_type: ' + node_type)
            sys.exit()

        url = 'https://{0}:{1}/aai/v11/search/nodes-query?search-node-type={2}&filter={3}:EQUALS:{4}'.format(
            self.hosts['aai'], self.aai_query_port, search_node_type, key, node_uuid)

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-FromAppID': 'vCPE-Robot', 'X-TransactionId': 'get_aai_subscr'}
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url, headers=headers, auth=self.aai_userpass, verify=False)
        response = r.json()
        self.logger.debug('aai query: ' + url)
        self.logger.debug('aai response:\n' + json.dumps(response, indent=4, sort_keys=True))
        return 'result-data' in response

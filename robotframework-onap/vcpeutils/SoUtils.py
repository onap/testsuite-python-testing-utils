#! /usr/bin/python

import time

from vcpeutils.csar_parser import *
import requests
from robot.api import logger
from datetime import datetime
import urllib3
import sys
from ONAPLibrary.PreloadSDNCKeywords import PreloadSDNCKeywords


class SoUtils:

    def __init__(self):
        self.region_name = None  # set later
        self.tenant_id = None  # set later
        self.logger = logger

        # SO urls, note: do NOT add a '/' at the end of the url
        self.so_nbi_port = '8080'
        self.so_host = 'so.onap'
        self.so_si_path = '/onap/so/infra/serviceInstantiation/v7/serviceInstances'
        self.so_orch_path = '/onap/so/infra/orchestrationRequests/v6'
        self.service_req_api_url = 'http://' + self.so_host + ':' + self.so_nbi_port + self.so_si_path
        self.so_check_progress_api_url = 'http://' + self.so_host + ':' + self.so_nbi_port + self.so_orch_path
        self.so_userpass = 'InfraPortalClient', 'password1$'
        self.so_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.so_db_name = 'catalogdb'
        self.so_db_user = 'root'
        self.so_db_pass = 'password'
        self.so_db_port = '30252'

        # aai urls
        self.aai_userpass = 'AAI', 'AAI'
        self.aai_query_port = '8443'
        self.aai_host = 'aai.onap'

        # mr utls
        self.mr_ip_addr = 'mr.onap'
        self.mr_ip_port = '3904'

        # sdnc urls
        self.sdnc_ip_addr = 'sdnc.onap'
        self.sdnc_preloading_port = '8282'
        self.sdnc_endpoint = 'http://' + self.sdnc_ip_addr + ':' + self.sdnc_preloading_port
        self.sdnc_preload_vnf_url = '/restconf/operations/VNF-API:preload-vnf-topology-operation'
        # properties
        self.homing_solution = 'sniro'  # value is either 'sniro' or 'oof'
        self.customer_location_used_by_oof = {
            "customerLatitude": "32.897480",
            "customerLongitude": "-97.040443",
            "customerName": "some_company"
        }
        self.product_family_id = 'f9457e8c-4afd-45da-9389-46acd9bf5116'
        self.custom_product_family_id = 'a9a77d5a-123e-4ca2-9eb9-0b015d2ee0fb'
        self.instance_name_prefix = {
            'service': 'svc',
            'network': 'net',
            'vnf': 'vnf',
            'vfmodule': 'vf'
        }

        # set the openstack cloud access credentials here
        self.cloud = {
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

        self.template_path = 'robot/assets/templates'
        self.pub_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKXDgoo3+WOqcUG8/5uUbk81+yczgwC4Y8ywTmuQqbNxlY1oQ0YxdMUqUnhitSXs5S/yRuAVOYHwGg2mCs20oAINrP+mxBI544AMIb9itPjCtgqtE2EWo6MmnFGbHB4Sx3XioE7F4VPsh7japsIwzOjbrQe+Mua1TGQ5d4nfEOQaaglXLLPFfuc7WbhbJbK6Q7rHqZfRcOwAMXgDoBqlyqKeiKwnumddo2RyNT8ljYmvB6buz7KnMinzo7qB0uktVT05FH9Rg0CTWH5norlG5qXgP2aukL0gk1ph8iAt7uYLf1ktp+LJI2gaF6L0/qli9EmVCSLr1uJ38Q8CBflhkh'
        self.owning_entity_name = 'OE-Demonstration1'
        self.project_name = 'Project-Demonstration'
        self.owning_entity_id = '520cc603-a3c4-4ec2-9ef4-ca70facd79c0'
        self.global_subscriber_id = 'Demonstration'
        self.vgw_VfModuleModelInvariantUuid = '26d6a718-17b2-4ba8-8691-c44343b2ecd2'

    def submit_create_req(self, req_json, req_type, service_instance_id=None, vnf_instance_id=None):
        """
        POST	{serverRoot}/serviceInstances/v4
        POST	{serverRoot}/serviceInstances/v4/{serviceInstanceId}/vnfs
        POST	{serverRoot}/serviceInstances/v4/{serviceInstanceId}/networks
        POST	{serverRoot}/serviceInstances/v4/{serviceInstanceId}/vnfs/{vnfInstanceId}/vfModules
        :param req_json:
        :param service_instance_id:  this is required only for networks, vnfs, and vf modules
        :param req_type:
        :param vnf_instance_id:
        :return: req_id, instance_id
        """
        if req_type == 'service':
            url = self.service_req_api_url
        elif req_type == 'vnf':
            url = '/'.join([self.service_req_api_url, service_instance_id, 'vnfs'])
        elif req_type == 'network':
            url = '/'.join([self.service_req_api_url, service_instance_id, 'networks'])
        elif req_type == 'vfmodule':
            url = '/'.join([self.service_req_api_url, service_instance_id, 'vnfs', vnf_instance_id, 'vfModules'])
        else:
            self.logger.error('Invalid request type: {0}. Can only be service/vnf/network/vfmodule'.format(req_type))
            return None, None

        self.logger.info(url)
        r = requests.post(url, headers=self.so_headers, auth=self.so_userpass, json=req_json)
        self.logger.debug(r)
        response = r.json()

        self.logger.debug('---------------------------------------------------------------')
        self.logger.debug('------- Creation request submitted to SO, got response --------')
        self.logger.debug(json.dumps(response, indent=4, sort_keys=True))
        self.logger.debug('---------------------------------------------------------------')
        req_id = response.get('requestReferences', {}).get('requestId', '')
        instance_id = response.get('requestReferences', {}).get('instanceId', '')

        return req_id, instance_id

    def check_progress(self, req_id, interval=5):
        if not req_id:
            self.logger.error('Error when checking SO request progress, invalid request ID: ' + req_id)
            return False
        duration = 0.0
        url = self.so_check_progress_api_url + '/' + req_id

        while True:
            time.sleep(interval)
            r = requests.get(url, headers=self.so_headers, auth=self.so_userpass)
            response = r.json()

            duration += interval

            if response['request']['requestStatus']['requestState'] == 'IN_PROGRESS':
                self.logger.debug('------------------Request Status-------------------------------')
                self.logger.debug(json.dumps(response, indent=4, sort_keys=True))
            else:
                self.logger.debug('---------------------------------------------------------------')
                self.logger.debug('----------------- Creation Request Results --------------------')
                self.logger.debug(json.dumps(response, indent=4, sort_keys=True))
                self.logger.debug('---------------------------------------------------------------')
                flag = response['request']['requestStatus']['requestState'] == 'COMPLETE'
                if not flag:
                    self.logger.error('Request failed.')
                    self.logger.error(json.dumps(response, indent=4, sort_keys=True))
                return flag

    @staticmethod
    def add_req_info(req_details, instance_name, product_family_id=None):
        req_details['requestInfo'] = {
                    'instanceName': instance_name,
                    'source': 'VID',
                    'suppressRollback': 'true',
                    'requestorId': 'vCPE-Robot'
        }
        if product_family_id:
            req_details['requestInfo']['productFamilyId'] = product_family_id

    @staticmethod
    def add_related_instance(req_details, instance_id, instance_model):
        instance = {"instanceId": instance_id, "modelInfo": instance_model}
        if 'relatedInstanceList' not in req_details:
            req_details['relatedInstanceList'] = [{"relatedInstance": instance}]
        else:
            req_details['relatedInstanceList'].append({"relatedInstance": instance})

    def generate_vnf_or_network_request(self, instance_name, vnf_or_network_model, service_instance_id, service_model):
        req_details = {
            'modelInfo':  vnf_or_network_model,
            'cloudConfiguration': {"lcpCloudRegionId": self.region_name,
                                   "tenantId": self.tenant_id},
            'requestParameters':  {"userParams": []},
            'platform': {"platformName": "Platform-Demonstration"}
        }
        self.add_req_info(req_details, instance_name, self.product_family_id)
        self.add_related_instance(req_details, service_instance_id, service_model)
        return {'requestDetails': req_details}

    def generate_vfmodule_request(self, instance_name, vfmodule_model, service_instance_id,
                                  service_model, vnf_instance_id, vnf_model):
        req_details = {
            'modelInfo':  vfmodule_model,
            'cloudConfiguration': {"lcpCloudRegionId": self.region_name,
                                   "tenantId": self.tenant_id},
            'requestParameters': {"usePreload": 'true'}
        }
        self.add_req_info(req_details, instance_name, self.product_family_id)
        self.add_related_instance(req_details, service_instance_id, service_model)
        self.add_related_instance(req_details, vnf_instance_id, vnf_model)
        return {'requestDetails': req_details}

    def generate_service_request(self, instance_name, model):
        req_details = {
            'modelInfo':  model,
            'subscriberInfo':  {'globalSubscriberId': self.global_subscriber_id},
            'requestParameters': {
                "userParams": [],
                "subscriptionServiceType": "vCPE",
                "aLaCarte": 'true'
            }
        }
        self.add_req_info(req_details, instance_name)
        self.add_project_info(req_details)
        self.add_owning_entity(req_details)
        return {'requestDetails': req_details}

    def add_project_info(self, req_details):
        req_details['project'] = {'projectName': self.project_name}

    def add_owning_entity(self, req_details):
        req_details['owningEntity'] = {'owningEntityId': self.owning_entity_id,
                                       'owningEntityName': self.owning_entity_name}

    def generate_custom_service_request(self, instance_name, model, brg_mac):
        brg_mac_enc = brg_mac.replace(':', '-')
        req_details = {
            'modelInfo':  model,
            'subscriberInfo':  {'subscriberName': 'Kaneohe',
                                'globalSubscriberId': self.global_subscriber_id},
            'cloudConfiguration': {"lcpCloudRegionId": self.region_name,
                                   "tenantId": self.tenant_id},
            'requestParameters': {
                "userParams": [
                    {
                        'name': 'BRG_WAN_MAC_Address',
                        'value': brg_mac
                    },
                    {
                       'name': 'VfModuleNames',
                       'value': [
                            {
                                'VfModuleModelInvariantUuid': self.vgw_VfModuleModelInvariantUuid,
                                'VfModuleName': 'VGW2BRG-{0}'.format(brg_mac_enc)
                            }
                       ]
                    },
                    {
                         "name": "Customer_Location",
                         "value": self.customer_location_used_by_oof
                    },
                    {
                         "name": "Homing_Solution",
                         "value": self.homing_solution
                    }
                ],
                "subscriptionServiceType": "vCPE",
                'aLaCarte': 'false'
            }
        }
        self.add_req_info(req_details, instance_name, self.custom_product_family_id)
        self.add_project_info(req_details)
        self.add_owning_entity(req_details)
        return {'requestDetails': req_details}

    def create_custom_service(self, csar_file, brg_mac, name_suffix=None):
        parser = CsarParser()
        if not parser.parse_csar(csar_file):
            return False

        # yyyymmdd_hhmm
        if not name_suffix:
            name_suffix = '_' + datetime.now().strftime('%Y%m%d%H%M')

        # create service
        instance_name = '_'.join([self.instance_name_prefix['service'],
                                  parser.svc_model['modelName'][0:10], name_suffix])
        instance_name = instance_name.lower()
        req = self.generate_custom_service_request(instance_name, parser.svc_model, brg_mac)
        self.logger.info(json.dumps(req, indent=2, sort_keys=True))
        self.logger.info('Creating custom service {0}.'.format(instance_name))
        req_id, svc_instance_id = self.submit_create_req(req, 'service')
        if not self.check_progress(req_id):
            return False
        return True

    def wait_for_aai(self, node_type, uuid):
        self.logger.info('Waiting for AAI traversal to complete...')
        for i in range(30):
            time.sleep(1)
            if self.is_node_in_aai(node_type, uuid):
                return

        self.logger.error("AAI traversal didn't finish in 30 seconds. Something is wrong. Type {0}, UUID {1}".format(
            node_type, uuid))
        sys.exit()

    def create_entire_service(self, csar_file, vnf_template_file, preload_dict, name_suffix, region_name, tenant_id):
        """
        :param csar_file:
        :param vnf_template_file:
        :param preload_dict:
        :param name_suffix:
        :param region_name:
        :param tenant_id
        :return:  service instance UUID
        """
        self.region_name = region_name
        self.tenant_id = tenant_id
        self.logger.info('\n----------------------------------------------------------------------------------')
        self.logger.info('Start to create entire service defined in csar: {0}'.format(csar_file))
        parser = CsarParser()
        self.logger.info('Parsing csar ...')
        if not parser.parse_csar(csar_file):
            self.logger.error('Cannot parse csar: {0}'.format(csar_file))
            return None

        # Set Global timestamp for instancenames
        global_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # create service
        instance_name = '_'.join([self.instance_name_prefix['service'],
                                  parser.svc_model['modelName'], global_timestamp, name_suffix])
        instance_name = instance_name.lower()
        instance_name = instance_name.replace(' ', '')
        instance_name = instance_name.replace(':', '')
        self.logger.info('Creating service instance: {0}.'.format(instance_name))
        req = self.generate_service_request(instance_name, parser.svc_model)
        self.logger.debug(json.dumps(req, indent=2, sort_keys=True))
        req_id, svc_instance_id = self.submit_create_req(req, 'service')
        if not self.check_progress(req_id, interval=5):
            return None

        # wait for AAI to complete traversal
        self.wait_for_aai('service', svc_instance_id)

        # create networks
        for model in parser.net_models:
            base_name = model['modelCustomizationName'].lower().replace('mux_vg', 'mux_gw')
            network_name = '_'.join([self.instance_name_prefix['network'], base_name, name_suffix])
            network_name = network_name.lower()
            self.logger.info('Creating network: ' + network_name)
            req = self.generate_vnf_or_network_request(network_name, model, svc_instance_id, parser.svc_model)
            self.logger.debug(json.dumps(req, indent=2, sort_keys=True))
            req_id, net_instance_id = self.submit_create_req(req, 'network', svc_instance_id)
            if not self.check_progress(req_id):
                return None

            self.logger.info('Changing subnet name to ' + self.network_name_to_subnet_name(network_name))
            self.set_network_name(network_name)
            subnet_name_changed = False
            for i in range(20):
                time.sleep(3)
                if self.set_subnet_name(network_name):
                    subnet_name_changed = True
                    break

            if not subnet_name_changed:
                self.logger.error('Failed to change subnet name for ' + network_name)
                return None

        vnf_model = None
        vnf_instance_id = None
        # create VNF
        if len(parser.vnf_models) == 1:
            vnf_model = parser.vnf_models[0]
            vnf_instance_name = '_'.join([self.instance_name_prefix['vnf'],
                                          vnf_model['modelCustomizationName'].split(' ')[0],  name_suffix])
            vnf_instance_name = vnf_instance_name.lower()
            vnf_instance_name = vnf_instance_name.replace(' ', '')
            vnf_instance_name = vnf_instance_name.replace(':', '')
            self.logger.info('Creating VNF: ' + vnf_instance_name)
            req = self.generate_vnf_or_network_request(vnf_instance_name, vnf_model, svc_instance_id, parser.svc_model)
            self.logger.debug(json.dumps(req, indent=2, sort_keys=True))
            req_id, vnf_instance_id = self.submit_create_req(req, 'vnf', svc_instance_id)
            if not self.check_progress(req_id, interval=5):
                self.logger.error('Failed to create VNF {0}.'.format(vnf_instance_name))
                return False

            # wait for AAI to complete traversal
            if not vnf_instance_id:
                self.logger.error('No VNF instance ID returned!')
                sys.exit()
            self.wait_for_aai('vnf', vnf_instance_id)

        # SDNC Preload 
        preloader = PreloadSDNCKeywords()
        vfmodule_name = '_'.join(['vf',
                                  parser.vfmodule_models[0]['modelCustomizationName'].split('..')[0].lower(),
                                  name_suffix])

        extra_preload = {
            'pub_key': self.pub_key,
            'vnf_type': parser.vfmodule_models[0]['modelCustomizationName'],
            'generic_vnf_type': parser.vfmodule_models[0]['modelCustomizationName'],
            'service_type': svc_instance_id,
            'generic_vnf_name': vnf_model['modelCustomizationName'],
            'vnf_name': vfmodule_name,
            'mr_ip_addr': self.mr_ip_addr,
            'mr_ip_port': self.mr_ip_port,
            'sdnc_oam_ip': self.sdnc_ip_addr,
            'suffix': name_suffix,
            'oam_onap_net': 'oam_network_2No2',
            'oam_onap_subnet': 'oam_network_2No2',
            'public_net': 'external',
            'public_net_id': '971040b2-7059-49dc-b220-4fab50cb2ad4'
        }

        preload_dict.update(extra_preload)
        preloader.preload_vfmodule(self.sdnc_endpoint, self.sdnc_preload_vnf_url, self.template_path, vnf_template_file,
                                   preload_dict)

        # create VF Module
        if len(parser.vfmodule_models) == 1:
            if not vnf_instance_id or not vnf_model:
                self.logger.error('Invalid VNF instance ID or VNF model!')
                sys.exit()

            model = parser.vfmodule_models[0]
            vfmodule_instance_name = '_'.join([self.instance_name_prefix['vfmodule'],
                                               model['modelCustomizationName'].split('..')[0], name_suffix])
            vfmodule_instance_name = vfmodule_instance_name.lower()
            vfmodule_instance_name = vfmodule_instance_name.replace(' ', '')
            vfmodule_instance_name = vfmodule_instance_name.replace(':', '')
            self.logger.info('Creating VF Module: ' + vfmodule_instance_name)
            req = self.generate_vfmodule_request(vfmodule_instance_name, model, svc_instance_id, parser.svc_model,
                                                 vnf_instance_id, vnf_model)
            self.logger.debug(json.dumps(req, indent=2, sort_keys=True))
            req_id, vfmodule_instance_id = self.submit_create_req(req, 'vfmodule', svc_instance_id, vnf_instance_id)
            if not self.check_progress(req_id, interval=50):
                self.logger.error('Failed to create VF Module {0}.'.format(vfmodule_instance_name))
                return None

        return svc_instance_id

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
            self.aai_host, self.aai_query_port, search_node_type, key, node_uuid)

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-FromAppID': 'vCPE-Robot', 'X-TransactionId': 'get_aai_subscr'}
        urllib3.disable_warnings()
        r = requests.get(url, headers=headers, auth=self.aai_userpass, verify=False)
        response = r.json()
        self.logger.debug('aai query: ' + url)
        self.logger.debug('aai response:\n' + json.dumps(response, indent=4, sort_keys=True))
        return 'result-data' in response

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

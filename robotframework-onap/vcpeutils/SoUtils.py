#! /usr/bin/python

import time

from vcpeutils.preload import *
from vcpeutils.vcpecommon import *

from robot.api import logger
from ONAPLibrary.RequestSOKeywords import RequestSOKeywords


class SoUtils:

    def __init__(self):
        self.region_name = None  # set later
        self.tenant_id = None  # set later
        self.logger = logger
        self.vcpecommon = VcpeCommon()
        self.api_version = 'v4'
        self.service_req_api_url = self.vcpecommon.so_req_api_url[self.api_version]
        self.request_keywords = RequestSOKeywords()

    def check_progress(self, req_id, interval=5):
        if not req_id:
            self.logger.error('Error when checking SO request progress, invalid request ID: ' + req_id)
            return False

        response = self.request_keywords.run_polling_get_request(
            self.vcpecommon.so_check_progress_api_url, '/' + req_id,
            auth=self.vcpecommon.so_userpass, tries=500, interval=interval)
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
        self.add_req_info(req_details, instance_name, self.vcpecommon.product_family_id)
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
        self.add_req_info(req_details, instance_name, self.vcpecommon.product_family_id)
        self.add_related_instance(req_details, service_instance_id, service_model)
        self.add_related_instance(req_details, vnf_instance_id, vnf_model)
        return {'requestDetails': req_details}

    def generate_service_request(self, instance_name, model):
        req_details = {
            'modelInfo':  model,
            'subscriberInfo':  {'globalSubscriberId': self.vcpecommon.global_subscriber_id},
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
        req_details['project'] = {'projectName': self.vcpecommon.project_name}

    def add_owning_entity(self, req_details):
        req_details['owningEntity'] = {'owningEntityId': self.vcpecommon.owning_entity_id,
                                       'owningEntityName': self.vcpecommon.owning_entity_name}

    def generate_custom_service_request(self, instance_name, model, brg_mac):
        brg_mac_enc = brg_mac.replace(':', '-')
        req_details = {
            'modelInfo':  model,
            'subscriberInfo':  {'subscriberName': 'Kaneohe',
                                'globalSubscriberId': self.vcpecommon.global_subscriber_id},
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
                                'VfModuleModelInvariantUuid': self.vcpecommon.vgw_VfModuleModelInvariantUuid,
                                'VfModuleName': 'VGW2BRG-{0}'.format(brg_mac_enc)
                            }
                       ]
                    },
                    {
                         "name": "Customer_Location",
                         "value": self.vcpecommon.customer_location_used_by_oof
                    },
                    {
                         "name": "Homing_Solution",
                         "value": self.vcpecommon.homing_solution
                    }
                ],
                "subscriptionServiceType": "vCPE",
                'aLaCarte': 'false'
            }
        }
        self.add_req_info(req_details, instance_name, self.vcpecommon.custom_product_family_id)
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
        instance_name = '_'.join([self.vcpecommon.instance_name_prefix['service'],
                                  parser.svc_model['modelName'][0:10], name_suffix])
        instance_name = instance_name.lower()
        req = self.generate_custom_service_request(instance_name, parser.svc_model, brg_mac)
        self.logger.info(json.dumps(req, indent=2, sort_keys=True))
        self.logger.info('Creating custom service {0}.'.format(instance_name))
        req_id, svc_instance_id = self.request_keywords.run_create_request(
            self.service_req_api_url, "/", req, auth=self.vcpecommon.so_userpass)
        if not self.check_progress(req_id):
            return False
        return True

    def wait_for_aai(self, node_type, uuid):
        self.logger.info('Waiting for AAI traversal to complete...')
        for i in range(30):
            time.sleep(1)
            if self.vcpecommon.is_node_in_aai(node_type, uuid):
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
        instance_name = '_'.join([self.vcpecommon.instance_name_prefix['service'],
                                  parser.svc_model['modelName'], global_timestamp, name_suffix])
        instance_name = instance_name.lower()
        instance_name = instance_name.replace(' ', '')
        instance_name = instance_name.replace(':', '')
        self.logger.info('Creating service instance: {0}.'.format(instance_name))
        req = self.generate_service_request(instance_name, parser.svc_model)
        self.logger.debug(json.dumps(req, indent=2, sort_keys=True))
        req_id, svc_instance_id = self.request_keywords.run_create_request(
            self.service_req_api_url, "/", req, auth=self.vcpecommon.so_userpass)
        if not self.check_progress(req_id, interval=5):
            return None

        # wait for AAI to complete traversal
        self.wait_for_aai('service', svc_instance_id)

        # create networks
        for model in parser.net_models:
            base_name = model['modelCustomizationName'].lower().replace('mux_vg', 'mux_gw')
            network_name = '_'.join([self.vcpecommon.instance_name_prefix['network'], base_name, name_suffix])
            network_name = network_name.lower()
            self.logger.info('Creating network: ' + network_name)
            req = self.generate_vnf_or_network_request(network_name, model, svc_instance_id, parser.svc_model)
            self.logger.debug(json.dumps(req, indent=2, sort_keys=True))
            req_id, net_instance_id = self.request_keywords.run_create_request(
                self.service_req_api_url, '/'.join([svc_instance_id, 'networks']), req,
                auth=self.vcpecommon.so_userpass)
            if not self.check_progress(req_id):
                return None

            self.logger.info('Changing subnet name to ' + self.vcpecommon.network_name_to_subnet_name(network_name))
            self.vcpecommon.set_network_name(network_name)
            subnet_name_changed = False
            for i in range(20):
                time.sleep(3)
                if self.vcpecommon.set_subnet_name(network_name):
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
            vnf_instance_name = '_'.join([self.vcpecommon.instance_name_prefix['vnf'],
                                          vnf_model['modelCustomizationName'].split(' ')[0],  name_suffix])
            vnf_instance_name = vnf_instance_name.lower()
            vnf_instance_name = vnf_instance_name.replace(' ', '')
            vnf_instance_name = vnf_instance_name.replace(':', '')
            self.logger.info('Creating VNF: ' + vnf_instance_name)
            req = self.generate_vnf_or_network_request(vnf_instance_name, vnf_model, svc_instance_id, parser.svc_model)
            self.logger.debug(json.dumps(req, indent=2, sort_keys=True))
            req_id, vnf_instance_id = self.request_keywords.run_create_request(
                self.service_req_api_url, '/'.join([svc_instance_id, 'vnfs']), req,
                auth=self.vcpecommon.so_userpass)
            if not self.check_progress(req_id, interval=5):
                self.logger.error('Failed to create VNF {0}.'.format(vnf_instance_name))
                return False

            # wait for AAI to complete traversal
            if not vnf_instance_id:
                self.logger.error('No VNF instance ID returned!')
                sys.exit()
            self.wait_for_aai('vnf', vnf_instance_id)

        # SDNC Preload 

        preloader = Preload(self.vcpecommon)
        preloader.preload_vfmodule(vnf_template_file, svc_instance_id, parser.vnf_models[0], parser.vfmodule_models[0],
                                   preload_dict, name_suffix)

        # create VF Module
        if len(parser.vfmodule_models) == 1:
            if not vnf_instance_id or not vnf_model:
                self.logger.error('Invalid VNF instance ID or VNF model!')
                sys.exit()

            model = parser.vfmodule_models[0]
            vfmodule_instance_name = '_'.join([self.vcpecommon.instance_name_prefix['vfmodule'],
                                               model['modelCustomizationName'].split('..')[0], name_suffix])
            vfmodule_instance_name = vfmodule_instance_name.lower()
            vfmodule_instance_name = vfmodule_instance_name.replace(' ', '')
            vfmodule_instance_name = vfmodule_instance_name.replace(':', '')
            self.logger.info('Creating VF Module: ' + vfmodule_instance_name)
            req = self.generate_vfmodule_request(vfmodule_instance_name, model, svc_instance_id, parser.svc_model,
                                                 vnf_instance_id, vnf_model)
            self.logger.debug(json.dumps(req, indent=2, sort_keys=True))
            req_id, vfmodule_instance_id = self.request_keywords.run_create_request(
                self.service_req_api_url, '/'.join([svc_instance_id, 'vnfs', vnf_instance_id, 'vfModules']),
                req, auth=self.vcpecommon.so_userpass)
            if not self.check_progress(req_id, interval=50):
                self.logger.error('Failed to create VF Module {0}.'.format(vfmodule_instance_name))
                return None

        return svc_instance_id

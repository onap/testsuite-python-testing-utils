#! /usr/bin/python

from vcpeutils.csar_parser import *
from robot.api import logger
from past import builtins
import requests


class Preload:
    def __init__(self, vcpecommon):
        self.vcpecommon = vcpecommon

    def replace(self, sz, replace_dict):
        for old_string, new_string in list(replace_dict.items()):
            sz = sz.replace(old_string, new_string)
        if self.vcpecommon.template_variable_symbol in sz:
            logger.error('Error! Cannot find a value to replace ' + sz)
        return sz

    def generate_json(self, template_file, replace_dict):
        with open(template_file) as json_input:
            json_data = json.load(json_input)
            stk = [json_data]
            while len(stk) > 0:
                data = stk.pop()
                for k, v in list(data.items()):
                    if type(v) is dict:
                        stk.append(v)
                    elif type(v) is list:
                        stk.extend(v)
                    elif type(v) is builtins.basestring:
                        if self.vcpecommon.template_variable_symbol in v:
                            data[k] = self.replace(v, replace_dict)
                    else:
                        logger.warn('Unexpected line in template: {}. Look for value {}'.format(template_file, v))
        return json_data

    def preload_network(self, template_file, network_role, subnet_start_ip, subnet_gateway, common_dict, name_suffix):
        """
        :param template_file:
        :param network_role: cpe_signal, cpe_public, brg_bng, bng_mux, mux_gw
        :param subnet_start_ip:
        :param subnet_gateway:
        :param common_dict:
        :param name_suffix: e.g. '201711201311'
        :return:
        """
        network_name = '_'.join([self.vcpecommon.instance_name_prefix['network'], network_role.lower(), name_suffix])
        subnet_name = self.vcpecommon.network_name_to_subnet_name(network_name)
        common_dict['${' + network_role+'_net}'] = network_name
        common_dict['${' + network_role+'_subnet}'] = subnet_name
        replace_dict = {'${network_role}': network_role,
                        '${service_type}': 'vCPE',
                        '${network_type}': 'Generic NeutronNet',
                        '${network_name}': network_name,
                        '${subnet_start_ip}': subnet_start_ip,
                        '${subnet_gateway}': subnet_gateway
                        }
        logger.info('Preloading network ' + network_role)
        return self.preload(template_file, replace_dict, self.vcpecommon.sdnc_preload_network_url)

    def preload(self, template_file, replace_dict, url):
        logger.debug(json.dumps(replace_dict, indent=4, sort_keys=True))
        json_data = self.generate_json(template_file, replace_dict)
        logger.debug(json.dumps(json_data, indent=4, sort_keys=True))
        r = requests.post(url, headers=self.vcpecommon.sdnc_headers, auth=self.vcpecommon.sdnc_userpass, json=json_data)
        response = r.json()
        if int(response.get('output', {}).get('response-code', 0)) != 200:
            logger.debug(json.dumps(response, indent=4, sort_keys=True))
            logger.error('Preloading failed.')
            return False
        return True

    def preload_vgw(self, template_file, brg_mac, commont_dict, name_suffix):
        replace_dict = {'${brg_mac}': brg_mac,
                        '${suffix}': name_suffix
                        }
        replace_dict.update(commont_dict)
        logger.info('Preloading vGW')
        return self.preload(template_file, replace_dict, self.vcpecommon.sdnc_preload_vnf_url)

    def preload_vgw_gra(self, template_file, brg_mac, commont_dict, name_suffix, vgw_vfmod_name_index):
        replace_dict = {'${brg_mac}': brg_mac,
                        '${suffix}': name_suffix,
                        '${vgw_vfmod_name_index}': vgw_vfmod_name_index
                        }
        replace_dict.update(commont_dict)
        logger.info('Preloading vGW-GRA')
        return self.preload(template_file, replace_dict, self.vcpecommon.sdnc_preload_gra_url)

    def preload_vfmodule(self, template_file, service_instance_id, vnf_model, vfmodule_model, common_dict, name_suffix):
        """
        :param template_file:
        :param service_instance_id:
        :param vnf_model:  parsing results from csar_parser
        :param vfmodule_model:  parsing results from csar_parser
        :param common_dict:
        :param name_suffix:
        :return:
        """

        # examples:
        # vfmodule_model['modelCustomizationName']: "Vspinfra111601..base_vcpe_infra..module-0",
        # vnf_model['modelCustomizationName']: "vspinfra111601 0",

        vfmodule_name = '_'.join([self.vcpecommon.instance_name_prefix['vfmodule'],
                                  vfmodule_model['modelCustomizationName'].split('..')[0].lower(), name_suffix])

        # vnf_type and generic_vnf_type are identical
        replace_dict = {'${vnf_type}': vfmodule_model['modelCustomizationName'],
                        '${generic_vnf_type}': vfmodule_model['modelCustomizationName'],
                        '${service_type}': service_instance_id,
                        '${generic_vnf_name}': vnf_model['modelCustomizationName'],
                        '${vnf_name}': vfmodule_name,
                        '${mr_ip_addr}': self.vcpecommon.mr_ip_addr,
                        '${mr_ip_port}': self.vcpecommon.mr_ip_port,
                        '${sdnc_oam_ip}': self.vcpecommon.sdnc_oam_ip,
                        '${suffix}': name_suffix}
        replace_dict.update(common_dict)
        logger.info('Preloading VF Module ' + vfmodule_name)
        return self.preload(template_file, replace_dict, self.vcpecommon.sdnc_preload_vnf_url)

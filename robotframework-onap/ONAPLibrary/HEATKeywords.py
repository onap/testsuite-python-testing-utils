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

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import json
import yaml
import io
import copy
from hashlib import md5
from paramiko import RSAKey
from paramiko.ssh_exception import PasswordRequiredException

from ONAPLibrary.Utilities import Utilities


class HEATKeywords(object):
    """Utilities useful for constructing OpenStack HEAT requests. """

    def __init__(self):
        super(HEATKeywords, self).__init__()
        self.application_id = "robot-ete"
        self.uuid = Utilities()
        self.builtin = BuiltIn()

    @keyword
    def get_yaml(self, template_file):
        """Template Yaml To Json reads a YAML Heat template file returns a JSON string that can be used included
        in an Openstack Add Stack Request"""
        if isinstance(template_file, str) or isinstance(template_file, unicode):
            fin = open(template_file, 'r')
            yamlobj = yaml.load(fin)
            return yamlobj
        return None

    @keyword
    def template_yaml_to_json(self, template_file):
        """Template Yaml To Json reads a YAML Heat template file returns a JSON string that can be used included
        in an Openstack Add Stack Request"""
        contents = None
        if isinstance(template_file, str) or isinstance(template_file, unicode):
            fin = open(template_file, 'r')
            yamlobj = yaml.load(fin)
            fin.close()
            if 'heat_template_version' in yamlobj:
                datetime = yamlobj['heat_template_version']
                yamlobj['heat_template_version'] = str(datetime)
            fout = io.BytesIO()
            json.dump(yamlobj, fout)
            contents = fout.getvalue()
            fout.close()
        return contents

    @keyword
    def env_yaml_to_json(self, template_file):
        """Env Yaml To JSon reads a YAML Heat env file and returns a JSON string that can be used included
        in an Openstack Add Stack Request"""
        if isinstance(template_file, str) or isinstance(template_file, unicode):
            fin = open(template_file, 'r')
            yamlobj = yaml.load(fin)
            fin.close()
            if 'parameters' in yamlobj:
                fout = io.BytesIO()
                json.dump(yamlobj['parameters'], fout)
                contents = fout.getvalue()
                fout.close()
                return contents
        return None

    @keyword
    def stack_info_parse(self, stack_info):
        """ returns a flattened version of the Openstack Find Stack results """
        d = {}
        if isinstance(stack_info, dict):
            s = stack_info['stack']
            p = s['parameters']
            d = copy.deepcopy(p)
            d['id'] = s['id']
            d['name'] = s['stack_name']
            d['stack_status'] = s['stack_status']
        return d

    @keyword
    def match_fingerprint(self, pvt_file, pw, fingerprint):
        try:
            ssh_key = RSAKey.from_private_key_file(pvt_file, pw)
            keybytes = md5(ssh_key.asbytes()).hexdigest()
            printable_fingerprint = ':'.join(a + b for a, b in zip(keybytes[::2], keybytes[1::2]))
            return printable_fingerprint == fingerprint.__str__()
        except PasswordRequiredException:
            return False

    @keyword
    def match_private_key_file_to_keypair(self, files, keypair):
        for keyfile in files:
            if self.match_fingerprint(keyfile, None, keypair['keypair']['fingerprint']):
                return keyfile
        return None

    @keyword
    def get_openstack_server_ip(self, server, network_name="public", ipversion=4):
        ipaddr = None
        try:
            versions = server['addresses'][network_name]
            for version in versions:
                if version['version'] == ipversion:
                    ipaddr = version['addr']
                    break
        except ValueError:
            return ipaddr
        return ipaddr

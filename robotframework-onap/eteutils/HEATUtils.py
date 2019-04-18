import json
import yaml
import StringIO
import copy
from hashlib import md5
from paramiko import RSAKey
from paramiko.ssh_exception import PasswordRequiredException

class HEATUtils:
    """ Utilities useful for constructing OpenStack HEAT requests """

    def get_yaml(self, template_file):
        """Template Yaml To Json reads a YAML Heat template file returns a JSON string that can be used included in an Openstack Add Stack Request"""
        if isinstance(template_file, basestring):
            fin = open(template_file, 'r')
            yamlobj = yaml.load(fin)
            return yamlobj
        return None
    
    def template_yaml_to_json(self, template_file):
        """Template Yaml To Json reads a YAML Heat template file returns a JSON string that can be used included in an Openstack Add Stack Request"""
        if isinstance(template_file, basestring):
            fin = open(template_file, 'r')
            yamlobj = yaml.load(fin)
            fin.close()
            if 'heat_template_version' in yamlobj:
                datetime = yamlobj['heat_template_version']
                yamlobj['heat_template_version'] = str(datetime)
            fout = StringIO.StringIO()
            json.dump(yamlobj, fout)
            contents = fout.getvalue()
            fout.close()
        return contents
    
    def env_yaml_to_json(self, template_file):
        """Env Yaml To JSon reads a YAML Heat env file and returns a JSON string that can be used included in an Openstack Add Stack Request"""
        if isinstance(template_file, basestring):
            fin = open(template_file, 'r')
            yamlobj = yaml.load(fin)
            fin.close()
            if 'parameters' in yamlobj:
                fout = StringIO.StringIO()
                json.dump(yamlobj['parameters'], fout)
                contents = fout.getvalue()
                fout.close()
                return contents
        return None
    
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
    
    
    def match_fingerprint(self, pvt_file, pw, fingerprint):
        try:
            sshKey = RSAKey.from_private_key_file(pvt_file, pw)
            keybytes = md5(sshKey.asbytes()).hexdigest()
            printableFingerprint = ':'.join(a+b for a,b in zip(keybytes[::2], keybytes[1::2]))
            return printableFingerprint == fingerprint.__str__()
        except PasswordRequiredException:
            return False    
    
    def match_private_key_file_to_keypair(self, files, keypair):
        for keyfile in files:
            if (self.match_fingerprint(keyfile, None, keypair['keypair']['fingerprint'])):
                return keyfile
        return None
    
    def get_openstack_server_ip(self, server, network_name="public", ipversion=4):
        ipaddr = None
        try:
            versions = server['addresses'][network_name]
            for version in versions:
                if version['version'] == ipversion:
                    ipaddr = version['addr']
                    break;
        except ValueError:
            return ipaddr
        return ipaddr
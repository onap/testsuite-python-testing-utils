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

import json
import yaml
import requests

stack_url = "{}/stacks/{}"
stack_resources_url = "{}/stacks/{}/resources"


# use this to import and run validation from robot
class HeatStackValidation:
    def __init__(self):
        pass

    @keyword
    def validate(self, orchestration_url, token, manifest):
        validator = StackValidation(orchestration_url, token, manifest)
        validator.create_summary()
        validator.validate_summary()

        return validator.report


class StackValidation:
    def __init__(self, orchestration_url, token, manifest):
        """retrieves stack and template details, and creates
        a report for submission to OVP portal.

        :orchestration_url:          heat service endpoint in openstack
        :token:                      keystone auth token
        :manifest:                   json that contains list of heat templates, env,
                                     preloads, and stack names for each module in
                                     a VNF
        """
        self.modules = []
        self.url = orchestration_url
        self.token = token
        self.manifest = manifest
        self.vnf_name = ""
        self.report = {}

        self.load_manifest()

    def load_manifest(self):
        with open(self.manifest, "r") as f:
            jdata = json.loads(f.read())

        self.vnf_name = jdata.get("VNF_Name")

        for entry in jdata.get("stacks"):
            module = HeatModule(
                entry.get("template_name"),
                entry.get("env_name"),
                entry.get("stack_name"),
                entry.get("preload_name"),
            )
            module.get_data(self.url, self.token)
            self.modules.append(module)

    def create_summary(self):
        """creates a report dictionary to compare stack
        resources, parameters, outputs w/ template"""
        self.report["modules"] = []
        self.report["VNF Name"] = self.vnf_name
        for module in self.modules:
            stack = module.stack
            preload = module.preload
            template = module.template

            module_report = {}
            module_report["stack_details"] = stack.stack_details

            module_report["resources"] = {}
            module_report["resources"]["summary"] = ""

            module_report["parameters"] = {}
            module_report["parameters"]["summary"] = ""

            module_report["outputs"] = {}
            module_report["outputs"]["summary"] = ""

            module_report["resources"]["stack_resources"] = stack.resources
            module_report["resources"]["template_resources"] = template.resources

            module_report["parameters"]["stack_parameters"] = stack.parameters
            module_report["parameters"]["template_parameters"] = dict(template.parameters, **preload.parameters)

            module_report["outputs"]["stack_outputs"] = stack.outputs
            module_report["outputs"]["template_outputs"] = template.outputs

            self.report["modules"].append(module_report)

    def validate_summary(self):
        # validates resources, parameters, and outputs
        self.validate_resources()
        self.validate_parameters()
        self.validate_outputs()

        self.report["summary"] = "SUCCESS"
        for module in self.report["modules"]:
            if module["resources"]["summary"] != "SUCCESS":
                self.report["summary"] = "FAILED"
                break
            if module["parameters"]["summary"] != "SUCCESS":
                self.report["summary"] = "FAILED"
                break
            if module["outputs"]["summary"] != "SUCCESS":
                self.report["summary"] = "FAILED"
                break

    def validate_resources(self):
        """validates that all resources from a heat template
        are present in instantiated heat stack"""
        report = self.report
        for module in report["modules"]:
            module["resources"]["summary"] = "SUCCESS"
            resources = module.get("resources", {})
            template_resources = resources.get("template_resources", [])
            stack_resources = resources.get("stack_resources", [])

            if len(stack_resources) != len(template_resources):
                module["resources"]["summary"] = "FAILED"
                continue

            stack_rids = []
            for s_resource in stack_resources:
                stack_rids.append(s_resource.get("resource_id"))

            template_rids = []
            for t_resource in template_resources:
                template_rids.append(t_resource.get("resource_id"))

            if stack_rids.sort() != template_rids.sort():
                module["resources"]["summary"] = "FAILED"
                continue

    def validate_parameters(self):
        """validates that parameter name/value from template
        == values from instantiated heat stack"""
        report = self.report
        for module in report["modules"]:
            module["parameters"]["summary"] = "SUCCESS"
            parameters = module.get("parameters", {})
            template_parameters = parameters.get("template_parameters", {})
            stack_parameters = parameters.get("stack_parameters", {})

            for parameter, parameter_value in template_parameters.items():
                stack_parameter = stack_parameters.get(parameter)
                if not stack_parameter:
                    module["parameters"]["summary"] = "FAILED"
                    break

                if stack_parameter != parameter_value:
                    module["parameters"]["summary"] = "FAILED"
                    break

    def validate_outputs(self):
        """validates that all outputs from a heat template
        are present in instantiated heat stack"""
        report = self.report
        for module in report["modules"]:
            module["outputs"]["summary"] = "SUCCESS"
            outputs = module.get("outputs", {})
            template_outputs = outputs.get("template_outputs", {})
            stack_outputs = outputs.get("stack_outputs", [])

            for output in stack_outputs:
                output_key = output.get("output_key")
                if output_key not in template_outputs:
                    module["outputs"]["summary"] = "FAILED"
                    break


class HeatModule:
    def __init__(self, heat_template, environment_file, stack_name, preload):
        """
        creates module object that has stack, preload, and template objects

        :heat_template:             /path/to/heat/template.yaml
        :environment_file:          /path/to/heat/env.env
        :preload:                   /path/to/preloads/file.json
        :stack_name:                name of heat stack in openstack
        """
        self.stack = HeatStack(stack_name)
        self.template = HeatTemplate(heat_template, environment_file)
        self.preload = HeatPreload(preload)

    def get_data(self, url, token):
        self.stack.get_data(url, token)
        self.template.get_data()
        self.preload.get_data()


class HeatTemplate:
    def __init__(self, heat_template, environment_file):
        """
        creates template object that holds template resources,
        parameters, and outputs of a heat template/env pair.

        :heat_template:             /path/to/heat/template.yaml
        :environment_file:          /path/to/heat/env.env
        """
        self.template = heat_template
        self.env = environment_file
        self.resources = []
        self.parameters = {}
        self.outputs = []

    def get_data(self):
        with open(self.template, "r") as f:
            ydata = yaml.safe_load(f)

        resources = ydata.get("resources", {})

        for rid, resource in resources.items():
            self.resources.append(
                {"resource_id": rid, "resource_type": resource.get("type", "")}
            )

        outputs = ydata.get("outputs", {})

        for output, output_value in outputs.items():
            self.outputs.append(output)

        with open(self.env, "r") as f:
            ydata = yaml.safe_load(f)

        self.parameters = ydata.get("parameters", {})


class HeatPreload:
    def __init__(self, preload):
        """
        creates preload object that holds parameter name/values

        :preload:             /path/to/preloads/file.json
        """
        self.preload = preload
        self.parameters = {}

    def get_data(self):
        with open(self.preload, "r") as f:
            jdata = json.loads(f.read())

        # get parameters regardless of API version

        vnf_api_parameters = (
            jdata.get("input", {})
            .get("vnf-topology-information", {})
            .get("vnf-parameters", [])
        )

        for parameter in vnf_api_parameters:
            p_name = parameter.get("vnf-parameter-name")
            p_value = parameter.get("vnf-parameter-value")
            self.parameters[p_name] = p_value

        gr_api_parameters = (
            jdata.get("input", {})
            .get("preload-vf-module-topology-information", {})
            .get("vf-module-topology", {})
            .get("vf-module-parameters", {})
            .get("param", [])
        )

        for parameter in gr_api_parameters:
            p_name = parameter.get("name")
            p_value = parameter.get("value")
            self.parameters[p_name] = p_value


class HeatStack:
    def __init__(self, stack_name):
        """
        creates stack object that hold stack resources,
        parameters, and outputs

        :stack_name:             name of heat stack in openstack
        """
        self.stack_name = stack_name
        self.resources = []
        self.parameters = {}
        self.outputs = []
        self.status = ""
        self.stack_details = {}

    def get_data(self, orchestration_url, token):
        url = stack_url.format(orchestration_url, self.stack_name)
        r = requests.get(headers={"X-Auth-Token": token}, url=url)

        if r.status_code == 200:
            response = r.json()
            self.parameters = response.get("stack", {}).get("parameters", {})
            self.outputs = response.get("stack", {}).get("outputs", {})
            self.status = response.get("stack", {}).get("stack_status", "")
            self.stack_details = response.get("stack", {})

        url = stack_resources_url.format(orchestration_url, self.stack_name)
        r = requests.get(headers={"X-Auth-Token": token}, url=url)
        if r.status_code == 200:
            response = r.json()
            resources = response.get("resources", [])
            for resource in resources:
                self.resources.append(
                    {
                        "resource_id": resource.get("resource_name"),
                        "resource_type": resource.get("resource_type"),
                        "resource_status": resource.get("resource_status"),
                    }
                )

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
import datetime
import hashlib
import json
import os
from copy import deepcopy
from robot.libraries.BuiltIn import BuiltIn
from zipfile import ZipFile

OUTPUT_DATA = {
    "vnf_checksum": "",
    "build_tag": "",
    "version": "2019.09",
    "test_date": "",
    "duration": "",
    "vnf_type": "heat",
    "testcases_list": [
        {
            "mandatory": "true",
            "name": "onap-vvp.validate.heat",
            "result": "NOT_STARTED",
            "objective": "onap heat template validation",
            "sub_testcase": [],
            "portal_key_file": "report.json",
        },
        {
            "mandatory": "true",
            "name": "onap-vvp.lifecycle_validate.heat",
            "result": "NOT_STARTED",
            "objective": "onap vnf lifecycle validation",
            "sub_testcase": [
                {"name": "model-and-distribute", "result": "NOT_STARTED"},
                {"name": "instantiation", "result": "NOT_STARTED"},
            ],
            "portal_key_file": "log.html",
        },
        {
            "mandatory": "true",
            "name": "stack_validation",
            "result": "NOT_STARTED",
            "objective": "onap vnf openstack validation",
            "sub_testcase": [],
            "portal_key_file": "stack_report.json",
        },
    ],
}


class OVPListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.report = deepcopy(OUTPUT_DATA)

        self.build_number = ""
        self.build_directory = ""
        self.output_directory = ""
        self.template_directory = ""

    def initialize(self):
        self.build_number = BuiltIn().get_variable_value("${GLOBAL_BUILD_NUMBER}")
        self.build_directory = BuiltIn().get_variable_value("${BUILD_DIR}")
        self.output_directory = BuiltIn().get_variable_value("${OUTPUTDIR}")

        self.template_directory = "{}/templates".format(self.build_directory)
        self.report["build_tag"] = "vnf-validation-{}".format(self.build_number)
        self.report["vnf_checksum"] = sha256(self.template_directory)

    def start_test(self, name, attrs):
        self.initialize()
        date = datetime.datetime.strptime(attrs["starttime"], '%Y%m%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
        self.report["test_date"] = date

    def end_keyword(self, name, attrs):
        kwname = attrs["kwname"]
        status = attrs["status"]

        if kwname == "Run VVP Validation Scripts":
            self.report["testcases_list"][0]["result"] = status
        elif kwname == "Model Distribution For Directory":
            self.report["testcases_list"][1]["sub_testcase"][0]["result"] = status
        elif kwname == "Instantiate VNF":
            self.report["testcases_list"][1]["sub_testcase"][1]["result"] = status
            self.report["testcases_list"][1]["result"] = status
        elif kwname == "Run VNF Instantiation Report":
            self.report["testcases_list"][2]["result"] = status

    def end_test(self, name, attrs):
        self.report["duration"] = attrs["elapsedtime"] / 1000

    def close(self):
        with open("{}/summary/results.json".format(self.output_directory), "w") as f:
            f.write(json.dump(self.report, f, indent=4))


def sha256(template_directory):
    heat_sha = None

    if os.path.exists(template_directory):
        zip_file = "{}/tmp_heat.zip".format(template_directory)
        with ZipFile(zip_file, "w") as zip_obj:
            for folder_name, subfolders, filenames in os.walk(template_directory):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    zip_obj.write(file_path)

        with open(zip_file, "rb") as f:
            bytes = f.read()
            heat_sha = hashlib.sha256(bytes).hexdigest()

        os.remove(zip_file)

    return heat_sha

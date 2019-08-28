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
import os
import subprocess

VVP_BRANCH = "master"
VVP_URL = "https://gerrit.onap.org/r/vvp/validation-scripts"


# use this to import and run validation from robot
class HeatValidationScripts:
    def __init__(self):
        pass

    @keyword
    def validate(self, build_dir, template_directory, output_directory):
        """
        keyword invoked by robot to execute VVP validation scripts

        :build_dir:                 directory to install virtualenv
                                    and clone validation scripts
        :template_directory:        directory with heat templates
        :output_directory:          directory to store output files
        """
        t = VVP(build_dir, template_directory, output_directory)
        t.install_requirements()
        status = t.run_vvp()

        return status


class VVP:
    def __init__(self, build_dir, template_directory, output_directory):
        self._build_dir = build_dir
        self.initialize()

        self.virtualenv = "{}/test_env".format(build_dir)
        self.vvp = "{}/validation_scripts".format(build_dir)
        self.template_directory = template_directory
        self.output_directory = output_directory

    def initialize(self):
        self.create_venv(self._build_dir)
        self.clone_vvp(self._build_dir)

    def create_venv(self, build_dir):
        try:
            subprocess.call(
                ["python3.7", "-m", "virtualenv", "--clear", "{}/test_env".format(build_dir)]
            )
        except OSError as e:
            print("error creating virtual environment for vvp {}".format(e))
            raise

    def clone_vvp(self, build_dir):
        if not os.path.exists("{}/validation_scripts".format(build_dir)):
            try:
                subprocess.call(
                    [
                        "git",
                        "clone",
                        "-b",
                        VVP_BRANCH,
                        VVP_URL,
                        "{}/validation_scripts".format(build_dir),
                    ]
                )
            except OSError as e:
                print("error cloning vvp validation scripts {}".format(e))
                raise

    def install_requirements(self):
        try:
            subprocess.call(
                [
                    "{}/bin/python".format(self.virtualenv),
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "pip",
                    "wheel",
                ]
            )
            subprocess.call(
                [
                    "{}/bin/python".format(self.virtualenv),
                    "-m",
                    "pip",
                    "install",
                    "wheel",
                    "-r",
                    "{}/requirements.txt".format(self.vvp),
                ]
            )
        except OSError as e:
            print("error installing vvp requirements {}".format(e))
            raise

    def run_vvp(self):
        try:
            ret = subprocess.call(
                [
                    "{}/bin/python".format(self.virtualenv),
                    "-m",
                    "pytest",
                    "--rootdir={}/ice_validator/".format(self.vvp),
                    "--template-directory={}".format(self.template_directory),
                    "--output-directory={}".format(self.output_directory),
                    "{}/ice_validator/tests/".format(self.vvp),
                ]
            )
        except OSError as e:
            print("error running vvp validation scripts {}".format(e))
            raise

        if ret != 0:
            raise ValueError("Validation Script error detected")

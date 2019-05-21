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


from jinja2 import Environment, FileSystemLoader, select_autoescape
from robot import utils


class TemplatingEngine(object):
    """TemplateImporter is common resource for templating with strings."""

    def __init__(self):
        self._cache = utils.ConnectionCache('No Jinja Environments created')

    def create_environment(self, alias, templates_folder):
        jinja_env = Environment(
            loader=FileSystemLoader(templates_folder),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self._cache.register(jinja_env, alias=alias)

    def apply_template(self, alias, template_location, values):
        """returns a string that is the jinja template in template_location filled in via the dictionary in values """
        template = self._cache.switch(alias).get_template(template_location)
        return template.render(values)

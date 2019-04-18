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


from setuptools import setup

setup(
    name='${PROJECT_NAME}',            # This is the name of your PyPI-package.
    keywords=("utils", "robotframework", "testing", "onap"),
    version='${VERSION}',                        # Update the version number for new releases
    license="Apache 2.0",
    description='Scripts written to be used during robot framework testing',    # Info about script
    long_description="python-package that provides convenience methods to make certain tasks in robot framework easier."
                     "since this uses robot framework internal libraries or may in the future, it is not meant as a"
                     "general purpose library",
    url="https://github.com/onap/testsuite-python-testing-utils",
    platforms=['all'],
    install_requires=[
        'dnspython',
        'paramiko',
        'pyyaml',
        'robotframework',
        'deepdiff>=2.5,<3.3',
        'Jinja2'
    ],  # what we need
    packages=['eteutils', 'loadtest', 'vcpeutils'],       # The name of your scripts package
    package_dir={'eteutils': 'eteutils', 'loadtest': 'loadtest', 'vcpeutils':'vcpeutils'}, # The location of your scipts package
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Environment :: Plugins',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Library',
        'License :: OSI Approved :: Apache Software License'
    ]
)

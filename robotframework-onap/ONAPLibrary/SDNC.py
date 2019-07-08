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

from ONAPLibrary.PreloadSDNCKeywords import PreloadSDNCKeywords
from ONAPLibrary.robotlibcore import HybridCore
from ONAPLibrary.BaseSDNCKeywords import BaseSDNCKeywords


class SDNC(HybridCore):
    """SDNC is an ONAP testing library for Robot Framework that provides functionality for interacting with the network
    controller. """

    def __init__(self):
        self.keyword_implementors = [
            BaseSDNCKeywords(),
            PreloadSDNCKeywords()
        ]
        HybridCore.__init__(self, self.keyword_implementors)

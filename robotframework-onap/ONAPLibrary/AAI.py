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

from ONAPLibrary.BaseAAIKeywords import BaseAAIKeywords
from robotlibcore import HybridCore


class AAI(HybridCore):
    """The main interface for interacting with A&AI. It handles low level stuff like managing the http request
    library and A&AI required fields """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.keyword_implementors = [
            BaseAAIKeywords()
        ]
        HybridCore.__init__(self, self.keyword_implementors)

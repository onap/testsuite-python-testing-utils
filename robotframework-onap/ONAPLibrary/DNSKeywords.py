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

import dns.message
import dns.name
import dns.query
from robot.api.deco import keyword


class DNSKeywords(object):
    """ Utilities useful for DNS requests """

    def __init__(self):
        super(DNSKeywords, self).__init__()

    @keyword
    def dns_request(self, domain, ns):
        """ return the ip address of the given domain name from the given nameserver """
        request = dns.message.make_query(domain, dns.rdatatype.A)
        request.flags |= dns.flags.AD
        request.find_rrset(request.additional, dns.name.root, 65535, dns.rdatatype.OPT, create=True, force_unique=True)
        response = dns.query.udp(request, ns)

        for answer in response.answer:
            for item in answer.items:
                return item

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

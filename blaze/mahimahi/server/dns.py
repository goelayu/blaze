""" This module defines a DNS Server that returns the specified DNS-IP mapping """

import subprocess
import sys
from typing import Dict


class DNSServer:
    """
    DNSServer runs dnsmasq on the default port (port 53) with the given host-ip mapping. It assumes that
    the system is set up to query the DNS server running on localhost. This DNS server will not allow other
    DNS queries to pass through -- you should set up another resolver to handle those and make this one the
    higher priority resolver.
    """

    def __init__(self, host_ip_map: Dict[str, str]):
        """
        Initialize the DNS Server

        :param host_ip_map: A mapping from DNS names to IP addresses to resolve each name to
        """
        self.host_ip_map = host_ip_map
        self.proc = None

    def __enter__(self):
        args = ["-k", "-R"]
        for host, ip_addr in self.host_ip_map.items():
            args.extend(["-A", f"/{host}/{ip_addr}"])
        
        # --keep-in-foreground --no-resolv --no-hosts
        args.extend(["--no-resolv"])
        args.extend(["--keep-in-foreground"])
        args.extend(["--no-hosts"])

        self.proc = subprocess.Popen(["dnsmasq", *args], stdout=sys.stderr, stderr=sys.stderr)

        # If wait lasts for more than 1 second, a TimeoutError will be raised, which is okay since it
        # means that dnsmasq is running successfully. If it finishes sooner, it means it crashed and
        # we should raise an exception
        try:
            self.proc.wait(1)
            raise RuntimeError("dnsmasq exited unsuccessfully")
        except subprocess.TimeoutExpired:
            pass

    def __exit__(self, exception_type, exception_value, traceback):
        pass
        # subprocess.call(["sudo","kill","-9",str(self.proc.pid)],shell=True)
        self.proc.kill()
        self.proc.wait()

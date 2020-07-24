""" Implements the commands for viewing and manipulating the training manifest """
import json
import time
import os

from blaze.action import Policy
from blaze.logger import logger as log
from blaze.mahimahi.server import start_server

from . import command


@command.argument("replay_dir", help="The directory containing the save files captured by mahimahi")
@command.argument("--policy", help="The file path to a JSON-formatted push policy to serve")
@command.argument("--cert_path", help="Location of the server certificate")
@command.argument("--key_path", help="Location of the server key")
@command.argument(
    "--cache_time", help="Do not cache objects which expire in less than this time (in seconds)", type=int, default=None
)
@command.argument(
    "--extract_critical_requests",
    help="true or false to specify if server should inject critical request extractor",
    action="store_true",
)
@command.argument(
    "--per_resource_latency",
    help="The file path to JSON-formatted per resource server side latency"
)
@command.argument(
    "--enable_http2",
    help="enable support for http2",
    action="store_true"
)
@command.command
def replay(args):
    """
    Starts a replay environment for the given replay directory, including setting up interfaces, running
    a DNS server, and configuring and running an nginx server to serve the requests
    """
    policy = None
    cert_path = os.path.abspath(args.cert_path) if args.cert_path else None
    key_path = os.path.abspath(args.key_path) if args.key_path else None
    per_resource_latency = os.path.abspath(args.per_resource_latency) if args.per_resource_latency else None

    if args.policy:
        log.debug("reading policy", push_policy=args.policy)
        with open(args.policy, "r") as policy_file:
            policy_dict = json.load(policy_file)
        policy = Policy.from_dict(policy_dict)

    with start_server(
        args.replay_dir,
        cert_path,
        key_path,
        policy,
        per_resource_latency,
        cache_time=args.cache_time,
        extract_critical_requests=args.extract_critical_requests,
        enable_http2=args.enable_http2
    ):
        while True:
            time.sleep(86400)

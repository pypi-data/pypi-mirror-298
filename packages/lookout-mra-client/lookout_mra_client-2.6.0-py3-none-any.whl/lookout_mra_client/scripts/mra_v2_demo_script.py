import logging, json, argparse, datetime, time, socket

from logging.handlers import RotatingFileHandler

from lookout_mra_client.event_forwarders.event_forwarder import EventForwarder
from lookout_mra_client.mra_v2_stream_thread import MRAv2StreamThread
from lookout_mra_client.lookout_logger import init_lookout_logger
from lookout_mra_client.syslog_client import SyslogClient


FILE_FORWARDER = "file"
SYSLOG_FORWARDER = "syslog"


class FileEventForwarder(EventForwarder):
    def __init__(self, filename: str, maxMegabytes: int = 10, backupCount: int = 5):
        self.logger = logging.getLogger("FileEventForwarder")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        maxBytes = maxMegabytes * 1e6
        file_handler = RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
        file_handler.formatter = logging.Formatter("%(message)s")

        self.logger.addHandler(file_handler)

    def write(self, event: dict, entName: str = ""):
        event["entName"] = entName
        self.logger.info(json.dumps(event) + "\r\n")


class SyslogEventForwarder(EventForwarder):
    def __init__(self, syslog_address) -> None:
        self.syslog_client = SyslogClient(
            "MRAv2SyslogClient", lambda d: str(d), (syslog_address, 514), True, socket.SOCK_DGRAM
        )

    def write(self, event: dict, entName: str = ""):
        event["entName"] = entName
        self.syslog_client.write(event)


def start_thread(key_filename: str, event_type: list, args) -> None:
    init_lookout_logger("./mra_v2_demo_script.log")

    if args.forwarder == FILE_FORWARDER:
        forwarder = FileEventForwarder(args.output)
    elif args.forwarder == SYSLOG_FORWARDER:
        forwarder = SyslogEventForwarder(args.address)
    else:
        print(f"Unknown event forwarder: {args.forwarder}")
        exit(0)

    key_file = open(key_filename, "r")
    api_key = key_file.read().strip()

    start_time = datetime.datetime.now() - datetime.timedelta(days=1)
    start_time = start_time.replace(tzinfo=datetime.timezone.utc)
    stream_args = {
        "api_domain": "https://api.lookout.com",
        "api_key": api_key,
        "start_time": start_time,
        "event_type": ",".join(event_type),
    }
    mra = MRAv2StreamThread("demoEnt", forwarder, **stream_args)

    try:
        mra.start()
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        mra.shutdown_flag.set()
        mra.join()
        print("\nGoodbye :)")


def get_parser() -> argparse.ArgumentParser:
    main_cmd = (
        'python3 -c "from lookout_mra_client.scripts.mra_v2_demo_script import main; main();"'
    )
    example_text = f"""example:
  {main_cmd} file \\
    --output /var/log/output.txt \\
    --api_key /var/opt/apikey.txt \\
    --event_type THREAT DEVICE

  {main_cmd} syslog \\
    --api_key /var/opt/apikey.txt \\
    --event_type THREAT DEVICE
    
  {main_cmd} syslog \\
    --address xxx.xxx.xxx.xxx \\
    --api_key /var/opt/apikey.txt \\
    --event_type THREAT DEVICE"""

    parser = argparse.ArgumentParser(
        description="Demonstrate MRAv2 event streams in python",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--api_key", required=True, help="Path of api key file.")
    common_parser.add_argument(
        "--event_type",
        help="MRA event types to retrieve, i.e. THREAT, DEVICE, AUDIT.",
        nargs="+",
        default=[],
    )

    subparsers = parser.add_subparsers(title="forwarders", dest="forwarder", required=True)

    file_args_desc = "Output events to a given file path"
    file_args = subparsers.add_parser(
        "file", help=file_args_desc, description=file_args_desc, parents=[common_parser]
    )
    file_args.add_argument("--output", required=True, help="Output file to write events to.")

    syslog_args_desc = "Output events to a local/remote syslog server"
    syslog_args = subparsers.add_parser(
        "syslog", help=syslog_args_desc, description=syslog_args_desc, parents=[common_parser]
    )
    syslog_args.add_argument("--address", help="IP address of syslog server", default="localhost")

    return parser


def main():
    args = get_parser().parse_args()
    start_thread(args.api_key, args.event_type, args)

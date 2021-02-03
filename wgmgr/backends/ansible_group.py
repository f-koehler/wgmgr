from pathlib import Path

from .base import Backend
from wgmgr.config import Config
from wgmgr.util import load_yaml_file, write_yaml_file


class AnsibleGroup(Backend):
    def __init__(self, path: Path, key: str):
        self.path = Path
        self.key = key

    def load(self) -> Config:
        yml = load_yaml_file(self.path)[self.key]

    def save(self, config: Config):
        yml = {"peers": {}, "default_port": config.default_port}
        yml["ipv4_subnet"] = str(config.network_ipv4) if config.network_ipv4 else None
        yml["ipv6_subnet"] = str(config.network_ipv6) if config.network_ipv6 else None

        for peer in config.peers:
            peer_entry = {
                "private_key": peer.private_key,
                "public_key": peer.public_key,
            }
            if peer.port != config.default_port:
                peer_entry["port"] = peer.port
            if peer.ipv4_address:
                peer.entry["ipv4"] = peer.ipv4_address
            if peer.ipv6_address:
                peer.entry["ipv6"] = peer.ipv6_address
            yml["peers"][peer.hostname] = peer_entry

        try:
            full_yml = load_yaml_file(self.path)
        except OSError:
            full_yml = {}

        full_yml[self.key] = yml

        write_yaml_file(self.path, full_yml)
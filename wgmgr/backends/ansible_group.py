from __future__ import annotations

from ipaddress import IPv4Network
from pathlib import Path
from typing import Dict

from wgmgr.config import Config
from wgmgr.util import load_yaml_file, write_yaml_file

from .base import Backend
from .error import MissingBackendOptionError


class AnsibleGroup(Backend):
    def __init__(self, path: Path, key: str):
        self.path = path
        self.key = key

    @staticmethod
    def from_options(options: Dict[str, str]) -> AnsibleGroup:
        options["key"] = options.get("key", "wgmgr")
        if not "path" in options:
            raise MissingBackendOptionError("path")
        return AnsibleGroup(Path(options["path"]), options["key"])

    def load(self) -> Config:
        yml = load_yaml_file(self.path)[self.key]
        config = Config()

        if "ipv4_subnet" in yml:
            config.network_ipv4 = IPv4Network(yml["ipv4_subnet"])

        if "ipv6_subnet" in yml:
            config.network_ipv6 = IPv6Network(yml["ipv6_subnet"])

        return config

    def save(self, config: Config):
        yml = {"peers": {}, "default_port": config.default_port}

        if config.network_ipv4:
            yml["ipv4_subnet"] = str(config.network_ipv4)

        if config.network_ipv6:
            yml["ipv6_subnet"] = str(config.network_ipv6)

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

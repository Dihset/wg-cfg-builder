import os
from ipaddress import IPv4Network
from os.path import exists

from app.settings import settings

from .models import Peer, WgConfig
from .utils import get_file_content


class PeerCreator:
    def __init__(self, conf: WgConfig):
        self.conf = conf

    def create(self, name: str) -> Peer:
        private_key, public_key = self._create_keys(name)
        allowed_ips = self._get_last_ip()
        return Peer(
            name=name,
            private_key=private_key,
            public_key=public_key,
            address=allowed_ips,
        )

    def _create_keys(self, name: str) -> tuple[str, str]:
        privatekey_path = f"{settings.WG_BASE_DIR}/peers/{name}.privatekey"
        publickey_path = f"{settings.WG_BASE_DIR}/peers/{name}.publickey"

        os.system(f"wg genkey | tee {privatekey_path} | wg pubkey | tee {publickey_path}")

        privatekey = get_file_content(privatekey_path)
        publickey = get_file_content(publickey_path)

        return privatekey, publickey

    def _get_last_ip(self) -> str:
        network = IPv4Network(settings.VPN_NETWOK)
        excluded_ids = [peer.address[:-3] for peer in self.conf.peers] + [
            settings.WG_IP,
            settings.VPN_NETWOK[:-3],
        ]
        last_ip = next(host for host in network.hosts() if str(host) not in excluded_ids)
        return f"{last_ip}/32"


class WgService:
    """"""

    CONF_FILE_NAME = "wg.conf.json"

    def __init__(self, base_dir: str | None = None):
        self.wg_cfg_json = f"{settings.WG_BASE_DIR}/{self.CONF_FILE_NAME}"
        self.wg_cfg_file = settings.WG_SERVER_CFG

        if exists(self.wg_cfg_file):
            self.conf = WgConfig.parse_file(self.wg_cfg_json)
        else:
            self.conf = self.build_empty_config()

    def build_empty_config(self) -> WgConfig:
        wg_conf = WgConfig(
            private_key=get_file_content(settings.WG_SERVER_PRIVATE_KEY),
            public_key=get_file_content(settings.WG_SERVER_PUBLIC_KEY),
            address=settings.SERVER_IP,
            ip=settings.WG_IP,
            port=settings.WG_PORG,
        )

        self._resave_conf(wg_conf)

        return wg_conf

    def get_peer(self, name) -> Peer:
        pass

    def create_peer(self, name: str) -> str:
        peer = PeerCreator(self.conf).create(name)
        self.conf.peers.append(peer)
        self._resave_conf(self.conf)

        conf = self.conf.get_client_conf(name)

        with open(f"{settings.WG_BASE_DIR}/peers/{name}.conf", "w") as file:
            file.write(conf)

        return conf

    def delete_peer(self, name: str) -> Peer:
        pass

    def reload_server(self):
        pass

    def _resave_conf(self, conf: WgConfig):
        with open(self.wg_cfg_json, "w") as cfg:
            cfg.write(conf.json())

        with open(self.wg_cfg_file, "w") as cfg:
            cfg.write(conf.get_server_conf())

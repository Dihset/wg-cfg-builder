import os
import re
from ipaddress import IPv4Network

from pydantic import BaseModel

from app.settings import settings
from app.utils import get_file_content

PEER_RE = r"\[Peer\]\nPublicKey = (\S{1,})\nAllowedIPs = (\S{1,})"

PEER_PATTERN_IN_SERVER = """
[Peer]
PublicKey = {client_public_key}
AllowedIPs = {allowed_ips}

"""

PEER_PATTERN_IN_CLIENT = """
[Interface]
PrivateKey = {client_private_key}
Address = {allowed_ips}
DNS = 8.8.8.8

[Peer]
PublicKey = {server_public_key}
Endpoint = {server_ip}:{server_port}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20
"""


class Peer(BaseModel):
    public_key: str
    allowed_ips: str


class WgConfService:
    """"""

    def __init__(self):
        self.server_private_key = get_file_content(settings.WG_SERVER_PRIVATE_KEY)
        self.server_public_key = get_file_content(settings.WG_SERVER_PUBLIC_KEY)
        self.all_peers = self._build_peers()

    def create_peer(self, name: str):
        """"""
        privatekey, publickey = self._create_keys(name)
        allowed_ips = self._get_last_ip()

        content_in_server = PEER_PATTERN_IN_SERVER.format(
            client_public_key=publickey, allowed_ips=allowed_ips
        )
        content_in_client = PEER_PATTERN_IN_CLIENT.format(
            client_private_key=privatekey,
            allowed_ips=allowed_ips,
            server_public_key=self.server_public_key,
            server_ip=settings.SERVER_IP,
            server_port=settings.WG_PORG,
        )

        with open(settings.WG_SERVER_CFG, "a") as cfg:
            cfg.write(content_in_server)

        with open(settings.WG_BASE_DIR / f"client.{name}.cfg", "w") as cfg:
            cfg.write(content_in_client)

        return content_in_client

    def apply_cfg(self):
        pass

    def _create_keys(self, name: str) -> tuple[str, str]:
        privatekey_path = f"{settings.WG_BASE_DIR}/client.{name}.privatekey"
        publickey_path = f"{settings.WG_BASE_DIR}/client.{name}.publickey"
        os.system(f"wg genkey | tee {privatekey_path} | wg pubkey | tee {publickey_path}")
        privatekey = get_file_content(privatekey_path)
        publickey = get_file_content(publickey_path)
        return privatekey, publickey

    def _build_peers(self) -> list[Peer]:
        cfg_content = get_file_content(settings.WG_SERVER_CFG)
        return [
            Peer(public_key=key, allowed_ips=ips) for key, ips in re.findall(PEER_RE, cfg_content)
        ]

    def _get_last_ip(self) -> str:
        network = IPv4Network(settings.VPN_NETWOK)
        excluded_ids = [item.allowed_ips[:-3] for item in self.all_peers] + [
            settings.WG_IP,
            settings.VPN_NETWOK[:-3],
        ]
        print(excluded_ids)
        last_ip = next(host for host in network.hosts() if str(host) not in excluded_ids)
        return f"{last_ip}/32"

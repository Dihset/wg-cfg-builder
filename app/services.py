import os

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


class WgConfService:
    def __init__(self):
        self.server_private_key = None
        self.server_public_key = None

    def create_peer(self, name: str):
        pass

    def _create_keys(self, name: str) -> tuple[str, str]:
        privatekey_path = f"{settings.WG_BASE_DIR}/client.{name}.privatekey"
        publickey_path = f"{settings.WG_BASE_DIR}/client.{name}.publickey"
        os.system(f"wg genkey | tee {privatekey_path} | wg pubkey | tee {publickey_path}")
        privatekey = get_file_content(privatekey_path)
        publickey = get_file_content(publickey_path)
        return privatekey, publickey

from pathlib import Path

from pydantic import BaseModel

from .utils import get_template_by_path


class Peer(BaseModel):
    name: str
    private_key: str
    public_key: str
    address: str
    dns: str = "8.8.8.8"


class WgConfig(BaseModel):
    private_key: str
    public_key: str
    address: str
    ip: str
    port: str
    post_up: str = (
        "iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"
    )
    post_down: str = (
        "iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERAD"
    )
    peers: list[Peer] = []

    def find_by_name(self, name: str) -> Peer | None:
        return next((peer for peer in self.peers if peer.name == name), None)

    def get_client_conf(self, name: str) -> str:
        path = Path(__file__).resolve().parent / "client.conf.jinja"
        template = get_template_by_path(path)
        return template.render(
            conf=self,
            peer=self.find_by_name(name),
        )

    def get_server_conf(self) -> str:
        path = Path(__file__).resolve().parent / "server.conf.jinja"
        template = get_template_by_path(path)
        return template.render(conf=self)

from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, FilePath


class Settings(BaseSettings):

    WG_BASE_DIR: DirectoryPath = "/home/admin/Документы/my-projects/wg-cfg-builder/wg"
    WG_SERVER_CFG: FilePath = Path(WG_BASE_DIR) / "wg.cfg"
    WG_SERVER_PRIVATE_KEY: FilePath = Path(WG_BASE_DIR) / "privatekey"
    WG_SERVER_PUBLIC_KEY: FilePath = Path(WG_BASE_DIR) / "publickey"
    WG_IP: str = "10.0.0.1"
    WG_PORG: int = 51830
    VPN_NETWOK: str = "10.0.0.0/24"
    SERVER_IP: str = "127.0.0.1"

    API_KEY: str = "change_me"


settings = Settings()

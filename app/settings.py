from pydantic import BaseSettings, DirectoryPath


class Settings(BaseSettings):

    WG_BASE_DIR: DirectoryPath = "/home/dihset/Документы/my_projects/wg-cfg-builder"
    WG_IP: str = ""
    WG_PORG: str = ""


settings = Settings()

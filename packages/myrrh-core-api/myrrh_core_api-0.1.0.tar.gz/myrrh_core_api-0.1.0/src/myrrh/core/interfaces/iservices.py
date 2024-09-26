import typing
import abc


from myrrh.core.exts.interfaces import IExtSession, IMyrrhExt, uri_wr, uri_wr_data, uri_rd
from myrrh.core.warehouse.item import ItemT

from .iprovider import IProvider

__all__ = [
    "IConfigServ",
    "ISecretServ",
    "ICmdServ",
    "ISecretSession",
    "IConfigSession",
    "ICmdSession",
    "ConfigValueT",
    "IProviderSession",
    "IWarehouseSession",
]

ConfigValueT = typing.TypeVar("ConfigValueT", int, float, bool, str)


class IConfigSession(IExtSession):

    @uri_wr
    @abc.abstractmethod
    def init(self, key: str, value: ConfigValueT | None, section: str = "") -> dict[str, ConfigValueT] | ConfigValueT: ...

    @uri_wr
    @abc.abstractmethod
    def rm(self, key: str = "", section: str = ""): ...

    @uri_rd
    @abc.abstractmethod
    def get(self, key: str = "", default: ConfigValueT | None = None, *, section: str = "") -> dict[str, ConfigValueT] | ConfigValueT: ...

    @uri_wr_data("value")
    @abc.abstractmethod
    def set(self, key: str, value: ConfigValueT | None, section: str = "", *, overwrite: bool = True): ...


class ISecretSession(IExtSession):

    @uri_wr
    @abc.abstractmethod
    def set_key(self, save: bool = True, backup_name: str = "", key: str = "") -> str: ...

    @uri_rd
    @abc.abstractmethod
    def get_key(self, key_name: str) -> str: ...

    @uri_wr
    @abc.abstractmethod
    def use_key(self, key_name: str) -> None: ...

    @uri_wr
    @abc.abstractmethod
    def delete_key(self, key_name: str) -> None: ...

    @uri_wr
    @abc.abstractmethod
    def backup_key(self, backup_name: str = "", key: str | None = None, overwrite: bool = False) -> None: ...

    @uri_wr
    @abc.abstractmethod
    def rename_key(self, old_key_name: str, new_key_name: str) -> None: ...

    @uri_wr
    @abc.abstractmethod
    def clean_key_history(self) -> None: ...

    @uri_wr
    @abc.abstractmethod
    def clean_all_keys(self) -> None: ...

    @uri_rd
    @abc.abstractmethod
    def dump(self) -> dict[str, str]: ...

    @uri_rd
    @abc.abstractmethod
    def encrypt(self, path: str, key_name: str | None = None) -> str: ...

    @uri_rd
    @abc.abstractmethod
    def decrypt(self, path: str, key_name: str | None = None) -> str: ...


class ICmdSession(IExtSession):

    @uri_rd
    @abc.abstractmethod
    def cmd(self) -> str: ...

    @uri_wr
    @abc.abstractmethod
    def feed(self, name: str, stream: str, data: str): ...

    @uri_wr
    @abc.abstractmethod
    def input(self, name: str, stream: str, data: str) -> typing.Any: ...

    @uri_rd
    @abc.abstractmethod
    def result(self) -> typing.Any: ...


class IDbSession(IExtSession):

    @uri_rd
    @abc.abstractmethod
    def search(registry: dict, footprint: dict, type: str) -> dict: ...

    @uri_rd
    @abc.abstractmethod
    def search_data(registry: dict, data: dict, type: str) -> dict: ...


class IWarehouseSession(IExtSession):

    @uri_rd
    @abc.abstractmethod
    def list(self) -> list[str]: ...

    @uri_rd
    @abc.abstractmethod
    def get(self, name) -> ItemT: ...

    @uri_rd
    @abc.abstractmethod
    def validate(self, **kwa) -> ItemT: ...


class IProviderSession(IExtSession):

    @uri_rd
    @abc.abstractmethod
    def list(self) -> list[str]: ...

    @uri_rd
    @abc.abstractmethod
    def get(self, name) -> IProvider: ...

    @uri_rd
    @abc.abstractmethod
    def version(self, name) -> IProvider: ...


class IConfigServ(IMyrrhExt[IConfigSession]): ...


class ISecretServ(IMyrrhExt[ISecretSession]): ...


class ICmdServ(IMyrrhExt[ICmdSession]): ...


class IDbServ(IMyrrhExt[IExtSession]): ...

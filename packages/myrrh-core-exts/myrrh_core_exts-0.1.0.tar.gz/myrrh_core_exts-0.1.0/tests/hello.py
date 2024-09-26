import urllib.request
import abc

from myrrh.core.exts.interfaces import IExtSession, uri_rd
from myrrh.core.exts.misc import URI
from myrrh.core.exts.protocol import StdExtSession, MyrrhExtBase


class IEchoProtocol(IExtSession):
    @uri_rd
    @abc.abstractmethod
    def hello(self): ...


class HelloSession(StdExtSession, IEchoProtocol):
    def __init__(self, path):
        super().__init__(IEchoProtocol)
        self.path = path

    def hello(self, myname):
        if self.path:
            return f"Hello {myname} from {self.path}"
        return f"Hello {myname}"


class Hello(MyrrhExtBase):
    def __init__(self):
        self._dirs = list()

    def open(
        self, uri: str, *, req: urllib.request.Request | None = None
    ) -> HelloSession:
        path = URI(uri).path.removeprefix(self._path)
        return HelloSession(path)

    def extend(self, path: str, _obj):
        self._dirs.append(path)

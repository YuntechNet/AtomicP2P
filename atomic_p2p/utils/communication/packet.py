from typing import Union, Dict, Tuple
from json import loads, dumps

from atomic_p2p.utils import host_valid


class Packet(object):
    """This class is about how actual information been parse to datas"""

    @staticmethod
    def serilize(obj: 'Packet') -> bytes:
        raw_data = dumps(obj.to_dict())
        return bytes(raw_data, encoding='utf-8')

    @staticmethod
    def deserilize(raw_data: Union[Dict, str]) -> 'Packet':
        """This is serilizer convert data from utf-8 format string to Packet"""
        data = raw_data if type(raw_data) is dict else loads(
                str(raw_data, encoding='utf-8'))
        return Packet(dst=(data['to']['ip'], int(data['to']['port'])),
                      src=(data['from']['ip'], int(data['from']['port'])),
                      _hash=data['hash'], _type=data['type'],
                      _data=data['data'])

    def __init__(self, dst: Tuple[str, int], src: Tuple[str, int], _hash: str,
                 _type: str, _data: Dict):
        """Init of Packet class

        Args:
            dst: Packet is made by who.
            src: Packet is sending to where.
            _hash: Sender's security hash.
                None means it's a reject packet need to hide security hash.
            _type: Unique handler key to determine packet made by what handler.
            _data: A dict object to payload on.
        """
        assert host_valid(dst) is True
        assert host_valid(src) is True
        assert type(_hash) == str or _hash is None
        assert type(_type) == str
        assert type(_data) == dict
        self.__dst = dst
        self.__src = src
        self.__hash = _hash
        self.__type = _type
        self.__data = _data

    @property
    def export(self):
        return self.__dst, self.__src, self.__hash, self.__type, self.__data

    @property
    def dst(self):
        return self.__dst

    @property
    def src(self):
        return self.__src

    @property
    def _hash(self):
        return self.__hash

    @property
    def _type(self):
        return self.__type

    @property
    def data(self):
        return self.__data

    def __str__(self):
        return 'Packet<DST={} SRC={} TYP={}>'.format(
                self.__dst, self.__src, self.__type)

    def clone(self) -> 'Packet':
        return Packet(dst=self.__dst, src=self.__src, _hash=self.__hash,
                      _type=self.__type, _data=self.__data)

    def redirect_to_host(
        self, src: Tuple[str, int], dst: Tuple[str, int]
    ) -> None:
        self.__src = src
        self.__dst = dst

    def set_reject(self, reject_data: object, maintain_data: bool = False,
                   maintain_secret: bool = False) -> None:
        if maintain_data is True:
            self.__data['reject'] = reject_data
        else:
            self.__data = {'reject': reject_data}

        if maintain_secret is False:
            self.__hash = None

    def is_reject(self) -> bool:
        return 'reject' in self.__data

    def to_dict(self) -> Dict[str, object]:
        return {
            'to': {'ip': self.__dst[0], 'port': self.__dst[1]},
            'from': {'ip': self.__src[0], 'port': self.__src[1]},
            'hash': self.__hash,
            'type': self.__type,
            'data': self.__data
        }

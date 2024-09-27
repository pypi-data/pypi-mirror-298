import json
import os
import ijson
from itertools import islice
from typing import Dict, Any, Generator, Tuple
from .dict_dataset import DictDataset
from .dataset_mixin import DiskIOMixin
from ...const import StrPath


class IJSONDataset(DictDataset, DiskIOMixin):
    DEFAULT_CONFIG = {
        **DictDataset.DEFAULT_CONFIG,
        **DiskIOMixin.DEFAULT_CONFIG,
        'encoding': None,
    }

    def __init__(self, source: StrPath, **kwargs):
        super().__init__({}, **kwargs)
        self.fp = source
        self.encoding = kwargs.get('encoding', None)
        self.register_to_config(
            fp=self.fp,
            encoding=self.encoding,
        )

    def __getitem__(self, key):
        if isinstance(key, str):  # -> Dict
            with open(self.fp, 'r', encoding=self.encoding) as f:
                objects = ijson.items(f, key)
                for obj in objects:
                    return obj
        elif isinstance(key, slice):  # -> Generator
            with open(self.fp, 'r', encoding=self.encoding) as f:
                objects = ijson.items(f, '')
                iter_objects = islice(objects, key.start, key.stop, key.step)
                for obj in iter_objects:
                    yield obj

        elif isinstance(key, int):  # -> Dict
            with open(self.fp, 'r', encoding=self.encoding) as f:
                objects = ijson.items(f, '')
                iter_objects = islice(objects, key, key + 1)
                for obj in iter_objects:
                    return obj
        else:
            raise KeyError(f"Key must be str, int or slice, not {type(key)}")

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __iter__(self):
        with open(self.fp, 'r', encoding=self.encoding) as f:
            objects = ijson.items(f, '')
            for obj in objects:
                yield obj

    def __len__(self):
        with open(self.fp, 'r', encoding=self.encoding) as f:
            objects = ijson.items(f, '')
            return len(list(objects))

    def keys(self):
        with open(self.fp, 'r', encoding=self.encoding) as f:
            objects = ijson.items(f, '')
            for obj in objects:
                yield obj

    def items(self):
        with open(self.fp, 'r', encoding=self.encoding) as f:
            objects = ijson.items(f, '')
            for obj in objects:
                yield obj

    def values(self):
        with open(self.fp, 'r', encoding=self.encoding) as f:
            objects = ijson.items(f, '')
            for obj in objects:
                yield obj

    @classmethod
    def from_disk(cls, fp, encoding='utf-8', **kwargs):
        if not os.path.exists(fp):
            with open(fp, 'w') as f:
                f.write('{}')
        return cls(fp, encoding=encoding, **kwargs)

    def commit(self, indent=4, **kwargs):
        return self.dump(self.fp, indent=indent, **kwargs)

    def dump(self, fp, indent=4):
        # load all data from file and update with self.data
        with open(fp, 'r', encoding=self.encoding) as f:
            data = json.load(f)
        data.update(self.data)
        with open(fp, 'w') as f:
            json.dump(data, f, indent=indent)

import os

import pyamf.sol


class DictAsObject(dict):
    """
    Custom dictionary class that allows attribute-style access.
    """

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        if key in self:
            del self[key]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")


class SharedObject:
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath
        self.data = DictAsObject(self._read_local())

    def _read_local(self):
        try:
            with open(self.filepath, "rb") as file:
                sol_data = pyamf.sol.decode(file.read())
                return sol_data[1] if isinstance(sol_data, tuple) and len(sol_data) > 1 else {}
        except IOError:
            return {}

    def flush(self):
        try:
            pyamf.sol.save(self, self.filepath)
        except IOError:
            pass  # Handle the error as needed

    def items(self):
        return self.data.items()

    @classmethod
    def getLocal(cls, key):
        app_data_path = os.getenv("APPDATA")
        sol_file_path = os.path.join(app_data_path, r"Dofus\Local Store\#SharedObjects\DofusInvoker.swf", f"{key}.sol")
        return cls(key, sol_file_path)

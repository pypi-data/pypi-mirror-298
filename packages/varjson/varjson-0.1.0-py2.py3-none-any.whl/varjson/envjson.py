__version__ = "0.1.0"

import os
import re

import json

_re = re.compile(r"\$([A-Z_][A-Z0-9_]+)|\${([A-Z_][A-Z0-9_]+)}")

class EnvJSON:
    __version__ = __version__

    def __init__(self, json_file, strict=True, **kwargs):
        """Create EnvJSON class instance and read content from environment and files if they exists

        :param str json_file: file path for json file
        :param bool strict: use strict mode and throw exception when have unset variable, by default true
        :param dict kwargs: additional environment variables keys and values
        :return: new instance of EnvJSON
        """

        # read environment
        self._cfg = dict(os.environ)

        # set strict mode to false if "ENVYAML_STRICT_DISABLE" presents in env else use "strict" from function
        self._strict = strict

        self._json_file = json_file
        self._data = self._read_json()

    def __repr__(self):
        return repr(self._data)

    def __str__(self):
        return self._data.__str__()

    def __getitem__(self, key):
        return self._data[key]

    def __contains__(self, key):
        return key in self._data

    def _get_env_var(self, key:str)->str:
        result = self._cfg.get(key.upper(), None)
        if not result:
            if self._strict:
                raise ValueError(
                    f"Strict mode enabled, variable {key} is not defined!"
                )
            else:
                result = ''
        return result

    def _environment_decoder(self, obj: dict):
        result = obj.copy()
        for key, value in obj.items():
            if not isinstance(value, str):
                continue

            m_res = _re.finditer(value)
            updated_value = value
            for match in m_res:
                group = match.group(1) if match.group(1) else match.group(2)
                updated_value = updated_value.replace(match.group(0), self._get_env_var(group))

            result[key] = updated_value
        return result

    def _read_json(self) -> dict:
        with open(self._json_file) as json_file:
            file_contents = json_file.read()
            return json.loads(
                file_contents,
                object_hook=self._environment_decoder,
            )

    def _process_json(self, data: dict) -> dict:
        for key, value in data.items():
            # print(f"{key}: {value}")
            pass

        return data

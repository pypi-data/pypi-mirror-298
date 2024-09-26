# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import sys
import pytest

from varjson import EnvJSON

# set os env
os.environ["DB_HOST"] = "substituted_host"
os.environ["DB_PORT"] = "1433"
os.environ["DB_USERNAME"] = "substituted_user"
os.environ["DB_PASSWORD"] = "substituted_password"
os.environ["DB_SERVER"] = "substituted_server"


def test_it_should_return_substituted_value():
    env = EnvJSON(json_file="tests/test.json", strict=True)
    assert env["db"]["host"] == "substituted_host"
    assert env["db"]["port"] == "1433"
    assert env["db"]["username"] == "substituted_user"
    assert env["db"]["password"] == "substituted_password"
    assert env["db"]["name"] == "my_database"
    assert (
        env["db"]["connectionString"]
        == "substituted_user:substituted_password@substituted_server"
    )


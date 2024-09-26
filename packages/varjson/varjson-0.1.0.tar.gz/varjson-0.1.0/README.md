varjson
=======

``varjson`` addresses a straightforward challenge: incorporating values from environment variables into JSON configuration files. This functionality is akin to `envyaml <https://github.com/thesimj/envyaml>`_ and `varyaml <https://github.com/abe-winter/varyaml>`_, which offer similar capabilities for YAML, and has significantly inspired this package.

Example
-------

Consider the following configuration saved in ``config.json``:

```json
  {
    "db": {
      "host": "$DB_HOST",
      "port": "$DB_PORT",
      "username": "$DB_USERNAME",
      "password": "$DB_PASSWORD",
      "name": "my_database"
    }
  }
```  

With the environment variables set as follows:

```
  DB_HOST=some-host.tld
  DB_PORT=3306
  DB_USERNAME=user01
  DB_PASSWORD=veryToughPas$w0rd
```  

This configuration can then be parsed using ``varjson`` like this:

```python
  from varjson import EnvJSON

  cfg = EnvJSON(json_file="./config.json", strict=True)

  print(cfg)
  
  # {'db': {'host': 'some-host.tld',
  #   'port': 3306,
  #   'username': 'user01',
  #   'password': 'veryToughPas$w0rd',
  #   'name': 'my_database'}}
```

Tests
-----


License
-------

Licensed under the MIT license (see `LICENSE <./LICENSE>`_ file for more details).
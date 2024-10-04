
# saconfig

The saconfig module provides a simple and efficient way to manage and access environment variables within Python applications. This module abstracts the complexity of environment variable handling by providing utility functions for retrieving and validating variables. 

IMPORTANT: module read only environment variables, it doesnt read the .env file, for this you can use python-dotenv
# usage 
## > presets
```python3
from saconfig import MysqlConfig

mysql = MysqlConfig() # it`s going to read MYSQL_HOST and etc.
mysql_test = MysqlConfig(prefix="TEST") # it`s going to read TEST_MYSQL_HOST and etc.
```

Take a look of preset configs in `saconfig.configs`, there is configs for redis, postgresql, mysql, rabbit, django, etc.

## > build a config 
```python3
from saconfig import BaseConfig, Field

class ApiConfig(BaseConfig):
    # name_of_variable: type = Field(settings...)
    host: str = Field(key="HOST")
    api_key: str = Field(key="API_KEY")

api = ApiConfig()
api_1 = ApiConfig(prefix="API1")
api_2 = ApiConfig(prefix="API2")

```
If you want to reuse the config, it can be inited with different prefixes

## > default type parsers
### config
```python3
from saconfig import BaseConfig, Field

class ExampleConfig(BaseConfig):
    var1: list = Field(parser_value_type=int)
    var2: dict = Field(parser_value_type=int)
    var3: int = Field()
    var4: tuple = Field()
    var5: set = Field()
    var6: bool = Field()

data = ExampleConfig()
print(data.var1)
print(data.var2)
print(data.var3)
print(data.var4)
print(data.var5)
print(data.var6)
```
### env
```
var1=1,2,3,4,5
var2=a:1,b:2,c:3
var3=6
var4=test,231,run
var5=test,test,3,3,3,1,2,3
var6=f
```
### output
```
[1, 2, 3, 4, 5]
{'a': 1, 'b': 2, 'c': 3}
6
('test', '231', 'run')
{'3', 'test', '1', '2'}
False
```
More about parsers you can see in `saconfig.parses`

## > fields configurations
```python3
from saconfig import BaseConfig, Field

class ExampleConfig(BaseConfig):
    var1: list = Field(
        key="ANOTHER_KEY_NAME", # key to look for value in the env, by default variable name(key1)
        required=True, # if the field required or not
        default=[1,2,3], # default value of the field if its not in env
        parser=None, # if you dont like default parser(in this case of list) or you need to parse more specific structures
        parser_value_type=int, # type of value for parsing list, dict, set, tuple, etc.
        pc_transformer=None # pc transformer class, will be explained later
    )
```

## > example of env file generating
### config
```python3
from saconfig import BaseConfig, Field
from saconfig import generate_env_example

class ExampleConfig(BaseConfig):
    var1: list = Field(parser_value_type=int, required=False)
    var2: dict = Field(parser_value_type=int, required=False)
    var3: int = Field(required=False)
    var4: tuple = Field(required=False)
    var5: set = Field(required=False)
    var6: bool = Field(required=False)

data = ExampleConfig()
data_2 = ExampleConfig(prefix="DATA_2")
generate_env_example(data, data_2)
```
### output
```
# ExampleConfig
var1=
var2=
var3=
var4=
var5=
var6=


# DATA_2 ExampleConfig
DATA_2_var1=
DATA_2_var2=
DATA_2_var3=
DATA_2_var4=
DATA_2_var5=
DATA_2_var6=
```

## > PCTransformers - parse/compile transformer
The most interesting part of this party. They allow you to transform one field into another ones, and compile field from them.
The best example for it `saconfig.transformers.URLPCTransformer` with usage of databases configs, it allows you to represent connection to database like a url or like params. 
### config
```python3
from saconfig import MysqlConfig

mysql = MysqlConfig()
print(mysql.url)
print(mysql.host)
print(mysql.port)
print(mysql.username)
print(mysql.password)
print(mysql.database)
```
### env
```
MYSQL_URL=mysql://username:pass@0.0.0.0:3306/test_db

# the same with

MYSQL_HOST=0.0.0.0
MYSQL_PORT=3306
MYSQL_USER=username
MYSQL_PASSWORD=pass
MYSQL_DATABASE=test_db
```
### output 
```
mysql://username:pass@0.0.0.0:3306/test_db
0.0.0.0
3306
username
pass
mysql
```

## > django integrations
For presets sql database configs you can use `.as_django()` to setup connection in `DATABASES`
### config
```python3
from saconfig import MysqlConfig

mysql = MysqlConfig()
print(mysql.as_django())
```
### output
```
{'ENGINE': 'django.db.backends.mysql', 'USER': 'username', 'PASSWORD': 'pass', 'HOST': '0.0.0.0', 'PORT': '3306', 'NAME': 'test_db'}
```
For django basic settings its posible to use:
```python3
for k, v in DjangoCommonSettings().items():
    globals()[k] = v
```
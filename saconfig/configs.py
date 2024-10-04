from .base import BaseConfig, Field
from .django import DjangoDatabaseMixin
from .transformers import *


class MysqlConfig(BaseConfig, DjangoDatabaseMixin):
    database = 'mysql'
    url: str = Field(key='MYSQL_URL', pc_transformer=URLPCTransformer(replace=[(("path", str), ("name", str))]))
    username: str = Field(key='MYSQL_USER', default="")
    password: str = Field(key='MYSQL_PASSWORD', default="")
    host: str = Field(key='MYSQL_HOST', default='localhost')
    port: int = Field(key='MYSQL_PORT', default=3306)
    name: str = Field(key='MYSQL_NAME', default='')
    scheme: str = Field(key='MYSQL_SCHEME', default='mysql')
    params: str = Field(key='MYSQL_PARAMS', default='')
    fragment: str = Field(key='MYSQL_FRAGMENTS', default='')
    

class PostgresqlConfig(BaseConfig, DjangoDatabaseMixin):
    database = 'postgresql'
    url: str = Field(key='POSTGRESQL_URL', pc_transformer=URLPCTransformer(replace=[(("path", str), ("name", str))]))
    username: str = Field(key='POSTGRESQL_USER', default="")
    password: str = Field(key='POSTGRESQL_PASSWORD', default="")
    host: str = Field(key='POSTGRESQL_HOST', default='localhost')
    port: int = Field(key='POSTGRESQL_PORT', default=5432)
    name: str = Field(key='POSTGRESQL_NAME', default='')
    scheme: str = Field(key='POSTGRESQL_SCHEME', default='postgresql')
    params: str = Field(key='POSTGRESQL_PARAMS', default='')
    fragment: str = Field(key='POSTGRESQL_FRAGMENTS', default='')


class Sqlite3Config(BaseConfig, DjangoDatabaseMixin):
    database = 'sqlite3'
    path: str = Field(key='SQLITE3_PATH', default="db.sqlite3")


class RedisConfig(BaseConfig):
    url: str = Field(key='REDIS_URL', pc_transformer=URLPCTransformer(replace=[(("path", str), ("db", int))]))
    username: str = Field(key='REDIS_USER', default="")
    password: str = Field(key='REDIS_PASSWORD', default="")
    host: str = Field(key='REDIS_HOST', default='localhost')
    port: int = Field(key='REDIS_PORT', default=6379)
    db: int = Field(key='REDIS_DATABASE', default=0)
    scheme: str = Field(key='REDIS_SCHEME', default='redis')
    params: str = Field(key='REDIS_PARAMS', default='')
    fragment: str = Field(key='REDIS_FRAGMENTS', default='')


class RabbitMQConfig(BaseConfig):
    url: str = Field(key='RABBITMQ_URL', pc_transformer=URLPCTransformer(replace=[(("path", str), ("vhost", str))]))
    username: str = Field(key='RABBITMQ_USER', default="guest")
    password: str = Field(key='RABBITMQ_PASSWORD', default="guest")
    host: str = Field(key='RABBITMQ_HOST', default='localhost')
    port: int = Field(key='RABBITMQ_PORT', default=5672)
    vhost: str = Field(key='RABBITMQ_NAME', default='')
    scheme: str = Field(key='RABBITMQ_SCHEME', default='amqp')
    params: str = Field(key='RABBITMQ_PARAMS', default='')
    fragment: str = Field(key='RABBITMQ_FRAGMENTS', default='')


class DjangoCommonSettings(BaseConfig):
    SECRET_KEY: str = Field(default='')
    DEBUG: bool = Field(default=True)
    ALLOWED_HOSTS: list = Field(default=['localhost', '0.0.0.0'], pc_transformer=DjangoHostsPCTransformer())
    CSRF_TRUSTED_ORIGINS: list = Field(required=False)

    CORS_ALLOWED_ORIGINS: list = Field(required=False) # for corsheaders 
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True) # for corsheaders 


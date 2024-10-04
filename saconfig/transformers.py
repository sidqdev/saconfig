from typing import Any, Dict
from urllib.parse import urlparse
from urllib.parse import urlunparse, urlencode

from .base import PCTransformer


class URLPCTransformer(PCTransformer):
    def parse(self, value: str) -> dict:
        parsed_url = urlparse(value)
        username, password = parsed_url._userinfo
        host, port = parsed_url._hostinfo
        return self._replace({
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "scheme": parsed_url.scheme,
            "path": parsed_url.path.strip('/'),
            "params": parsed_url.params,
            "query": parsed_url.query,
            "fragment": parsed_url.fragment,
        })

    def compile(self, url_parts: dict) -> str:
        url_parts = self._unreplace(url_parts)
        scheme = url_parts.get('scheme', '')
        username = url_parts.get('username', '')
        password = url_parts.get('password', '')
        host = url_parts.get('host', '')
        port = url_parts.get('port', '')
        
        netloc = host
        if username and password:
            netloc = f"{username}:{password}@{host}"
        elif username:
            netloc = f"{username}@{host}"
        
        if port:
            netloc = f"{netloc}:{port}"
        
        path = url_parts.get('path', '')

        params = url_parts.get('params', '')
        query = urlencode(url_parts.get('query', {})) if isinstance(url_parts.get('query'), dict) else url_parts.get('query', '')
        fragment = url_parts.get('fragment', '')
        
        url = urlunparse((scheme, netloc, path, params, query, fragment))
        return url
    

class DjangoHostsPCTransformer(PCTransformer):
    def parse(self, hosts: list) -> Dict:
        return {
            "CSRF_TRUSTED_ORIGINS": [f"https://{x}" for x in hosts] + [f"http://{x}" for x in hosts],
            "CORS_ALLOWED_ORIGINS": [f"https://{x}" for x in hosts] + [f"http://{x}" for x in hosts]
        }

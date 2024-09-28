import os
from typing import Optional

import boto3
import dotenv

from .aws_secret_manager import AWSSecretManager

dotenv.load_dotenv()


class EnvResolver:
    def __init__(
            self,
            access_key_id: Optional[str] = None,
            secret_access_key: Optional[str] = None,
            region: Optional[str] = None,
    ):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region
        self._secret_manager = AWSSecretManager(access_key_id=access_key_id, secret_access_key=secret_access_key)
        self._resolved_values = {}

    def get(self, key: str, default=None) -> Optional[str]:
        if key in self._resolved_values:
            return self._resolved_values[key]
        value = os.environ.get(key)
        if not value:
            return default

        if value.startswith("arn:aws:"):
            # aws resource, load from aws
            if value.startswith("arn:aws:secretsmanager:"):
                value = self._secret_manager.get(arn=value)
            elif value.startswith("arn:aws:ssm:"):
                client = boto3.client(
                    "ssm",
                    region_name=self.region,
                    access_key_id=self.access_key_id,
                    secret_access_key=self.secret_access_key
                )
                ssm_response = client.get_parameter(Name=key, WithDecryption=True)
                value = ssm_response["Parameter"]["Value"]
        self._resolved_values[key] = value
        return value

    def set(self, key: str, value: str | None):
        self._resolved_values[key] = value

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key: str, value: str | None):
        self.set(key, value)

    def __delitem__(self, key):
        if key in self._resolved_values:
            del self._resolved_values[key]
        if key in os.environ:
            del os.environ[key]

    def __contains__(self, item: str):
        return item in self._resolved_values or item in os.environ


default_resolver = EnvResolver()

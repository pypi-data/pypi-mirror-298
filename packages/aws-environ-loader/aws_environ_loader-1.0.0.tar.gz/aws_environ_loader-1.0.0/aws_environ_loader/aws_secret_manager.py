import json
from functools import cache
from typing import Optional

import boto3


class AWSSecretManager:
    def __init__(
            self,
            access_key_id: Optional[str] = None,
            secret_access_key: Optional[str] = None
    ):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    @cache
    def get(self, arn: str):
        region, secret_name, key_name = self._parse_arn(arn)
        secrets = self._get_secret(region, secret_name)
        return secrets.get(key_name, None)

    @cache
    def _get_secret(self, region: str, secret_name: str):
        client = boto3.client(
            "secretsmanager",
            region_name=region,
            access_key_id=self.access_key_id,
            secret_access_key=self.secret_access_key
        )
        secret_response = client.get_secret_value(SecretId=secret_name)
        value = secret_response["SecretString"]
        return json.loads(value)

    @staticmethod
    def _parse_arn(arn: str):
        parts = arn.split(':')
        region = parts[3]
        secret_name = parts[6]
        key_name = parts[7]

        last_hyphen_idx = secret_name.rindex('-')
        if len(secret_name) - last_hyphen_idx == 7:
            secret_name = secret_name[:last_hyphen_idx]
        return region, secret_name, key_name

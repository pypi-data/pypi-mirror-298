from abc import abstractmethod
from getpass import getpass
import os
import json
import boto3
from mantlebio.core.constants import MANTLE_PROD_API
import requests
import time
import random
from mantlebio.exceptions import MantleRetriesExceededError
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class AuthMethod:
    @abstractmethod
    def authenticate(self, mantle_api: str = MANTLE_PROD_API):
        pass

    @abstractmethod
    def get_token(self):
        pass

    # helper function to get secret from AWS Secrets Manager
    def get_secret(self, secret_arn: str) -> dict:
        """
        Get secret from AWS Secrets Manager
        Args:
            secret_arn (str): ARN of the secret in AWS Secrets Manager
        Returns:
            dict: response from the API
        """
        arn_parts = secret_arn.split(':')
        region = arn_parts[3]
        try:
            client = boto3.client('secretsmanager', region_name=region)
            response = json.loads(client.get_secret_value(
                SecretId=secret_arn)["SecretString"])
            return response
        except Exception as e:
            logging.error(
                f"Error getting secret from AWS Secrets Manager for ARN: {secret_arn}: {e}")
            return {}


class PasswordCredentials(AuthMethod):
    """Object for storing password credentials"""

    def __init__(self, email: str = None, password: str = None) -> None:
        self.email = email
        self.password = password
        self._max_retries = 5

        MANTLE_USE_SECRETS_CRED = os.getenv("MANTLE_USE_SECRETS_CRED")
        MANTLE_SECRET_CRED_ARN = os.getenv("MANTLE_SECRET_CRED_ARN")
        if MANTLE_USE_SECRETS_CRED is not None and MANTLE_SECRET_CRED_ARN is not None:
            mantle_creds = self.get_secret(MANTLE_SECRET_CRED_ARN)
            self.email = mantle_creds.get("email")
            self.password = mantle_creds.get("password")
        else:
            if not self.email:
                self.email = os.getenv("MANTLE_USER")
            if not self.password:
                self.password = os.getenv("MANTLE_PASSWORD")

    def authenticate(self, mantle_api: str = MANTLE_PROD_API):
        """Authenticate the session object with a password

        Args:
          mantle_api (str): URL of the Mantle API

        Returns:
          dict: response from the API
        """
        if not (self.email and self.password):
            # prompt user to enter credentials
            self.email = input("Email: ")
            self.password = getpass()

        base_delay = 1
        max_total_delay = 600  # Maximum total delay in seconds (10 minutes)
        total_delay = 0
        for attempt in range(self._max_retries):
            data = requests.post(mantle_api + '/signin',
                                 json={'email': self.email, 'password': self.password})

            if data.status_code < 300:
                self._access_token = data.json()["access_token"]
                return data

            elif data.status_code in [500, 502, 503, 504, 401, 400, 403]:
                # Calculate delay with jitter
                delay = base_delay * (2 ** attempt)
                jitter = random.uniform(0, delay)
                delay_with_jitter = delay + jitter

                # Ensure the cumulative delay does not exceed max_total_delay
                if total_delay + delay_with_jitter > max_total_delay:
                    delay_with_jitter = max_total_delay - total_delay

                total_delay += delay_with_jitter

                print(
                    f"Transient error received ({data.status_code}), retrying in {delay_with_jitter:.2f} seconds... (total delay: {total_delay:.2f} seconds)")
                time.sleep(delay_with_jitter)

                if total_delay >= max_total_delay:
                    break

                continue

        raise MantleRetriesExceededError("Maximum retries exceeded")

    def get_token(self):
        if self._access_token:
            return self._access_token
        else:
            self.authenticate()
            return self._access_token


class JwtCredentials(AuthMethod):
    """Object for storing JWT credentials"""

    def __init__(self, jwt: str) -> None:
        self.jwt = jwt

    def authenticate(self, mantle_api: str = MANTLE_PROD_API):
        '''
        Authenticate the session object with a JWT

        Args:
            mantle_api (str): URL of the Mantle API

        Returns:
            dict: response from the API
        '''
        data = requests.get(mantle_api + '/user', headers={
            'Authorization': f'Bearer {self.jwt}'})
        if data.status_code < 300:
            return data
        else:
            raise Exception("Error authenticating with JWT")

    def get_token(self):
        return self.jwt

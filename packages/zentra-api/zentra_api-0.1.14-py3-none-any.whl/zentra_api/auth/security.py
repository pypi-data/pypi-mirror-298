"""
Security classes and methods for Zentra API projects.
"""

from datetime import datetime, timedelta, timezone
from typing import Literal

from zentra_api.core.config import AuthConfig
from zentra_api.responses import exceptions

import jwt
from pydantic import BaseModel


TokenTypeLiteral = Literal["access", "refresh"]


class SecurityUtils(BaseModel):
    """
    Contains utility methods for managing user authentication.

    Parameters:
        auth (AuthConfig): a Zentra API AuthConfig model
    """

    auth: AuthConfig

    def hash_password(self, password: str) -> str:
        """
        Uses the pwd_context to hash a password.

        Parameters:
            password (str): a plain text password

        Returns:
            str: a hashed password
        """
        return self.auth.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Uses the pwd_context to verify a password.

        Parameters:
            plain_password (str): a plain text password
            hashed_password (str): a hashed password

        Returns:
            bool: True if the password is valid, False otherwise
        """
        return self.auth.pwd_context.verify(plain_password, hashed_password)

    def expiration(
        self, token_type: TokenTypeLiteral, expires_delta: timedelta | None = None
    ) -> datetime:
        """
        Creates an expiration datetime object for a JWT token. If `expires_delta=None`, automatically generates one using environment variables.

        Parameters:
            token_type (TokenTypeLiteral): the type of token to create. Options: `['access', 'refresh']`
            expires_delta (timedelta): a timedelta object representing the expiration time

        Returns:
            datetime: a datetime object representing the expiration time
        """
        if expires_delta:
            return datetime.now(timezone.utc) + expires_delta

        return datetime.now(timezone.utc) + self.expire_mins(token_type)

    def expire_mins(self, token_type: TokenTypeLiteral) -> timedelta:
        """
        Returns the token expire minutes as a timedelta.

        Parameters:
            token_type (TokenTypeLiteral): the type of token to create. Options: `['access', 'refresh']`

        Returns:
            timedelta: a timedelta object representing the expiration time
        """
        mins = (
            self.auth.ACCESS_TOKEN_EXPIRE_MINS
            if token_type == "access"
            else self.auth.REFRESH_TOKEN_EXPIRE_MINS
        )
        return timedelta(minutes=mins)

    def encrypt(self, model: BaseModel, attributes: str | list[str]) -> BaseModel:
        """
        Encrypts a set of data in a model and returns it as a new model.

        Parameters:
            model (BaseModel): a Pydantic BaseModel object
            attributes (str | list[str]): a string or list of strings representing the attributes to encrypt

        Returns:
            BaseModel: a new BaseModel object with the encrypted data
        """
        if isinstance(attributes, str):
            attributes = [attributes]

        data = model.model_dump()
        for attr in attributes:
            try:
                hashed_value = self.hash_password(getattr(model, attr))
                data[attr] = hashed_value

            except AttributeError:
                raise AttributeError(f"'{attr}' does not exist in '{type(model)}'!")

        return type(model)(**data)

    def _create_token(
        self,
        data: dict,
        secret_key: str,
        token_type: TokenTypeLiteral,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        A helper method for creating JWT tokens.

        Parameters:
            data (dict): a dictionary of data to encrypt
            secret_key (str): the secret key to use for encryption
            token_type (TokenTypeLiteral): the type of token to create. Options: `['access', 'refresh']`
            expires_delta (timedelta): a timedelta object representing the expiration time

        Returns:
            str: a JWT token
        """
        payload = data.copy()
        expire = self.expiration(token_type, expires_delta)

        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload,
            key=secret_key,
            algorithm=self.auth.ALGORITHM,
        )
        return encoded_jwt

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """
        Creates a JWT access token for the given data and returns it.

        Parameters:
            data (dict): a dictionary of data to encrypt
            expires_delta (timedelta): a timedelta object representing the expiration time

        Returns:
            str: a JWT access token
        """
        return self._create_token(
            data,
            secret_key=self.auth.SECRET_ACCESS_KEY,
            token_type="access",
            expires_delta=expires_delta,
        )

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """
        Creates a JWT refresh token for the given data and returns it.

        Parameters:
            data (dict): a dictionary of data to encrypt
            expires_delta (timedelta): a timedelta object representing the expiration time

        Returns:
            str: a JWT refresh token
        """
        return self._create_token(
            data,
            secret_key=self.auth.SECRET_REFRESH_KEY,
            token_type="refresh",
            expires_delta=expires_delta,
        )

    def _verify_token(self, token: str, secret_key: str) -> str:
        """
        A helper method for verifying the validity of a JWT token. Returns the token data if valid.

        Parameters:
            token (str): a JWT token
            secret_key (str): the secret key to use for decryption

        Returns:
            str: the token data
        """
        try:
            payload: dict = jwt.decode(
                token,
                key=secret_key,
                algorithms=[self.auth.ALGORITHM],
            )
            token_data: str | None = payload.get("sub")

            if token_data is None:
                raise exceptions.INVALID_CREDENTIALS

            return token_data

        except jwt.InvalidTokenError:
            raise exceptions.INVALID_CREDENTIALS

    def verify_access_token(self, token: str) -> str:
        """
        Verifies the validity of a JWT access token. Returns the token data if valid.

        Parameters:
            token (str): a JWT access token

        Returns:
            str: the token data
        """
        return self._verify_token(token, secret_key=self.auth.SECRET_ACCESS_KEY)

    def verify_refresh_token(self, token: str) -> str:
        """
        Verifies the validity of a JWT refresh token. Returns the token data if valid.

        Parameters:
            token (str): a JWT refresh token

        Returns:
            str: the token data
        """
        return self._verify_token(token, secret_key=self.auth.SECRET_REFRESH_KEY)

# SimpleSocialAuthLib


Je suis entrain de crée une lib python pour facilité les connexion avec social auth.

Voici mon:

```py
# src/simplesocialauthlib/abstract.py

from abc import ABC, abstractmethod
from collections.abc import Mapping
from enum import StrEnum
from typing import Any, Generic, TypeVar

T = TypeVar("T", bound=Mapping[str, Any])


class Providers(StrEnum):
    APPLE = "apple"
    FACEBOOK = "facebook"
    GITHUB = "github"
    GOOGLE = "google"
    LINKEDIN = "linkedin"
    MICROSOFT = "microsoft"
    TWITTER = "twitter"


class SocialAuthAbstract(ABC, Generic[T]):
    """
    Abstract class for social authentication.

    This class defines the interface for all social authentication providers.
    Each provider should implement these methods according to their specific API.
    """

    provider: Providers

    @abstractmethod
    def exchange_code_for_access_token(self, code: str) -> str:
        """
        Exchange the authorization code for an access token.

        Args:
            code (str): The authorization code received from the OAuth provider.

        Returns:
            str: The access token.

        Raises:
            CodeExchangeError: If the authorization code is invalid or the exchange fails.
        """
        pass

    @abstractmethod
    def retrieve_user_data(self, access_token: str) -> T:
        """
        Retrieve the user data from the social network.

        Args:
            access_token (str): The access token obtained from exchange_code_for_access_token.

        Returns:
            T: The user data in a provider-specific format.

        Raises:
            UserDataRetrievalError: If the access token is invalid or the data retrieval fails.
        """
        pass

    def sign_in(self, code: str) -> T:
        """
        Complete the sign-in process by exchanging the code for a token and retrieving user data.

        Args:
            code (str): The authorization code received from the OAuth provider.

        Returns:
            T: The user data in a provider-specific format.

        Raises:
            CodeExchangeError: If the code exchange fails.
            UserDataRetrievalError: If the user data retrieval fails.
        """
        access_token = self.exchange_code_for_access_token(code=code)
        return self.retrieve_user_data(access_token=access_token)
```

```py
# src/simplesocialauthlib/exceptions.py

from typing import Any


class ApplicationError(Exception):
    def __init__(self, message: str, extra: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


class TokenInvalidError(ApplicationError):
    pass


class CodeExchangeError(ApplicationError):
    pass


class UserDataRetrievalError(ApplicationError):
    pass


class ConfigurationError(ApplicationError):
    pass
```

```py
# src/simplesocialauthlib/types.py

from typing import Annotated, TypedDict


class GoogleUserData(TypedDict):
    first_name: Annotated[str, "Corresponds to 'given_name' in Google API"]
    last_name: Annotated[str, "Corresponds to 'family_name' in Google API"]
    full_name: Annotated[str | None, "Corresponds to 'name' in Google API"]
    email: Annotated[str, "Corresponds to 'email' in Google API"]
    email_verified: Annotated[bool, "Corresponds to 'email_verified' in Google API"]
    picture: Annotated[str | None, "Corresponds to 'picture' in Google API"]


class GithubUserData(TypedDict):
    username: Annotated[str, "Corresponds to 'login' in GitHub API"]
    full_name: Annotated[str, "Corresponds to 'name' in GitHub API"]
    email: Annotated[str, "Corresponds to 'email' in GitHub API"]
    picture: Annotated[str | None, "Corresponds to 'avatar_url' in GitHub API"]
    bio: Annotated[str | None, "Corresponds to 'bio' in GitHub API"]
    location: Annotated[str | None, "Corresponds to 'location' in GitHub API"]
```

```py
# src/simplesocialauthlib/utils.py

import logging
from collections.abc import Callable
from typing import Any

from requests.exceptions import HTTPError, RequestException

logger = logging.getLogger(__name__)


def handle_request_exceptions(action: str, error_cls: type[Exception]) -> Callable[..., Callable[..., Any]]:
    """
    Handle common request exceptions for social auth providers.

    Args:
        action (str): The action being performed (e.g., 'code exchange', 'user data retrieval').
        error_cls (Exception): The exception class to raise (e.g., CodeExchangeError, UserDataRetrievalError).

    Returns:
        A function to be used as a decorator for handling exceptions.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
            try:
                return func(*args, **kwargs)
            except HTTPError as http_err:
                logger.error(f"HTTP error during {action}: {http_err}")
                raise error_cls(f"HTTP error during {action}") from http_err
            except RequestException as req_err:
                logger.error(f"Request exception during {action}: {req_err}")
                raise error_cls(f"Request exception during {action}") from req_err
            except Exception as err:
                logger.error(f"Unexpected error during {action}: {err}")
                raise error_cls(f"Unexpected error during {action}") from err

        return wrapper

    return decorator
```

```py
# src/simplesocialauthlib/providers/google.py

import logging
from typing import Final, cast, override

from google.auth.exceptions import GoogleAuthError
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from requests_oauthlib import OAuth2Session

from simplesocialauthlib.abstract import Providers, SocialAuthAbstract
from simplesocialauthlib.exceptions import CodeExchangeError, UserDataRetrievalError
from simplesocialauthlib.types import GoogleUserData
from simplesocialauthlib.utils import handle_request_exceptions

logger = logging.getLogger(__name__)


class GoogleSocialAuth(SocialAuthAbstract[GoogleUserData]):
    """
    Google authentication provider.

    This class implements the SocialAuthAbstract for Google OAuth2 authentication.
    It handles the OAuth2 flow and retrieves user data from Google.

    Attributes:
        client_id (str): The Google OAuth2 client ID.
        client_secret (str): The Google OAuth2 client secret.
        redirect_uri (str): The redirect URI for the OAuth2 flow.
        provider (Providers): The provider enum for Google.
        GOOGLE_SCOPES (list[str]): The scopes for Google OAuth2 authentication.
        GOOGLE_TOKEN_ENDPOINT (str): The endpoint for exchanging the authorization code for an access token.

    Example:
        auth = GoogleSocialAuth(client_id="your_id", client_secret="your_secret", redirect_uri="your_uri")\n
        user_data = auth.sign_in(code="received_code")
    """

    provider = Providers.GOOGLE
    GOOGLE_SCOPES: list[str] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
    GOOGLE_TOKEN_ENDPOINT: Final[str] = "https://oauth2.googleapis.com/token"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @override
    @handle_request_exceptions("code exchange", CodeExchangeError)
    def exchange_code_for_access_token(self, code: str) -> str:
        oauth2_session = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=GoogleSocialAuth.GOOGLE_SCOPES,
        )
        token = oauth2_session.fetch_token(
            token_url=GoogleSocialAuth.GOOGLE_TOKEN_ENDPOINT,
            client_secret=self.client_secret,
            code=code,
        )
        if "id_token" not in token:
            logger.error(f"Invalid token response: {token}")
            raise CodeExchangeError("Invalid token response: missing 'id_token'")
        return cast(str, token["id_token"])

    @override
    @handle_request_exceptions("user data retrieval", UserDataRetrievalError)
    def retrieve_user_data(self, access_token: str) -> GoogleUserData:
        try:
            id_info = id_token.verify_oauth2_token(
                id_token=access_token,
                request=Request(),
                audience=self.client_id,
            )
            if "accounts.google.com" not in id_info.get("iss", ""):
                logger.error(f"Invalid token issuer: {id_info.get('iss')}")
                raise ValueError("Invalid token issuer")

            return GoogleUserData(
                first_name=id_info["given_name"],
                last_name=id_info["family_name"],
                full_name=id_info["name"],
                email=id_info["email"],
                picture=id_info.get("picture"),
                email_verified=id_info["email_verified"],
            )
        except GoogleAuthError as auth_err:
            logger.error(f"Google authentication error: {auth_err}")
            raise UserDataRetrievalError("Google authentication error") from auth_err
```

```py
# src/simplesocialauthlib/providers/github.py

import logging
from typing import Final, cast, override

import requests

from simplesocialauthlib.abstract import Providers, SocialAuthAbstract
from simplesocialauthlib.exceptions import CodeExchangeError, UserDataRetrievalError
from simplesocialauthlib.types import GithubUserData
from simplesocialauthlib.utils import handle_request_exceptions

logger = logging.getLogger(__name__)


class GithubSocialAuth(SocialAuthAbstract[GithubUserData]):
    """
    Github authentication provider.

    This class implements the SocialAuthAbstract for Github OAuth2 authentication.
    It handles the OAuth2 flow and retrieves user data from Github.

    Attributes:
        client_id (str): The Github OAuth2 client ID.
        client_secret (str): The Github OAuth2 client secret.
        provider (Providers): The provider enum for Github.
        GITHUB_TOKEN_ENDPOINT (str): The endpoint for exchanging the authorization code for an access token.
        GITHUB_USER_INFO_ENDPOINT (str): The endpoint for retrieving user data.

    Example:
        auth = GithubSocialAuth(client_id="your_id", client_secret="your_secret")\n
        user_data = auth.sign_in(code="received_code")
    """

    provider: Providers = Providers.GITHUB
    GITHUB_TOKEN_ENDPOINT: Final[str] = "https://github.com/login/oauth/access_token"
    GITHUB_USER_INFO_ENDPOINT: Final[str] = "https://api.github.com/user"

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    @override
    @handle_request_exceptions("code exchange", CodeExchangeError)
    def exchange_code_for_access_token(self, code: str) -> str:
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
        }
        headers = {"Accept": "application/json"}
        response = requests.post(url=self.GITHUB_TOKEN_ENDPOINT, data=payload, headers=headers)
        response.raise_for_status()
        token_response = response.json()
        if "access_token" not in token_response:
            logger.error(f"Invalid token response: {token_response}")
            raise CodeExchangeError("Invalid token response: missing 'access_token'")
        return cast(str, token_response["access_token"])

    @override
    @handle_request_exceptions("user data retrieval", UserDataRetrievalError)
    def retrieve_user_data(self, access_token: str) -> GithubUserData:
        response = requests.get(
            url=self.GITHUB_USER_INFO_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        user_data = response.json()

        return GithubUserData(
            username=user_data["login"],
            full_name=user_data["name"],
            email=user_data["email"],
            picture=user_data["avatar_url"],
            bio=user_data.get("bio"),
            location=user_data.get("location"),
        )
```

comment je faire les tests ?

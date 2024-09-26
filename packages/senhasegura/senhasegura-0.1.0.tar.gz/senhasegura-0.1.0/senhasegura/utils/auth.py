from requests_oauthlib import OAuth1, OAuth2Session
from typing import Dict, Union

class Auth:
    def __init__(self, auth_type: str, **auth_params: Dict[str, str]) -> None:
        self.__auth_methods = {
            "OAuth1": self.__get_oauth1,
            "OAuth2": self.__get_oauth2
        }
        self.__auth_type = auth_type
        self.__auth = self._setup_auth(auth_type, **auth_params)

    def __get_oauth1(self, **auth_params: Dict[str, str]) -> OAuth1:
        return OAuth1(auth_params["consumer_key"], auth_params["consumer_secret"],
                      auth_params["token_key"], auth_params["token_secret"])

    def __get_oauth2(self, **auth_params: Dict[str, str]) -> OAuth2Session:
        return OAuth2Session(**auth_params)

    def _validate_auth_params(self, auth_params: Dict[str, str]) -> Dict[str, str]:
        valid_params = {"OAuth1": ["consumer_key", "consumer_secret", "token_key", "token_secret"],
                        "OAuth2": ["client_id", "token"]}

        if self.__auth_type not in valid_params:
            raise ValueError(f'Invalid auth type: "{self.__auth_type}"')

        errors = []

        for param in valid_params[self.__auth_type]:
            if param not in auth_params:
                errors.append(f'Missing parameter: "{param}"')
            elif not isinstance(auth_params[param], str):
                errors.append(f'Parameter "{param}" must be a string')

        for param in auth_params:
            if param not in valid_params[self.__auth_type]:
                errors.append(f'Invalid parameter: "{param}"')

        if errors:
            raise ValueError("\n".join(errors))

        return auth_params

    def _setup_auth(self, auth_type: str, **auth_params: Dict[str, str]) -> Union[OAuth1, OAuth2Session]:
        if auth_type not in self.__auth_methods:
            raise ValueError(f'Invalid auth type: "{auth_type}", valid types: {", ".join(self.__auth_methods.keys())}')

        return self.__auth_methods[auth_type](**self._validate_auth_params(auth_params))

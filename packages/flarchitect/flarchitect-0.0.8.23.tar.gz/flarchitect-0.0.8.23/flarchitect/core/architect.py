import importlib
import os
from functools import wraps
from pathlib import Path
from typing import Optional, List, Type, Callable

from flask import Flask
from flask_jwt_extended import jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from marshmallow import Schema
from sqlalchemy.orm import DeclarativeBase

from flarchitect.logging import logger
from flarchitect.utils.general import (
    AttributeInitializerMixin,
    check_rate_services,
    validate_flask_limiter_rate_limit_string,
)
from flarchitect.utils.config_helpers import get_config_or_model_meta
from flarchitect.utils.decorators import handle_many, handle_one
from flarchitect.core.routes import find_rule_by_function, RouteCreator
from flarchitect.specs.generator import CustomSpec

FLASK_APP_NAME = "flarchitect"


class Architect(AttributeInitializerMixin):
    app: Flask
    api_spec: Optional[CustomSpec] = None
    api: Optional["RouteCreator"] = None
    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    route_spec: List = []
    limiter: Limiter

    def __init__(self, app: Optional[Flask] = None, *args, **kwargs):
        """
        Initializes the Architect object.

        Args:
            app (Flask): The flask app.
            *args (list): List of arguments.
            **kwargs (dict): Dictionary of keyword arguments.
        """
        if app is not None:
            self.init_app(app, *args, **kwargs)
            logger.verbosity_level = self.get_config("API_VERBOSITY_LEVEL", 0)

    def init_app(self, app: Flask, *args, **kwargs):
        """
        Initializes the Architect object.

        Args:
            app (Flask): The flask app.
            *args (list): List of arguments.
            **kwargs (dict): Dictionary of keyword arguments.
        """
        super().__init__(app=app, *args, **kwargs)
        self._register_app(app)
        logger.verbosity_level = self.get_config("API_VERBOSITY_LEVEL", 0)
        self.api_spec = None

        if self.get_config("FULL_AUTO", True):
            self.init_api(app=app, **kwargs)
        if get_config_or_model_meta("API_CREATE_DOCS", default=True):
            self.init_apispec(app=app, **kwargs)

        logger.log(2, "Creating rate limiter")
        storage_uri = check_rate_services()
        self.app.config["RATELIMIT_HEADERS_ENABLED"] = True
        self.app.config["RATELIMIT_SWALLOW_ERRORS"] = True
        self.app.config["RATELIMIT_IN_MEMORY_FALLBACK_ENABLED"] = True
        self.limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            storage_uri=storage_uri if storage_uri else None,
        )

    def _register_app(self, app: Flask):
        """
        Registers the app with the extension, and saves it to self.

        Args:
            app (Flask): The flask app.
        """
        if FLASK_APP_NAME not in app.extensions:
            app.extensions[FLASK_APP_NAME] = self
        self.app = app

    def init_apispec(self, app: Flask, **kwargs):
        """
        Initializes the api spec object.

        Args:
            app (Flask): The flask app.
            **kwargs (dict): Dictionary of keyword arguments.
        """
        self.api_spec = CustomSpec(app=app, architect=self, **kwargs)

    def init_api(self, **kwargs):
        """
        Initializes the api object, which handles flask route creation for models.

        Args:
            **kwargs (dict): Dictionary of keyword arguments.
        """
        self.api = RouteCreator(architect=self, **kwargs)

    def to_api_spec(self):
        """
        Returns the api spec object.

        Returns:
            APISpec: The api spec json object.
        """
        if self.api_spec:
            return self.api_spec.to_dict()

    def get_config(self, key, default: Optional = None):
        """
        Gets a config value from the app config.

        Args:
            key (str): The key of the config value.
            default (Optional): The default value to return if the key is not found.

        Returns:
            Any: The config value.
        """
        if self.app:
            return self.app.config.get(key, default)

    def schema_constructor(
        self,
        output_schema: Optional[Type[Schema]] = None,
        input_schema: Optional[Type[Schema]] = None,
        model: Optional[DeclarativeBase] = None,
        group_tag: Optional[str] = None,
        many: Optional[bool] = False,
        **kwargs,
    ) -> Callable:
        """
        Decorator to specify OpenAPI metadata for an endpoint, along with schema information for the input and output.

        Args:
            output_schema (Optional[Type[Schema]], optional): Output schema. Defaults to None.
            input_schema (Optional[Type[Schema]], optional): Input schema. Defaults to None.
            model (Optional[DeclarativeBase], optional): Database model. Defaults to None.
            group_tag (Optional[str], optional): Group name. Defaults to None.
            many (Optional[Bool], optional): Is many or one? Defaults to False
            kwargs (dict): Dictionary of keyword arguments.

        Returns:
            Callable: The decorated function.
        """

        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapped(*_args, **_kwargs):
                f_decorated = f

                auth_method = get_config_or_model_meta(
                    "API_AUTHENTICATE",
                    model=model,
                    output_schema=output_schema,
                    input_schema=input_schema,
                    default=False,
                )

                def jwt_authentication(func):
                    @wraps(func)
                    def auth_wrapped(*args, **kwargs):
                        return func(*args, **kwargs)

                    return auth_wrapped

                if auth_method == "jwt":
                    f_decorated = jwt_authentication(f_decorated)
                elif auth_method == "basic":
                    f_decorated = None  # authentication(f_decorated)
                elif auth_method == "api_key":
                    f_decorated = None  # authentication(f_decorated)

                f_decorated = (
                    handle_many(output_schema, input_schema)(f_decorated)
                    if many
                    else handle_one(output_schema, input_schema)(f_decorated)
                )

                rl = get_config_or_model_meta(
                    "API_RATE_LIMIT",
                    model=model,
                    input_schema=input_schema,
                    output_schema=output_schema,
                    default=False,
                )
                if (
                    rl
                    and isinstance(rl, str)
                    and validate_flask_limiter_rate_limit_string(rl)
                ):
                    f_decorated = self.limiter.limit(rl)(f_decorated)
                elif rl:
                    rule = find_rule_by_function(self, f).rule
                    logger.error(
                        f"Rate limit definition not a string or not valid. Skipping for `{rule}` route."
                    )

                result = f_decorated(*_args, **_kwargs)
                return result

            route_info = {
                "function": wrapped,
                "output_schema": output_schema,
                "input_schema": input_schema,
                "model": model,
                "group_tag": group_tag,
                "tag": kwargs.get("tag"),
                "summary": kwargs.get("summary"),
                "error_responses": kwargs.get("error_responses"),
                "many_to_many_model": kwargs.get("many_to_many_model"),
                "multiple": many or kwargs.get("multiple"),
                "parent": kwargs.get("parent_model"),
            }

            self.set_route(route_info)
            return wrapped

        return decorator

    @classmethod
    def get_templates_path(cls, folder_name="html", max_levels=3):
        """
        Recursively searches for the folder_name in the source directory
        or its parent directories up to max_levels levels.

        Args:
            folder_name (str): The name of the folder to search for. Default is "html".
            max_levels (int): Maximum number of levels to search upwards. Default is 3.

        Returns:
            str: The path to the folder if found, else None.
        """
        # Find the source directory of the class/module
        spec = importlib.util.find_spec(cls.__module__)
        source_dir = Path(os.path.split(spec.origin)[0])

        # Traverse up to max_levels levels
        for level in range(max_levels):
            # Search for the folder in the current directory
            potential_path = source_dir / folder_name
            if potential_path.exists() and potential_path.is_dir():
                return str(potential_path)

            # Move to the parent directory for the next level search
            source_dir = source_dir.parent

        # Return None if the folder is not found
        return None

    def set_route(self, route: dict):
        """
        Adds a route to the route spec list, which is used to generate the api spec.

        Args:
            route (dict): The route object.
        """
        if not hasattr(route["function"], "_decorators"):
            route["function"]._decorators = []

        route["function"]._decorators.append(self.schema_constructor)
        self.route_spec.append(route)

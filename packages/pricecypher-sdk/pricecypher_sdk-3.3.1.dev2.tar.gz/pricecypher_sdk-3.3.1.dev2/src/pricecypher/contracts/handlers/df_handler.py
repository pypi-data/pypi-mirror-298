from abc import abstractmethod
from typing import Any, Optional

import pandas as pd

from .base_handler import BaseHandler
from pricecypher.dataclasses import HandlerSettings
from pricecypher.enums import AccessTokenGrantType
from pricecypher.oidc import AccessTokenGenerator
from pricecypher.storage import FileStorage


class DataFrameHandler(BaseHandler):
    """
    The top-level, abstract BaseHandler class serves as an interaction contract such that by extending it with its
        methods implemented, any (event) handler script can be created that can be used in a generalized yet controlled
        setting.
    NB: This is the most general task handler. Hence, it is intended to be executable in all available runtimes. So
        for (possibly) long-running tasks during e.g. an intake workflow, as well as more "real-time" tasks like
        handling an HTTP request, and any other type of task that might be needed in the future.
        In general, this generic BaseHandler as well as (most of) its subclasses intend to abstract away from the
        specific source of the event that triggers the task execution. To that end, a "runtime" has to be defined once
        for each possible event source (e.g. HTTP request, Argo workflow step, Kafka event message, etc.). Such runtime
        should be able to execute any handler that implements (a subclass of) this BaseHandler class.
        Please see the subclasses of this BaseHandler for a given, specific, task at hand since using the most specific
        handler contract should simplify the specific handler implementation.
    """

    _dataset_id: int
    _settings: HandlerSettings
    _config: dict[str, dict[str, Any]]
    _token_generator: AccessTokenGenerator
    _file_storage: FileStorage

    def get_allowed_access_token_grant_types(self) -> set[AccessTokenGrantType]:
        """
        Defines the allowed access token grant types of (the children of) this event handler class.
        """
        return set()

    def get_config_dependencies(self) -> dict[str, list[str]]:
        """
        Fetch the configuration sections and keys in the sections that the script will use that are not yet provided.

        NB: It is not needed to return all required sections and keys, only at least one that has not been provided yet.
        If all required config is provided, an empty dictionary is to be returned.

        NBB: Note that this allows for a dynamic config dependency. I.e., this enables a task handler to determine
        which parts of the configuration are required based on the concrete values that are configured as part of the
        rest of that same configuration. On the other hand, a "static" config dependency can simply be expressed by
        returning the difference between the desired static config and the given config dict within this instance.

        :return: dictionary mapping from section key (string) to a (potentially empty) list of keys of that section
            that the script requires additionally.
        """
        return dict()

    def handle(self, user_input: dict[str, Any]) -> any:
        """
        Handle the given `user_input`.

        NB: All required config dependencies are assumed to be present.

        :param user_input: Dictionary of additional json-serializable input provided as input to the task being handled,
            provided by the caller of the script.
        :return: Any json-serializable task results / outputs.
        """
        path_in: Optional[str] = user_input.get('path_in', None)
        path_out: Optional[str] = user_input.get('path_out', None)
        if path_in is None or path_out is None:
            raise 'TODO'

        with self._file_storage.load(path_in, 'rb') as f:
            df = pd.read_pickle(f)

        df_processed = self.process_df(df)

        with self._file_storage.save(path_out, 'wb') as f:
            pd.to_pickle(df_processed, f)

        return self._file_storage.get_path_remote(path_out)

    @abstractmethod
    def process_df(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

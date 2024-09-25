from enum import Enum


# TODO: sync this code with the backend code, exact same enum is found there.
# HACK: we have 2 separate enums keep it simple. Eventually a single source
# of truth would be better.
class AuthCompatibleFeatures(Enum):
    """
    List the available features for which we can enable nginx authentication
    """

    ANALYTICS = "analytics"
    MAIN_APP = "main_app"

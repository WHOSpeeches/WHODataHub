from . import utils
from .dtypes import settings

class RetrieveSpeeches:

    def __init__(self, settings: settings):
        """
        Get all the WHO's Director General's Speeches.
        Parameters
        ----------
        settings : dtypes.settings
            The settings for the process
        """
        self._settings = settings

    def init(self) -> None:
        self._settings.validate()
        self._settings.init()

    def retrieve(self) -> None:
        # get last speech from disk
        # get list of all speeches from the web
        # download all speeches not downloaded
        # convert all speeches to txt files
        speeches_cache = utils.cached_api_speeches(self._settings.metadata_json)
        speeches_cache = utils.progress_overlay("Reviewing cache", speeches_cache)
        speeches_cache_urls = utils.extract_urls(speeches_cache)
        skip = len(set(speeches_cache_urls))
        speeches_live = utils.api_speeches(skip)
        speeches_live = utils.progress_overlay("Listing speeches", speeches_live)
        speeches_live = utils.cache_api_speeches(self._settings.metadata_json, speeches_live)
        for _ in speeches_live: pass

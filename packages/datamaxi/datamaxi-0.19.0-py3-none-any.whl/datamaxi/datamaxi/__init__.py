from typing import Any
from datamaxi.lib.constants import BASE_URL
from datamaxi.datamaxi.cex import Cex
from datamaxi.datamaxi.dex import Dex
from datamaxi.datamaxi.funding_rate import FundingRate
from datamaxi.datamaxi.forex import Forex
from datamaxi.datamaxi.ticker import Ticker
from datamaxi.datamaxi.premium import Premium


class Datamaxi:
    """Client to fetch unified data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL

        self.cex = Cex(api_key, **kwargs)
        self.dex = Dex(api_key, **kwargs)
        self.funding_rate = FundingRate(api_key, **kwargs)
        self.forex = Forex(api_key, **kwargs)
        self.ticker = Ticker(api_key, **kwargs)
        self.premium = Premium(api_key, **kwargs)

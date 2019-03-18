"""
Request listings for a given store from the Etsy API.
"""

import logging
import math
import time
from typing import Any, Dict, Optional

from requests_futures.sessions import FuturesSession


class EtsyShop:
    """
    Manage requests to the Etsy API for a given Etsy shop.
    Requests after the first page are made in parallel.
    """

    def __init__(self,
                 name: str,
                 api_key: str,
                 api_base_url: Optional[str] = None,
                 log_level: str = 'INFO',
                 api_max_reqs_per_sec: int = 10,
                 api_query_limit: int = 25,
                 logger: Optional[logging.Logger] = None,
                 session: Optional[FuturesSession] = None):
        self.name = name
        self.session = session or FuturesSession()
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(getattr(logging, log_level))

        self.api_key = api_key
        self.api_base_url = api_base_url or 'https://openapi.etsy.com/v2'
        self.api_query_limit = api_query_limit
        self.api_request_timeout = (1 / api_max_reqs_per_sec) + 0.05

        self.total_pages: int = 0
        self.listings: list = []

    @property
    def active_listings_url(self) -> str:
        """Return the active listings request URL."""
        return f'{self.api_base_url}/shops/{self.name}/listings/active'

    def active_listings_query_dict(self, page: int = 1) -> Dict[str, Any]:
        """Return the active listings request query params dict."""
        return dict(
            api_key=self.api_key,
            page=page,
            limit=self.api_query_limit,
        )

    def get_active_listings(self) -> 'EtsyShop':
        """
        Query the Etsy API for this shop's active listings.
        Side effect: Populates `self.listings`.
        Return self.
        """
        if self.listings:
            return self

        # Get first page of listings
        request = self._initiate_request(page_num=1)
        self._process_response(request, page_num=1)

        if self.total_pages == 1:
            return self

        # Initialize parallel requests for subsequent pages
        requests = {
            page_num: self._initiate_request(page_num)
            for page_num in range(2, self.total_pages + 1)
        }

        for page_num, request in requests.items():
            self._process_response(request, page_num)

        return self

    def _initiate_request(self, page_num: int) -> FuturesSession:
        template = '[%s] Requesting active listings page: %s'
        self.logger.info(template, self.name, page_num)

        self._buffer_request()

        url = self.active_listings_url
        query = self.active_listings_query_dict(page=page_num)
        request = self.session.get(url, params=query)

        return request

    def _process_response(self, request: FuturesSession,
                          page_num: int) -> Dict[str, Any]:
        response = self._parsed_response(request, page_num)
        self.listings.extend(response['results'])
        self.total_pages = math.ceil(response['count'] / self.api_query_limit)

        page_template = '[%s] Received page: %s of %s'
        self.logger.info(page_template, self.name, page_num, self.total_pages)

        results_template = '[%s] Received %s records'
        self.logger.debug(results_template, self.name,
                          len(response['results']))

        return response

    def _parsed_response(self, request: FuturesSession,
                         page_num: int) -> Dict[str, Any]:
        """
        Handle Request result. If request succeeds, parse JSON.
        Else, return a null dict and log the failure.
        """
        response = request.result()

        if response.status_code == 200:
            return response.json()

        template = '[%s] ERROR: Request for page %s failed with status %s'
        self.logger.info(template, self.name, page_num, response.status_code)
        return {'results': [], 'count': 0}

    def _buffer_request(self) -> None:
        """
        Sleep for the number of seconds given by self.api_request_timeout.

        Retry with exponential backoff would be closer to optimal, but
        given knowledge of the api rate limit (10 req/s), a sleep will do
        in a pinch.
        """
        time.sleep(self.api_request_timeout)

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def urllib3_retry(
    retries=5,
    backoff_factor=0.3,
    status_forcelist=(408, 429, 500, 502, 503, 504),
    method_whitelist=frozenset({"GET", "POST"}),
):
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        status=retries,
        backoff_factor=backoff_factor,
        allowed_methods=method_whitelist,
        status_forcelist=status_forcelist,
        respect_retry_after_header=True,
    )
    return retry


def requests_retry_session(
    retries=5,
    backoff_factor=0.3,
    status_forcelist=(408, 429, 500, 502, 503, 504),
    method_whitelist=frozenset({"GET", "POST"}),
    session=None,
):
    """
    Returns a `requests` session with retry capabilities for certain HTTP status codes.

    Args:
        retries (int): The number of retries for HTTP requests.
        backoff_factor (float): The backoff factor for exponential backoff during retries.
        status_forcelist (tuple): A tuple of HTTP status codes that should trigger a retry.
        method_whitelist (frozenset): The set of HTTP methods that should be retried.
        session (requests.Session, optional): An optional existing requests session to use.

    Returns:
        requests.Session: A session with retry capabilities.
    """
    # Implementation taken from https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    session = session or requests.Session()
    retry = urllib3_retry(
        retries=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        method_whitelist=method_whitelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

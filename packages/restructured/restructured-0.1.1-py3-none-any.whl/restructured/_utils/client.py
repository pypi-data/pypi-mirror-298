from typing import Optional
from restructured._generated.openapi_client import ApiClient, Configuration  # type: ignore
from restructured._utils.config import get_api_key, get_host


def get_client(
    api_key: Optional[str] = None,
    host: Optional[str] = None,
) -> ApiClient:
    if api_key is None:
        api_key = get_api_key()
    if host is None:
        host = get_host()

    if api_key is None:
        raise ValueError("No API token provided")

    configuration = Configuration(
        host=host,
        api_key={"APIKeyHeader": api_key},
    )
    client = ApiClient(configuration)
    return client

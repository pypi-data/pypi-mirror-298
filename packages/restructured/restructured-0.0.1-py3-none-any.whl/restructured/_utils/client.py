from typing import Optional
from restructured._generated.openapi_client import ApiClient, Configuration  # type: ignore
from restructured._utils.config import get_api_key, get_host


def get_client(
    api_key: Optional[str] = get_api_key(),
    host: str = get_host(),
) -> ApiClient:
    if api_key is None:
        raise ValueError("No API token provided")

    configuration = Configuration(
        host=host,
        api_key={"APIKeyHeader": api_key},
    )
    client = ApiClient(configuration)
    return client

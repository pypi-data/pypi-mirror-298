from typing import List, Literal, Dict, Any
from restructured._utils.client import get_client
from restructured._generated.openapi_client import ApiClient, DatasetApi  # type: ignore

parser_setting = Literal["fast", "accurate"]


def upload_datapoints(
    dataset_id: int,
    file_paths: List[str],
    parser_setting: parser_setting = "fast",
    client: ApiClient = get_client(),
) -> None:
    api_instance = DatasetApi(client)
    api_instance.add_datapoints_api_v1_dataset_dataset_id_add_put(
        dataset_id, file_paths, parser_setting
    )


def download_dataset(
    dataset_id: int,
    client: ApiClient = get_client(),
) -> List[Dict[str, Any]]:
    api_instance = DatasetApi(client)
    response = api_instance.get_api_v1_dataset_dataset_id_get(dataset_id)
    return response

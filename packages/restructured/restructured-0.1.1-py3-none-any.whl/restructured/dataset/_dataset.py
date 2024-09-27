from typing import List, Literal, Dict, Any, Optional
from restructured._utils.client import get_client
from restructured._generated.openapi_client import ApiClient, DatasetApi  # type: ignore

ParserSetting = Literal["fast", "accurate"]
INTERNAL_FIELDS = ["_datapoint_id", "_kolena_data_type"]


def _process_datapoints(datapoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    processed_datapoints = [
        {
            k: v.get("value") if isinstance(v, dict) else v
            for k, v in dp.items()
            if k not in INTERNAL_FIELDS
        }
        for dp in datapoints
    ]

    return processed_datapoints


def upload_datapoints(
    dataset_id: int,
    file_paths: List[str],
    parser_setting: ParserSetting = "fast",
    client: Optional[ApiClient] = None,
) -> None:
    if client is None:
        client = get_client()
    api_instance = DatasetApi(client)
    api_instance.add_datapoints_api_v1_dataset_dataset_id_add_put(
        dataset_id, file_paths, parser_setting
    )


def download_dataset(
    dataset_id: int,
    client: Optional[ApiClient] = None,
) -> List[Dict[str, Any]]:
    if client is None:
        client = get_client()
    api_instance = DatasetApi(client)
    response = api_instance.get_api_v1_dataset_dataset_id_get(dataset_id)
    return _process_datapoints(response.datapoints)

import io
import os
from typing import Any, Dict

import pandas as pd
import requests
from morph_lib.type import MorphApiError, SignedUrlResponse
from pandas import DataFrame


def handle_morph_response(response: requests.Response) -> Dict[str, Any]:
    if response.status_code != 200:
        raise MorphApiError(response.text)
    response_json: Dict[str, Any] = response.json()
    if (
        "error" in response_json
        and "subCode" in response_json
        and "message" in response_json
    ):
        error_message = response_json["message"]
        if response_json["error"] == "internal_server_error":
            error_message = (
                "System internal server error occurred. Please try again later."
            )
        if response_json["error"] == "notebook_error":
            if response_json["subCode"] == 2:
                error_message = "Reference cell not found. Please check the cell name and try again."
        if response_json["error"] == "storage_error":
            if response_json["subCode"] == 4:
                error_message = "Could not find data in the reference cell. Please check if the reference cell was executed successfully and retrieved the result correctly, and try again."
        if response_json["error"] == "template_error":
            if response_json["subCode"] == 3:
                error_message = "The auth connection info not found while connecting external source. Please check if the auth has not been deleted and try again."
            if response_json["subCode"] == 4 or response_json["subCode"] == 5:
                error_message = "The auth token connecting external source has been expired. Please authorize the connector and try again."
        if response_json["error"] == "external_connection_error":
            if response_json["subCode"] == 1:
                error_message = "The connector not found. Please check if the connector exists and try again."
        if response_json["error"] == "integration_error":
            if response_json["subCode"] == 1:
                error_message = "The integration not found. Please check if the integration exists and try again."
            if response_json["subCode"] == 3:
                error_message = "Authentication failed. The token is missing or invalid or expired. Please check if the token is correct and try again."
        raise MorphApiError(error_message)
    return response_json


def convert_signed_url_response_to_dataframe(
    response: SignedUrlResponse,
) -> DataFrame:
    ext = response.url.split("?")[0].split("/")[-1].split(".")[-1]
    r = requests.get(response.url)

    if ext == "csv":
        chunks = []
        for chunk in pd.read_csv(
            io.BytesIO(r.content),
            header=0,
            chunksize=1_000_000,
            encoding_errors="replace",
        ):
            chunks.append(chunk)
        return pd.concat(chunks, axis=0)  # type: ignore
    elif ext == "parquet":
        return pd.read_parquet(io.BytesIO(r.content))
    else:
        engine = "openpyxl" if ext == "xlsx" else "xlrd"
        return pd.read_excel(io.BytesIO(r.content), engine=engine, header=0, sheet_name=0)  # type: ignore


def convert_filepath_to_df(abs_path: str) -> DataFrame:
    ext = os.path.splitext(os.path.basename(abs_path))[1][1:]
    mode = "rb" if ext == "parquet" else "r"
    with open(abs_path, mode) as f:
        content = f.read()

    if ext == "csv":
        chunks = []
        for chunk in pd.read_csv(
            io.StringIO(content),
            header=0,
            chunksize=1_000_000,
            encoding_errors="replace",
        ):
            chunks.append(chunk)
        return pd.concat(chunks, axis=0)  # type: ignore
    elif ext == "parquet":
        return pd.read_parquet(io.BytesIO(content))
    else:
        engine = "openpyxl" if ext == "xlsx" else "xlrd"
        return pd.read_excel(  # type: ignore
            io.StringIO(content), engine=engine, header=0, sheet_name=0
        )

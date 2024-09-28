"""Send data from GRDF ADICT API into BEMServer

https://sites.grdf.fr/web/portail-api-grdf-adict/documentation-api-grdf-adict-production
"""

import configparser
import datetime as dt
import logging

import click
import requests
from bemserver_api_client import BEMServerApiClient
from bemserver_api_client.enums import DataFormat
from bemserver_api_client.exceptions import BEMServerAPIError
from lowatt_grdf.api import API

logger = logging.getLogger(__name__)


def get_grdf_data(config, start_date, end_date):
    """Get GRDF data"""

    grdf = API(config["CLIENT_ID"], config["CLIENT_SECRET"])

    logger.info("Get GRDF consumptions")
    try:
        resp = grdf.donnees_consos_informatives(
            config["PCE"],
            from_date=start_date.isoformat(),
            to_date=end_date.isoformat(),
        )
    except requests.exceptions.RequestException as exc:
        logger.error("Get GRDF consumptions failed")
        raise RuntimeError from exc

    logger.info("Parse GRDF response")
    data = {}
    for releve in resp:
        rel = releve["releve_fin"]["index_brut_fin"]
        date = rel["horodate_Index"]
        index = rel["valeur_index"]
        data[date] = index

    return data


def upload_data(config, data):
    """Upload data to BEMServer"""

    logger.info("Upload data to BEMServer")

    logger.info("Get auth token")
    api_client = BEMServerApiClient(config["URL"])
    auth_resp = api_client.auth.get_tokens(config["AUTH_MAIL"], config["AUTH_PASSWORD"])
    if auth_resp.data["status"] == "failure":
        logger.error("BEMServer auth data failed")
        raise RuntimeError

    api_client.set_authentication_method(
        BEMServerApiClient.make_bearer_token_auth(
            auth_resp.data["access_token"],
            auth_resp.data["refresh_token"],
        )
    )

    logger.info("Post data")
    try:
        api_client.timeseries_data.upload_by_names(
            config["CAMPAIGN_ID"],
            config["DATA_STATE_ID"],
            {config["TS_NAME"]: data},
            DataFormat.json,
        )
    except BEMServerAPIError as exc:
        error = {
            attr: getattr(exc, attr)
            for attr in ("status_code", "errors", "code")
            if getattr(exc, attr, None) is not None
        }
        logger.error("Upload data failed: %(error)s", {"error": error})
        raise RuntimeError from exc


@click.command()
@click.argument("config_file_path", type=click.Path(exists=True))
def bemserver_grdf_adict_loader(config_file_path):
    """Load GRDF Adict data into BEMServer"""
    cfg = configparser.ConfigParser()
    with open(config_file_path, encoding="utf-8") as config_fp:
        cfg.read_file(config_fp)

    logging.basicConfig(level=cfg["LOGGING"]["LEVEL"])

    now = dt.date.today()
    start = now - dt.timedelta(days=int(cfg["SCHEDULE"]["START_DAYS_DELAY"]))
    end = now - dt.timedelta(days=int(cfg["SCHEDULE"]["END_DAYS_DELAY"]))

    try:
        grdf_data = get_grdf_data(cfg["GRDF"], start, end)
        upload_data(cfg["BEMSERVER"], grdf_data)
    except RuntimeError:
        pass

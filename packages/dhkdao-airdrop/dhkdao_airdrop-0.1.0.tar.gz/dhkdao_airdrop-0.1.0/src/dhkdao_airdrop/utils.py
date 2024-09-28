import io
import json
import os


def round_number(val):
    if isinstance(val, float):
        if val < 1:  # keep 4 decimals
            return round(val, 4)
        if val < 100:  # keep 3 decimals
            return round(val, 3)
        else:  # keep 2 decimals
            return round(val, 2)
    return val


def round_output(df):
    for label, col_data in df.items():
        df[label] = col_data.apply(round_number)
    return df


def is_number(i):
    return isinstance(i, (int, float))


def get_config_with_apikey_envs(config):
    if isinstance(config, io.TextIOWrapper):
        config = json.loads(config.read())

    if os.getenv("CRYPTOCOMPARE_APIKEY") is not None:
        config["apis"]["cryptocompare"]["apikey"] = os.getenv("CRYPTOCOMPARE_APIKEY")

    if os.getenv("MINTSCAN_APIKEY") is not None:
        config["apis"]["mintscan"]["apikey"] = os.getenv("MINTSCAN_APIKEY")

    return config

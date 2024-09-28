import json
import pandas as pd
import sys
import typer
from datetime import datetime, timezone
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from rich import print
from typing import Optional

from .utils import is_number


class Airdrop:
    @classmethod
    def check_config(cls, config):
        # Check that all required fields exist
        required_keys = ["dhk_distribution", "reference_date", "tokens", "apis"]

        for key in required_keys:
            if key not in config or config[key] == "":
                print(
                    f"Required key [bold red]{key}[/bold red] is missing in the config file."
                )
                raise typer.Exit(code=1)

        return True

    def __init__(self, config):
        if Airdrop.check_config(config):
            self.config = config

        # Set to 12:00 UTC timezone of the reference_date
        self.reference_datetime = datetime.strptime(
            f"{config['reference_date']} 12:00", "%Y-%m-%d %H:%M"
        ).replace(tzinfo=timezone.utc)

    # API doc:
    #   https://min-api.cryptocompare.com/documentation?key=Historical&cat=dataPriceHistorical
    def fetch_price(self, from_symbol, to_symbol="USD") -> Optional[float]:
        api = self.config["apis"]["cryptocompare"]
        endpoint, apikey = api["endpoint"], api["apikey"]
        if endpoint is None or apikey is None:
            raise Exception(
                "fetch_price: cryptocompare API endpoint or key is missing."
            )

        parameters = {
            "fsym": from_symbol,
            "tsyms": to_symbol,
            "calculationType": "MidHighLow",
            "ts": self.reference_datetime.timestamp(),
        }
        headers = {
            "Accepts": "application/json",
            "authorization": f"Apikey {apikey}",
        }

        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(endpoint, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(f"fetch_price {from_symbol} connection error: {e}", file=sys.stderr)

        if from_symbol not in data:
            print(
                f"Unable to fetch price for {from_symbol}, returning: {data}",
                file=sys.stderr,
            )
            return None

        return float(data[from_symbol][to_symbol])

    # API doc: https://docs.cosmostation.io/apis/reference/utilities/staking-apr
    def fetch_staking_apr(self, staking_network) -> Optional[float]:
        api = self.config["apis"]["mintscan"]
        endpoint, apikey = api["endpoint"], api["apikey"]
        if endpoint is None or apikey is None:
            raise Exception(
                "fetch_staking_apr: mintscan API endpoint or key is missing."
            )

        endpoint = endpoint.replace(":network", staking_network)
        headers = {
            "Accepts": "application/json",
            "authorization": f"Bearer {apikey}",
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(endpoint)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(
                f"fetch_staking_apr {staking_network} connection error: {e}",
                file=sys.stderr,
            )

        if "apr" not in data:
            print(
                f"Unable to fetch staking_apr for {staking_network}, returning: {data}",
                file=sys.stderr,
            )
            return None

        return float(data["apr"])

    def monthly_alloc(self):
        columns = [
            "token",
            "price",
            "staking-amt",
            "staking-val",
            "staking-apr",
            "reward",
            "dhk-distribution-pc",
            "dhk-distribution",
        ]

        # Used later in panda
        lst = []

        for t in self.config["tokens"]:
            token, staking_amt = t["token"], t["qty"]
            token_price = t["price"] if "price" in t else self.fetch_price(token)

            staking_val = (
                token_price * staking_amt
                if is_number(token_price) and is_number(staking_amt)
                else None
            )

            staking_apr = None
            if "staking-apr" in t:
                staking_apr = t["staking-apr"]
            elif "network" in t:
                staking_apr = self.fetch_staking_apr(t["network"])

            # NX> handles TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'
            reward = (
                staking_apr * staking_val
                if is_number(staking_apr) and is_number(staking_val)
                else None
            )

            lst.append(
                [
                    token,
                    token_price,
                    staking_amt,
                    staking_val,
                    staking_apr,
                    reward,
                    0,
                    0,
                ]
            )

        # Panda dataframe
        df = pd.DataFrame(lst, columns=columns)

        # Append a total row at the end of the table
        ttl_staking_val = df["staking-val"].sum()
        ttl_reward = df["reward"].sum()
        ttl = pd.Series(
            {"token": "TOTAL", "staking-val": ttl_staking_val, "reward": ttl_reward}
        )
        df = pd.concat([df, ttl.to_frame().T], ignore_index=True)

        # Calculate DHK distribution and distribution percent
        for idx, row in df.iterrows():
            df.at[idx, "dhk-distribution-pc"] = (
                (row["reward"] / ttl_reward) * 100
                if is_number(row["reward"]) and ttl_reward > 0
                else None
            )
            df.at[idx, "dhk-distribution"] = (
                (row["reward"] / ttl_reward) * self.config["dhk_distribution"]
                if is_number(row["reward"]) and ttl_reward > 0
                else None
            )

        return df

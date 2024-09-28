# DHK Tokens Airdrop Scripts

A Python script to retrieve historical token prices and compute DHK tokens to distribute out each month.

Output example

![ss-example](./docs/ss-example.png)

The key output is the table at the bottom. It can also be exported as csv or json.

It is fine to see error messages as above saying unable to fetch price and  staking apr for some tokens, as they may not be popular enough or not indexed by the service providers we used.

## Usage

```bash
pip install dhkdao-airdrop

# Get help
dhkdao-airdrop --help

# Run script with api keys set in config.json
dhkdao-airdrop config.json -o output -t type

# Run script with api keys set in env vars
CRYPTOCOMPARE_APIKEY="cc-apikey" MINTSCAN_APIKEY="ms-apikey" dhkdao-airdrop config.json -o output -t type
```

Options:

- `-o`: Output file path. If skipped, output is printed on screen.
- `-t`: [table|csv|json]. Output type.

You can have api keys set in the input config file or env var. Env vars will override the one set in config file.

### Input Config

An input config example is follows.

```json
{
    "dhk_distribution": 100000,
    "reference_date": "2024-08-27",
    "tokens": [
        { "token": "AKT", "network": "akash", "qty": 188787 },
        { "token": "ATOM", "network": "cosmos", "qty": 592015 }
    ],
    "apis": {
        "cryptocompare": {
            "endpoint": "https://min-api.cryptocompare.com/data/pricehistorical",
            "apikey": "cryptocompare-123456"
        },
        "mintscan": {
            "endpoint": "https://apis.mintscan.io/v1/:network/apr",
            "apikey": "mintscan-123456"
        }
    }
}
```

- The config used to run for **2024 Sep** output is [shown here](./configs/config-202409.json), with the two `apikey` values redacted.

- Most of the time, you only need to change the `reference_date` and the content inside `tokens`, after you have set the two `apikey` values correctly.

- For each token inside `tokens`, you also need to provide a `network` value, which is different from the token name. This is required by [Cosmostation API](https://docs.cosmostation.io/apis/reference/utilities/staking-apr). If an incorrect network value is provided, the staking APR will not be fetched. You can test the network value in the API panel provided by the link above. Another way is going to [Mintscan](https://www.mintscan.io/) and search for the token/network, the white label underneath it, as circled below, is the network value used in Cosmostation.

  ![network value](./docs/ss-networkvalue.png)

- If you couldn't get a network staking APR from Mintscan API but know it somewhere, you can set `{..., "staking-apr": 0.xxx}` manually. This will prevent the script from fetching it from Cosmostation.

  Same principle goes that if you couldn't get a token price from Cyptocompare API but know it somewhere, you can set `{..., "price": xx.xxx }` manually. This will override the token price.

  An example is [here](https://github.com/dhkdao/airdrop-scripts/blob/jc/dev/configs/config-202409.json#L10).

## Data Sources

- Token price: <https://www.cryptocompare.com/>
- Staking APR: <https://www.mintscan.io/> (operated by [Cosmostation](https://cosmostation.io/))
- [DHK airdrop template master speadsheet](https://docs.google.com/spreadsheets/d/1QliDXE6yMNnPxhqraLqhTDnRQ0vbpvapLYoMC0vFgSc/edit?usp=sharing)

## Development

```bash
# sync all the dependencies
pdm sync -d

# show the help text
pdm exe --help

# Run the regular command
pdm exe input.json -o output -t json

# Run test cases with no output capture
pdm test:no-capture
```

Please copy `.env.example` over to `.env` and fills in the API_KEYs inside before running `pdm test`. Otherwise, tests expected to pass will fail.

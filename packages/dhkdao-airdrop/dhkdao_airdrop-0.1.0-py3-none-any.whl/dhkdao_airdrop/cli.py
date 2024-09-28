import typer
from typing_extensions import Annotated
from enum import Enum
from rich import print

from .airdrop import Airdrop
from .utils import round_output, get_config_with_apikey_envs


class OutputType(str, Enum):
    table = "table"
    csv = "csv"
    json = "json"


app = typer.Typer()


@app.command()
def monthly_alloc(
    config: Annotated[typer.FileText, typer.Argument(help="Input config file.")],
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="Output file path. If skipped, output is printed on screen.",
        ),
    ] = None,
    type: Annotated[
        OutputType, typer.Option("--type", "-t", help="Output type.")
    ] = OutputType.table,
):
    """
    Compute the DHK dao monthly airdrop allocation based on staked value on various blockchains.
    """
    config = get_config_with_apikey_envs(config)
    airdrop = Airdrop(config)
    result = round_output(airdrop.monthly_alloc())
    result_output = None

    # Transform the result suitable for output
    match type:
        case OutputType.json:
            result_output = result.to_json(orient="records")
        case OutputType.csv:
            result_output = result.to_csv()
        case OutputType.table:
            result_output = result
        case _:  # Unexpected output type
            raise Exception("Unexpected output type.")

    # Write the output either to screen or a file
    fh = open(output, "w") if (output is not None) else None
    print(result_output, file=fh)


def cli():
    app()

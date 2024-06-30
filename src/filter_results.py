""" Filter the property to find desired houses """

import pandas as pd
from pathlib import Path
import json
from loguru import logger
from pydantic import BaseModel
from typing import List, Dict
import typer

app = typer.Typer()


class BasicInfo(BaseModel):
    bathrooms: int
    bedrooms: int
    livingArea: int
    price: int
    streetAddress: str
    zpid: int


class BasicResults(BaseModel):
    results: List[BasicInfo]


def filter_houses(data_dict: Dict,
                  bedroom_min_size: int = 4,
                  bathroom_min_size: int = 3,
                  price_min: int = 800_000,
                  price_max: int = 1_150_000):

    data_df = pd.DataFrame(data=data_dict)

    wanted_df = data_df[(data_df['bedrooms'] >= bedroom_min_size) &
                        (data_df['bathrooms'] >= bathroom_min_size) &
                        (data_df['price'] >= price_min) &
                        (data_df['price'] <= price_max)]

    return wanted_df


def find_my_houses(data: Dict, 
                   bedroom_min_size: int,
                   bathroom_min_size: int,
                   price_min: int,
                   price_max: int
                   ):
    logger.info(data)
    results = BasicResults(**data)
    logger.info(f"result count {len(results.results)}")

    result_dicts = [x.model_dump() for x in results.results]
    data_df = filter_houses(data_dict=result_dicts,
                            bedroom_min_size=bedroom_min_size,
                            bathroom_min_size=bathroom_min_size,
                            price_min=price_min,
                            price_max=price_max)

    return data_df


@app.command()
def main(json_path: Path):
    # json_path = Path("data/search_response.json")

    with json_path.open() as file:
        data = json.load(file)
    houses_df = find_my_houses(data=data)
    print(houses_df)


if __name__ == "__main__":
    app()

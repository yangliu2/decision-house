from pydantic import BaseModel
from typing import List, Dict, Tuple
from pathlib import Path
from loguru import logger
import json
import typer
app = typer.Typer()


class Pictures(BaseModel):
    url: str
    height: int
    width: int


class ComparableAddress(BaseModel):
    city: str
    state: str
    streetAddress: str
    zipcode: str


class Comparables(BaseModel):
    address: ComparableAddress
    bathrooms: int
    bedrooms: int
    livingArea: int
    price: int
    zpid: int


class Features(BaseModel):
    appliances: List[str]
    # associationFee: str
    bathroomsFull: int
    bathroomsHalf: int
    communityFeatures: List[str]
    daysOnZillow: int
    flooring: List[str]
    # hoaFee: str
    interiorFeatures: List[str]
    lotFeatures: List[str]
    poolFeatures: List[str]
    utilities: List[str]


class Schools(BaseModel):
    grades: str
    distance: float
    level: str
    name: str
    rating: int
    type: str


class DetailResults (BaseModel):
    hugePhotos: List[Pictures]
    comps: List[Comparables]
    description: str
    favoriteCount: int
    lotAreaValue: float
    photoCount: int
    propertyTaxRate: float
    resoFacts: Features
    schools: List[Schools]
    yearBuilt: int
    zpid: int


def is_good_school(results: Dict,
                   min_rating: int = 7,
                   desired_schools: Tuple[str] = ("Westwood High School")) -> bool:
    schools = results.schools
    ratings = [x.rating for x in schools]
    logger.info(f"ratings are {ratings}")
    names = [x.name for x in schools]
    
    if min(ratings) < min_rating:
        logger.info(f"School rating for {results.zpid} lower than {min_rating}")
        return False
    
    if bool(set(desired_schools) & set(names)):
        logger.info(f"{results.zpid} Does not have the desired school {desired_schools}")
        return False
    
    return True


def get_detailed_info(data: Dict) -> Dict:
    
    results = DetailResults(**data)

    return results


@app.command()
def main(json_path: Path):
    with json_path.open() as file:
        data = json.load(file)
    results = get_detailed_info(data=data)
    print(results)


if __name__ == "__main__":
    app()

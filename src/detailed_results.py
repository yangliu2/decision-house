""" Checking the detailed info for each house """
from pydantic import BaseModel
from typing import List, Dict, Tuple, Optional
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
    bathrooms: float
    bedrooms: Optional[float]
    livingArea: int
    price: int
    zpid: int


class Features(BaseModel):
    appliances: List[str]
    # associationFee: str
    bathroomsFull: Optional[int]
    bathroomsHalf: Optional[int]
    communityFeatures: List[str]
    daysOnZillow: int
    flooring: List[str]
    # hoaFee: str
    interiorFeatures: List[str]
    lotFeatures: List[str]
    poolFeatures: Optional[List[str]]
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
    hdpUrl: str
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
                   min_rating: int,
                   desired_schools: Tuple[str]) -> bool:
    schools = results.schools
    ratings = [x.rating for x in schools]
    logger.info(f"ratings are {ratings}")
    
    if min(ratings) < min_rating:
        logger.info(f"School rating for {results.zpid} lower than {min_rating}")
        return False
    
    # Flag if desired school is in the list
    school_flag = False
    for desired_school in desired_schools:
        for name in schools:
            if desired_school.lower() in name.name.lower():
                school_flag = True
    
    # if not bool(set(desired_schools) & set(names)):
    if not school_flag:
        logger.info(f"{results.zpid} Does not have the desired school {desired_schools}")
        return False
    
    return True


def get_detailed_info(data: Dict) -> Dict:
    """Check the validity of detailed house information

    :param data: dictionary returned from API service
    :type data: Dict
    :return: pydantic object after type checking
    :rtype: Dict
    """
    
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

""" Filter the property to find desired houses """

import typer
from loguru import logger
from typing import List
from typing import Optional
from src.pull_data import search_house, get_detail
from src.filter_results import find_my_houses
from src.detailed_results import get_detailed_info, is_good_school

app = typer.Typer()


def get_house(zipcode: str,
              bedroom_min_size: int,
              bathroom_min_size: int,
              price_min: int,
              price_max: int,
              min_school_rating: int,
              desired_school: Optional[str] = None) -> List:
    """Get house info based on filtered info

    :param zipcode: zipcode as location
    :type zipcode: str
    :param bedroom_min_size: min bedroom size
    :type bedroom_min_size: int
    :param bathroom_min_size: min bathroom size
    :type bathroom_min_size: int
    :param price_min: min price
    :type price_min: int
    :param price_max: max price
    :type price_max: int
    :param min_school_rating: min school rating
    :type min_school_rating: int
    :param desired_school: one school that must be included, defaults to None
    :type desired_school: Optional[str], optional
    :return: list of houses after filtering
    :rtype: List
    """
    logger.info(f"Looking for houses in zipcode: {zipcode}")
    search_results = search_house(location=zipcode)
    
    logger.info(f"Filtering houses according to default parameters")
    my_houses_df = find_my_houses(data=search_results,
                                  bedroom_min_size=bedroom_min_size,
                                  bathroom_min_size=bathroom_min_size,
                                  price_min=price_min,
                                  price_max=price_max)
    # print(my_houses_df)
    
    logger.info(f"Get detailed info for each of the results")
    houses_with_schools = []
    for index, row in my_houses_df.iterrows():
        zpid = row['zpid']
        detailed_result = get_detail(zpid=zpid)
        details = get_detailed_info(data=detailed_result)
        if is_good_school(results=details, 
                          min_rating=min_school_rating,
                          desired_schools=(desired_school,)):
            url = details.hdpUrl
            houses_with_schools.append(f"https://www.zillow.com{url}")
            
    return houses_with_schools

@app.command()
def main(zipcode: str):

    houses = get_house(zipcode=zipcode)
    print(houses)

if __name__ == "__main__":
    app()

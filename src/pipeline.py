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
    logger.info(f"Looking for houses in zipcode: {zipcode}")
    search_results = search_house(location=zipcode)
    
    logger.info(f"Filtering houses according to default parameters")
    my_houses_df = find_my_houses(data=search_results,
                                  bedroom_min_size=bedroom_min_size,
                                  bathroom_min_size=bathroom_min_size,
                                  price_min=price_min,
                                  price_max=price_max)
    print(my_houses_df)
    
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

""" Filter the property to find desired houses """

import typer
from loguru import logger
from src.pull_data import search_house, get_detail
from src.filter_results import find_my_houses
from src.detailed_results import get_detailed_info, is_good_school

app = typer.Typer()


@app.command()
def main(zipcode: str):
    logger.info(f"Looking for houses in zipcode: {zipcode}")
    search_results = search_house(location=zipcode)
    
    logger.info(f"Filtering houses according to default parameters")
    my_houses_df = find_my_houses(data=search_results)
    print(my_houses_df)
    
    logger.info(f"Get detailed info for each of the results")
    houses_with_schools = []
    for index, row in my_houses_df.iterrows():
        zpid = row['zpid']
        detailed_result = get_detail(zpid=zpid)
        details = get_detailed_info(data=detailed_result)
        if is_good_school(results=details):
            houses_with_schools.append(zpid)
        
    print(houses_with_schools)

if __name__ == "__main__":
    app()

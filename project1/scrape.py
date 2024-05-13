import asyncio
import os

from yahoo_api_client import YahooApiClient


async def main() -> None:
    api = YahooApiClient()

    snp_500 = api.get_history('^GSPC')
    vix = api.get_history('^VIX')
    us_treasury_bonds = api.get_history('^TYX')
    # Dow Jones Industrial Average
    djia = api.get_history('^DJI')

    snp_path = os.path.join(os.getcwd(), 'project1', 'assets', 's&p500_max.csv')
    vix_path = os.path.join(os.getcwd(), 'project1', 'assets', 'vix_max.csv')
    us_treasury_bonds_path = os.path.join(os.getcwd(), 'project1', 'assets', 'us_bonds_max.csv')
    djia_path = os.path.join(os.getcwd(), 'project1', 'assets', 'djia_max.csv')

    snp_500.to_csv(snp_path)
    vix.to_csv(vix_path)
    us_treasury_bonds.to_csv(us_treasury_bonds_path)
    djia.to_csv(djia_path)


asyncio.run(main())

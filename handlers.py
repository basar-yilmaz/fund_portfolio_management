from bs4 import BeautifulSoup
import requests
from pandas import DataFrame


def get_fund_data(fund_code: str) -> dict:
    url = f"https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={fund_code}"
    page_source = requests.get(url)
    soup = BeautifulSoup(page_source.content, "html.parser")

    found_info = soup.find_all("ul", {"class": "top-list"})

    if not found_info:
        return {
            "current_price": 0,
            "change_perc": 0,
            "type_of_fund": "",
        }

    current_price = found_info[0].find_all("span")[0].text
    current_price = current_price.replace(",", ".")

    change_perc = found_info[0].find_all("span")[1].text
    change_perc = change_perc.replace("%", "")
    change_perc = change_perc.replace(",", ".")

    type_of_fund = found_info[0].find_all("span")[4].text

    return {
        "current_price": float(current_price),
        "change_perc": float(change_perc),
        "type_of_fund": type_of_fund,
    }


def update_profits(df: DataFrame) -> DataFrame:
    # Get current prices for existing funds using get_fund_data
    for index, row in df.iterrows():
        fund_code = row["Fund Code"]
        fund_data = get_fund_data(fund_code)
        current_price = fund_data["current_price"]
        df.at[index, "Current Price"] = current_price

        # Calculate profit based on current price
        cost_per_share = row["Cost per Share"]
        shares = row["Shares"]
        profit = (current_price - cost_per_share) * shares
        df.at[index, "Profit"] = profit  # Format profit with currency symbol

    return df


def update_prices(df: DataFrame) -> DataFrame:
    # Get current prices for existing funds using get_fund_data
    for index, row in df.iterrows():
        fund_code = row["Fund Code"]
        fund_data = get_fund_data(fund_code)
        current_price = fund_data["current_price"]
        df.at[index, "Current Price"] = current_price
        df.at[index, "Profit"] = (current_price - row["Cost per Share"]) * row["Shares"]

    return df


def delete_zero_shares(df: DataFrame) -> DataFrame:
    # delete rows with zero shares
    for index, row in df.iterrows():
        if row["Shares"] <= 0:
            df.drop(index, inplace=True)

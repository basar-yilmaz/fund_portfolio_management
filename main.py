# # Portföy Görüntüleme Aracı

import pandas as pd
import numpy as np
import os
from handlers import *

data_file = "fund_data.csv"

# Check if the CSV file exists and has data
if os.path.isfile(data_file):
    # Read existing data from CSV
    df = pd.read_csv(data_file)
    if df.empty:
        print("Your wallet is currently empty. Please add some funds first.")
        df = pd.DataFrame(
            columns=[
                "Fund Code",
                "Cost per Share",
                "Current Price",
                "Shares",
                "Total Cost",
                "Profit",
            ]
        )  # Create empty DataFrame
else:
    # Create an empty DataFrame with columns
    df = pd.DataFrame(
        columns=[
            "Fund Code",
            "Cost per Share",
            "Current Price",
            "Shares",
            "Total Cost",
            "Profit",
        ]
    )


df = update_profits(df)  # Update profits for each fund

# User actions loop
while True:
    delete_zero_shares(df)

    print("Do you want to:")
    print("0. View your wallet")
    print("1. Add a new fund")
    print("2. Add shares to an existing fund")
    print("3. Decrease shares of an existing fund")
    print("4. Update current prices and profits")
    print("5. Exit")

    action = input("Enter your choice (0-5): ")

    if action == "0":
        # View wallet
        print(df)

    elif action == "1":
        # Add a new fund
        fund_code = input("Enter fund code: ")
        cost_per_share = float(input("Enter cost per share: "))
        shares = int(input("Enter number of shares: "))
        current_price = get_fund_data(fund_code)["current_price"]

        total_cost = cost_per_share * shares
        # Append new fund data to the DataFrame
        new_row = {
            "Fund Code": fund_code,
            "Cost per Share": cost_per_share,
            "Current Price": current_price,
            "Shares": shares,
            "Total Cost": total_cost,
            "Profit": current_price * shares - total_cost,
        }
        df.loc[len(df)] = new_row
    elif action == "2":
        # Check if there are existing funds before adding shares
        if df.empty:
            print(
                "There are no existing funds in your wallet. Please add a fund first."
            )
        else:
            # Get fund code and additional shares
            fund_code = input("Enter fund code add new shares: ")
            cost_per_share = float(input("Enter cost per share: "))
            shares = int(input("Enter number of shares: "))

            old_cost_per_share = df.loc[
                df["Fund Code"] == fund_code, "Cost per Share"
            ].values[0]
            old_shares = df.loc[df["Fund Code"] == fund_code, "Shares"].values[0]
            new_shares = old_shares + shares

            # Update cost per share
            new_cost_per_share = (
                old_cost_per_share * old_shares + cost_per_share * shares
            ) / new_shares

            df.loc[df["Fund Code"] == fund_code, "Cost per Share"] = new_cost_per_share
            df.loc[df["Fund Code"] == fund_code, "Shares"] = new_shares
            df.loc[df["Fund Code"] == fund_code, "Total Cost"] = (
                new_cost_per_share * new_shares
            )
            df.loc[df["Fund Code"] == fund_code, "Profit"] = (
                -new_cost_per_share
                + df.loc[df["Fund Code"] == fund_code, "Current Price"].values[0]
            ) * new_shares
        

    elif action == "3":
        # Check if there are existing funds before decreasing shares
        

    elif action == "4":
        # Update current prices and profits
       

    elif action == "5":
        # Save the DataFrame to CSV (assuming you want to persist data)
       

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

    print("\n")  
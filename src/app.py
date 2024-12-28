import os
from bs4 import BeautifulSoup
import requests
import pandas as pd  # Import pandas for DataFrame handling
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Fetch the HTML data
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    raise ConnectionError(f"Failed to fetch data. Status code: {response.status_code}")

html_data = response.text

# Step 2: Parse the HTML
soup = BeautifulSoup(html_data, "html.parser")

# Step 3: Locate the <div> with class="col-xs-6"
div = soup.find("div", class_="col-xs-6")
if div is None:
    raise ValueError("Error: The <div> with class 'col-xs-6' was not found in the HTML.")

# Step 4: Locate the <table> within the <div>
table = div.find("table", class_="historical_data_table")
if table is None:
    raise ValueError("Error: The <table> with class 'historical_data_table' was not found within the specified <div>.")

# Step 5: Validate the table's content
header = table.find("th")
if header and "Tesla Quarterly Revenue" not in header.get_text(strip=True):
    raise ValueError("Error: The table does not contain a header with 'Tesla Quarterly Revenue'.")

# Step 6: Extract data from the identified table
data = []
for row in table.find_all("tr"):
    col = row.find_all("td")
    if len(col) >= 2:  # Ensure at least 2 columns (Date and Revenue) are present
        date = col[0].text.strip()
        revenue = col[1].text.strip().replace("$", "").replace(",", "")
        data.append({"Date": date, "Revenue": revenue})

# Step 7: Create the DataFrame
tesla_revenue = pd.DataFrame(data)

# Step 8: Convert Revenue to numeric type
tesla_revenue["Revenue"] = pd.to_numeric(tesla_revenue["Revenue"], errors="coerce")  # Handle invalid data

# Display the first 5 rows
print(tesla_revenue.head())

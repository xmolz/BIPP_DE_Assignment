import requests
import pandas as pd
import os

# Set up the headers for the HTTP request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "deviceType": "Web",
    "Connection": "keep-alive",
    "Referer": "https://pmfby.gov.in/adminStatistics/dashboard",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

# Define the schemes and seasons to fetch data for
schemes = {"02", "04"}
seasons = {"01", "02"}

# This function fetches dashboard data for a given year, season, and scheme
def fetch_dashboard_data(year, season, scheme):
    # Set up the URL and query parameters
    url = "https://pmfby.gov.in/goiConfig/getAdminDashboardStateWiseReport"
    querystring = {
        "year": f"{year}",
        "seasonCode": f"{season}",
        "schemeCode": f"{scheme}",
        "isCombined": "1",
    }

    try:
        # Send the HTTP GET request and store the response
        response = requests.get(url, headers=headers, params=querystring)

        # Parse the JSON data from the response
        data = response.json()

        # Extract the 'data' key from the parsed JSON object
        data1 = data['data']

        # Convert the data into a pandas DataFrame
        df = pd.DataFrame(data1)

    except Exception as e:
        print(f"Error fetching data for year {year}, season {season}, scheme {scheme}: {e}")
        return None

    return df

# Level 1 extraction (statewise) starts here
# Create the base folder if it doesn't exist
folder_name = "./raw data/"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Create an empty list to capture next-level identifiers (statecodes)
state_codes = []

# Iterate through the years, seasons, and schemes
for year in range(2018, 2023):
    for season in seasons:
        for scheme in schemes:
            df = fetch_dashboard_data(year, season, scheme)

            # If an error occurred, skip this iteration
            if df is None:
                continue

            # Generate the CSV file name for the current combination of year, season, and scheme
            file_name = "Sc" + scheme + "_Se" + season + "_Yr" + str(year) + ".csv"

            # Create the file path for the CSV file
            file_path = os.path.join(folder_name, file_name)

            # Save the DataFrame to a CSV file
            df.to_csv(file_path, index=False)

            print(file_path + " saved!")
            
print("all files finished downloading")
import requests
import pandas as pd
import os

schemes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

output_folder = "data/raw"

for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if "data" in data:
                df = pd.DataFrame(data["data"])

                file_name = f"{output_folder}/{name}_nav.csv"

                df.to_csv(file_name, index=False)

                print(f"Saved: {file_name}")

        else:
            print(f"Failed for {code}")

    except Exception as e:
        print(e)
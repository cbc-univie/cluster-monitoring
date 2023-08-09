""" Fetch data from the GeoSPere austria api hub.
It is currently without authentication possbile
https://dataset.api.hub.geosphere.at/v1/docs/index.html
(https://data.hub.geosphere.at/)
"""
from datetime import datetime

import pandas as pd
import requests

#ToDo: make it a class and retrieve certain info as dfs(?)
# add all the data variable to the init to je able to inport rhem snd do mor call the functions twice


host = "https://dataset.api.hub.geosphere.at"
version = "v1"

resource_id = "klima-v1-1h" #one of: https://dataset.api.hub.geosphere.at/v1/docs/user-guide/resource.html#resources

def data_from_hourly(param_name: str, metadata: bool=False) -> pd.DataFrame:
    """This uses data from the folling dataset:
    https://data.hub.geosphere.at/dataset/klima-v1-1h
    param_name can be sth from the metadata query if set True
    in metadata["parameters"] and the in the list the name attribute.
    Examples:
    RSX: Niederschlag
    SUX: Sonnenscheindauer
    VKM: Windgeschwindigkeit
    """
    type = "station" #could also be grid or timeseries for other datasets
    mode = "historical" #could also be current for other datasets

    url = f"{host}/{version}/{type}/{mode}/{resource_id}"
    # https://dataset.api.hub.geosphere.at/app/frontend/station/historical/klima-v1-1h
    # 5925 is inner stadt
    #TODO: use as star the day after the last already fetched one
    start = "2023-07-20" #format: YYYY-MM-DDThh:mm time is optional
    end = datetime.today().strftime("%Y-%m-%d")
    params = {"station_ids": "5925",
            "parameters": param_name, #VKM Windgeschwindigkeit in km/h
            "start": start,
            "end": end
    }
    r = requests.get(url, params=params)
    data = r.json()
    df = pd.DataFrame(
        [data["timestamps"],data["features"][0]["properties"]["parameters"][param_name]["data"]]
        ).T
    df.columns=["date", param_name]
    if metadata:
        r2 = requests.get(url + "/metadata")
        metadata = r2.json()
        return df,metadata
    return df, None
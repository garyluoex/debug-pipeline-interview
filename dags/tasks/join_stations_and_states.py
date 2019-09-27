import pandas as pd


def join_stations_and_states(stations_path, states_path, output_path):
    stations_df = read_stations_fwf(stations_path)
    states_df = read_states_fwf(states_path)

    joined_df = pd.merge(
        stations_df, states_df, how="inner", left_on="STATE", right_on="CODE"
    )

    joined_df.to_csv(output_path)


def read_stations_fwf(stations_path):
    station_columns = [
        "ID",
        "LATITUDE",
        "LONGITUDE",
        "ELEVATION",
        "STATE",
        "STATION_NAME",
        "GSN_FLAG",
        "CRN_FLAG",
        "WMO_ID",
    ]
    column_specs = [
        (0, 11),
        (12, 20),
        (21, 30),
        (31, 37),
        (38, 40),
        (41, 71),
        (72, 75),
        (76, 79),
        (80, 85),
    ]

    return pd.read_fwf(stations_path, names=station_columns, colspecs=column_specs)


def read_states_fwf(states_path):
    states_columns = ["CODE", "STATE_NAME"]
    column_specs = [(1, 2), (3, 51)]

    return pd.read_fwf(states_path, names=states_columns, colspecs=column_specs)

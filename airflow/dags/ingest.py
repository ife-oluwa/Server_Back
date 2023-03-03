import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings
import pandas as pd
import os

TOKEN = os.getenv("TOKEN")
ORG = os.getenv("ORG")
BUCKET = os.getenv("BUCKET")
URL = os.getenv("URL")
CSV_LOCATION = os.getenv("CSV_LOCATION")


def load_data():
    df = pd.read_csv(CSV_LOCATION).set_index('date_exploitation')

    with influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG) as client:

        point_settings = PointSettings(**{"type": 'incidents'})
        point_settings.add_default_tag("server", "ingest-data-frame")

        write_api = client.write_api(
            write_options=SYNCHRONOUS, point_settings=point_settings)
        write_api.write(bucket=BUCKET, record=df,
                        data_frame_measurement_name="server-df")


def del_file() -> None:
    os.remove(CSV_LOCATION)


def data_ingest():
    with influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG) as client:

        query = f'from(bucket:"{BUCKET}")' \
            ' |> range(start: 0, stop: now())' \
            ' |> filter(fn: (r) => r._measurement == "server-df")' \
            ' |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")' \
            ' |> limit(n:10, offset: 0)'
        result = client.query_api().query(query=query)

    """
    Processing results
    """
    print()
    print("=== results ===")
    print()
    for table in result:
        for record in table.records:
            print(record['_time'], record['TERMINE'], record['INCIDENTE'])

from prometheus_client import start_http_server, Summary
import random
import time
import glob
import pandas as pd
from pandas.errors import EmptyDataError
from prometheus_client import Counter

COUNTER = Counter('tables', 'results', ['name', 'status', 'info'])


def show_results(csv_dir: str):
    data = []

    for filename in glob.glob(f"{csv_dir}/*.csv"):
        try:
            df = pd.read_csv(filename, names=["table", "status", "info"], index_col=False)
            data.append(df)
        except EmptyDataError as ex:
            print(filename)

    df = pd.concat(data, axis=0, ignore_index=True)

    for idx, row in df.iterrows():
        COUNTER.labels(row["table"], row["status"], row["info"]).inc()


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)

    # Generate some requests.
    while True:
        show_results(csv_dir="data")
        # sleep 5 minutes = 5 * 60 seconds
        time.sleep(5*60)

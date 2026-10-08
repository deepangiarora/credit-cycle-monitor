"""Refresh the Credit Cycle Monitor with the latest FRED data.

Usage:
    python update_data.py           # download every series from FRED, then rebuild index.html
    python update_data.py --local   # skip the download and rebuild from data.json

FRED's public CSV links need no API key.
"""
import csv
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

SERIES = {
    "DRCCLACBS": "Delinquency rate, credit card loans",
    "DRCLACBS": "Delinquency rate, consumer loans",
    "DRSFRMACBS": "Delinquency rate, single-family residential mortgages",
    "DRCRELEXFACBS": "Delinquency rate, commercial real estate loans (excl. farmland)",
    "DRBLACBS": "Delinquency rate, business loans",
    "CORCCACBS": "Charge-off rate, credit card loans",
    "CORALACBS": "Charge-off rate, all loans",
    "DRTSCILM": "Net % of banks tightening standards, C&I loans to large and middle-market firms",
    "DRTSCLCC": "Net % of banks tightening standards, credit card loans",
    "BAA10YM": "Moody's Baa corporate yield minus 10-year Treasury (monthly)",
    "GS10": "10-year Treasury yield (monthly)",
}
START = "2000-01-01"
HERE = Path(__file__).parent
PAGE = HERE / "index.html"
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={start}"


def download(sid):
    req = urllib.request.Request(URL.format(sid=sid, start=START), headers={"User-Agent": "credit-cycle-monitor"})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode("utf-8")
    rows = []
    for row in csv.reader(io.StringIO(text)):
        if not row or row[0].lower() in ("date", "observation_date"):
            continue
        if row[1] in (".", ""):
            continue  # FRED marks missing values with "."
        rows.append((row[0], float(row[1])))
    if not rows:
        raise ValueError(f"No data returned for {sid}")
    return rows


def rebuild_page(data):
    blob = json.dumps(data, separators=(",", ":"))
    html = PAGE.read_text(encoding="utf-8")
    new, n = re.subn(r"/\*DATA\*/.*?/\*END\*/", lambda m: f"/*DATA*/{blob}/*END*/", html, flags=re.S)
    if n != 1:
        raise RuntimeError("Could not find the data block in index.html")
    PAGE.write_text(new, encoding="utf-8")
    (HERE / "data.json").write_text(blob, encoding="utf-8")
    for sid, rows in data.items():
        print(f"{sid:15s} {len(rows):4d} rows, latest {rows[-1][0]} = {rows[-1][1]}")


if __name__ == "__main__":
    if "--local" in sys.argv:
        data = json.loads((HERE / "data.json").read_text(encoding="utf-8"))
    else:
        data = {}
        for sid in SERIES:
            data[sid] = [[d[:7], v] for d, v in download(sid)]
            print(f"Downloaded {sid}")
    rebuild_page(data)
    print("index.html updated.")

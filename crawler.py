#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv
import json
from urllib.request import urlopen

URL = "https://act1.ff.sdo.com/FF14/api/ViolationPlatform/violationRoles?page=1&limit=1000000"
CSV_FILE = "violation_roles.csv"

def fetch_data():
    print("Fetching data from URL:", URL)
    with urlopen(URL) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    if data.get("code") == 10000 and "data" in data:
        lst = data["data"].get("list", [])
        print("Fetched data size:", len(lst))
        r = []
        for item in lst:
            a = item.get("role_name", "")
            b = item.get("group_name", "")
            c = item.get("vio_reason", "")
            r.append((a, b, c))
        return r
    print("Data format unexpected or code != 10000")
    return []

def load_csv_data(f):
    if not os.path.exists(f):
        print("CSV file not found:", f)
        return []
    print("Loading CSV file:", f)
    r = []
    with open(f, "r", encoding="utf-8", newline="") as ff:
        rr = csv.reader(ff)
        for row in rr:
            if len(row) < 3:
                continue
            r.append((row[0], row[1], row[2]))
    print("Loaded lines from CSV:", len(r))
    return r

def save_csv_data(f, d):
    print("Saving CSV file:", f, "with lines:", len(d))
    with open(f, "w", encoding="utf-8", newline="") as ff:
        w = csv.writer(ff)
        for x in d:
            w.writerow(x)

def main():
    print("Starting crawler...")
    o = load_csv_data(CSV_FILE)
    n = fetch_data()
    print("Old data lines:", len(o), "New data lines:", len(n))
    if not o:
        print("No old data, saving all new data.")
        save_csv_data(CSV_FILE, n)
        return
    print("Comparing old data with new data...")
    fr = o[0]
    idx = None
    for i, v in enumerate(n):
        if v == fr:
            idx = i
            break
    if idx is not None:
        inc = n[:idx]
    else:
        inc = n
    if not inc:
        print("No new lines found, skip update.")
        return
    print("New lines to add:", len(inc))
    final_data = inc + o
    print("Final CSV lines will be:", len(final_data))
    save_csv_data(CSV_FILE, final_data)

if __name__ == "__main__":
    main()

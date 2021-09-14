import json
import os
from os import listdir
from os.path import isfile, join, isdir, splitext
from typing import Type
from PIL import Image
import pathlib
import random
import re
import csv
import pandas as pd
import csv

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


basepath = f"{pathlib.Path(__file__).parent.resolve()}"
end_trxn_no = "0x4ef3d92b6ec4d867b63de15fa64ed8f7a35e41eab03f88d161b7f52cf9507154"
all_lp_before_end = 0
all_trxn_before_end = []
wallet_before_end = []
lp_100 = 61434

for i in range(5):
    with open(f'{basepath}/{i}.csv', newline='') as csvfile:
        print(f"Reading File {i}....")
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            if end_trxn_no == row['Txhash']:
                break

            if row['TokenSymbol'] == 'Cake-LP' and row['To'] == '0xcf701a6809e30cf615eb0b446d62091a3bf0cf0f':
                all_lp_before_end += float(row['Value'].replace(',',''))
                if row['From'] not in wallet_before_end:
                    wallet_before_end.append(row['From'])
                all_trxn_before_end.append({
                    "Trxn": row['Txhash'],
                    "From": row['From'],
                    "Value": float(row['Value'].replace(',','')),
                })
                

output = {
    "before_88": {
        "88Guy":"",
        "total_lp_88": 0,
        "wallets_count":0,
        "wallets":[],
        "trxn_count":0,
        "trxn":[],
    },
    "before_end_count": {
        "total_lp": all_lp_before_end,
        "wallets_count": len(wallet_before_end),
        "wallets": wallet_before_end,
        "trxn_count": len(all_trxn_before_end),
        "trxn": all_trxn_before_end,
    }
}

all_lp_calc = 0
for k in all_trxn_before_end:
    output['before_88']['total_lp_88'] += k['Value']
    current_p = output['before_88']['total_lp_88']/lp_100*100
    k['%TillDate'] = current_p
    output['before_88']['trxn'].append(k)
    if k['From'] not in output['before_88']['wallets']:
        output['before_88']['wallets'].append(k['From'])
    if current_p >= 88:
        break


output['before_88']['wallets_count'] = len(output['before_88']['wallets'])
output['before_88']['trxn_count'] = len(output['before_88']['trxn'])
file = f"{basepath}/nft.json"
with open(file, "w") as fp:
  json.dump(output,fp, indent=2)
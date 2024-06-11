import os
import json
from tqdm import tqdm
import requests

payload = ""
headers = {
  'Ok-Access-Key': 'de951da3-6774-4fc8-a207-3068fc37fc63'
}

def is_sorted_desc_except_first(lst):
    if len(lst) <= 1:
        return True

    for i in range(1, len(lst)):
        if lst[i] > lst[i - 1]:
            return False

    return True

def request_transaction_list(height):
  url = f"https://www.oklink.com/api/v5/explorer/block/transaction-list?chainShortName=BTC&height={height}&limit=100"
  response = requests.request("GET", url, headers=headers, data=payload)
  data = json.loads(response.text)
  pages = data.get("data", {})
  for page in pages:
    txs = page.get("blockList", {})
    txfees = [request_transaction_fills(tx["txid"]) for tx in txs]
    del txfees[0]
    print(height, is_sorted_desc_except_first(txfees), txfees)
    
def request_transaction_fills(txid):
  url = f"https://www.oklink.com/api/v5/explorer/transaction/transaction-fills?chainShortName=BTC&txid={txid}"
  response = requests.request("GET", url, headers=headers, data=payload)
  data = json.loads(response.text)
  transaction = data['data'][0]
  txfee = float(transaction['txfee'])
  virtual_size = int(transaction['virtualSize'])
  # 平均手续费 Satoshis/vByte
  txfee_per_size = 100000000 * txfee / virtual_size
  return txfee_per_size


def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def parse_block_height(directory):
  blocks = list()
  json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
  for json_file in json_files:
    file_path = os.path.join(directory, json_file)
    with open(file_path, 'r', encoding='utf-8') as f:
      data = json.load(f)
      hits = data["data"]["hits"]
      for hit in hits:
        height = hit["height"]
        blocks.append(height)
  return blocks

if __name__ == "__main__":
  directory = os.path.dirname(os.path.abspath(__file__))
  data_directory = os.path.join(directory, "data")
  heights = parse_block_height(data_directory)
  for height in tqdm(heights):
    request_transaction_list(height)
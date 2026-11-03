"""Submit the poidh claim for bounty 1527 (Best poidh Meme, on-chain #541).

Same Lasso-RPC flow as submit_1520_lasso.py. Never prints the RPC key or the
signing key. Fails closed: refuses to send if the bounty stopped accepting
claims, if we already claimed it, or if the simulation reverts.
"""
import json
import subprocess
import time

from eth_abi import encode as abi_encode
from eth_account import Account
from eth_utils import keccak, to_checksum_address

P = r'C:/Users/nicoa/poidh-auto/claims/1527'
W = r'C:/Users/nicoa/poidh-auto'
w = json.load(open(W + '/agent_wallet.json'))
ADDR, KEY = w['addr'], w['key']
POIDH = "0x5555Fa783936c260f77385b4e153b9725fef1719"

LASSO = json.load(open(r'C:/Users/nicoa/AppData/Local/Temp/lasso/key.json'))
RPC = LASSO["rpc_url"] + "/base"
assert "lasso.sh" in RPC

OID_UI = 1527
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
_raw = json.loads(subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA,
                                  f"https://poidh.xyz/base/bounty/{OID_UI}/data"],
                                 capture_output=True, text=True).stdout)
_b = _raw.get("bounty", _raw)
OID = int(_b["onChainId"])
claims = _b.get("claims") or []
print(f"poidh {OID_UI} -> on-chain {OID}; acceptingClaims={_b.get('acceptingClaims')} "
      f"status={_b.get('statusLabel')} claims={len(claims)} pot={int(_b['amount'])/1e18} ETH")
if OID != 541:
    raise SystemExit(f"unexpected onChainId {OID}")
if not _b.get("acceptingClaims"):
    raise SystemExit("bounty no longer accepting claims")
mine = [c for c in claims
        if (c.get("issuerAddress") or "").lower() == ADDR.lower()]
if mine:
    raise SystemExit(f"already claimed: {len(mine)} claim(s) from this wallet")

NAME = "Pics of the escrow or the bounty didn't happen (bounty #541, 0.007 ETH)"
BODY = open(P + '/body1527.txt', encoding='utf-8').read().strip()
URI = "https://raw.githubusercontent.com/nicoarias81/poidh1527-escrow-meme/main/card1527.png"

trace = []


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    r = subprocess.run(["curl", "-s", "--max-time", "45", "-X", "POST",
                        RPC + "?include_meta=body",
                        "-H", "Content-Type: application/json",
                        "-H", "User-Agent: hermes-agent/1.0", "-d", body],
                       capture_output=True, text=True)
    j = json.loads(r.stdout)
    meta = j.get("lasso_meta") or {}
    trace.append({"method": method, "request_id": meta.get("request_id"),
                  "provider": (meta.get("selected_provider") or {}).get("id"),
                  "retries": meta.get("retries"), "error": j.get("error")})
    if "error" in j:
        raise RuntimeError(json.dumps(j)[:300])
    return j["result"]


sel = keccak(b"createClaim(uint256,string,string,string)")[:4]
data = sel + abi_encode(["uint256", "string", "string", "string"], [OID, NAME, BODY, URI])
calldata = "0x" + data.hex()
print(f"name {len(NAME)} chars, body {len(BODY)} chars, calldata {len(calldata)//2} bytes")

sim = rpc("eth_call", [{"from": ADDR, "to": POIDH, "data": calldata}, "latest"])
if sim != "0x":
    raise SystemExit(f"simulate FAILED: {sim[:160]}")
print("simulate OK")

gas = int(rpc("eth_estimateGas", [{"from": ADDR, "to": POIDH, "data": calldata}]), 16)
nonce = int(rpc("eth_getTransactionCount", [ADDR, "pending"]), 16)
gp = int(rpc("eth_gasPrice", []), 16)
bal = int(rpc("eth_getBalance", [ADDR, "latest"]), 16)
gas_price = max(gp, 100000000)
print(f"gas {gas}  nonce {nonce}  gasPrice {gas_price}  balance {bal/1e18:.6f} ETH")
if bal < (gas + 200000) * gas_price:
    raise SystemExit("insufficient balance for gas")

tx = {"to": to_checksum_address(POIDH), "data": calldata, "chainId": 8453,
      "gas": gas + 200000, "gasPrice": gas_price, "nonce": nonce, "value": 0}
signed = Account.sign_transaction(tx, KEY)
raw = (signed.raw_transaction.hex() if hasattr(signed.raw_transaction, "hex")
       else signed.rawTransaction.hex())
txh = rpc("eth_sendRawTransaction", ["0x" + raw])
print("sent tx:", txh)

for _ in range(40):
    time.sleep(3)
    rec = rpc("eth_getTransactionReceipt", [txh])
    if rec:
        status = int(rec["status"], 16)
        print(f"status {status} block {int(rec['blockNumber'],16)} "
              f"gasUsed {int(rec['gasUsed'],16)} logs {len(rec['logs'])}")
        if status != 1:
            raise SystemExit("tx FAILED")
        json.dump(rec, open(P + '/submit1527.json', 'w'), indent=1)
        break
else:
    raise SystemExit("no receipt after 120s")

json.dump(trace, open(P + '/lasso_trace_1527.json', 'w'), indent=1)
print("lasso request_ids:", len(trace), "con meta:", sum(1 for t in trace if t["request_id"]))
print("tx:", txh)

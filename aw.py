from web3 import Web3
from requests import get
from time import sleep, time
from sys import exit
from json import loads
import os

def getgas(web3):
    return web3.toWei(get('https://ethgasstation.info/json/ethgasAPI.json').json()["fastest"]/10, "gwei")

def transfer(web3, privatekey, from_addr, to, gas, value):
    nonce = web3.eth.getTransactionCount(from_addr)
    tx = {
    'nonce': nonce,
    'to': to,
    'value': value,
    'gas': 21000,
    'gasPrice': gas
    }
    signed = web3.eth.account.sign_transaction(tx, privatekey)
    txid = web3.eth.sendRawTransaction(signed.rawTransaction)
    return web3.toHex(txid)

def main():
    print("// aw.py by phonkuser v1.0 // fuck vatos\n// buy cryptochecker, best cryptowallets checker - https://lolz.guru/threads/2915136")

    if not os.path.isfile("aw.json"):
        print("aw.json doesn't exists. make sure you extracted all files from repo!")
        exit()
    pkdata = loads(open("aw.json", "r").read())
    privatekey = pkdata["privatekey"]

    web3 = Web3(Web3.HTTPProvider(pkdata["infura_url"]))
    address = web3.eth.account.from_key(privatekey).address
    to = pkdata["transfer_to"]
    
    emptycalls = 0
    prevbalance = 0

    while True:
        starttime = time()
        balance = web3.eth.getBalance(address)
        if balance != 0:
            print("balance found!", balance/1e+18, "ETH")
            gas = getgas(web3)
            if gas*21000 < balance:
                if prebalance != balance:
                    try:
                        txid = transfer(web3, privatekey, address, to, gas, balance-gas*21000)
                    except:
                        print("seems we didn't have time :(")
                        continue
                    print(f"transfer successful! link: https://etherscan.io/tx/{txid}\ntime elapsed from round started to the withdrawal - {round(time() - starttime, 2)} seconds.")
                else:
                    print(f"balance is {str(balance/1e+18)} ETH, but it already got withdrawn.")
            else:
                print("there is balance, but moving it isn't possible - it is smaller than gas price ({} ETH)".format(gas*21000/1e+18))
            emptycalls = 0
        else:
            print(f"balance is 0, trying again... (#{str(emptycalls)})")
            emptycalls += 1
        prevbalance = balance

main()
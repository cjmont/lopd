# Descripción: Script para compilar y desplegar el contrato MultiCompanyDataStorage en Avalanche C-Chain
# Requiere: Python 3.8 o superior, web3, solcx
# Uso: python deploy_contract.py
from web3 import Web3
from solcx import compile_standard, install_solc, set_solc_version
import json
import os

# Instalar y configurar el compilador Solidity
install_solc('0.8.0')
set_solc_version('0.8.0')

# Conectar a Avalanche
w3 = Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))

# Configurar cuenta
private_key = "32390417a1b11f4df93a1f1d751ea8a214b4a523274263a14f4bbc37c5215bb9"
if private_key is None:
    raise ValueError("The PRIVATE_KEY environment variable is not set.")
account = w3.eth.account.from_key(private_key)

# Compilar contrato
with open('MultiCompanyDataStorage.sol', 'r') as file:
    source_code = file.read()

compiled_sol = compile_standard({
    'language': 'Solidity',
    'sources': {'MultiCompanyDataStorage.sol': {'content': source_code}},
    'settings': {'outputSelection': {'*': {'*': ['abi', 'evm.bytecode']}}}
})

abi = compiled_sol['contracts']['MultiCompanyDataStorage.sol']['MultiCompanyDataStorage']['abi']
bytecode = compiled_sol['contracts']['MultiCompanyDataStorage.sol']['MultiCompanyDataStorage']['evm']['bytecode']['object']

# Guardar el ABI en un archivo JSON
with open('MultiCompanyDataStorage.abi', 'w') as abi_file:
    json.dump(abi, abi_file)

# Desplegar contrato
MultiCompanyDataStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
tx = MultiCompanyDataStorage.constructor().build_transaction({
    'chainId': 43114,
    'gas': 8000000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': w3.eth.get_transaction_count(account.address),
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print(f'Contrato desplegado en: {contract_address}')

# Guardar la dirección del contrato en un archivo de texto
with open('contract_address.txt', 'w') as address_file:
    address_file.write(contract_address)

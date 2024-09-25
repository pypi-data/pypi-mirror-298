from cryptskeletonkey import generate_mnemonic, derive_eth_address, derive_btc_address

mnemonic = generate_mnemonic()
eth_address = derive_eth_address(mnemonic)
btc_address_p2pkh = derive_btc_address(mnemonic, 'p2pkh')
btc_address_p2sh = derive_btc_address(mnemonic, 'p2sh')
btc_address_bech32 = derive_btc_address(mnemonic, 'bech32')

print(f"Mnemonic: {mnemonic}")
print(f"Ethereum Address: {eth_address}")
print(f"Bitcoin P2PKH Address: {btc_address_p2pkh}")
print(f"Bitcoin P2SH Address: {btc_address_p2sh}")
print(f"Bitcoin Bech32 Address: {btc_address_bech32}")

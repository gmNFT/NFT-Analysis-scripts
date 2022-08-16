from web3.auto.infura import w3
import numpy as np
from datetime import datetime
from web3._utils.events import get_event_data
import matplotlib
import matplotlib.pyplot as plt

# art blocks contract address for first three mints
ab_contract = "0x059EDD72Cd353dF5106D2B9cC5ab83a52287aC3a"

# looking at first 10,000 transactions on etherscan using
# 'get_erc721_token_transfer_events_by_contract_address_paginated'
# first transaction: block 11438389
# ~10,000 transaction: block 11479109
# had an error when I tried to do too large of a range
# seems like more of a data limit than a block range limit
# need a small range if gathering data during an art drop...
# current block 12762577

block1 = 12260000
block2 = 12270000

logs_fil = w3.eth.filter({'fromBlock': block1, 'toBlock': block2, 'address': ab_contract})
tx_log = logs_fil.get_all_entries()

# art blocks projects by number
# remember this is indexed from 0
projects = (['Squiggly', 'Genesis', 'Construction Token', 'Cryptoblots', 'Dynamic Slices', 
    'Variant Plan', 'View Card', 'Elevated Deconstructions', 'Singularity', 
    'Ignition', 'NimBuds', 'HyperHash', 'Unigrids', 'Ringers', 'Cyber Cities', 
    'Utopia', 'Color Study', 'Spectron', 'Gen 2', 'R3sonance', 'Sentience',
    '27-Bit Digital', 'The Eternal Pump', 'Archetype', 'Pixel Glass', 
    'Pathfinders', 'Energy Sculpture', '720 Minutes', 'Apparitions', 'Inspirals',
    'Hieroglyphs', 'Galaxiss', 'Light Beams', 'Empyrean', 'Enso', 'Aerial View',
    'Gazettes', 'Paper Armada', 'ByteBeats', 'Synapses', 'Algobots', 'Elementals',
    'Void', 'Origami Dream', 'CryptoGodKing', 'Gravity Grid', '70s Pop Series One',
    'Asterisms', 'Gen 3', 'Dear Hash,', 'The Opera', 'Stipple Sunsets', 
    'Star Flower', 'Subscapes', 'P:X', 'Talking Blocks', 'Aurora IV', 'Rhythm',
    'Color Magic Planets', 'Watercolor Dreams', 'Event Horizon Sunset (Series C)',
    '70s Pop Super Fun Summertime Bonus Pack', 'Bubble Blobby', 'Ode to Roy',
    'AlgoRhythms', 'Traversals', 'Patchwork Saguaros', 'Petri', 'Messengers',
    'Abstraction', 'Antennas', 'Andradite', 'Frammenti', 'CatBlocks', 
    'The Blocks of Art', 'Breathe You', 'dino pals', 'Return', 'Fidenza', 
    'Space Debris [m aider]', 'Space Debris [warning]', 'Space Debris [ravaged]',
    'Incantation', 'Panelscape AB', 'PrimiDance', '70s Pop Series Two', 
    'Stroming', ' ', 'Orthogone', 'Dreams', 'Hashtractors', 'planets', 
    'Libertad Parametrizada', 'Sigils', 'Portal', 'CryptoVenetian', 'Gravity 12',
    '(Dis)entanglement', 'sail-o-bots', 'Spaghettification', 'CENTURY', 
    'Enchiridion', ' ', 'Octo Garden', 'Eccentrics', ' ', ' ', ' ', 'Divisions'])



Ntx = len(tx_log)
tokenID = np.zeros(Ntx, dtype = int)
NSerial = np.zeros(Ntx, dtype = int)
Nblock = np.zeros(Ntx, dtype = int)
txTime = np.zeros(Ntx, dtype = int)
price = np.zeros(Ntx)

for j in range(Ntx):
    tx_hash = tx_log[j]['transactionHash']
    print(tx_hash.hex())
    if len(tx_log[j]['topics']) == 4:
        tok_hex = tx_log[j]['topics'][-1].hex()[-20:]
        if int(tok_hex, 16) >= 900000 and int(tok_hex, 16) <= 1e9:
            tok_str = str(int(tok_hex, 16))
            tokenID[j] = int(tok_str[:-6])
            print('Project: ', projects[tokenID[j]])
            NSerial[j] = int(tok_str[-6:])
            print('Serial # ', NSerial[j])
            Nblock[j] = int(tx_log[j]['blockNumber'])
            print('Block # ', Nblock[j])
            txTime[j] = int(w3.eth.get_block(tx_log[j]['blockNumber'])['timestamp'])
            print('Tx Time ', datetime.utcfromtimestamp(txTime[j]).strftime('%Y-%m-%d %H:%M:%S'))
            try:
                # trx = eth.get_internal_txs_by_txhash(txhash = tx_hash.hex())
                trx = w3.eth.getTransaction(tx_hash)
            except:
                price[j] = np.nan
                print('******** No transactions found ***********')
                continue

            val = trx['value']
            price[j] = float(val) / 1e18
            print('Sale value = {0} eth'.format(price[j]))
    print('----------------------------------------------------------------')

# ---------------------------------------------------------------- #
# plot data
project = 'Cryptoblots'
Ip = projects.index(project)
It = np.where(tokenID == Ip)[0]

plt.figure(1)
plt.plot(txTime[It], price[It], 'x')
plt.title(project)
plt.show(block = False)

# ---------------------------------------------------------------- #
# save data
fname = 'artblock_sales/sales_b{0}_b{1}'.format(block1, block2)
np.savez(fname, tokenID = tokenID, NSerial = NSerial, Nblock = Nblock, txTime = txTime, price = price)

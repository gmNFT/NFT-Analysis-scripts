# reads metadata from the lostpoets website
# N1 and N2 need to be set based on the range of poets available
# Typically I set N2 greater than the number of poets minted so the code
# will pull the available metadata for all of the minted poets
# the code will then crash, but you can save the data using the last two lines

from web3.auto.infura import w3
import requests
import numpy as np
from datetime import datetime

# lostpoets contract address
address = "0x4b3406a41399c7FD2BA65cbC93697Ad9E7eA61e5"

# metadata website
url_base = "https://lostpoets.api.manifoldxyz.dev/metadata/"

# first origin is indexed to 1
# last origin 1024
# first latent poet 1025
# last token 65536

# poets
N1 = 1025
N2 = 20000
Nrange = np.arange(N1, N2)

Name = []
Genre = []
Latent = []
Age = []
Origin = []

for j in Nrange:
    url = url_base + str(j)
    response = requests.request("GET", url)

    Name.append(response.json()['name'])
    print('Name: ', Name[-1])

    for j in range(len(response.json()['attributes'])):
        if response.json()['attributes'][j]['trait_type'] == 'Genre':
            Genre.append(response.json()['attributes'][j]['value'])
            print('Genre: ', Genre[-1])

        if response.json()['attributes'][j]['trait_type'] == 'Latent':
            Latent.append(response.json()['attributes'][j]['value'])
            print('Latent: ', Latent[-1])

        if response.json()['attributes'][j]['trait_type'] == 'Age':
            Age.append(response.json()['attributes'][j]['value'])
            print('Age: ', Age[-1])

        if response.json()['attributes'][j]['trait_type'] == 'Origin':
            Origin.append(response.json()['attributes'][j]['value'])
            print('Origin: ', Origin[-1])


fname = 'lostpoets.npz'
np.savez(fname, Name = Name, Genre = Genre, Latent = Latent, Age = Age, Origin = Origin)


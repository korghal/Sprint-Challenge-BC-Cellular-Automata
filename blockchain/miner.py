import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """

    start = timer()
    print(last_proof)
    print("Searching for next proof")
    proof = last_proof
    last_hash = f'{last_proof}'.encode()
    last_hash = hashlib.sha256(last_hash).hexdigest()
    #  TODO: Your code here

    proof_found = False

    while not proof_found:
        proof_found = valid_proof(last_hash, proof)
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """

    # TODO: Your code here!
    guess = f'{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    lead_sequence = guess_hash[0:6]
    str_last_hash = str(last_hash)
    end_sequence = str_last_hash[::-1] # Reverse the hash end_sequence = "654321999..."
    end_sequence = end_sequence[:6] # Get the first 6 items of the reversed hash : "654321"
    end_sequence = end_sequence[::-1] # Reverse them again : "123456"
    #print(f'lead_sequence: {lead_sequence}, end_sequence: {end_sequence}')
    if lead_sequence == end_sequence:
        return True
    else:
        return False

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        #node = "https://lambda-coin.herokuapp.com"
        node = "https://lambda-coin-test-2.herokuapp.com"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                    "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))

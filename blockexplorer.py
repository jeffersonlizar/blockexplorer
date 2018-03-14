import requests
import json


class BlockExplorer:
    base_url = 'https://blockexplorer.com'

    def __init__(self, testnet='prod'):
        if testnet == 'test':
            self.base_url = 'https://testnet.blockexplorer.com'

    def check_confirmations(self, txid, amount, receiver):
        confirmations = 0
        value = 0
        response_server = False
        valid_address = False
        time = None
        path = '/api/tx/{0}'.format(txid)
        uri = self.base_url + path
        response = requests.get(uri)
        if response.ok:
            response_server = True
            json_data = json.loads(response.content.decode("utf-8"))
            confirmations = json_data.get('confirmations')
            time = json_data.get('time')
            transactions = json_data.get('vout')
            for transaction in transactions:
                value = float(transaction['value'])
                # if value == amount:
                #     for address in transaction.get('scriptPubKey').get('addresses'):
                #         if address == receiver:
                #             valid_address = True
                #             break
                #     break
                addresses = transaction.get('scriptPubKey').get('addresses')
                if len(addresses) == 1:
                    if addresses[0] == receiver:
                        valid_address = True
                        break
        data = ({
            'confirmations': confirmations,
            'amount': value,
            'valid_address': valid_address,
            'time': time,
            'response_server': response_server,
        })
        return data

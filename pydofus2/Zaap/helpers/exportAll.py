import json

from pydofus2.Zaap.helpers.CryptoHelper import CryptoHelper

apikeys = CryptoHelper.get_all_stored_apikeys()
certs = CryptoHelper.get_all_stored_certificates()

with open("accounts.json", "w") as f:
    json.dump(apikeys, f, indent=4)
    
with open("certs.json", "w") as f:
    json.dump(certs, f, indent=4)
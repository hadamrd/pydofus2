
from pyd2bot.logic.managers.AccountManager import AccountManager
from pyd2bot.thriftServer.pyd2botService.ttypes import D2BotError
from pydofus2.Zaap.helpers.CryptoHelper import CryptoHelper
from pydofus2.com.ankamagames.atouin.BrowserRequests import HttpError

apikeys = CryptoHelper.get_all_stored_apikeys()
certs = CryptoHelper.get_all_stored_certificates()
AccountManager.clear()
discovered_accounts = []
for apikey_details in apikeys:
    keydata = apikey_details['apikey']
    apikey = keydata['key']
    certid = ""
    certhash = ""
    if 'certificate' in keydata:
        certid = keydata['certificate']['id']
        for cert in certs:
            certdata = cert['cert']
            if certdata['id'] == certid:
                certhash = cert['hash']
                break
    try:
        account_data = AccountManager.fetch_account(1, apikey, certid, certhash)
    except HttpError as e:
        print(f"Failed to get login token for reason: {e.body}")
    except D2BotError as e:
        print(f"Failed to fetch characters from game server:\n{e.message}")

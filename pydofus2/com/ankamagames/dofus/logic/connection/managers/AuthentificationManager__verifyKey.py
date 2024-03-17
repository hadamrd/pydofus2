from Cryptodome.PublicKey import RSA

from pydofus2.com.ankamagames.jerakine.types.BinaryDofusData import \
    BinaryResource


class AuthentificationManager__verifyKey(BinaryResource):
    ID = "115"

    @classmethod
    def create(cls) -> RSA.RsaKey:
        return RSA.import_key(cls.getBinaries())

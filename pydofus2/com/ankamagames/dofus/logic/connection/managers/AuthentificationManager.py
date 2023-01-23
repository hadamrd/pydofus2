from argparse import ArgumentError
from pydofus2.com.ankamagames.dofus.BuildInfos import BuildInfos
from pydofus2.com.ankamagames.dofus.logic.connection.actions.LoginValidationAction import (
    LoginValidationAction,
)
from pydofus2.com.ankamagames.dofus.logic.connection.managers.AuthentificationManager__verifyKey import (
    AuthentificationManager__verifyKey,
)
from pydofus2.com.ankamagames.dofus.network.messages.connection.IdentificationMessage import (
    IdentificationMessage,
)
from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.metaclasses.Singleton import Singleton
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import ByteArray
from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage
from pydofus2.com.ankamagames.jerakine.types.Version import Version
from pydofus2.com.hurlan.crypto.symmetric.AESKey import AESKey
from pydofus2.com.hurlan.crypto.symmetric.CBCMode import CBCMode
from pydofus2.com.hurlan.crypto.symmetric.NullPAd import NullPad
from pydofus2.com.hurlan.crypto.symmetric.PKCS1 import PKCS1
from pydofus2.com.hurlan.crypto.symmetric.PSAKey import RSACipher
from pydofus2.com.hurlan.crypto.symmetric.SimpleIVMode import SimpleIVMode
from Cryptodome.PublicKey import RSA

logger = Logger("Dofus2")

class AuthentificationManager(metaclass=Singleton):
    _verifyKey = AuthentificationManager__verifyKey.create()
    AES_KEY_LENGTH = 32

    def __init__(self) -> None:
        self._publicKey: str = None
        self._salt: str = None
        self.gameServerTicket: str = None
        self._AESKey: ByteArray = None
        self.nextToken: str = None
        self.tokenMode: bool = None
        self.username: str = "   "
        self._password = None
        self._certificate = None
        self._lva = None
        super().__init__()
    
    @property
    def loginValidationAction(self) -> LoginValidationAction:
        return self._lva

    def initAESKey(self):
        self._AESKey = AESKey.generateRandomAESKey(self.AES_KEY_LENGTH)

    def setSalt(self, salt: str) -> None:
        if len(salt) < 32:
            logger.warn("Authentification salt size is lower than 32 ")
        while len(salt) < 32:
            salt += " "
        self._salt = salt

    def setPublicKey(self, enc_publicKey: list[int]):
        baSignedKey = ByteArray.from_int8Arr(enc_publicKey)
        rsacipher = RSACipher(self._verifyKey, PKCS1())
        ba_pubKey = ByteArray()
        if not rsacipher.verify(baSignedKey, ba_pubKey):
            raise Exception("Pubkey Sign validation failed!")
        self._publicKey = "-----BEGIN PUBLIC KEY-----\n" + str(ba_pubKey) + "\n-----END PUBLIC KEY-----"

    @loginValidationAction.setter
    def loginValidationAction(self, lva: LoginValidationAction):
        self._lva = lva

    def getCanAutoConnectWithToken(self) -> bool:
        return self.nextToken != None

    def setCredentials(self, username, password):
        self.username = username
        self._password = password

    def setToken(self, token: str):
        self._token = token
        self.username = "   "

    def getIdentificationMessage(self) -> IdentificationMessage:
        imsg = IdentificationMessage()
        imsg.init(
            autoconnect_ = self._lva.autoSelectServer,
            credentials_ = self.getAuthCredentials(),
            failedAttempts_ = [],
            lang_ = "fr",
            serverId_ = self._lva.serverId,
            sessionOptionalSalt_ = 0,
            useCertificate_ = False,
            useLoginToken_ = True,
            version_ = Version.fromServerData(
                build = BuildInfos.VERSION.build,
                buildType = BuildInfos.VERSION.buildType,
                code = BuildInfos.VERSION.code,
                major = BuildInfos.VERSION.major,
                minor = BuildInfos.VERSION.minor,
            )
        )
        return imsg

    def getAuthCredentials(self) -> list[int]:
        baIn = ByteArray()
        baIn += bytes(self._salt, "utf")
        baIn += self._AESKey
        baIn += len(self.username).to_bytes(1, "big")
        baIn += bytes(self.username, "utf")
        baIn += bytes(self._token, "utf")
        rsa_key = RSA.importKey(bytes(self._publicKey, "utf"))
        rsacipher = RSACipher(rsa_key, PKCS1())
        baOut = rsacipher.encrypt(baIn)
        return baOut.to_int8Arr()

    def decodeWithAES(self, byteArrayOrVector) -> ByteArray:
        aescipher = SimpleIVMode(CBCMode(AESKey(self._AESKey), NullPad()))
        result = ByteArray()
        result.writeByteArray(self._AESKey, 0, 16)

        if type(byteArrayOrVector) == list:
            for i in byteArrayOrVector:
                result.writeByte(i, signed=True)

        else:
            if not isinstance(byteArrayOrVector, ByteArray):
                raise ArgumentError("Argument must be a bytearray or a vector of int/uint")
            result.writeByteArray(byteArrayOrVector)

        aescipher.decrypt(result)
        return result

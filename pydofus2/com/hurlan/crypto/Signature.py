import hashlib
import traceback

from Cryptodome.PublicKey import RSA

from pydofus2.com.ankamagames.jerakine.logger.Logger import Logger
from pydofus2.com.ankamagames.jerakine.network.CustomDataWrapper import \
    ByteArray
from pydofus2.com.hurlan.crypto.SignatureKey import SignatureKey
from pydofus2.com.hurlan.crypto.symmetric.PKCS1 import PKCS1
from pydofus2.com.hurlan.crypto.symmetric.PSAKey import RSACipher


class SignatureError(Exception):
    pass


class Signature:
    ANKAMA_SIGNED_FILE_HEADER: str = "AKSF"
    SIGNATURE_HEADER: str = "AKSD"

    def __init__(self, key1: SignatureKey, key2: RSA.RsaKey):
        self._keyV1 = key1
        self._keyV2 = key2

    def verify(self, input: ByteArray, message: bytes) -> ByteArray:
        headerSize = input.readUnsignedShort()
        if headerSize != len(self.ANKAMA_SIGNED_FILE_HEADER):
            input.position = 0
            headerPosition = input.remaining() - len(self.ANKAMA_SIGNED_FILE_HEADER)
            input.position = headerPosition
            header = input.readUTFBytes(len(self.ANKAMA_SIGNED_FILE_HEADER))
            if header == self.ANKAMA_SIGNED_FILE_HEADER:
                return self.verifyV2Signature(input, headerPosition)
        else:
            header = input.readUTFBytes(len(self.ANKAMA_SIGNED_FILE_HEADER))
            if header == self.ANKAMA_SIGNED_FILE_HEADER:
                formatVersion = int(input.readShort())
                Logger().debug(f"Signature format version: {formatVersion}")
                if formatVersion != 1:
                    raise SignatureError(f"Invalid signature format version, expected 1, got {formatVersion}.")
                signature_length = input.readInt()
                signature = input.readBytes(0, signature_length)
                if not input.remaining() == 0:
                    Logger().warning("Too much data found in the signature.")
                return self.verifyV1Signature(signature, message)
        raise SignatureError("Invalid header")

    def verifyV2Signature(self, input: ByteArray, headerPosition: int) -> bool:
        if not self._keyV2:
            raise SignatureError("No key for self signature version (2)")
        try:
            input.position = headerPosition - 4
            signedDataLenght = input.readShort()
            input.position = headerPosition - 4 - signedDataLenght
            cryptedData = input.readBytes(0, signedDataLenght)
            rsaceipher = RSACipher(self._keyV2, PKCS1())
            sigData = ByteArray()
            if not rsaceipher.verify(cryptedData, sigData):
                return False
            sigData.position = 0
            sigHeader = sigData.readUTF()
            if sigHeader != self.SIGNATURE_HEADER:
                return None
            sigData.readByte()
            sigData.readInt()
            sigData.readInt()
            sigFileLenght = sigData.readInt()
            if sigFileLenght != headerPosition - 4 - signedDataLenght:
                return None
            hashType = sigData.readByte()
            sigHash = sigData.readUTF()
            input.position = 0
            output = input.readBytes(0, headerPosition - 4 - signedDataLenght)
            if hashType == 0:
                contentHash = hashlib.md5(output).hexdigest()
            elif hashType == 1:
                contentHash = hashlib.sha256(output).hexdigest()
            else:
                return None
            if sigHash != contentHash:
                return None
        except Exception as e:
            traceback.print_exc()
            return None
        return output

    def verifyV1Signature(self, signature: ByteArray, message: str) -> bytearray:
        decryptedHash = ByteArray()
        rsacipher = RSACipher(self._keyV1, PKCS1())
        rsacipher.verify(signature, decryptedHash)
        decryptedHash.position = 0
        randomPart = decryptedHash[0]

        # Apply XOR starting from the third byte
        for i in range(2, len(decryptedHash)):
            decryptedHash[i] ^= randomPart

        expected_msg_len = decryptedHash.readUnsignedInt()
        signHash = decryptedHash.readUTFBytes(decryptedHash.remaining())[1:]
        
        message_bytes = message.encode("utf-8")
        message_hash = hashlib.md5(message_bytes).hexdigest()[1:]
        
        if signHash and signHash == message_hash and expected_msg_len == len(message_bytes):
            return message_bytes
        else:
            return None

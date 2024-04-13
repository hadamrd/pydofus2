from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class CharacterDeletionPrepareMessage(NetworkMessage):
    characterId: int
    characterName: str
    secretQuestion: str
    needSecretAnswer: bool

    def init(self, characterId_: int, characterName_: str, secretQuestion_: str, needSecretAnswer_: bool):
        self.characterId = characterId_
        self.characterName = characterName_
        self.secretQuestion = secretQuestion_
        self.needSecretAnswer = needSecretAnswer_

        super().__init__()

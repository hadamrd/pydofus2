from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import \
    NetworkMessage


class ReportRequestMessage(NetworkMessage):
    targetId: int
    categories: list[int]
    description: str

    def init(self, targetId_: int, categories_: list[int], description_: str):
        self.targetId = targetId_
        self.categories = categories_
        self.description = description_

        super().__init__()

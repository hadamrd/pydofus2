from pydofus2.com.ankamagames.jerakine.network.NetworkMessage import NetworkMessage


class OpenGuideBookMessage(NetworkMessage):
    articleId: int

    def init(self, articleId_: int):
        self.articleId = articleId_

        super().__init__()

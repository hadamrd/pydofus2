import uuid


class UIDUtil:

    @staticmethod
    def createUID():
        return str(uuid.uuid4())

    @staticmethod
    def isUID(uid):
        try:
            uuid.UUID(uid)
            return True
        except ValueError:
            return False

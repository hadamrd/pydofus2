from pydofus2.com.ankamagames.dofus.network.messages.web.haapi.HaapiValidationMessage import HaapiValidationMessage


class HaapiBuyValidationMessage(HaapiValidationMessage):
    amount: int
    email: str

    def init(self, amount_: int, email_: str, action_: int, code_: int):
        self.amount = amount_
        self.email = email_

        super().init(action_, code_)

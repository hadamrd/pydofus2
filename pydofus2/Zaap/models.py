from typing import Optional
from pydantic import BaseModel


class Certificate(BaseModel):
    id: int
    encodedCertificate: str
    login: str

    def __repr__(self):
        return f"Certificate(id={self.id}, login='{self.login}')"


class StoredApikey(BaseModel):
    key: str
    provider: str
    refreshToken: str
    isStayLoggedIn: bool
    accountId: int
    login: str
    certificate: Optional[Certificate]
    refreshDate: int

    def __repr__(self):
        return f"StoredApikey(login={self.login}, provider={self.provider}, accountId={self.accountId}, isStayLoggedIn={self.isStayLoggedIn})"


class StoredCertificate(BaseModel):
    id: int
    encodedCertificate: str
    login: str
    hash: Optional[str] = ""

    def __repr__(self):
        return f"StoredCertificate(id={self.id}, login='{self.login}', hash='{self.hash}')"

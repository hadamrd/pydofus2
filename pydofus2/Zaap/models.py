from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Optional

@dataclass_json
@dataclass
class Certificate:
    id: int
    encodedCertificate: str
    login: str

@dataclass_json
@dataclass
class StoredApikey:
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

@dataclass_json
@dataclass
class StoredCertificate:
    id: int
    encodedCertificate: str
    login: str
    hash: Optional[str] = field(default="")
    
    def __repr__(self):
        return f"StoredCertificate(id={self.id}, login='{self.login}', hash='{self.hash}')"
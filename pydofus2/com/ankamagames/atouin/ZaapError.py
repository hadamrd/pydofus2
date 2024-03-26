from pydofus2.com.ankamagames.atouin.ErrorsCodes import codeErrors


class ZaapError(Exception):
    def __init__(self, codeError="", error=None, displayMessageOnFront=True, complement={}):
        super().__init__()
        self.code = self.errorCode = ""
        self.message = self.errorMessage = ""
        self.displayMessageOnFront = displayMessageOnFront
        self.complement = complement
        self.codeErr = []
        if error:
            non_function_props = [prop for prop in dir(error) if not callable(getattr(error, prop))]
            for prop in non_function_props:
                setattr(self, prop, getattr(error, prop))
            self.errorMessage = self.message
            self.errorCode = self.code
        serialized_error = serialize_error(codeError)
        self.code = serialized_error["code"] or self.errorCode
        self.message = serialized_error["message"] or self.errorMessage
        self.codeErr = codeError.split(".")[1:]

    def toJSON(self):
        return {"code": self.code, "message": self.message}

    def __str__(self):
        return self.toJSON()


def serialize_error(code_error: str):
    obj: dict = None
    for key in code_error.split("."):
        obj = obj.get(key, {}) if obj else codeErrors.get(key.lower(), {})
    return obj if obj else {}

import json
import os

currdir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(currdir, "errorsCodes.json"), "r") as file:
    code_errors = json.load(file)


# Recursive function to build the code to error mapping
def build_map_code_to_err(dict_, result=None):
    if result is None:
        result = {}
    for key, value in dict_.items():
        # If a code is found, add it to the result mapping
        if "code" in value:
            result[value["code"]] = {"message": value["message"]}
        else:
            # Recursively fill the mapping for nested dictionaries
            build_map_code_to_err(value, result)
    return result


MAP_CODE_TO_ERR = build_map_code_to_err(code_errors)


class ZaapError(Exception):
    def __init__(self, code_error="", error=None, display_message_on_front=True, complement=None):
        super().__init__()
        self.errorCode = None
        self.errorMessage = None
        self.displayMessageOnFront = display_message_on_front
        self.complement = complement or {}

        if error:
            self.__dict__.update((k, v) for k, v in error.__dict__.items() if not callable(v))
            self.errorMessage = self.message
            self.errorCode = getattr(self, "code", None)

        serialized_error = self.serialize_error(code_error)
        self.code = serialized_error.get("code", self.errorCode)
        self.message = serialized_error.get("message", self.errorMessage)
        self.codeErr = code_error.split(".")[-1]

    def serialize_error(self, code_error):
        parts = code_error.split(".")
        result = code_errors
        for part in parts:
            result = result.get(part, {})
            if not result:
                break
        return result

    def toJSON(self):
        return json.dumps({"code": self.code, "message": self.message}, ensure_ascii=False)

    def __str__(self):
        return self.toJSON()

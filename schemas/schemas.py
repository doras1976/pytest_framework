from pydantic import BaseModel


# Ensures the API response contains an id (integer) and a name (string).
# If the API response is missing a field or has wrong data types, the test will fail.
class UserSchema(BaseModel):
    id: int
    name: str


USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"}
    },
    "required": ["id", "name"]
}


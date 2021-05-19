from typing import Any, Generic, TypeVar, cast

Value = TypeVar("Value")


class AutoAssignable(Generic[Value]):
    def __init__(self, value: Value, auto_assigned: bool):
        self.value: Value = value
        self.auto_assigned: bool = auto_assigned

    def serialize(self) -> dict[str, Any]:
        return {"value": self.value, "auto": self.auto_assigned}

    @staticmethod
    def deserialize(data: dict[str, Any]):
        obj = AutoAssignable[Value](
            cast(Value, data["value"]),
            data["auto"],
        )
        return obj

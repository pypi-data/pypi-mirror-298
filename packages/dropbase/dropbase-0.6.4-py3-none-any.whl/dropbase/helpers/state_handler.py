from typing import Any, Dict

from pydantic import BaseModel


def get_changed_values(old_state: BaseModel, new_state: BaseModel) -> Dict[str, Any]:
    def recursive_compare(old: Any, new: Any) -> Any:
        if isinstance(old, BaseModel) and isinstance(new, BaseModel):
            changes = {}
            for field in old.model_fields.keys():
                old_value = getattr(old, field, None)
                new_value = getattr(new, field, None)
                field_changes = recursive_compare(old_value, new_value)
                if field_changes is not None:
                    changes[field] = field_changes
            return changes if changes else None
        elif old is None and isinstance(new, BaseModel):
            return new.model_dump()
        elif isinstance(old, BaseModel) and new is None:
            return None
        # TODO: compare dics
        elif isinstance(old, dict) and isinstance(new, dict):
            if old != new:
                return new
        elif isinstance(old, list) and isinstance(new, list):
            if old != new:
                return new
            return None
        else:
            if old != new:
                return new
            return None

    if old_state.__class__ != new_state.__class__:
        raise ValueError("old_state and new_state must be instances of the same Pydantic model")

    return recursive_compare(old_state, new_state) or {}


def state_to_dict(state) -> dict:
    def recursive_model_dump(model_instance):
        if isinstance(model_instance, BaseModel):
            return {k: recursive_model_dump(v) for k, v in model_instance.model_dump().items()}
        elif isinstance(model_instance, list):
            return [recursive_model_dump(item) for item in model_instance]
        elif isinstance(model_instance, dict):
            return {k: recursive_model_dump(v) for k, v in model_instance.items()}
        else:
            return model_instance

    return recursive_model_dump(state)

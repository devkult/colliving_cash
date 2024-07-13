from dataclasses import dataclass


@dataclass
class BaseEntity:
    uuid: str
    created_at: str
    updated_at: str



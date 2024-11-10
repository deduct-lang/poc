__all__ = ("Entity",)


from dataclasses import dataclass


@dataclass
class Entity:
    """エンティティ"""

    name: str

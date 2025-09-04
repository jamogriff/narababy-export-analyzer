from dataclasses import dataclass


@dataclass
class ModelImportError:
    model: str
    expected: int
    actual: int

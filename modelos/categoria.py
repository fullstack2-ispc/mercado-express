from dataclasses import dataclass


@dataclass
class Categoria:
    nombre: str
    descripcion: str = ""
    id: int | None = None

from dataclasses import dataclass


@dataclass
class Producto:
    nombre: str
    precio: float
    stock: int
    id: int | None = None

from dataclasses import dataclass


@dataclass
class Proveedor:
    nombre: str
    telefono: str = ""
    email: str = ""
    id: int | None = None

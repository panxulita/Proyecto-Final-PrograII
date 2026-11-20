from abc import ABC, abstractmethod
from modelos import Equipo


class FabricaEquipo(ABC):

    @abstractmethod
    def crear_equipo(self, nombre, categoria_id, precio_diario,
                     stock_total):
        pass


class FabricaBalon(FabricaEquipo):

    def crear_equipo(self, nombre, categoria_id, precio_diario,
                     stock_total):

        return Equipo(
            nombre=nombre,
            categoria_id=categoria_id,
            precio_diario=precio_diario,
            stock_total=stock_total,
            stock_disponible=stock_total
        )


class FabricaRaqueta(FabricaEquipo):

    def crear_equipo(self, nombre, categoria_id, precio_diario,
                     stock_total):

        return Equipo(
            nombre=nombre,
            categoria_id=categoria_id,
            precio_diario=precio_diario,
            stock_total=stock_total,
            stock_disponible=stock_total
        )


class FabricaPesa(FabricaEquipo):

    def crear_equipo(self, nombre, categoria_id, precio_diario,
                     stock_total):

        return Equipo(
            nombre=nombre,
            categoria_id=categoria_id,
            precio_diario=precio_diario,
            stock_total=stock_total,
            stock_disponible=stock_total
        )


def obtener_fabrica(tipo_equipo):

    if tipo_equipo.lower() == "balon":
        return FabricaBalon()

    elif tipo_equipo.lower() == "raqueta":
        return FabricaRaqueta()

    elif tipo_equipo.lower() == "pesa":
        return FabricaPesa()

    else:
        raise ValueError("Tipo de equipo no reconocido.")

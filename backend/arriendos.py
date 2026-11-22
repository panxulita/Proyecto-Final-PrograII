from conexion import Session
from modelos import Arriendo, Equipo, Cliente
from datetime import date
from sqlalchemy.orm import joinedload

def registrar_arriendo(equipo_id, cliente_id, fecha_inicio,
                      fecha_fin_prevista, cantidad):

    if cantidad <= 0:
        return False, "La cantidad debe ser mayor a cero."

    if fecha_fin_prevista < fecha_inicio:
        return False, "La fecha de término no puede ser anterior al inicio."

    if fecha_inicio < date.today():
        return False, "La fecha de inicio no puede ser anterior a hoy."

    with Session.begin() as sesion:

        equipo = sesion.get(Equipo, equipo_id)
        cliente = sesion.get(Cliente, cliente_id)

        if equipo is None:
            return False, "El equipo no existe."

        if cliente is None:
            return False, "El cliente no existe."

        if cantidad > equipo.stock_disponible:
            return False, (
                f"Stock insuficiente. "
                f"Disponibles: {equipo.stock_disponible} unidades."
            )

        equipo.stock_disponible -= cantidad

        nuevo_arriendo = Arriendo(
            equipo_id=equipo_id,
            cliente_id=cliente_id,
            fecha_inicio=fecha_inicio,
            fecha_fin_prevista=fecha_fin_prevista,
            cantidad=cantidad,
            estado="ACTIVO"
        )

        sesion.add(nuevo_arriendo)

    return True, "Arriendo registrado correctamente."

def listar_arriendos_activos():
    with Session() as sesion:
        arriendos = (
            sesion.query(Arriendo)
            .options(
                joinedload(Arriendo.equipo).joinedload(Equipo.categoria),
                joinedload(Arriendo.cliente)
            )
            .filter(Arriendo.estado == "ACTIVO")
            .order_by(Arriendo.id)
            .all()
        )

        return arriendos

def listar_historial_arriendos():
    with Session() as sesion:
        arriendos = (
            sesion.query(Arriendo)
            .options(
                joinedload(Arriendo.equipo).joinedload(Equipo.categoria),
                joinedload(Arriendo.cliente)
            )
            .order_by(Arriendo.id)
            .all()
        )

        return arriendos


def registrar_devolucion(id_arriendo):

    with Session.begin() as sesion:

        arriendo = sesion.get(Arriendo, id_arriendo)

        if arriendo is None:
            print("Error: el arriendo no existe.")
            return False

        if arriendo.estado != "ACTIVO":
            print("Error: este arriendo ya fue devuelto.")
            return False

        equipo = sesion.get(Equipo, arriendo.equipo_id)

        if equipo is None:
            print("Error: no se encontro el equipo asociado.")
            return False

        equipo.stock_disponible += arriendo.cantidad

        arriendo.estado = "DEVUELTO"

    print("Devolucion registrada correctamente.")
    print("Stock restituido correctamente.")
    return True

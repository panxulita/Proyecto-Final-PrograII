from conexion import Session
from modelos import Equipo, Categoria
from backend.fabrica import obtener_fabrica
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload


def registrar_equipo(nombre, categoria_id, precio_diario,
                    stock_total, tipo_equipo):

    nombre = nombre.strip()

    if not nombre:
        return False, "El nombre del equipo es obligatorio."

    try:
        precio_diario = float(precio_diario)
        stock_total = int(stock_total)
    except (ValueError, TypeError):
        return False, "El precio y el stock deben ser valores numéricos válidos."

    if precio_diario <= 0:
        return False, "El precio diario debe ser mayor que cero."

    if stock_total < 0:
        return False, "El stock no puede ser negativo."

    try:
        with Session.begin() as sesion:

            categoria = sesion.get(Categoria, categoria_id)

            if categoria is None:
                return False, "La categoría seleccionada no existe."

            fabrica = obtener_fabrica(tipo_equipo)

            nuevo_equipo = fabrica.crear_equipo(
                nombre,
                categoria_id,
                precio_diario,
                stock_total
            )

            sesion.add(nuevo_equipo)

        return True, "Equipo registrado correctamente."

    except (IntegrityError, ValueError, TypeError) as error:
        return False, f"No se pudo registrar el equipo: {error}"


def listar_equipos():
    with Session() as sesion:
        equipos = (
            sesion.query(Equipo)
            .options(joinedload(Equipo.categoria))
            .order_by(Equipo.id)
            .all()
        )

        return equipos


def buscar_equipo(id_equipo):
    with Session() as sesion:
        equipo = sesion.get(Equipo, id_equipo)
        return equipo


def actualizar_equipo(id_equipo, nombre, categoria_id,
                     precio_diario, stock_total):

    nombre = nombre.strip()

    if not nombre:
        return False, "El nombre del equipo es obligatorio."

    try:
        precio_diario = float(precio_diario)
        stock_total = int(stock_total)
    except (ValueError, TypeError):
        return False, "El precio y el stock deben ser valores numéricos válidos."

    if precio_diario <= 0:
        return False, "El precio diario debe ser mayor que cero."

    if stock_total < 0:
        return False, "El stock no puede ser negativo."

    try:
        with Session.begin() as sesion:

            equipo = sesion.get(Equipo, id_equipo)
            categoria = sesion.get(Categoria, categoria_id)

            if equipo is None:
                return False, "El equipo no existe."

            if categoria is None:
                return False, "La categoría no existe."

            # Calculamos cuántos equipos están actualmente arrendados.
            stock_arrendado = (
                equipo.stock_total - equipo.stock_disponible
            )

            if stock_total < stock_arrendado:
                return False, (
                    "El nuevo stock no puede ser menor "
                    "a los equipos actualmente arrendados."
                )

            equipo.nombre = nombre
            equipo.categoria_id = categoria_id
            equipo.precio_diario = precio_diario
            equipo.stock_total = stock_total

            # Descontamos del nuevo stock los equipos arrendados.
            equipo.stock_disponible = stock_total - stock_arrendado

        return True, "Equipo actualizado correctamente."

    except (IntegrityError, ValueError, TypeError) as error:
        return False, f"No se pudo actualizar el equipo: {error}"


def eliminar_equipo(id_equipo):

    try:
        with Session.begin() as sesion:

            equipo = sesion.get(Equipo, id_equipo)

            if equipo is None:
                return False, "El equipo no existe."

            if equipo.arriendos:
                return False, (
                    "No se puede eliminar un equipo "
                    "que tenga arriendos asociados."
                )

            sesion.delete(equipo)

        return True, "Equipo eliminado correctamente."

    except IntegrityError:
        return False, "No se pudo eliminar el equipo porque tiene registros asociados."

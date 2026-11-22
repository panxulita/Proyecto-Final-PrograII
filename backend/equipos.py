from conexion import Session
from modelos import Equipo, Categoria
from backend.fabrica import obtener_fabrica
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

def registrar_equipo(nombre, categoria_id, precio_diario,
                     stock_total, tipo_equipo):

    nombre = nombre.strip()

    if not nombre:
        print("El nombre del equipo es obligatorio.")
        return False

    if precio_diario <= 0:
        print("El precio diario debe ser mayor que cero.")
        return False

    if stock_total < 0:
        print("El stock no puede ser negativo.")
        return False

    try:
        with Session.begin() as sesion:

            categoria = sesion.get(Categoria, categoria_id)

            if categoria is None:
                print("La categoría seleccionada no existe.")
                return False

            fabrica = obtener_fabrica(tipo_equipo)

            nuevo_equipo = fabrica.crear_equipo(
                nombre,
                categoria_id,
                precio_diario,
                stock_total
            )

            sesion.add(nuevo_equipo)

        print("Equipo registrado correctamente.")
        return True

    except (IntegrityError, ValueError) as error:
        print("No se pudo registrar el equipo:", error)
        return False

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

def actualizar_equipo(id_equipo, nombre, categoria_id, precio_diario,
                     stock_total):

    nombre = nombre.strip()

    if not nombre:
        print("El nombre del equipo es obligatorio.")
        return False

    if precio_diario <= 0:
        print("El precio diario debe ser mayor que cero.")
        return False

    if stock_total < 0:
        print("El stock no puede ser negativo.")
        return False

    try:
        with Session.begin() as sesion:

            equipo = sesion.get(Equipo, id_equipo)
            categoria = sesion.get(Categoria, categoria_id)

            if equipo is None:
                print("El equipo no existe.")
                return False

            if categoria is None:
                print("La categoría no existe.")
                return False

            # Calculamos cuántos equipos están actualmente arrendados.
            stock_arrendado = equipo.stock_total - equipo.stock_disponible

            if stock_total < stock_arrendado:
                print("El nuevo stock no puede ser menor a los equipos arrendados.")
                return False

            equipo.nombre = nombre
            equipo.categoria_id = categoria_id
            equipo.precio_diario = precio_diario
            equipo.stock_total = stock_total

            # El stock disponible se calcula descontando los equipos arrendados.
            equipo.stock_disponible = stock_total - stock_arrendado

        print("Equipo actualizado correctamente.")
        return True

    except (IntegrityError, ValueError) as error:
        print("No se pudo actualizar el equipo:", error)
        return False

def eliminar_equipo(id_equipo):

    try:
        with Session.begin() as sesion:

            equipo = sesion.get(Equipo, id_equipo)

            if equipo is None:
                print("El equipo no existe.")
                return False

            if equipo.arriendos:
                print("No se puede eliminar un equipo que tenga arriendos asociados.")
                return False

            sesion.delete(equipo)

        print("Equipo eliminado correctamente.")
        return True

    except IntegrityError as error:
        print("No se pudo eliminar el equipo:", error)
        return False
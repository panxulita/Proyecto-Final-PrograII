from conexion import Session
from modelos import Categoria
from sqlalchemy.exc import IntegrityError


def registrar_categoria(nombre, descripcion):
    nombre = nombre.strip()
    descripcion = descripcion.strip()

    if nombre == "" or descripcion == "":
        return False, "Debe completar todos los datos."

    try:
        with Session.begin() as sesion:
            categoria_existente = sesion.query(Categoria).filter(
                Categoria.nombre == nombre
            ).first()

            if categoria_existente:
                return False, "Esta categoría ya existe."

            nueva_categoria = Categoria(
                nombre=nombre,
                descripcion=descripcion
            )

            sesion.add(nueva_categoria)

        return True, "Categoría registrada correctamente."

    except IntegrityError:
        return False, "No se pudo registrar la categoría."


def listar_categorias():
    with Session() as sesion:
        categorias = sesion.query(Categoria).order_by(
            Categoria.id
        ).all()

        return categorias


def buscar_categoria(id_categoria):
    with Session() as sesion:
        categoria = sesion.get(Categoria, id_categoria)
        return categoria


def actualizar_categoria(id_categoria, nombre, descripcion):
    nombre = nombre.strip()
    descripcion = descripcion.strip()

    if nombre == "" or descripcion == "":
        return False, "Debe completar todos los datos."

    try:
        with Session.begin() as sesion:
            categoria = sesion.get(Categoria, id_categoria)

            if categoria is None:
                return False, "Categoría no encontrada."

            categoria_repetida = sesion.query(Categoria).filter(
                Categoria.nombre == nombre,
                Categoria.id != id_categoria
            ).first()

            if categoria_repetida:
                return False, "Ya existe otra categoría con ese nombre."

            categoria.nombre = nombre
            categoria.descripcion = descripcion

        return True, "Categoría modificada correctamente."

    except IntegrityError:
        return False, "No se pudo modificar la categoría."


def eliminar_categoria(id_categoria):
    try:
        with Session.begin() as sesion:
            categoria = sesion.get(Categoria, id_categoria)

            if categoria is None:
                return False, "Categoría no encontrada."

            if categoria.equipos:
                return False, "No se puede eliminar una categoría que tiene equipos asociados."

            sesion.delete(categoria)

        return True, "Categoría eliminada correctamente."

    except IntegrityError:
        return False, "No se pudo eliminar la categoría porque tiene registros asociados."

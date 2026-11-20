from conexion import Session
from modelos import Categoria
from sqlalchemy.exc import IntegrityError


def registrar_categoria(nombre, descripcion):

    nombre = nombre.strip()
    descripcion = descripcion.strip()

    if nombre == "" or descripcion == "":
        print("Error: debe completar todos los datos.")
        return False

    try:
        with Session.begin() as sesion:

            categoria_existente = sesion.query(Categoria).filter(
                Categoria.nombre == nombre
            ).first()

            if categoria_existente:
                print("Error: esta categoria ya existe.")
                return False

            nueva_categoria = Categoria(
                nombre=nombre,
                descripcion=descripcion
            )

            sesion.add(nueva_categoria)

        print("Categoria registrada correctamente.")
        return True

    except IntegrityError:
        print("Error: no se pudo registrar la categoria.")
        return False


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
        print("Error: debe completar todos los datos.")
        return False

    try:
        with Session.begin() as sesion:

            categoria = sesion.get(Categoria, id_categoria)

            if categoria is None:
                print("Error: categoria no encontrada.")
                return False

            categoria_repetida = sesion.query(Categoria).filter(
                Categoria.nombre == nombre,
                Categoria.id != id_categoria
            ).first()

            if categoria_repetida:
                print("Error: ya existe otra categoria con ese nombre.")
                return False

            categoria.nombre = nombre
            categoria.descripcion = descripcion

        print("Categoria modificada correctamente.")
        return True

    except IntegrityError:
        print("Error: no se pudo modificar la categoria.")
        return False


def eliminar_categoria(id_categoria):

    with Session.begin() as sesion:

        categoria = sesion.get(Categoria, id_categoria)

        if categoria is None:
            print("Error: categoria no encontrada.")
            return False

        if categoria.equipos:
            print("Error: no se puede eliminar una categoria")
            print("que tiene equipos asociados.")
            return False

        sesion.delete(categoria)

    print("Categoria eliminada correctamente.")
    return True

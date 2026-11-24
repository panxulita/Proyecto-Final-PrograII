from conexion import Session
from modelos import Cliente
from sqlalchemy.exc import IntegrityError


def registrar_cliente(nombre, correo, telefono):
    nombre = nombre.strip()
    correo = correo.strip().lower()
    telefono = telefono.strip()

    if nombre == "" or correo == "" or telefono == "":
        return False, "Debe completar todos los datos."

    if "@" not in correo or "." not in correo:
        return False, "Ingrese un correo válido."

    try:
        with Session.begin() as sesion:
            cliente_existente = sesion.query(Cliente).filter(
                Cliente.correo == correo
            ).first()

            if cliente_existente:
                return False, "Ya existe un cliente con ese correo."

            nuevo_cliente = Cliente(
                nombre=nombre,
                correo=correo,
                telefono=telefono
            )

            sesion.add(nuevo_cliente)

        return True, "Cliente registrado correctamente."

    except IntegrityError:
        return False, "No se pudo registrar el cliente."


def listar_clientes():
    with Session() as sesion:
        clientes = sesion.query(Cliente).order_by(
            Cliente.id
        ).all()

        return clientes


def buscar_cliente(id_cliente):
    with Session() as sesion:
        cliente = sesion.get(Cliente, id_cliente)
        return cliente


def actualizar_cliente(id_cliente, nombre, correo, telefono):
    nombre = nombre.strip()
    correo = correo.strip().lower()
    telefono = telefono.strip()

    if nombre == "" or correo == "" or telefono == "":
        return False, "Debe completar todos los datos."

    if "@" not in correo or "." not in correo:
        return False, "Ingrese un correo válido."

    try:
        with Session.begin() as sesion:
            cliente = sesion.get(Cliente, id_cliente)

            if cliente is None:
                return False, "Cliente no encontrado."

            correo_repetido = sesion.query(Cliente).filter(
                Cliente.correo == correo,
                Cliente.id != id_cliente
            ).first()

            if correo_repetido:
                return False, "Ese correo pertenece a otro cliente."

            cliente.nombre = nombre
            cliente.correo = correo
            cliente.telefono = telefono

        return True, "Cliente modificado correctamente."

    except IntegrityError:
        return False, "No se pudo modificar el cliente."


def eliminar_cliente(id_cliente):
    try:
        with Session.begin() as sesion:
            cliente = sesion.get(Cliente, id_cliente)

            if cliente is None:
                return False, "Cliente no encontrado."

            if cliente.arriendos:
                return False, "No se puede eliminar un cliente que tiene arriendos registrados."

            sesion.delete(cliente)

        return True, "Cliente eliminado correctamente."

    except IntegrityError:
        return False, "No se puede eliminar el cliente porque tiene registros asociados."

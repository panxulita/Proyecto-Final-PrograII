from conexion import Session
from modelos import Cliente
from sqlalchemy.exc import IntegrityError


def registrar_cliente(nombre, correo, telefono):

    nombre = nombre.strip()
    correo = correo.strip().lower()
    telefono = telefono.strip()

    if nombre == "" or correo == "" or telefono == "":
        print("Error: debe completar todos los datos.")
        return False

  
    if "@" not in correo or "." not in correo:
        print("Error: ingrese un correo valido.")
        return False

    try:
        with Session.begin() as sesion:

            cliente_existente = sesion.query(Cliente).filter(
                Cliente.correo == correo
            ).first()

            if cliente_existente:
                print("Error: ya existe un cliente con ese correo.")
                return False

            nuevo_cliente = Cliente(
                nombre=nombre,
                correo=correo,
                telefono=telefono
            )

            sesion.add(nuevo_cliente)

        print("Cliente registrado correctamente.")
        return True

    except IntegrityError:
        print("Error: no se pudo registrar el cliente.")
        return False


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
        print("Error: debe completar todos los datos.")
        return False

    if "@" not in correo or "." not in correo:
        print("Error: ingrese un correo valido.")
        return False

    try:
        with Session.begin() as sesion:

            cliente = sesion.get(Cliente, id_cliente)

            if cliente is None:
                print("Error: cliente no encontrado.")
                return False

            correo_repetido = sesion.query(Cliente).filter(
                Cliente.correo == correo,
                Cliente.id != id_cliente
            ).first()

            if correo_repetido:
                print("Error: ese correo pertenece a otro cliente.")
                return False

            cliente.nombre = nombre
            cliente.correo = correo
            cliente.telefono = telefono

        print("Cliente modificado correctamente.")
        return True

    except IntegrityError:
        print("Error: no se pudo modificar el cliente.")
        return False


def eliminar_cliente(id_cliente):

    with Session.begin() as sesion:

        cliente = sesion.get(Cliente, id_cliente)

        if cliente is None:
            print("Error: cliente no encontrado.")
            return False

      
        if cliente.arriendos:
            print("Error: no se puede eliminar un cliente")
            print("que tiene arriendos registrados.")
            return False

        sesion.delete(cliente)

    print("Cliente eliminado correctamente.")
    return True

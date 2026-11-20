from conexion import engine
from modelos import Base
from sqlalchemy import inspect


def crear_tablas():

    Base.metadata.create_all(bind=engine)

    print("Base de datos creada correctamente.")

    
    inspector = inspect(engine)
    tablas = inspector.get_table_names()

    print("\nTablas creadas:")

    for tabla in tablas:
        print("-", tabla)


def main():

    print("================================")
    print(" SISTEMA DE ARRIENDO DE EQUIPOS")
    print("================================")

    crear_tablas()


if __name__ == "__main__":
    main()

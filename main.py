import tkinter as tk
import subprocess
import sys

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


def abrir_modulo(modulo):
    subprocess.Popen([sys.executable, "-m", modulo])


def main():
    crear_tablas()

    ventana = tk.Tk()
    ventana.title("Sistema de Arriendo de Equipos Deportivos")
    ventana.geometry("500x620")
    ventana.resizable(False, False)

    titulo = tk.Label(
        ventana,
        text="SISTEMA DE ARRIENDO",
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=25)

    subtitulo = tk.Label(
        ventana,
        text="Gestión de equipamiento deportivo",
        font=("Arial", 11)
    )
    subtitulo.pack(pady=5)

    botones = tk.Frame(ventana)
    botones.pack(pady=30)

    tk.Button(
        botones,
        text="Gestionar Clientes",
        width=30,
        height=2,
        command=lambda: abrir_modulo("interfaz.clientes")
    ).pack(pady=8)

    tk.Button(
        botones,
        text="Gestionar Equipos",
        width=30,
        height=2,
        command=lambda: abrir_modulo("interfaz.equipos")
    ).pack(pady=8)

    tk.Button(
        botones,
        text="Gestionar Categorías",
        width=30,
        height=2,
        command=lambda: abrir_modulo("interfaz.categorias")
    ).pack(pady=8)

    tk.Button(
        botones,
        text="Gestionar Arriendos",
        width=30,
        height=2,
        command=lambda: abrir_modulo("interfaz.arriendos")
    ).pack(pady=8)

    tk.Button(
        botones,
        text="Estadísticas",
        width=30,
        height=2,
        command=lambda: abrir_modulo("interfaz.graficos")
    ).pack(pady=8)

    ventana.mainloop()


if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from conexion import Session
from modelos import Cliente, Equipo, Arriendo
from backend.arriendos import registrar_arriendo, registrar_devolucion


def abrir_arriendos():

    ventana = tk.Tk()
    ventana.title("Gestion de arriendos")
    ventana.geometry("850x550")

    tk.Label(ventana, text="GESTION DE ARRIENDOS",
             font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(ventana, text="Cliente").pack()
    cliente = ttk.Combobox(ventana, width=35, state="readonly")
    cliente.pack()

    tk.Label(ventana, text="Equipo").pack()
    equipo = ttk.Combobox(ventana, width=35, state="readonly")
    equipo.pack()

    tk.Label(ventana, text="Fecha de inicio (AAAA-MM-DD)").pack()
    fecha_inicio = tk.Entry(ventana, width=35)
    fecha_inicio.pack()

    tk.Label(ventana, text="Fecha de termino (AAAA-MM-DD)").pack()
    fecha_fin = tk.Entry(ventana, width=35)
    fecha_fin.pack()

    tk.Label(ventana, text="Cantidad").pack()
    cantidad = tk.Entry(ventana, width=35)
    cantidad.pack()

    tabla = ttk.Treeview(
        ventana,
        columns=("ID", "Cliente", "Equipo", "Inicio",
                 "Termino", "Cantidad", "Estado"),
        show="headings"
    )

    for columna in ("ID", "Cliente", "Equipo", "Inicio",
                    "Termino", "Cantidad", "Estado"):
        tabla.heading(columna, text=columna)
        tabla.column(columna, width=100, anchor="center")

    tabla.pack(pady=15, fill="x")

    def cargar_datos():

        with Session() as sesion:

            clientes = sesion.query(Cliente).order_by(Cliente.id).all()
            equipos = sesion.query(Equipo).filter(
                Equipo.stock_disponible > 0
            ).order_by(Equipo.id).all()

            cliente["values"] = [
                str(c.id) + " - " + c.nombre for c in clientes
            ]

            equipo["values"] = [
                str(e.id) + " - " + e.nombre for e in equipos
            ]

    modo_arriendos = tk.StringVar(value="ACTIVOS")

    def cargar_arriendos():
        tabla.delete(*tabla.get_children())

        with Session() as sesion:
            consulta = sesion.query(
                Arriendo.id,
                Cliente.nombre,
                Equipo.nombre,
                Arriendo.fecha_inicio,
                Arriendo.fecha_fin_prevista,
                Arriendo.cantidad,
                Arriendo.estado
            ).join(Cliente).join(Equipo)

            if modo_arriendos.get() == "ACTIVOS":
                consulta = consulta.filter(Arriendo.estado == "ACTIVO")

            arriendos = consulta.order_by(Arriendo.id).all()

        for a in arriendos:
            tabla.insert("", "end", values=(
                a[0],
                a[1],
                a[2],
                str(a[3]),
                str(a[4]),
                a[5],
                a[6]
            ))

    def cambiar_vista(modo):
        modo_arriendos.set(modo)
        cargar_arriendos()

    def guardar_arriendo():
        try:
            id_cliente = int(cliente.get().split(" - ")[0])
            id_equipo = int(equipo.get().split(" - ")[0])

            inicio = date.fromisoformat(fecha_inicio.get())
            termino = date.fromisoformat(fecha_fin.get())
            unidades = int(cantidad.get())

            resultado, mensaje = registrar_arriendo(
                id_equipo, id_cliente, inicio, termino, unidades
            )

            if resultado:
                messagebox.showinfo("Éxito", mensaje)
                cargar_arriendos()
                cargar_datos()
            else:
                messagebox.showerror("Error al registrar arriendo", mensaje)

        except (ValueError, IndexError):
            messagebox.showerror(
                "Error",
                "Revise los datos, la cantidad y las fechas ingresadas."
            )

    def devolver():

        seleccionado = tabla.selection()

        if seleccionado:
            datos = tabla.item(seleccionado[0], "values")

            if datos[6] != "ACTIVO":
                messagebox.showwarning(
                    "Aviso", "Este arriendo ya fue devuelto."
                )
                return

            if messagebox.askyesno("Confirmar", "¿Registrar devolucion?"):

                if registrar_devolucion(int(datos[0])):
                    cargar_arriendos()
                    cargar_datos()
        else:
            messagebox.showwarning(
                "Aviso", "Seleccione un arriendo."
            )

    tk.Button(
        ventana,
        text="Registrar arriendo",
        command=guardar_arriendo
    ).pack(side="left", padx=30)

    tk.Button(
        ventana,
        text="Registrar devolucion",
        command=devolver
    ).pack(side="left", padx=10)

    filtros = tk.Frame(ventana)
    filtros.pack(pady=5)

    tk.Button(
        filtros,
        text="Arriendos activos",
        command=lambda: cambiar_vista("ACTIVOS")
    ).pack(side="left", padx=5)

    tk.Button(
        filtros,
        text="Historial completo",
        command=lambda: cambiar_vista("HISTORIAL")
    ).pack(side="left", padx=5)

    cargar_datos()
    cargar_arriendos()

    ventana.mainloop()

if __name__ == "__main__":
    abrir_arriendos()

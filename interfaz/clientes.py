
import tkinter as tk
from tkinter import ttk, messagebox

from backend.clientes import (
    registrar_cliente,
    listar_clientes,
    actualizar_cliente,
    eliminar_cliente
)


def abrir_clientes():

    ventana = tk.Tk()
    ventana.title("Gestion de clientes")
    ventana.geometry("700x450")

    tk.Label(ventana, text="GESTION DE CLIENTES",
             font=("Arial", 16, "bold")).pack(pady=10)

    nombre = tk.Entry(ventana, width=35)
    correo = tk.Entry(ventana, width=35)
    telefono = tk.Entry(ventana, width=35)

    tk.Label(ventana, text="Nombre").pack()
    nombre.pack()

    tk.Label(ventana, text="Correo").pack()
    correo.pack()

    tk.Label(ventana, text="Telefono").pack()
    telefono.pack()

    tabla = ttk.Treeview(
        ventana,
        columns=("ID", "Nombre", "Correo", "Telefono"),
        show="headings"
    )

    for columna in ("ID", "Nombre", "Correo", "Telefono"):
        tabla.heading(columna, text=columna)

    tabla.pack(pady=15)

    def cargar_clientes():
        tabla.delete(*tabla.get_children())

        for cliente in listar_clientes():
            tabla.insert("", "end", values=(
                cliente.id,
                cliente.nombre,
                cliente.correo,
                cliente.telefono
            ))

    def limpiar():
        nombre.delete(0, tk.END)
        correo.delete(0, tk.END)
        telefono.delete(0, tk.END)

    def guardar():
        resultado = registrar_cliente(
            nombre.get(), correo.get(), telefono.get()
        )

        if resultado:
            messagebox.showinfo("Aviso", "Cliente registrado")
            limpiar()
            cargar_clientes()

    def seleccionar(evento):
        seleccionado = tabla.selection()

        if seleccionado:
            datos = tabla.item(seleccionado[0], "values")
            limpiar()
            nombre.insert(0, datos[1])
            correo.insert(0, datos[2])
            telefono.insert(0, datos[3])

    def modificar():
        seleccionado = tabla.selection()

        if seleccionado:
            datos = tabla.item(seleccionado[0], "values")

            resultado = actualizar_cliente(
                int(datos[0]),
                nombre.get(),
                correo.get(),
                telefono.get()
            )

            if resultado:
                messagebox.showinfo("Aviso", "Cliente modificado")
                limpiar()
                cargar_clientes()
        else:
            messagebox.showwarning("Aviso", "Seleccione un cliente")

    def eliminar():
        seleccionado = tabla.selection()

        if seleccionado:
            datos = tabla.item(seleccionado[0], "values")

            if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
                if eliminar_cliente(int(datos[0])):
                    cargar_clientes()
                    limpiar()
        else:
            messagebox.showwarning("Aviso", "Seleccione un cliente")

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    tk.Button(ventana, text="Registrar", command=guardar).pack(side="left", padx=40)
    tk.Button(ventana, text="Modificar", command=modificar).pack(side="left")
    tk.Button(ventana, text="Eliminar", command=eliminar).pack(side="left", padx=10)

    cargar_clientes()
    ventana.mainloop()


if __name__ == "__main__":
    abrir_clientes()

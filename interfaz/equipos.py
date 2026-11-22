import tkinter as tk
from tkinter import ttk, messagebox

from backend.equipos import (
    registrar_equipo,
    listar_equipos,
    actualizar_equipo,
    eliminar_equipo
)

from backend.categorias import listar_categorias


def abrir_equipos():

    ventana = tk.Tk()
    ventana.title("Gestion de equipos")
    ventana.geometry("900x600")

    tk.Label(
        ventana,
        text="GESTION DE EQUIPOS",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    formulario = tk.Frame(ventana)
    formulario.pack(pady=10)

    nombre = tk.Entry(formulario, width=30)
    precio = tk.Entry(formulario, width=30)
    stock = tk.Entry(formulario, width=30)

    tk.Label(formulario, text="Nombre del equipo").grid(row=0, column=0, padx=5, pady=5)
    nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(formulario, text="Precio diario").grid(row=1, column=0, padx=5, pady=5)
    precio.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(formulario, text="Stock total").grid(row=2, column=0, padx=5, pady=5)
    stock.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(formulario, text="Categoria").grid(row=3, column=0, padx=5, pady=5)

    categoria = ttk.Combobox(formulario, width=27, state="readonly")
    categoria.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(formulario, text="Tipo de equipo").grid(row=4, column=0, padx=5, pady=5)

    tipo = ttk.Combobox(
        formulario,
        values=("balon", "raqueta", "pesa"),
        width=27,
        state="readonly"
    )
    tipo.grid(row=4, column=1, padx=5, pady=5)

    tabla = ttk.Treeview(
        ventana,
        columns=("ID", "Nombre", "Categoria", "Precio", "Stock", "Disponible"),
        show="headings"
    )

    columnas = ("ID", "Nombre", "Categoria", "Precio", "Stock", "Disponible")

    for columna in columnas:
        tabla.heading(columna, text=columna)

    tabla.column("ID", width=50)
    tabla.column("Nombre", width=200)
    tabla.column("Categoria", width=130)
    tabla.column("Precio", width=100)
    tabla.column("Stock", width=100)
    tabla.column("Disponible", width=100)

    tabla.pack(fill="both", expand=True, padx=20, pady=15)

    categorias_lista = []

    def cargar_categorias():
        categorias_lista.clear()
        categorias_lista.extend(listar_categorias())

        categoria["values"] = [
            f"{c.id} - {c.nombre}" for c in categorias_lista
        ]

    def cargar_equipos():
        tabla.delete(*tabla.get_children())

        for equipo in listar_equipos():
            tabla.insert("", "end", values=(
                equipo.id,
                equipo.nombre,
                equipo.categoria.nombre,
                equipo.precio_diario,
                equipo.stock_total,
                equipo.stock_disponible
            ))

    def limpiar():
        nombre.delete(0, tk.END)
        precio.delete(0, tk.END)
        stock.delete(0, tk.END)
        categoria.set("")
        tipo.set("")

    def guardar():
        try:
            nombre_equipo = nombre.get()
            precio_equipo = float(precio.get())
            stock_equipo = int(stock.get())

            if not categoria.get():
                messagebox.showwarning("Aviso", "Seleccione una categoria")
                return

            if not tipo.get():
                messagebox.showwarning("Aviso", "Seleccione el tipo de equipo")
                return

            categoria_id = int(categoria.get().split(" - ")[0])

            resultado = registrar_equipo(
                nombre_equipo,
                categoria_id,
                precio_equipo,
                stock_equipo,
                tipo.get()
            )

            if resultado:
                messagebox.showinfo("Aviso", "Equipo registrado correctamente")
                limpiar()
                cargar_equipos()

        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio y el stock deben ser numeros validos"
            )

    def seleccionar(evento):
        seleccionado = tabla.selection()

        if seleccionado:
            datos = tabla.item(seleccionado[0], "values")

            limpiar()

            nombre.insert(0, datos[1])
            precio.insert(0, datos[3])
            stock.insert(0, datos[4])

            for c in categorias_lista:
                if c.nombre == datos[2]:
                    categoria.set(f"{c.id} - {c.nombre}")
                    break

    def modificar():
        seleccionado = tabla.selection()

        if seleccionado:
            datos = tabla.item(seleccionado[0], "values")

            try:
                categoria_id = int(categoria.get().split(" - ")[0])

                resultado = actualizar_equipo(
                    int(datos[0]),
                    nombre.get(),
                    categoria_id,
                    float(precio.get()),
                    int(stock.get())
                )

                if resultado:
                    messagebox.showinfo(
                        "Aviso",
                        "Equipo modificado correctamente"
                    )
                    limpiar()
                    cargar_equipos()

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Verifique los datos ingresados"
                )

        else:
            messagebox.showwarning(
                "Aviso",
                "Seleccione un equipo para modificar"
            )
    def eliminar():
        seleccionado = tabla.selection()

        if seleccionado:
            datos = tabla.item(seleccionado[0], "values")

            confirmar = messagebox.askyesno(
                "Confirmar",
                f"¿Desea eliminar el equipo {datos[1]}?"
            )

            if confirmar:
                resultado = eliminar_equipo(int(datos[0]))

                if resultado:
                    messagebox.showinfo(
                        "Aviso",
                        "Equipo eliminado correctamente"
                    )
                    limpiar()
                    cargar_equipos()

        else:
            messagebox.showwarning(
                "Aviso",
                "Seleccione un equipo para eliminar"
            )

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    botones = tk.Frame(ventana)
    botones.pack(pady=10)

    tk.Button(
        botones,
        text="Registrar",
        command=guardar
    ).pack(side="left", padx=5)

    tk.Button(
        botones,
        text="Modificar",
        command=modificar
    ).pack(side="left", padx=5)

    tk.Button(
        botones,
        text="Eliminar",
        command=eliminar
    ).pack(side="left", padx=5)

    tk.Button(
        botones,
        text="Limpiar",
        command=limpiar
    ).pack(side="left", padx=5)

    tk.Button(
        botones,
        text="Actualizar lista",
        command=cargar_equipos
    ).pack(side="left", padx=5)

    cargar_categorias()
    cargar_equipos()

    ventana.mainloop()

if __name__ == "__main__":
    abrir_equipos()
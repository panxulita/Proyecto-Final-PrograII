import tkinter as tk
from tkinter import ttk, messagebox

from backend.categorias import (
    registrar_categoria,
    listar_categorias,
    actualizar_categoria,
    eliminar_categoria
)

def abrir_categorias():

    ventana = tk.Tk()
    ventana.title("Gestion de categorias")
    ventana.geometry("700x500")

    tk.Label(
        ventana,
        text="GESTION DE CATEGORIAS",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    formulario = tk.Frame(ventana)
    formulario.pack(pady=10)

    tk.Label(formulario, text="Nombre").grid(
        row=0, column=0, padx=5, pady=5
    )

    nombre = tk.Entry(formulario, width=35)
    nombre.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(formulario, text="Descripcion").grid(
        row=1, column=0, padx=5, pady=5
    )

    descripcion = tk.Entry(formulario, width=35)
    descripcion.grid(row=1, column=1, padx=5, pady=5)

    tabla = ttk.Treeview(
        ventana,
        columns=("ID", "Nombre", "Descripcion"),
        show="headings"
    )

    for columna in ("ID", "Nombre", "Descripcion"):
        tabla.heading(columna, text=columna)

    tabla.column("ID", width=60)
    tabla.column("Nombre", width=180)
    tabla.column("Descripcion", width=350)

    tabla.pack(fill="both", expand=True, padx=20, pady=15)

    def cargar_categorias():
        tabla.delete(*tabla.get_children())

        for categoria in listar_categorias():
            tabla.insert(
                "",
                "end",
                values=(
                    categoria.id,
                    categoria.nombre,
                    categoria.descripcion
                )
            )

    def limpiar():
        nombre.delete(0, tk.END)
        descripcion.delete(0, tk.END)

    def guardar():
        nombre_categoria = nombre.get().strip()
        descripcion_categoria = descripcion.get().strip()

        if not nombre_categoria:
            messagebox.showerror(
                "Error",
                "Debe ingresar el nombre de la categoria."
            )
            return

        if not descripcion_categoria:
            messagebox.showerror(
                "Error",
                "Debe ingresar la descripcion de la categoria."
            )
            return

        resultado, mensaje = registrar_categoria(
            nombre_categoria,
            descripcion_categoria
        )

        if resultado:
            messagebox.showinfo("Aviso", mensaje)
            limpiar()
            cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar(event):
        seleccionado = tabla.selection()

        if seleccionado:
            datos = tabla.item(seleccionado[0], "values")

            limpiar()
            nombre.insert(0, datos[1])
            descripcion.insert(0, datos[2])

    def modificar():
        seleccionado = tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Aviso",
                "Seleccione una categoria para modificar."
            )
            return

        datos = tabla.item(seleccionado[0], "values")

        nombre_categoria = nombre.get().strip()
        descripcion_categoria = descripcion.get().strip()

        if not nombre_categoria:
            messagebox.showerror(
                "Error",
                "Debe ingresar el nombre de la categoria."
            )
            return

        if not descripcion_categoria:
            messagebox.showerror(
                "Error",
                "Debe ingresar la descripcion de la categoria."
            )
            return

        resultado, mensaje = actualizar_categoria(
            int(datos[0]),
            nombre_categoria,
            descripcion_categoria
        )

        if resultado:
            messagebox.showinfo("Aviso", mensaje)
            limpiar()
            cargar_categorias()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar():
        seleccionado = tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Aviso",
                "Seleccione una categoria para eliminar."
            )
            return

        datos = tabla.item(seleccionado[0], "values")

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Desea eliminar la categoria {datos[1]}?"
        )

        if confirmar:
            resultado, mensaje = eliminar_categoria(int(datos[0]))

            if resultado:
                messagebox.showinfo("Aviso", mensaje)
                limpiar()
                cargar_categorias()
            else:
                messagebox.showerror(
                    "No se puede eliminar",
                    mensaje
                )

    def deseleccionar_al_hacer_clic(event):
        fila = tabla.identify_row(event.y)

        if fila and fila in tabla.selection():
            tabla.selection_remove(fila)
            limpiar()
            return "break"

    tabla.bind("<<TreeviewSelect>>", seleccionar)
    tabla.bind("<Button-1>", deseleccionar_al_hacer_clic)

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
        command=cargar_categorias
    ).pack(side="left", padx=5)

    cargar_categorias()
    ventana.mainloop()

if __name__ == "__main__":
    abrir_categorias()
from collections import Counter
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from backend.arriendos import listar_historial_arriendos


def abrir_graficos():
    ventana = tk.Toplevel()
    ventana.title("Estadísticas de arriendos")
    ventana.geometry("1000x700")

    titulo = tk.Label(
        ventana,
        text="ESTADÍSTICAS DE ARRIENDOS",
        font=("Arial", 16, "bold")
    )
    titulo.pack(pady=15)

    arriendos = listar_historial_arriendos()

    conteo_categorias = Counter()

    for arriendo in arriendos:
        categoria = arriendo.equipo.categoria.nombre
        conteo_categorias[categoria] += 1

    conteo_equipos = Counter()

    for arriendo in arriendos:
        nombre_equipo = arriendo.equipo.nombre
        conteo_equipos[nombre_equipo] += 1

    figura = Figure(figsize=(9, 7), dpi=100)

    grafico = figura.add_subplot(211)

    if conteo_categorias:
        categorias = list(conteo_categorias.keys())
        cantidades = list(conteo_categorias.values())

        grafico.bar(categorias, cantidades)
        grafico.set_title("Arriendos por categoría")
        grafico.set_xlabel("Categoría")
        grafico.set_ylabel("Cantidad de arriendos")

    else:
        grafico.text(
            0.5,
            0.5,
            "No hay arriendos registrados",
            ha="center",
            va="center"
        )

    grafico2 = figura.add_subplot(212)

    if conteo_equipos:
        equipos = list(conteo_equipos.keys())
        cantidades_equipos = list(conteo_equipos.values())

        grafico2.bar(equipos, cantidades_equipos)
        grafico2.set_title("Equipos más arrendados")
        grafico2.set_xlabel("Equipo")
        grafico2.set_ylabel("Cantidad de arriendos")
        grafico2.tick_params(axis="x", rotation=45)

    else:
        grafico2.text(
            0.5,
            0.5,
            "No hay arriendos registrados",
            ha="center",
            va="center"
        )

    figura.tight_layout()

    canvas = FigureCanvasTkAgg(figura, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    abrir_graficos()
    root.mainloop()

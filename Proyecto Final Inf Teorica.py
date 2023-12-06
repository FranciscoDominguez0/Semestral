import networkx as nx  # networkx se utiliza para trabajar con grafos
import matplotlib.pyplot as plt  # matplotlib se usa para visualizar gráficos
import tkinter as tk  # tkinter es una biblioteca para crear interfaces gráficas de usuario
from tkinter import ttk  # ttk es un módulo adicional de tkinter que proporciona widgets temáticos mejorados

# Definición de la clase para el grafo de ciudades
class GrafoCiudades:
    def __init__(self):
        # Constructor: Inicializa un grafo vacío utilizando networkx
        self.grafo = nx.Graph()

    def agregar_ciudad(self, ciudad):
        # Añade un nodo (ciudad) al grafo
        self.grafo.add_node(ciudad)

    def agregar_conexion(self, ciudad_origen, ciudad_destino, distancia):
        # Añade una conexión entre dos ciudades con una distancia específica al grafo
        self.grafo.add_edge(ciudad_origen, ciudad_destino, weight=distancia)

    def visualizar_grafo(self, nombre_archivo="Graph.png", mensaje="", ruta_resaltada=None):
        # Visualiza el grafo utilizando matplotlib y guarda la representación en un archivo PNG
        pos = nx.spring_layout(self.grafo)
        nx.draw(self.grafo, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray', width=2, font_color='black')
        
        if ruta_resaltada:
            # Si se proporciona una ruta resaltada, la resalta en rojo
            edges = list(zip(ruta_resaltada, ruta_resaltada[1:]))
            nx.draw(self.grafo, pos, edgelist=edges, edge_color='red', width=3)

        # Etiquetas de las conexiones con las distancias redondeadas a 2 decimales
        labels = nx.get_edge_attributes(self.grafo, 'weight')
        rounded_labels = {k: round(v, 2) for k, v in labels.items()}
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=rounded_labels)
        
        # Anotación del mensaje en el gráfico
        plt.annotate(mensaje, xy=(0.5, 0.95), xycoords='axes fraction', ha='center', va='center', bbox=dict(boxstyle="round,pad=0.1", edgecolor="black", facecolor="white"))
        
        # Guarda el gráfico como un archivo PNG y lo muestra
        plt.savefig(nombre_archivo, format="PNG")
        plt.show()

    def encontrar_ruta_mas_corta(self, inicio, destino):
        try:
            # Utiliza el algoritmo de Dijkstra para encontrar la ruta más corta y su distancia
            distancia_corta = nx.single_source_dijkstra_path_length(self.grafo, inicio, weight='weight')
            ruta = nx.shortest_path(self.grafo, inicio, destino, weight='weight')
            return distancia_corta[destino], ruta
        except nx.NetworkXNoPath:
            # Maneja la excepción cuando no hay ruta entre las ciudades
            return float('inf'), []

# Definición de la clase para la interfaz de usuario
class InterfazUsuario:
    def __init__(self, grafo_ciudades):
        # Constructor: Inicializa la interfaz gráfica de usuario (GUI) con tkinter
        self.grafo_ciudades = grafo_ciudades
        self.ventana = tk.Tk()
        self.ventana.title("Ruta más corta entre ciudades")

        # Configuración y creación de widgets para la selección de ciudades de inicio
        self.label_inicio = ttk.Label(self.ventana, text="Ciudad de inicio:")  
        # Crea una etiqueta (label) con el texto "Ciudad de inicio"
        self.label_inicio.grid(row=0, column=0, padx=10, pady=10)  
        # Coloca la etiqueta en la fila 0, columna 0 de la interfaz, con márgenes de 10 píxeles en x y 10 píxeles en y
        self.ciudades = grafo_ciudades.grafo.nodes()  
        # Obtiene la lista de nodos (ciudades) del grafo
        self.combo_inicio = ttk.Combobox(self.ventana, values=list(self.ciudades))  
        # Crea un cuadro combinado (combobox) con las ciudades como opciones
        self.combo_inicio.grid(row=0, column=1, padx=10, pady=10)  
        # Coloca el cuadro combinado en la fila 0, columna 1 de la interfaz, con márgenes de 10 píxeles en x y 10 píxeles en y

        # Configuración y creación de widgets para la selección de ciudades de destino
        self.label_destino = ttk.Label(self.ventana, text="Ciudad de destino:")  
        # Crea una etiqueta (label) con el texto "Ciudad de destino"
        self.label_destino.grid(row=1, column=0, padx=10, pady=10)  
        # Coloca la etiqueta en la fila 1, columna 0 de la interfaz, con márgenes de 10 píxeles en x y 10 píxeles en y
        self.combo_destino = ttk.Combobox(self.ventana, values=list(self.ciudades))  
        # Crea un cuadro combinado (combobox) con las ciudades como opciones
        self.combo_destino.grid(row=1, column=1, padx=10, pady=10)  
        # Coloca el cuadro combinado en la fila 1, columna 1 de la interfaz, con márgenes de 10 píxeles en x y 10 píxeles en y

        # Botón para calcular la ruta más corta
        self.boton_calcular = ttk.Button(self.ventana, text="Calcular Ruta", command=self.calcular_ruta)
        self.boton_calcular.grid(row=2, column=0, columnspan=2, pady=10)  
        # Coloca el botón en la fila 2, columnas 0 y 1 de la interfaz, abarcando ambas columnas, con un margen de 10 píxeles en y

        # Etiqueta para mostrar el resultado
        self.label_resultado = ttk.Label(self.ventana, text="")
        self.label_resultado.grid(row=3, column=0, columnspan=2, pady=10)  
        # Coloca la etiqueta en la fila 3, columnas 0 y 1 de la interfaz, abarcando ambas columnas, con un margen de 10 píxeles en y

    def calcular_ruta(self):
        # Obtiene las ciudades seleccionadas por el usuario
        inicio = self.combo_inicio.get()
        destino = self.combo_destino.get()

        # Llama al método para encontrar la ruta más corta
        distancia_corta, ruta = self.grafo_ciudades.encontrar_ruta_mas_corta(inicio, destino)

        if distancia_corta != float('inf'):
            # Mensaje con la distancia más corta y la ruta sugerida
            mensaje = f"La distancia más corta entre {inicio} y {destino} es {round(distancia_corta, 2)} km.\nRuta sugerida: {ruta}"
        else:
            # Mensaje cuando no hay ruta válida
            mensaje = f"No hay ruta válida entre {inicio} y {destino}."

        # Actualiza la etiqueta de resultado y visualiza el grafo con la ruta resaltada
        self.label_resultado.config(text=mensaje)
        self.grafo_ciudades.visualizar_grafo(mensaje=mensaje, ruta_resaltada=ruta)

    def ejecutar(self):
        # Inicia el bucle principal de la interfaz gráfica
        self.ventana.mainloop()

# Función principal
def main():
    # Creación de una instancia de GrafoCiudades
    grafo_ciudades = GrafoCiudades()

    # Agregando ciudades y conexiones al grafo
    ciudades = ["Penonomé", "Antón", "Aguadulce", "Natá", "La Pintada", "Olá", "Los Uveros", "Universidad", "El Ingenio", "Rio Grande", "La Soledad"]
    for ciudad in ciudades:
        grafo_ciudades.agregar_ciudad(ciudad)

    grafo_ciudades.agregar_conexion("Penonomé", "Los Uveros", 7.5)
    grafo_ciudades.agregar_conexion("Los Uveros", "La Pintada", 11.3)

    grafo_ciudades.agregar_conexion("Penonomé", "Universidad", 4.5)
    grafo_ciudades.agregar_conexion("Universidad", "Antón", 13)
    
    grafo_ciudades.agregar_conexion("Penonomé", "Rio Grande", 27.3)
    grafo_ciudades.agregar_conexion("Rio Grande", "Natá", 35.0)
    
    grafo_ciudades.agregar_conexion("Olá", "La Soledad", 4.2)
    grafo_ciudades.agregar_conexion("La Soledad", "Aguadulce", 32)
    
    grafo_ciudades.agregar_conexion("Aguadulce", "El Ingenio", 9.3)
    grafo_ciudades.agregar_conexion("El Ingenio", "Natá", 6.6)

    # Creación de una instancia de InterfazUsuario y ejecución
    interfaz = InterfazUsuario(grafo_ciudades)
    interfaz.ejecutar()

# Verifica si el script está siendo ejecutado directamente
if __name__ == "__main__":
    main()

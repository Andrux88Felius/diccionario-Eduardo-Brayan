import matplotlib.pyplot as plt
import networkx as nx

class Nodo:
    def __init__(self, palabra, significado):
        self.palabra = palabra.lower()
        self.significado = significado
        self.izquierda = None
        self.derecha = None

class DiccionarioArbol:
    def __init__(self):
        self.raiz = None
    
    # =======================
    #       INSERTAR
    # =======================
    def insertar(self, palabra, significado):
        palabra = palabra.lower()
        if self.raiz is None:
            self.raiz = Nodo(palabra, significado)
        else:
            self._insertar_recursivo(self.raiz, palabra, significado)
    
    def _insertar_recursivo(self, nodo_actual, palabra, significado):
        if palabra < nodo_actual.palabra:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(palabra, significado)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, palabra, significado)
        
        elif palabra > nodo_actual.palabra:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(palabra, significado)
            else:
                self._insertar_recursivo(nodo_actual.derecha, palabra, significado)
        
        else:
            nodo_actual.significado = significado 
    
    # =======================
    #       BUSCAR
    # =======================
    def buscar(self, palabra):
        palabra = palabra.lower()
        return self._buscar_recursivo(self.raiz, palabra)
    
    def _buscar_recursivo(self, nodo_actual, palabra):
        if nodo_actual is None:
            return None
        
        if palabra == nodo_actual.palabra:
            return nodo_actual.significado
        
        elif palabra < nodo_actual.palabra:
            return self._buscar_recursivo(nodo_actual.izquierda, palabra)
        else:
            return self._buscar_recursivo(nodo_actual.derecha, palabra)

    # =======================
    #       ELIMINAR
    # =======================
    def eliminar(self, palabra):
        palabra = palabra.lower()
        self.raiz = self._eliminar_recursivo(self.raiz, palabra)
    
    def _eliminar_recursivo(self, nodo_actual, palabra):
        if nodo_actual is None:
            return None
        
        if palabra < nodo_actual.palabra:
            nodo_actual.izquierda = self._eliminar_recursivo(nodo_actual.izquierda, palabra)
        
        elif palabra > nodo_actual.palabra:
            nodo_actual.derecha = self._eliminar_recursivo(nodo_actual.derecha, palabra)
        
        else:
            if nodo_actual.izquierda is None and nodo_actual.derecha is None:
                return None
            
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            if nodo_actual.derecha is None:
                return nodo_actual.izquierda
            
            sucesor = self._encontrar_minimo(nodo_actual.derecha)
            nodo_actual.palabra = sucesor.palabra
            nodo_actual.significado = sucesor.significado
            nodo_actual.derecha = self._eliminar_recursivo(nodo_actual.derecha, sucesor.palabra)
        
        return nodo_actual
    
    def _encontrar_minimo(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo

    # =======================
    #       INORDEN
    # =======================
    def mostrar_todo(self):
        palabras = []
        self._inorden_recursivo(self.raiz, palabras)
        return palabras
    
    def _inorden_recursivo(self, nodo_actual, lista):
        if nodo_actual is not None:
            self._inorden_recursivo(nodo_actual.izquierda, lista)
            lista.append((nodo_actual.palabra, nodo_actual.significado))
            self._inorden_recursivo(nodo_actual.derecha, lista)


# ============================================================
#                GRAFICADO CENTRADO Y FUNCIONAL CODESPACES
# ============================================================

def graficar_arbol(diccionario):
    if diccionario.raiz is None:
        print("Árbol vacío.")
        return

    G = nx.DiGraph()
    posiciones = {}

    def recorrer(nodo, x=0, y=0, dx=3):
        if nodo is None:
            return
        
        posiciones[nodo.palabra] = (x, y)
        G.add_node(nodo.palabra, significado=nodo.significado)

        if nodo.izquierda:
            G.add_edge(nodo.palabra, nodo.izquierda.palabra)
            recorrer(nodo.izquierda, x - dx, y - 2, dx * 0.6)
        
        if nodo.derecha:
            G.add_edge(nodo.palabra, nodo.derecha.palabra)
            recorrer(nodo.derecha, x + dx, y - 2, dx * 0.6)

    recorrer(diccionario.raiz)

    # Guardamos la figura automáticamente
    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        posiciones,
        with_labels=False,
        node_color="#B3D9FF",
        node_size=2000,
        font_size=9,
        font_weight="bold",
        arrows=False,
        edge_color="gray"
    )

    labels = {nodo: f"{nodo}\n{datos['significado']}" for nodo, datos in G.nodes(data=True)}
    nx.draw_networkx_labels(
        G,
        posiciones,
        labels=labels,
        font_size=6,
        verticalalignment='center'
    )

    plt.title("Árbol Binario - Diccionario", fontsize=14)
    plt.axis("off")

    archivo = "arbol_diccionario.png"
    plt.savefig(archivo, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Árbol guardado como '{archivo}' en el directorio actual.")


# ============================================================
#                 PROGRAMA PRINCIPAL
# ============================================================

def main():
    diccionario = DiccionarioArbol()

    palabras_ejemplo = [
        ("algoritmo", "Conjunto ordenado de operaciones para resolver un problema"),
        ("abeja", "Insecto polinizador"),
        ("binario", "Sistema de numeración de base 2"),
        ("compilador", "Programa que traduce código fuente a código máquina"),
        ("datos", "Información representada de forma digital"),
        ("estructura", "Organización y disposición de elementos"),
        ("función", "Bloque de código que realiza una tarea específica"),
        ("grafo", "Conjunto de nodos conectados por aristas"),
        ("servidor", "Equipo que proporciona servicios a otros equipos"),
        ("cliente", "Programa que solicita servicios a un servidor"),
        ("internet", "Red global que conecta millones de computadoras"),
        ("navegador", "Programa que permite acceder a páginas web"),
        ("archivo", "Conjunto de datos almacenados bajo un nombre único")
    ]

    for palabra, significado in palabras_ejemplo:
        diccionario.insertar(palabra, significado)

    while True:
        print("\n=== DICCIONARIO CON ÁRBOL BINARIO ===")
        print("1. Buscar palabra")
        print("2. Agregar palabra")
        print("3. Eliminar palabra")
        print("4. Mostrar todas las palabras")
        print("5. Graficar árbol")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            palabra = input("Palabra a buscar: ")
            significado = diccionario.buscar(palabra)
            if significado:
                print(f"> {palabra}: {significado}")
            else:
                print(f"> '{palabra}' no está en el diccionario")

        elif opcion == "2":
            p = input("Nueva palabra: ")
            s = input("Significado: ")
            diccionario.insertar(p, s)
            print(f"> '{p}' agregada!")

        elif opcion == "3":
            p = input("Palabra a eliminar: ")
            if diccionario.buscar(p):
                diccionario.eliminar(p)
                print(f"> '{p}' eliminada")
            else:
                print(f"> '{p}' no existe")

        elif opcion == "4":
            print("\n--- Todas las palabras ---")
            for palabra, significado in diccionario.mostrar_todo():
                print(f"• {palabra}: {significado}")

        elif opcion == "5":
            graficar_arbol(diccionario)

        elif opcion == "6":
            print("¡Hasta luego!")
            break

        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()

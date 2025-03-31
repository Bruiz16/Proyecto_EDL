from collections import deque

def generar_lenguaje(VT, VN, S, P, max_longitud):
    """
    Genera todas las cadenas del lenguaje L(G) hasta una longitud máxima especificada.
    
    Parámetros:
    VT (set): Conjunto de símbolos terminales
    VN (set): Conjunto de símbolos no terminales
    S (str): Símbolo inicial de la gramática
    P (dict): Producciones en formato {NoTerminal: [producciones]}
    max_longitud (int): Longitud máxima de las cadenas generadas
    
    Retorna:
    list: Lista ordenada de cadenas del lenguaje
    """
    # Configurar estructura para BFS y control de estados
    cola = deque()                  # Cola para procesar cadenas
    cola.append(S)                  # Iniciar con el símbolo inicial
    procesados = set()              # Cadenas ya procesadas
    lenguaje = set()                # Conjunto para cadenas válidas

    while cola:
        actual = cola.popleft()     # Obtener primer elemento de la cola
        
        # Evitar reprocesar cadenas
        if actual in procesados:
            continue
        procesados.add(actual)
        
        # Verificar si es una cadena terminal
        es_terminal = True
        contador_terminales = 0
        for caracter in actual:
            if caracter in VN:
                es_terminal = False
                break
            elif caracter in VT:
                contador_terminales += 1
        
        # Si es terminal y cumple con la longitud máxima
        if es_terminal:
            if len(actual) <= max_longitud:
                lenguaje.add(actual)
            continue  # Pasar al siguiente elemento de la cola
        
        # Encontrar el primer no terminal por la izquierda
        primer_nt = None
        posicion = -1
        for i, caracter in enumerate(actual):
            if caracter in VN:
                primer_nt = caracter
                posicion = i
                break
        
        # Si no se encontró no terminal (caso inesperado)
        if primer_nt is None:
            continue
        
        # Generar nuevas cadenas aplicando producciones
        for produccion in P.get(primer_nt, []):
            nueva_cadena = actual[:posicion] + produccion + actual[posicion+1:]
            
            # Calcular terminales en la nueva cadena
            nuevos_terminales = sum(1 for c in nueva_cadena if c in VT)
            
            # Filtrar cadenas que excedan la longitud máxima
            if nuevos_terminales > max_longitud:
                continue
            
            # Agregar a la cola si no ha sido procesada
            if nueva_cadena not in procesados:
                cola.append(nueva_cadena)
    
    # Ordenar resultados por longitud y orden lexicográfico
    return sorted(lenguaje, key=lambda x: (len(x), x))

# Ejemplo de uso
if __name__ == "__main__":
    # Definir gramática de ejemplo
    VT = {'0', '1'}
    VN = {'S', 'X', 'Y'}
    S = 'S'
    P = {
        'S': ['XY'],
        'X': ['1', '1X'],
        'Y': ['0']
    }
    max_longitud = 10

    # Generar y mostrar lenguaje
    L = generar_lenguaje(VT, VN, S, P, max_longitud)

    print("Lenguaje L(G) generado:")
    
    print(f"L = {{ {', '.join(L)} }}")
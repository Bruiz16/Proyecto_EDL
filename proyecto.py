from collections import deque
import argparse
import sys
import re

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

def validar_produccion(prod, vt, vn):
    """Valida que una producción solo contenga símbolos válidos"""
    for char in prod:
        if char not in vt and char not in vn:
            return False
    return True

def mostrar_gramatica(vt, vn, s, p, max_longitud):
    """Muestra la gramática en formato formal"""
    print("\nGramática definida:")
    print(f"VT = {{{', '.join(sorted(vt))}}}")
    print(f"VN = {{{', '.join(sorted(vn))}}}")
    print(f"S = {s}")
    print("P = {")
    for nt, prods in sorted(p.items()):
        for prod in prods:
            if prod == "":
                print(f"    {nt} → ε")
            else:
                print(f"    {nt} → {prod}")
    print("}")
    print(f"Longitud máxima: {max_longitud}")
    print()

def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description='Generador de lenguajes formales a partir de gramáticas.')
    parser.add_argument('-i', '--interactivo', action='store_true', help='Modo interactivo para ingresar la gramática')
    parser.add_argument('-t', '--terminales', type=str, help='Símbolos terminales separados por coma (ej: "a,b,c")')
    parser.add_argument('-n', '--no-terminales', type=str, help='Símbolos no terminales separados por coma (ej: "S,A,B")')
    parser.add_argument('-s', '--inicial', type=str, help='Símbolo inicial de la gramática')
    parser.add_argument('-p', '--producciones', type=str, nargs='+', 
                        help='Producciones en formato "X->Y1,Y2,...". Para epsilon usar ""')
    parser.add_argument('-l', '--longitud', type=int, default=10, help='Longitud máxima de las cadenas (default: 10)')
    
    args = parser.parse_args()
    
    # Decidir modo de ejecución
    if args.interactivo or (not args.terminales and not args.no_terminales and not args.inicial and not args.producciones):
        # Modo interactivo
        print("=== Generador de Lenguajes Formales ===")
        print("Ingrese los componentes de la gramática G = (VT, VN, S, P)")
        
        # Solicitar símbolos terminales
        while True:
            try:
                vt_input = input("Símbolos terminales (separados por coma, ej: a,b,c): ").strip()
                vt = set(vt_input.split(',')) if vt_input else set()
                
                # Validar que no estén vacíos
                if not vt:
                    print("Error: Debe ingresar al menos un símbolo terminal.")
                    continue
                
                # Validar que no haya espacios o símbolos vacíos
                if any(not t.strip() for t in vt) or '' in vt:
                    print("Error: Los símbolos no pueden estar vacíos o contener espacios.")
                    continue
                    
                break
            except Exception as e:
                print(f"Error: {e}")
        
        # Solicitar símbolos no terminales
        while True:
            try:
                vn_input = input("Símbolos no terminales (separados por coma, ej: S,A,B): ").strip()
                vn = set(vn_input.split(',')) if vn_input else set()
                
                # Validar que no estén vacíos
                if not vn:
                    print("Error: Debe ingresar al menos un símbolo no terminal.")
                    continue
                
                # Validar que no haya espacios o símbolos vacíos
                if any(not n.strip() for n in vn) or '' in vn:
                    print("Error: Los símbolos no pueden estar vacíos o contener espacios.")
                    continue
                    
                # Validar que VT y VN sean disjuntos
                if vt.intersection(vn):
                    print(f"Error: Los conjuntos VT y VN deben ser disjuntos. Símbolos repetidos: {vt.intersection(vn)}")
                    continue
                    
                break
            except Exception as e:
                print(f"Error: {e}")
        
        # Solicitar símbolo inicial
        while True:
            try:
                s = input("Símbolo inicial (debe ser un no terminal): ").strip()
                
                # Validar que sea un no terminal
                if s not in vn:
                    print(f"Error: El símbolo inicial debe ser un no terminal (uno de {vn}).")
                    continue
                    
                break
            except Exception as e:
                print(f"Error: {e}")
        
        # Solicitar producciones
        p = {nt: [] for nt in vn}
        print("\nIngrese las producciones (una por línea)")
        print("Formato: X->Y1,Y2,... (para epsilon use X->)")
        print("Ingrese una línea vacía para terminar.")
        
        while True:
            prod_input = input("> ").strip()
            if not prod_input:
                break
                
            # Validar formato
            match = re.match(r'^([^->\s]+)\s*->\s*(.*)$', prod_input)
            if not match:
                print("Error: Formato inválido. Use 'X->Y1,Y2,...'")
                continue
                
            nt, prods_str = match.groups()
            
            # Validar que el no terminal exista
            if nt not in vn:
                print(f"Error: '{nt}' no es un símbolo no terminal válido.")
                continue
                
            # Procesar producciones
            if not prods_str:
                # Caso epsilon
                p[nt].append("")
            else:
                for prod in prods_str.split(','):
                    prod = prod.strip()
                    if not validar_produccion(prod, vt, vn):
                        print(f"Error: La producción '{prod}' contiene símbolos que no están en VT o VN.")
                        continue
                    p[nt].append(prod)
        
        # Solicitar longitud máxima
        while True:
            try:
                max_longitud = int(input("Longitud máxima de las cadenas: ").strip())
                if max_longitud <= 0:
                    print("Error: La longitud debe ser un número positivo.")
                    continue
                break
            except ValueError:
                print("Error: Ingrese un número entero válido.")
                
    else:
        # Modo argumentos de línea de comandos
        try:
            # Procesar símbolos terminales
            vt = set(args.terminales.split(',')) if args.terminales else set()
            
            # Procesar símbolos no terminales
            vn = set(args.no_terminales.split(',')) if args.no_terminales else set()
            
            # Validar que VT y VN sean disjuntos
            if vt.intersection(vn):
                print(f"Error: Los conjuntos VT y VN deben ser disjuntos. Símbolos repetidos: {vt.intersection(vn)}")
                sys.exit(1)
                
            # Procesar símbolo inicial
            s = args.inicial
            if s not in vn:
                print(f"Error: El símbolo inicial debe ser un no terminal (uno de {vn}).")
                sys.exit(1)
                
            # Procesar producciones
            p = {nt: [] for nt in vn}
            if args.producciones:
                for prod_str in args.producciones:
                    match = re.match(r'^([^->\s]+)\s*->\s*(.*)$', prod_str)
                    if not match:
                        print(f"Error: Formato inválido en producción '{prod_str}'. Use 'X->Y1,Y2,...'")
                        sys.exit(1)
                        
                    nt, prods_str = match.groups()
                    
                    # Validar que el no terminal exista
                    if nt not in vn:
                        print(f"Error: '{nt}' no es un símbolo no terminal válido.")
                        sys.exit(1)
                        
                    # Procesar producciones
                    if not prods_str:
                        # Caso epsilon
                        p[nt].append("")
                    else:
                        for prod in prods_str.split(','):
                            prod = prod.strip()
                            if not validar_produccion(prod, vt, vn):
                                print(f"Error: La producción '{prod}' contiene símbolos que no están en VT o VN.")
                                sys.exit(1)
                            p[nt].append(prod)
            
            # Procesar longitud máxima
            max_longitud = args.longitud
            if max_longitud <= 0:
                print("Error: La longitud debe ser un número positivo.")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error procesando argumentos: {e}")
            parser.print_help()
            sys.exit(1)
    
    # Mostrar la gramática definida
    mostrar_gramatica(vt, vn, s, p, max_longitud)
    
    # Generar y mostrar lenguaje
    lenguaje = generar_lenguaje(vt, vn, s, p, max_longitud)
    
    if not lenguaje:
        print("El lenguaje generado está vacío hasta la longitud especificada.")
    else:
        print(f"Lenguaje L(G) generado (hasta longitud {max_longitud}):")
        print(f"L = {{ {', '.join(lenguaje)} }}")
        print(f"Total de cadenas: {len(lenguaje)}")

if __name__ == "__main__":
    main()
# crear_tablero : None -> [[char]]
# Crea un tablero de 8x8 y coloca las 4 fichas iniciales de la partida con sus correspondientes colores;
def crear_tablero():
    lista = [[" " for i in range(8)] for i in range(8)]
    lista[3][3] = "B"
    lista[4][3] = "N"
    lista[4][4] = "B"
    lista[3][4] = "N"
    return lista

# crear_contorno : None -> Set((Int,Int))
# Crea un set donde guarda el contorno de las casillas vacías que son adyacentes a una casilla con una ficha de color
def crear_contorno():
    contorno = set()
    #lista = [C3, D3, E3, F3, C4, F4, C5, F5, C6, D6, E6, F6]
    lista = [(2,2),(3,2),(4,2),(5,2),(2,3),(5,3),(2,4),(5,4),(2,5),(3,5),(4,5),(5,5)]
    for i in lista:
        contorno.add(i)

    return contorno
# sintaxis_correcta : String -> Boolean
# Recibe la jugada y si no esta fuera del tablero devuelve True. En caso de que la jugada exceda
# los limites del tablero, o su sintaxis sea incorrecta, retorna False.
# ej: "B9" -> False
def sintaxis_correcta(jugada):
    try:
        return ((ord(jugada[0]) in range(97,105) or ord(jugada[0]) in range(65,73)) and int(jugada[1:])-1 in range(0,8))
    except: 
        return False


# buscar_ficha : (Int, Int) (Int, Int) [[Char]] Chart -> Boolean
# Dada una ficha y una dirección, busca si hay una ficha del jugador contrario en dicha direccion
def buscar_ficha(ficha, direccion, tablero, jugador_contrario):
    
    halloficha=False
    (a,b) = direccion
    (x,y) = (ficha[0] + a,ficha[1] + b)
    veces_desplazado = 1
    
    while not(halloficha) and x in range(8) and y in range(8):
        if tablero[x][y] == jugador_contrario:
            x += a
            y += b
            veces_desplazado +=1
        elif tablero[x][y] == " ":
            veces_desplazado = 0 
            halloficha = True
        else:
            halloficha = True

    return veces_desplazado if x in range(8) and y in range(8) else 0


# jugada_valida : (Int,Int) [[Char]] Char Boolean -> Boolean
# Dada una posicion valida, un tablero, el color del jugador actual, y un modo,
# determina si esa posicion puede reducir la cantidad de fichas del equipo contrario y altera el tablero si el modo es True.
# Si la jugada es invalida retorna False y si la jugada es valida retorna True.
def jugada_valida(jugada, tablero, jugador_actual, modo):
    (y, x) = jugada 
    pos_valida = False
    vectores = ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)) #todas las posibles direcciones adyacentes
    cambiar_ficha = {'B':'N','N':'B'}
    jugador_contrario = cambiar_ficha[jugador_actual]

    if tablero[x][y] == " ":
        for (a,b) in vectores:
            if  x+a in range(8) and y+b in range(8) and tablero[x+a][y+b] == cambiar_ficha[jugador_actual] : # esto es rapido, lo juro
                veces_desplazado = buscar_ficha((x+a, y+b), (a,b), tablero, jugador_contrario)
                if(veces_desplazado):
                    pos_valida = True
                    if(modo): voltear((x,y),(a,b),veces_desplazado, tablero)
    
    if(pos_valida and modo):
        tablero[x][y] = cambiar_ficha[jugador_contrario]

    return pos_valida

#voltear : (Int,Int) (Int,Int) Int [[Char]] -> None
#Dada una posicion, una direccion, un numero n y un tablero,
#Cambia el color de n fichas apartir de la posicion desplazandose por la direccion
def voltear(posicion, direccion, veces_desplazado, tablero):
    (x,y) = posicion
    (a,b) = direccion
    cambiar_ficha = {'B':'N','N':'B'}
    for i in range(veces_desplazado):
        x += a
        y += b
        tablero[x][y] = cambiar_ficha[tablero[x][y]]

#agregar_a_contorno : (Int, Int, Char) Set((Int,Int)) [[Char]] -> None
# Toma una jugada, un contorno y un tablero y agrega al contorno todas los espacios adyacentes a la jugada, tal que
# el espacio adyacente no esta ocupado
def agregar_a_contorno(coordenadas, contorno, tablero):
    (x,y) = coordenadas
    vectores = ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))

    for (a,b) in vectores:
        if x+a in range(8) and y+b in range(8) and tablero[y+b][x+a] == " ":
            contorno.add((x+a , y+b))

#hay_ganador: [[Char]] -> Char
#Analiza si no hay más posibles jugadas válidas para ninguno de los equipos.
#En caso de que ninguno de los dos equipos tenga mas movimientos, retorna el equipo con mas fichas
#de su color en el tablero.
#En caso de que no haya un ganador retorna "".
def hay_ganador(tablero, contorno):
    fichasB=0
    fichasN=0
    existeganador=True
    for k in contorno:
        if jugada_valida(k, tablero, "B" , False) or jugada_valida(k, tablero, "N", False):
            existeganador=False
    if (existeganador==False):
        return ""
    for i in range(8):
        for j in range (8):
            if (tablero[i][j]=="N"):
                fichasN=fichasN+1
            elif (tablero[i][j]=="B"):
                fichasB=fichasB+1
    if (fichasB>fichasN):
        return "B"
    else:
        return "N"

#imprimir: [[Char]] -> None
#Dado un tablero, imprime el contenido en un formato amigable para su lectura
def imprimir(tablero):
    columnas = ["A","B","C","D","E","F","G","H"]
    i = 0 # perdonenme la falta de respeto pero esta variable no se me ocurre como llamarla
    cantidad_columnas = len(columnas)
    while i < cantidad_columnas:
        print(f"\t| {columnas[i]}", end = "") 
        i +=1
    print()
    print("\t------------------------------------------------------------")
    for fila in range(1,9):
        print(f"{fila} ", end = "" )
        for casillero in tablero[fila-1]:
            print(f"\t|",casillero, end = "")
        print()
    
#intentar_saltear: [[Char]] Char Set((Int,Int)) -> Boolean
#la función toma un tablero, el jugador actual y el contorno de las fichas jugadas
#si el jugador actual no puede jugar y el otro jugador si puede, entonces se saltó el turno correctamente, retorna True
#si el jugador actual puede jugar entonces no se puede saltear, retorna False
#si el jugador actual no puede jugar y el otro jugador tampoco entonces debió haber terminado el juego, retorna False
def intentar_saltear(tablero, jugador_actual, contorno):
    
    cambiar_jugador = {'B':'N','N':'B'}
    puede_jugar_actual = False
    puede_jugar_contrario = False

    for coordenadas in contorno:
        if(jugada_valida(coordenadas, tablero, jugador_actual, False)):
            puede_jugar_actual = True
        if(jugada_valida(coordenadas, tablero, cambiar_jugador[jugador_actual], False)):
            puede_jugar_contrario = True
    
    return not(puede_jugar_actual) and puede_jugar_contrario

#que_tipo_de_error String String -> String
#Retorna un mensaje persoalizado de error, dependiendo de la jugada final que se intentó hacer.
def que_tipo_de_error(jugada_final, nombre_j_final, ultima_ficha):
    error_handler = {
        
        "": "No se ingresó ninguna jugada",
        
        " " : "No se podía saltear el turno",
        
        "s" : (f"{nombre_j_final} trató de poner una ficha que no existe, la ficha {ultima_ficha} no existe")
    }
    error_de_posicion = f"El jugador {nombre_j_final}, trato de colocar una ficha en {jugada_final} y esa es una posicion invalida"
    return(error_handler.get(jugada_final, error_de_posicion))

#jugar : None -> None
# Función en la que se llaman al resto de funciones y se lee el archivo.
def jugar():
    ingreso = input("Ingrese el nombre del archivo que desea verificar:")
    partida = open(f"{ingreso}.txt", "r")

    
    (jugador1, color_j1) = partida.readline().strip('\n').split(",")
    (jugador2, color_j2) = partida.readline().strip('\n').split(",")
    jugador_actual = partida.readline().strip('\n')
    cambiar_jugador = {'B':'N','N':'B'}
    nombres = {color_j1:jugador1,color_j2:jugador2}

    tablero = crear_tablero()
    contorno = crear_contorno()
    hubo_error = False
    jugada = partida.readline()
    jugada_final = jugada
    ficha_con_mala_sintaxis = ""

    while  not(hubo_error) and jugada != "":
        jugada = jugada.strip("\n")
        if jugada == "":
            hubo_error = (not intentar_saltear(tablero,jugador_actual,contorno))
            jugada_final = " "
        elif sintaxis_correcta(jugada):
            coordenadas = (ord(jugada[0].upper())-65,int(jugada[1:])-1) #convierte la jugada en una coordenada del tablero
            hubo_error = not(jugada_valida(coordenadas, tablero, jugador_actual, True))
            jugada_final = jugada
            if not(hubo_error):
                contorno.remove(coordenadas) # si la ficha era una jugada valida, entonces pertenecía al contorno
                agregar_a_contorno(coordenadas, contorno, tablero)
        else:
            hubo_error = True
            jugada_final = "s" # "s" para representar una sintaxis incorrecta
            ficha_con_mala_sintaxis = jugada
            
        jugador_actual = cambiar_jugador[jugador_actual]
        jugada = partida.readline()
    
    imprimir(tablero)
    if hubo_error:
        jugador_actual = cambiar_jugador[jugador_actual]
        output = que_tipo_de_error(jugada_final, nombres[jugador_actual],ficha_con_mala_sintaxis)
        print(output)
    else:
        posibilidad_ganador=hay_ganador(tablero,contorno)
        if(posibilidad_ganador!=""):
            print("El ganador es", nombres[posibilidad_ganador])
        else:
            print("Ahora le toca a:", nombres[jugador_actual])
    
    partida.close()

#generador_tableros_prueba: ((Int)) Char -> [[Chart]]
#Genera tableros de prueba a usarse en los pytest con una tupla de casillas que van a estar y el color que inicia
#la partida
def generador_tableros_prueba(casillas, color):
    tablero=crear_tablero()
    cambiar_jugador = {'B':'N','N':'B'}
    for (x,y) in casillas:
        tablero[x][y]=color
        color=cambiar_jugador[color]
    return tablero

           

#Test de la función sintaxis_correcta()
def test_sintaxis_correcta():
    sintaxis_correcta("F90") == False
    sintaxis_correcta("G6") == True
    sintaxis_correcta("7F") == False
    sintaxis_correcta("f5") == False

#Test de la función buscar_ficha()
def test_buscar_ficha():
    prueba1=((2,3),(2,2),(2,1),(5,3),(5,4),(5,5),(6,6),(5,6),(6,3),(1,1),(0,0),(7,2),(5,7),(5,2),(5,1),(4,1),(3,1),(2,5),(4,5),(6,5),(1,7))
    tablero=generador_tableros_prueba(prueba1,"N")
    buscar_ficha((6,5),(-1,1),tablero,"N") == True
    buscar_ficha((5,5),(0,-1),tablero,"B") == True
    buscar_ficha((1,1),(-1,-1),tablero,"N") == False

#Test de jugada_valida()
def test_jugada_valida():
    prueba1=((2,3),(2,2),(2,1),(5,3),(5,4),(5,5),(6,6),(5,6),(6,3),(1,1),(0,0),(7,2),(5,7),(5,2),(5,1),(4,1),(3,1),(2,5),(4,5),(6,5),(1,7))
    tablero=generador_tableros_prueba(prueba1,"N")
    jugada_valida((5,0),tablero,"B",False) == True
    jugada_valida((7,7),tablero,"B",True) == False
    jugada_valida((4,6),tablero,"B",True) == True

 #Test de hay_ganador()
def test_hay_ganador():
    prueba2=((3,4),(3,3),(3,2),(2,2),(4,3),(3,5))
    tablero1 = [["N" for i in range(8)] for i in range(8)]
    tablero3 = [["B" for i in range(8)] for i in range(8)]
    tablero3[1][1] = "N"
    tablero2 = crear_tablero()
    contorno2 = crear_contorno()
    hay_ganador(tablero1,set()) == "N"
    hay_ganador(tablero2, contorno2) == ""
    hay_ganador(tablero3,set()) == "B"

#Test de intentar_saltear()
def test_intentar_saltear():
    tablero1 = [["N" for i in range(8)] for i in range(8)]
    tablero2 = [["" for i in range(8)] for i in range(8)]
    for i in range(8):
        tablero2[4][i]="N"
    tablero2[4][5]="B"
    contorno2 = set()
    for i in range(8):
        contorno2.add((3,i))
        contorno2.add((5,i))
    tablero3 = crear_tablero()
    contorno3 = crear_contorno()
    intentar_saltear(tablero3,"N",contorno3) == False
    intentar_saltear(tablero1,"N",set()) == False
    intentar_saltear(tablero2,"B",contorno2) == True

#Test de generador_tableros_prueba()
def test_generador_tableros_prueba():
    tablero1=crear_tablero()
    tablero1[0][1]="B"
    tablero1[0][2]="N"
    tablero2 = crear_tablero()
    for i in range(3,8):
        tablero2[i][4]="B"
    tablero2[0][0]="N"
    generador_tableros_prueba((),"N") == crear_tablero()
    generador_tableros_prueba(((0,1),(0,2)),"B") == tablero1
    generador_tableros_prueba(((3,4),(0,0),(4,4),(0,0),(5,4),(0,0),(6,4),(0,0),(7,4)),"B") == tablero2

if __name__ == "__main__":
    jugar()
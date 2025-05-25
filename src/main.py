from src.JuegoAhorcado import JuegoAhorcado, Estado
from src.Letra import Letra

def mostrar_ahorcado(intentos_restantes):
    """
    Muestra el dibujo del ahorcado según los intentos restantes.
    Cada intento perdido agrega una parte al dibujo del ahorcado.
    :param intentos_restantes: Número de intentos que le quedan al jugador
    """
    # Lista con los dibujos del ahorcado según los intentos restantes
    # Índice 0 = 0 intentos (ahorcado completo), Índice 6 = 6 intentos (solo la horca)
    dibujos = [
        """
        +---+
        |   |
        O   |    ¡AHORCADO!
       /|\\  |    Has perdido
       / \\  |
            |
        =========
        """,  # 0 intentos - ahorcado completo
        """
        +---+
        |   |
        O   |
       /|\\  |
       /    |    ¡Cuidado! Solo 1 intento
            |
        =========
        """,  # 1 intento
        """
        +---+
        |   |
        O   |
       /|\\  |    Te quedan 2 intentos
            |
            |
        =========
        """,  # 2 intentos
        """
        +---+
        |   |
        O   |
       /|   |    Te quedan 3 intentos
            |
            |
        =========
        """,  # 3 intentos
        """
        +---+
        |   |
        O   |
        |   |    Te quedan 4 intentos
            |
            |
        =========
        """,  # 4 intentos
        """
        +---+
        |   |
        O   |    Te quedan 5 intentos
            |
            |
            |
        =========
        """,  # 5 intentos
        """
        +---+
        |   |    Tienes 6 intentos
            |    ¡Comencemos!
            |
            |
            |
        =========
        """   # 6 intentos - inicio
    ]
    
    # Mostramos el dibujo correspondiente a los intentos restantes
    print(dibujos[intentos_restantes])

def mostrar_estado_juego(juego):
    """
    Muestra toda la información del estado actual del juego.
    :param juego: Objeto JuegoAhorcado con el estado actual
    """
    # Obtenemos las ocurrencias (letras adivinadas y guiones)
    ocurrencias = juego.dar_ocurrencias()
    
    # Mostramos la palabra con espacios entre cada letra/guión
    # Por ejemplo: "a l g o r i t m o" o "_ _ _ _ _ _ _ _ _"
    print("Palabra: " + " ".join(ocurrencias))
    
    # Mostramos cuántos intentos le quedan al jugador
    print(f"Intentos restantes: {juego.dar_intentos_disponibles()}")
    
    # Mostramos las letras que ya ha jugado el usuario
    jugadas = juego.dar_jugadas()
    if jugadas:  # Solo si hay jugadas realizadas
        # Convertimos los objetos Letra a strings para mostrarlos
        letras_jugadas = []
        for letra in jugadas:
            letras_jugadas.append(letra.dar_letra())
        print(f"Letras jugadas: {', '.join(letras_jugadas)}")
    
    # Mostramos el dibujo del ahorcado correspondiente
    mostrar_ahorcado(juego.dar_intentos_disponibles())

def main():
    """
    Función principal del juego que maneja toda la interfaz de usuario
    y el bucle principal del juego.
    """
    # Creamos una instancia del juego
    juego = JuegoAhorcado()
    
    # Mostramos el mensaje de bienvenida
    print("¡Bienvenido al Juego del Ahorcado!")
    print("Adivina la palabra letra por letra.")
    print("Tienes 6 intentos antes de ser ahorcado.")
    print("-" * 40)  # Línea separadora
    
    # Bucle principal para jugar múltiples partidas
    while True:
        # Iniciar nuevo juego
        juego.iniciar_juego()
        print("¡Nuevo juego iniciado!")
        
        # Bucle del juego actual - continúa mientras el estado sea JUGANDO
        while juego.dar_estado() == Estado.JUGANDO:
            print()  # Línea en blanco para separar
            
            # Mostramos el estado actual del juego
            mostrar_estado_juego(juego)
            
            # Pedimos al usuario que ingrese una letra
            entrada = input("Ingresa una letra: ").strip().lower()
            
            # Validamos que la entrada sea válida
            if len(entrada) != 1 or not entrada.isalpha():
                # Si no es una sola letra del alfabeto, mostramos error
                print("Por favor, ingresa solo una letra válida.")
                continue  # Volvemos al inicio del bucle
            
            # Creamos un objeto Letra con la entrada del usuario
            letra = Letra(entrada)
            
            # Verificamos si la letra ya fue utilizada
            if juego.letra_utilizada(letra):
                print("¡Ya jugaste esa letra! Intenta con otra.")
                continue  # Volvemos al inicio del bucle
            
            # Jugamos la letra y obtenemos el resultado
            resultado = juego.jugar_letra(letra)
            
            # Informamos al usuario el resultado de su jugada
            if resultado:
                # La letra estaba en la palabra
                print(f"¡Bien! La letra '{entrada}' está en la palabra.")
            else:
                # La letra no estaba en la palabra
                print(f"¡Oh no! La letra '{entrada}' no está en la palabra.")
        
        # El juego terminó (ya no estamos en estado JUGANDO)
        print()  # Línea en blanco
        
        # Mostramos el estado final del juego
        mostrar_estado_juego(juego)
        
        # Verificamos cómo terminó el juego y mostramos el mensaje apropiado
        if juego.dar_estado() == Estado.GANADOR:
            print("¡FELICIDADES! ¡Adivinaste la palabra!")
        elif juego.dar_estado() == Estado.AHORCADO:
            print("¡GAME OVER! Has sido ahorcado.")
            
            # Mostramos cuál era la palabra correcta
            palabra_completa = ""
            # Recorremos todas las letras de la palabra actual
            for letra in juego.dar_palabra_actual().dar_letras():
                palabra_completa += letra.dar_letra()
            print(f"La palabra era: {palabra_completa}")
        
        # Preguntamos si quiere jugar otra partida
        print()  # Línea en blanco
        jugar_otra = input("¿Quieres jugar otra vez? (s/n): ").strip().lower()
        
        # Si no responde 's' o 'si', salimos del bucle principal
        if jugar_otra != 's' and jugar_otra != 'si':
            break
    
    # Mensaje de despedida
    print("¡Gracias por jugar al Ahorcado!")

# Punto de entrada del programa
if __name__ == "__main__":
    # Solo ejecutamos main() si este archivo se ejecuta directamente
    # (no si se importa desde otro archivo)
    main()
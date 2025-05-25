import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QGridLayout, QPushButton, QLabel, 
                              QFrame, QSpacerItem, QSizePolicy, QScrollArea)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtGui import QFont, QPainter, QPen, QColor, QPixmap, QFontMetrics
import random
from enum import Enum
from typing import List

# Importar las clases del juego
from src.JuegoAhorcado import JuegoAhorcado, Estado
from src.Letra import Letra
from src.Palabra import Palabra

class HangmanDrawing(QWidget):
    """Widget personalizado para dibujar el ahorcado - Responsive"""
    
    def __init__(self):
        super().__init__()
        self.intentos_fallidos = 0
        self.setMinimumSize(200, 250)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("""
            background-color: white; 
            border: 2px solid #BDC3C7;
            border-radius: 10px;
            margin: 5px;
        """)
    
    def set_intentos_fallidos(self, intentos):
        self.intentos_fallidos = max(0, min(intentos, 6))
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Configurar el pincel - escalable
        pen_width = max(2, self.width() // 60)
        pen = QPen(QColor(50, 50, 50), pen_width)
        painter.setPen(pen)
        
        # Dimensiones escalables
        w = self.width()
        h = self.height()
        margin = w * 0.1
        
        # Calcular posiciones escalables
        base_y = h - margin
        base_left = margin
        base_right = w - margin
        post_x = w * 0.3
        post_top = margin
        beam_right = w * 0.7
        rope_y = margin + (h * 0.15)
        head_center_x = beam_right
        head_center_y = rope_y + (h * 0.1)
        head_radius = min(w, h) * 0.08
        
        # Base de la horca
        if self.intentos_fallidos >= 1:
            painter.drawLine(int(base_left), int(base_y), int(base_right), int(base_y))
        
        # Poste vertical
        if self.intentos_fallidos >= 2:
            painter.drawLine(int(post_x), int(base_y), int(post_x), int(post_top))
        
        # Poste horizontal
        if self.intentos_fallidos >= 3:
            painter.drawLine(int(post_x), int(post_top), int(beam_right), int(post_top))
        
        # Cuerda
        if self.intentos_fallidos >= 4:
            painter.drawLine(int(beam_right), int(post_top), int(beam_right), int(rope_y))
        
        # Cabeza
        if self.intentos_fallidos >= 5:
            painter.drawEllipse(int(head_center_x - head_radius), int(head_center_y), 
                              int(head_radius * 2), int(head_radius * 2))
        
        # Cuerpo
        if self.intentos_fallidos >= 6:
            body_start_y = head_center_y + (head_radius * 2)
            body_end_y = base_y - margin
            painter.drawLine(int(head_center_x), int(body_start_y), 
                           int(head_center_x), int(body_end_y))

class ResponsiveWordLabel(QLabel):
    """Label que se adapta automáticamente al tamaño de la palabra"""
    
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            color: #2C3E50; 
            background-color: #ECF0F1;
            border: 2px solid #BDC3C7;
            border-radius: 8px;
            padding: 15px;
            margin: 5px;
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    
    def update_word_display(self, word_parts, max_width=None):
        """Actualiza la visualización de la palabra con tamaño de fuente adaptativo"""
        if not word_parts:
            self.setText("Presiona 'Nuevo Juego'")
            return
            
        # Crear el texto con espacios
        display_text = " ".join(word_parts)
        
        # Calcular tamaño de fuente apropiado
        if max_width is None:
            max_width = self.width() - 40  # Margen para padding
        
        # Empezar con un tamaño base y ajustar
        font_size = 28
        min_font_size = 14
        
        while font_size >= min_font_size:
            font = QFont("Courier New", font_size, QFont.Bold)
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(display_text)
            
            if text_width <= max_width or font_size <= min_font_size:
                break
            font_size -= 2
        
        # Aplicar la fuente
        self.setFont(QFont("Courier New", font_size, QFont.Bold))
        self.setText(display_text)

class LetterButton(QPushButton):
    """Botón personalizado para las letras - Responsive"""
    
    def __init__(self, letter):
        super().__init__(letter)
        self.letter = letter
        self.setMinimumSize(35, 35)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setFont(QFont("Arial", 10, QFont.Bold))
        self.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #357ABD;
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background-color: #2F5F8F;
            }
            QPushButton:disabled {
                background-color: #BDC3C7;
                color: #7F8C8D;
            }
        """)

class HangmanGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.juego = JuegoAhorcado()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Juego del Ahorcado")
        self.setMinimumSize(600, 500)
        self.resize(1000, 700)
        
        # Widget central con scroll para pantallas pequeñas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        central_widget = QWidget()
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)
        
        # Layout principal responsive
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Título responsive
        title_label = QLabel("JUEGO DEL AHORCADO")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("""
            color: #2C3E50;
            margin-bottom: 10px;
            padding: 15px;
            background-color: #ECF0F1;
            border-radius: 10px;
            border: 2px solid #BDC3C7;
        """)
        main_layout.addWidget(title_label)
        
        # Layout para contenido principal (dibujo + juego)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        # Panel izquierdo - Dibujo del ahorcado
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.Box)
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border: 2px solid #E9ECEF;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        left_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout = QVBoxLayout(left_panel)
        
        # Dibujo del ahorcado
        self.hangman_drawing = HangmanDrawing()
        left_layout.addWidget(self.hangman_drawing)
        
        # Panel derecho - Juego
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 15px;
                padding: 15px;
                border: 2px solid #E9ECEF;
            }
        """)
        right_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout = QVBoxLayout(right_panel)
        
        # Palabra a adivinar - Responsive
        self.word_label = ResponsiveWordLabel()
        right_layout.addWidget(self.word_label)
        
        # Pista
        self.hint_label = QLabel("Pista: Términos de Programación")
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setFont(QFont("Arial", 11))
        self.hint_label.setStyleSheet("""
            color: #7F8C8D; 
            margin: 5px;
            padding: 8px;
            background-color: #F8F9FA;
            border-radius: 6px;
        """)
        right_layout.addWidget(self.hint_label)
        
        # Información del juego
        info_layout = QHBoxLayout()
        
        self.attempts_label = QLabel("Intentos: 6")
        self.attempts_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.attempts_label.setStyleSheet("""
            color: #E74C3C; 
            padding: 8px;
            background-color: #FADBD8;
            border-radius: 6px;
            border: 1px solid #F1948A;
        """)
        
        self.status_label = QLabel("¡Presiona 'Nuevo Juego' para comenzar!")
        self.status_label.setFont(QFont("Arial", 11))
        self.status_label.setStyleSheet("""
            color: #27AE60; 
            padding: 8px;
            background-color: #D5F4E6;
            border-radius: 6px;
            border: 1px solid #82E0AA;
        """)
        self.status_label.setWordWrap(True)
        
        info_layout.addWidget(self.attempts_label)
        info_layout.addStretch()
        info_layout.addWidget(self.status_label, 1)
        
        right_layout.addLayout(info_layout)
        
        # Teclado de letras - Responsive
        keyboard_frame = QFrame()
        keyboard_frame.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border-radius: 10px;
                padding: 10px;
                margin: 5px 0;
                border: 1px solid #DEE2E6;
            }
        """)
        keyboard_layout = QVBoxLayout(keyboard_frame)
        
        # Crear botones de letras con mejor distribución
        self.letter_buttons = {}
        letters = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        
        # Distribución en 3 filas más equilibrada
        rows = [
            letters[:9],   # A-I (9 letras)
            letters[9:18], # J-R (9 letras)
            letters[18:]   # S-Z (8 letras)
        ]
        
        for row_letters in rows:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(3)
            
            for letter in row_letters:
                btn = LetterButton(letter)
                btn.clicked.connect(lambda checked, l=letter: self.letter_clicked(l))
                self.letter_buttons[letter] = btn
                row_layout.addWidget(btn)
            
            keyboard_layout.addLayout(row_layout)
        
        right_layout.addWidget(keyboard_frame)
        
        # Botón de nuevo juego
        self.new_game_btn = QPushButton("Nuevo Juego")
        self.new_game_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.new_game_btn.setMinimumHeight(45)
        self.new_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #219A52;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        self.new_game_btn.clicked.connect(self.new_game)
        right_layout.addWidget(self.new_game_btn)
        
        # Agregar paneles al layout de contenido
        content_layout.addWidget(left_panel, 1)
        content_layout.addWidget(right_panel, 2)
        
        main_layout.addLayout(content_layout)
        
        # Estilo general de la ventana
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F2F5;
            }
            QScrollArea {
                border: none;
                background-color: #F0F2F5;
            }
        """)
        
        # Inicializar interfaz
        self.update_display()
    
    def resizeEvent(self, event):
        """Manejar cambios de tamaño de ventana"""
        super().resizeEvent(event)
        # Actualizar el display cuando cambie el tamaño
        if hasattr(self, 'word_label'):
            self.update_word_display()
    
    def new_game(self):
        """Inicia un nuevo juego"""
        self.juego.iniciar_juego()
        
        # Habilitar todos los botones y restaurar colores
        for btn in self.letter_buttons.values():
            btn.setEnabled(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4A90E2;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 2px;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
                QPushButton:pressed {
                    background-color: #2F5F8F;
                }
            """)
        
        self.update_display()
    
    def letter_clicked(self, letter):
        """Maneja el clic en una letra"""
        if self.juego.dar_estado() != Estado.JUGANDO:
            return
        
        letra = Letra(letter.lower())
        resultado = self.juego.jugar_letra(letra)
        
        # Deshabilitar el botón y cambiar su color
        btn = self.letter_buttons[letter]
        btn.setEnabled(False)
        
        if resultado:
            # Letra correcta - verde
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #27AE60;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 2px;
                }
            """)
        else:
            # Letra incorrecta - rojo
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E74C3C;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 2px;
                }
            """)
        
        self.update_display()
    
    def update_word_display(self):
        """Actualiza solo la visualización de la palabra"""
        estado = self.juego.dar_estado()
        
        if estado == Estado.NO_INICIADO:
            self.word_label.update_word_display(["_"] * 8)
        elif estado in [Estado.JUGANDO, Estado.GANADOR]:
            # Mostrar palabra con letras adivinadas
            ocurrencias = self.juego.dar_ocurrencias()
            word_parts = [part.upper() if part != "_" else "_" for part in ocurrencias]
            self.word_label.update_word_display(word_parts)
        elif estado == Estado.AHORCADO:
            # Mostrar palabra completa
            if self.juego.palabra_actual:
                palabra_completa = []
                for letra in self.juego.palabra_actual.dar_letras():
                    palabra_completa.append(letra.dar_letra().upper())
                self.word_label.update_word_display(palabra_completa)
    
    def update_display(self):
        """Actualiza la interfaz con el estado actual del juego"""
        estado = self.juego.dar_estado()
        
        if estado == Estado.NO_INICIADO:
            self.word_label.update_word_display([])
            self.status_label.setText("¡Presiona 'Nuevo Juego' para comenzar!")
            self.status_label.setStyleSheet("""
                color: #3498DB; 
                padding: 8px;
                background-color: #D6EAF8;
                border-radius: 6px;
                border: 1px solid #85C1E9;
            """)
            self.attempts_label.setText("Intentos: 6")
            self.hangman_drawing.set_intentos_fallidos(0)
            
        elif estado == Estado.JUGANDO:
            # Actualizar palabra
            self.update_word_display()
            
            # Actualizar intentos
            intentos = self.juego.dar_intentos_disponibles()
            self.attempts_label.setText(f"Intentos: {intentos}")
            
            # Actualizar color de intentos según el número
            if intentos <= 2:
                attempts_color = "#E74C3C"
                attempts_bg = "#FADBD8"
            elif intentos <= 4:
                attempts_color = "#F39C12"
                attempts_bg = "#FCF3CF"
            else:
                attempts_color = "#27AE60"
                attempts_bg = "#D5F4E6"
            
            self.attempts_label.setStyleSheet(f"""
                color: {attempts_color}; 
                padding: 8px;
                background-color: {attempts_bg};
                border-radius: 6px;
                font-weight: bold;
            """)
            
            # Actualizar dibujo
            intentos_fallidos = self.juego.MAX_INTENTOS - intentos
            self.hangman_drawing.set_intentos_fallidos(intentos_fallidos)
            
            self.status_label.setText("¡Adivina la palabra!")
            self.status_label.setStyleSheet("""
                color: #F39C12; 
                padding: 8px;
                background-color: #FCF3CF;
                border-radius: 6px;
                border: 1px solid #F7DC6F;
            """)
            
        elif estado == Estado.GANADOR:
            self.update_word_display()
            
            self.status_label.setText("🎉 ¡FELICIDADES! ¡Has ganado! 🎉")
            self.status_label.setStyleSheet("""
                color: #27AE60; 
                padding: 10px;
                background-color: #D5F4E6;
                border-radius: 8px;
                border: 2px solid #58D68D;
                font-weight: bold;
                font-size: 13px;
            """)
            
            # Deshabilitar todos los botones restantes
            for btn in self.letter_buttons.values():
                if btn.isEnabled():
                    btn.setEnabled(False)
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #BDC3C7;
                            color: #7F8C8D;
                            border: none;
                            border-radius: 6px;
                            font-weight: bold;
                            margin: 2px;
                        }
                    """)
            
        elif estado == Estado.AHORCADO:
            # Mostrar palabra completa
            self.update_word_display()
            
            palabra_texto = ""
            if self.juego.palabra_actual:
                letras = [letra.dar_letra().upper() for letra in self.juego.palabra_actual.dar_letras()]
                palabra_texto = "".join(letras)
            
            self.status_label.setText(f"💀 ¡Perdiste! La palabra era: {palabra_texto}")
            self.status_label.setStyleSheet("""
                color: #E74C3C; 
                padding: 10px;
                background-color: #FADBD8;
                border-radius: 8px;
                border: 2px solid #F1948A;
                font-weight: bold;
                font-size: 12px;
            """)
            
            # Actualizar dibujo completo
            self.hangman_drawing.set_intentos_fallidos(6)
            
            # Deshabilitar todos los botones restantes
            for btn in self.letter_buttons.values():
                if btn.isEnabled():
                    btn.setEnabled(False)
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #BDC3C7;
                            color: #7F8C8D;
                            border: none;
                            border-radius: 6px;
                            font-weight: bold;
                            margin: 2px;
                        }
                    """)

def main():
    app = QApplication(sys.argv)
    
    # Configurar fuente por defecto
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = HangmanGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
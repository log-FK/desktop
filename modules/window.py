from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .app import app  # QApplication має бути створений до вікна

WIDTH_WINDOW = 800
HEIGHT_WINDOW = 600
SQUARE_SIZE = 30

WINDOW_COLOR = "#393939"
CANVAS_COLOR = "#e2eced"
SQUARE_COLOR = "#0ea1e6"


class MainWindow(QMainWindow):
    """Головне вікно: Escape очищає всі квадрати."""

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            clear_squares()
        super().keyPressEvent(event)


main_window = MainWindow()
main_window.setWindowTitle("Weather app")
main_window.resize(WIDTH_WINDOW, HEIGHT_WINDOW)

central = QWidget(parent=main_window)
central.setObjectName("central")
central.setStyleSheet(f"QWidget#central {{ background-color: {WINDOW_COLOR}; }}")
main_window.setCentralWidget(central)

window_layout = QVBoxLayout()
window_layout.setContentsMargins(8, 8, 8, 8)
window_layout.setSpacing(10)
central.setLayout(window_layout)


canvas = QPushButton()
canvas.setObjectName("canvas")
# присваивает виджету canvas внутреннее текстовое имя
canvas.setFocusPolicy(Qt.FocusPolicy.NoFocus)
# метод, который определяет, каким образом виджет может стать «активным» (получить фокус) для работы с клавиатурой
canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
# специальный флаг (константа), который говорит окну: «Этот элемент готов расширяться и забирать себе всё лишнее» метод, который устанавливает политику изменения размеров виджета
canvas.setStyleSheet(
    f"QPushButton#canvas {{ background-color: {CANVAS_COLOR}; border: 1px solid #1a1a1a; }}"
    f"QPushButton#canvas:pressed {{ background-color: {CANVAS_COLOR}; }}"
)
window_layout.addWidget(canvas, stretch=1)

hint_label = QLabel("Ліва кнопка миші - додати фрейм, Escape: очистити")
hint_label.setStyleSheet("color: white; background: transparent;")
window_layout.addWidget(hint_label)

count_label = QLabel("Всього фреймів: 0")
count_label.setStyleSheet("color: white; background: transparent;")
window_layout.addWidget(count_label)

squares = []


def update_counter():
    count_label.setText(f"Всього фреймів: {len(squares)}")

# mapFromGlobal-пересчитывает глобальные координаты экрана
def add_square():
    point = canvas.mapFromGlobal(QCursor.pos())
    x = point.x()
    y = point.y()
    square = QFrame(canvas)
    square.setFixedSize(SQUARE_SIZE, SQUARE_SIZE)
    square.setStyleSheet(f"background-color: {SQUARE_COLOR}; border: none;")
    square.move(x - SQUARE_SIZE // 2, y - SQUARE_SIZE // 2)
    square.show()
    squares.append(square)
    update_counter()


def clear_squares():
    for square in squares:
        square.deleteLater()
        # безпечне видалення об'єкта
    squares.clear()
    update_counter()


canvas.clicked.connect(add_square)
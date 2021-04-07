import sys

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow

from functools import partial

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPen, QColor, QBrush

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    Form, Window = uic.loadUiType("toaster_main.gui")

    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)

    MODES = {
        # Режим №1. Заливка экрана чередующимися полосами цвета
        1: {
            "1x8":
                {"width": 1,
                 "line1": (85, 107, 86),
                 "line2": (170, 148, 169),
                 "background": (0, 0, 0), },

            "2x8":
                {"width": 2,
                 "line1": (85, 107, 86),
                 "line2": (170, 148, 169),
                 "background": (0, 0, 0), },

            "1x6":
                {"width": 1,
                 "line1": (168, 80, 164),
                 "line2": (84, 172, 88),
                 "background": (0, 0, 0), },

            "2x6":
                {"width": 2,
                 "line1": (168, 80, 164),
                 "line2": (84, 172, 88),
                 "background": (0, 0, 0), },
        },
        # Режим №2. Заливка экрана чередующимися полосами цвета
        2: {"1x8":
                {"width": 1,
                 "line1": (255, 255, 255),
                 "line2": (0, 0, 0),
                 "background": (0, 0, 0), },

            "2x8":
                {"width": 2,
                 "line1": (255, 255, 255),
                 "line2": (0, 0, 0),
                 "background": (0, 0, 0), },
            }
    }
    CURRENT_MODE = {}

    SCREEN_HEIGHT_DIVIDER = 1

    LINES_ORIENTATION = 0  # 0 - vertical, 1 - horizontal


    def on_test_clicked(mode, lines):
        form.buttonStart.setEnabled(True)
        global CURRENT_MODE
        CURRENT_MODE = MODES[mode][lines]


    def on_full_screen_clicked():
        global SCREEN_HEIGHT_DIVIDER
        SCREEN_HEIGHT_DIVIDER = 1


    def on_half_screen_clicked():
        global SCREEN_HEIGHT_DIVIDER
        SCREEN_HEIGHT_DIVIDER = 2


    def on_vertical_orientation_clicked():
        global LINES_ORIENTATION
        LINES_ORIENTATION = 0


    def on_horizontal_orientation_clicked():
        global LINES_ORIENTATION
        LINES_ORIENTATION = 1


    def on_slider_clicked():
        form.labelBlinking.setText(str(form.sliderBlinking.value() / 2))


    def on_start_button_clicked():
        full_screen = QDialog()
        full_screen.scene = QGraphicsScene()
        full_screen.scene.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
        full_screen.graphic_view = QGraphicsView(full_screen.scene, full_screen)
        full_screen.graphic_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        full_screen.graphic_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        full_screen.graphic_view.setAlignment(Qt.AlignTop)

        screen = app.primaryScreen()
        size = screen.size()
        width, height = size.width(), size.height()
        # rect = screen.availableGeometry()
        # width, height = rect.width(), rect.height()

        full_screen.graphic_view.setGeometry(0, 0, width, height)

        show = True

        def toggle_lines():
            nonlocal show

            if show:
                full_screen.pen = QPen(QColor(*CURRENT_MODE['line1']))
                full_screen.bg_pen = QPen(QColor(*CURRENT_MODE['line2']))

                full_screen.pen.setWidth(CURRENT_MODE['width'])

                full_screen.scene.addRect(0, 0, width, height, QColor(*CURRENT_MODE['line2']),
                                          QBrush(QColor(*CURRENT_MODE['line2'])))

                if LINES_ORIENTATION == 0:
                    for x in range(0, width, 2 * CURRENT_MODE['width']):
                        full_screen.scene.addLine(x, 0, x, height // SCREEN_HEIGHT_DIVIDER, full_screen.pen)

                else:
                    for y in range(0, height // SCREEN_HEIGHT_DIVIDER, 2 * CURRENT_MODE['width']):
                        full_screen.scene.addLine(0, y, width, y, full_screen.pen)
            else:
                full_screen.scene.clear()

            show = not show

        if form.sliderBlinking.value():
            full_screen.timer = QTimer()
            full_screen.timer.timeout.connect(toggle_lines)

            stopped = False

            def on_key(e):
                if e.key() != Qt.Key_Space:
                    full_screen.close()

                nonlocal stopped
                if e.key() == Qt.Key_Space:
                    if not stopped:
                        full_screen.timer.stop()
                        full_screen.scene.clear()
                    if stopped:
                        full_screen.timer.start(form.sliderBlinking.value() * 500)
                    stopped = not stopped

            full_screen.keyPressEvent = on_key
            full_screen.timer.start(form.sliderBlinking.value() * 500)
        else:
            toggle_lines()

        full_screen.showFullScreen()
        full_screen.exec()


    form.buttonStart.clicked.connect(on_start_button_clicked)
    form.radioTestLVDS1_1x6.clicked.connect(partial(on_test_clicked, 1, '1x6'))
    form.radioTestLVDS1_1x8.clicked.connect(partial(on_test_clicked, 1, '1x8'))
    form.radioTestLVDS1_2x6.clicked.connect(partial(on_test_clicked, 1, '2x6'))
    form.radioTestLVDS1_2x8.clicked.connect(partial(on_test_clicked, 1, '2x8'))

    form.radioTestLVDS2_1x8.clicked.connect(partial(on_test_clicked, 2, '1x8'))
    form.radioTestLVDS2_2x8.clicked.connect(partial(on_test_clicked, 2, '2x8'))

    form.radioScreenFull.clicked.connect(on_full_screen_clicked)
    form.radioScreenUpperHalf.clicked.connect(on_half_screen_clicked)

    form.radioOrientationVertical.clicked.connect(on_vertical_orientation_clicked)
    form.radioOrientationHorizontal.clicked.connect(on_horizontal_orientation_clicked)

    form.sliderBlinking.valueChanged.connect(on_slider_clicked)

    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)

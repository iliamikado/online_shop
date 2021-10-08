from PyQt5 import QtCore
from lib.window import ShopWindow


def test_buttons_start(qtbot):
    window = ShopWindow()
    assert len(window.buttons) == len(window.data)

    for i, button in enumerate(window.buttons):
        assert 'Товар {}'.format(i+1) == button.text()

    # кликаем по левой кнопке мвши (LeftButton)
    qtbot.mouseClick(window.buttons[0], QtCore.Qt.LeftButton)
    qtbot.mouseClick(window.buttons[0], QtCore.Qt.LeftButton)

    for i, button in enumerate(window.buttons):
        print(button.text())

    assert 'Товар 1'.format(window.data[1]) == window.buttons[0].text()

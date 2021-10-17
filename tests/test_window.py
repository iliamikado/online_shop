from PyQt5 import QtCore
from lib.window import ShopWindow
import pytest


@pytest.fixture
def data():
    return {"Good 1": 5, "Good 3": 4, "Good 2": 10}


def test_buttons_start(qtbot):
    window = ShopWindow(data_path='../')
    assert len(window.buttons) == len(window.data)

    for key, but in window.buttons.items():
        assert but.text().find(key) != -1

    # кликаем по левой кнопке мвши (LeftButton)
    good = list(window.buttons.items())[0]
    for i in range(window.data[good[0]]):
        qtbot.mouseClick(good[1], QtCore.Qt.LeftButton)
    assert window.data[good[0]] == 0
    qtbot.mouseClick(good[1], QtCore.Qt.LeftButton)
    assert window.data[good[0]] == 0


def test_buttons_count(data):
    window = ShopWindow(test_data=data, data_path='../')
    assert len(window.buttons) == 3


def test_buttons_text(data):
    window = ShopWindow(test_data=data, data_path='../')
    for good in window.data:
        assert window.buttons[good].text().find(good) != -1
        assert window.buttons[good].text().find('Осталось: ' + str(window.data[good])) != -1


def test_sorting(qtbot, data):
    window = ShopWindow(test_data=data, data_path='../')
    but1 = window.buttons['Good 1']
    but2 = window.buttons['Good 3']
    but3 = window.buttons['Good 2']
    assert but1.x() < but3.x() < but2.x()
    qtbot.mouseClick(window.sort_button, QtCore.Qt.LeftButton)
    assert but3.x() > but1.x() > but2.x()
    qtbot.mouseClick(but1, QtCore.Qt.LeftButton)
    qtbot.mouseClick(but1, QtCore.Qt.LeftButton)
    assert but3.x() > but2.x() > but1.x()

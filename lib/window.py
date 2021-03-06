from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
import json
import requests

from functools import partial


class ShopWindow(QMainWindow):

    def __init__(self, test_data=None):
        super().__init__()

        with open('data/parameters.json', 'r', encoding='utf-8') as file:
            self.param = json.load(file)

        self.setWindowTitle(self.param['window_title'])
        self.resize(self.param['sizeX'], self.param['sizeY'])

        if test_data is None:
            self.data = requests.get('http://' + self.param['server_address'] + ':'
                                     + str(self.param['server_port']) + '/api/stats').json()['data']
        else:
            self.data = test_data

        self.label = QLabel(self.param['main_label']['text'], self)
        self.label.setGeometry(0, 0, 1000, 300)

        self.sort_button = QPushButton(self)
        self.sort_button.setGeometry(0, 60, 200, 50)
        self.sort_button.setText(self.param['sort_button']['start_text'] + self.param['sort_button']['conditions'][1])
        self.buttons_sort = 'by_name'
        self.sort_button.clicked.connect(self.click_on_sorting_button)

        self.buttons = dict()
        for good in self.data:
            self.buttons[good] = QPushButton(good + "\nОсталось: " + str(self.data[good]), self)
        for good in self.buttons.keys():
            self.buttons[good].clicked.connect(partial(self.on_click, good))
        self.set_buttons()

    def on_click(self, good):
        if self.data[good] > 0:
            self.data[good] -= 1
        request = requests.post('http://' + self.param['server_address'] + ':'
                                + str(self.param['server_port']) + '/api/reserve',
                                data={'username': 'Ilia', 'item': good})
        print(request.text)
        self.buttons[good].setText(good + '\n' + 'Осталось: ' + str(self.data[good]))
        self.set_buttons()

    def set_buttons(self):
        arr = sorted(self.buttons.items(), key=self.buttons_sorting_key)
        for i in range(len(arr)):
            arr[i][1].setGeometry(i * 100, 0, 100, 50)

    def buttons_sorting_key(self, x):
        if self.buttons_sort == 'by_name':
            return x[0]
        elif self.buttons_sort == 'by_count':
            return self.data[x[0]]
        else:
            return x[0]

    def click_on_sorting_button(self):
        if self.buttons_sort == 'by_name':
            self.buttons_sort = 'by_count'
            self.sort_button.setText(
                self.param['sort_button']['start_text'] + self.param['sort_button']['conditions'][0])
        elif self.buttons_sort == 'by_count':
            self.buttons_sort = 'by_name'
            self.sort_button.setText(
                self.param['sort_button']['start_text'] + self.param['sort_button']['conditions'][1])
        self.set_buttons()

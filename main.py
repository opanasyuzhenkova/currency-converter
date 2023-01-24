import sys
import lxml
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon
from ui import Ui_MainWindow
from bs4 import BeautifulSoup
import requests

class Currency():
    """Class for receiving and returning currencies"""

    def __init__(self):
        """Constructor"""
        self.url = 'http://www.cbr.ru/scripts/XML_daily.asp'

    def __del__(self):
        """Destructor"""
        #print("Destructor called")

    def get_currency(self):  # receive one currency
        return self.get_rate()[self._v_chc]


    def set_currency(self, chc: str):  # adding a new currency to the list of tracked currencies
        self._v_chc = chc
        if chc == 'R9999':
            return {chc: None}

    def get_rate(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "xml")
        result = {}
        vals = soup.find_all('Valute')
        for item in vals:
            v_id = item['ID']
            v_name = item.find('Name').text
            v_chc = item.find('CharCode').text
            v_nom = item.find('Nominal').text
            value = item.find('Value').text.replace(',', '.')
            result[v_chc] = {
                'value': "%.5f" % (float(value)/ float(v_nom))
            }
        return result


class CurrencyConv(Currency, QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Currency Converter')
        self.setWindowIcon(QIcon('currencies.png'))
        self.ui.input_currency.setPlaceholderText('from currency')
        self.ui.input_amount.setPlaceholderText('value')
        self.ui.output_currency.setPlaceholderText('to currency')
        self.ui.output_amount.setPlaceholderText('result')
        self.ui.pushButton.clicked.connect(self.converter)

    def input_data(self, chc_cur):
        selected_currency = Currency()
        selected_currency.set_currency(chc_cur)
        result = selected_currency.get_currency()
        return result.get('value')

    def converter(self):
        c = Currency()
        input_currency = self.ui.input_currency.text()
        output_currency = self.ui.output_currency.text()
        input_amount = self.ui.input_amount.text()
        cur1_rate = self.input_data(input_currency)
        cur2_rate = self.input_data(output_currency)
        output_amount = "%.5f" % (float(cur1_rate) / float(cur2_rate) * float(input_amount))
        self.ui.output_amount.setText(str(output_amount))

app = QtWidgets.QApplication([])
application = CurrencyConv()
application.show()

sys.exit(app.exec())

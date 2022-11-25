import sys
import time
from pathlib import Path

from PyQt5 import QtWidgets
from gui import auto24
from selenium_24.parser import Auto24Parser

# Path
file_path = Path.cwd() / 'files'
if not file_path.is_dir():
    file_path.mkdir(parents=True, exist_ok=True)


class ExampleApp(QtWidgets.QMainWindow, auto24.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run_parser)
        self.pushButton2.clicked.connect(self.check_time)

        self.input_file = file_path / 'article.xlsx'
        self.output_file = file_path / 'result.xlsx'

        self.label.setText('Для работы парсера необходимо разместить файл с названием article.xlsx в папке files.\n'
                           'В эту же папку будет записан файл result.xlsx с результатами парсинга.\n'
                           'Страна: GERMANY. Тип: BTC')

    def run_parser(self):
        parser = Auto24Parser(
            input_fl=self.input_file,
            output_fl=self.output_file
        )
        try:
            parser.run_parser()
            time.sleep(3)
            self.close()
        except UserWarning:
            self.label.setText(f'Файл article.xlsx в папке /files не найден.')



    def check_time(self):
        parser = Auto24Parser(
            input_fl=self.input_file,
            output_fl=self.output_file
        )

        try:
            lenght, time = parser.get_parsing_time()
            self.label.setText(f'Кол-во Артикулей: {lenght}\nПримерное время работы: {time}')
        except:
            self.label.setText(f'Файл article.xlsx в папке /files не найден.')

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

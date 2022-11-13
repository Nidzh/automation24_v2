import sys
from pathlib import Path
from PyQt5 import QtWidgets
from selenium_24.parser import Auto24Parser
from gui import auto24

# Path
file_path = Path.cwd() / 'files'
if not file_path.is_dir():
    file_path.mkdir(parents=True, exist_ok=True)


class ExampleApp(QtWidgets.QMainWindow, auto24.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progressBar.setProperty('value', 0)
        self.pushButton.clicked.connect(self.run_parser)

        self.input_file = file_path / 'article.xlsx'
        self.output_file = file_path / 'result.xlsx'

    def run_parser(self):
        parser = Auto24Parser(
            input_fl=self.input_file,
            output_fl=self.output_file
        )

        parser.run_parser()

        # self.label.setText(f'Файл загружен.\nКол-во артикулей: {length}. \n'
        #                    f'Примерное время обработки: {parsing_time}')


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()

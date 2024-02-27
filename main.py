import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class WordDisplayApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Отображение слов')
        self.showFullScreen()

        self.setStyleSheet("background-color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showNextWord)

    def startDisplaying(self, words, interval):
        self.words = words
        self.word_index = 0
        self.timer_interval = interval
        self.paused = False
        self.showNextWord()

    def stopDisplaying(self):
        self.timer.stop()

    def showNextWord(self):
        if (self.word_index < len(self.words)):
            word = self.words[self.word_index]
            self.label.setText(word)
            font = QFont("Times New Roman", 100)
            self.label.setFont(font)
            self.word_index += 1
            self.timer.start(self.timer_interval)
        else:
            self.stopDisplaying()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if not self.paused:
                words_str = words[self.word_index -3] + ' ' + words[self.word_index -2] + ' ' +  words[self.word_index -1]
                self.label.setText(words_str)
                self.timer.stop()
                self.paused = True
                print('1')
            else:
                self.showNextWord()
                self.paused = False
                print('2')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WordDisplayApp()
    file = open('Книга.txt', encoding='UTF-8')
    s = file.read()
    zxc = s.split()
    words = []
    sigma = 'НенеНоноИиАаСсВвУу'
    for i in range(len(zxc) - 1):
        if zxc[i] in sigma:
            words.append(zxc[i] + ' ' + zxc[i + 1])

        elif len(zxc) == i + 2:
            words.append(zxc[i])
            words.append(zxc[i + 1])
        else:
            words.append(zxc[i])
    interval = 350  # Интервал между словами в миллисекундах
    window.startDisplaying(words, interval)
    window.show()
    sys.exit(app.exec_())
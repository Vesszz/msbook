import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import time

#pip install PyQt5

'''
СДЕЛАТЬ: (возможно)
выбор книги
узнавание главы от индекса
узнавание страница (в случае .doc/.docx файла)
процент книги
'''

global book
global log 
log = True #Логгать или нет

class Book():
    def __init__(self, name: str, author: str, word_index: int, words: list):
        self.name = name
        self.author = author
        self.word_index = word_index
        self.words = words

    def __str__(self):
        return str(self.name + ";" + self.author + ";" + str(self.word_index))

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



    def startDisplaying(self, interval):
        self.words = book.words
        self.word_index = book.word_index
        self.timer_interval = interval
        self.paused = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showNextWord)
        #self.timer.start(3000)  ##

    def stopDisplaying(self):
        save(book, self.word_index)
        sys.exit()

    def showNextWord(self):
        save(book, self.word_index)
        print(self.word_index)
        if (self.word_index < len(self.words)):
            word = self.words[self.word_index]
            self.label.setText(word)
            font = QFont("Times New Roman", 100) ##
            self.label.setFont(font)
            self.word_index += 1
            self.timer.start(self.timer_interval)
        else:
            self.stopDisplaying()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if not self.paused:
                self.timer.stop()
                self.paused = True
            else:
                self.showNextWord()
                self.paused = False
        if event.key() == Qt.Key_F1:
            self.stopDisplaying()

# надо переработать и не сохранять каждую секунду
def save(book: Book, word_index: int):
    global log
    print(word_index)
    with open('info.txt', 'r', encoding='utf-8') as f:
        old_data = f.read()

    new_data = old_data.replace(book.name+";"+book.author+";"+str(word_index-1), book.name+";"+book.author+";"+str(word_index), 1)
    with open('info.txt', 'w', encoding='utf-8') as f: f.write(new_data)
    if log: print("saved")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    books = os.listdir('.books/')
    book_name_input = input("Введите название книги\n")
    book_path = '.books/' + book_name_input + ".txt"
    pre_words = open(book_path, encoding='UTF-8').read().split()
    words = []
    i = 0
    while i < len(pre_words):
        current_word = pre_words[i]

        if len(current_word) < 4:
            if i + 1 < len(pre_words):
                next_word = pre_words[i + 1]
                combined_word = current_word + ' ' + next_word
                words.append(combined_word)
                i += 1
        else:
            words.append(current_word)

        i += 1

    if len(pre_words) % 2 != 0:
        words.append(pre_words[-1])
    info = open("info.txt", encoding="utf-8").readlines()
    for book_info in info:
        if len(book_info.replace("\n","").split(";")) != 3: print("Неизвестная ошибка")
        else: 
            book_name, book_author, book_word_index = book_info.split(";")
            if book_name == book_name_input + ".txt": 
                word_index = int(book_word_index)
                book_selected = Book(book_name,book_author,word_index,words)
    
    book = book_selected
    print(book.word_index) 
    window = WordDisplayApp()
    interval = 350  # Интервал между словами в миллисекундах
    window.startDisplaying(interval)
    window.show()
    sys.exit(app.exec_())

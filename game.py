import sys
import json
import random
import glob

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, pyqtSignal, QTimer
from playsound import playsound


class picButton(QPushButton):
	answered = pyqtSignal(str)

	def __init__(self, text):
		super().__init__()
		self.text = text
		self.clicked.connect(self.answer)

	def answer(self, *args):
		self.answered.emit(self.text)


class Main(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()
		self.image_paths = ""
		self.last_correct_answer = ""
		self.vowels = ["ա", "ի", "ու", "օ", "ո", "է", "ե", "ը", "յ"]

	def load_game(self, answer):
		for i in reversed(range(self.grid.count())):
			self.grid.itemAt(i).widget().setParent(None)

		with open(f"jsons/{answer}.json", "r") as f:
			self.dictionary = json.load(f)
		self.image_paths = f"pics/{answer}"
		self.process()

	def extract_name(self, name):
		name = name[:-5]
		name = name.split("/")[1]
		return name

	def choose_game(self):
		self.question_lbl.setText("Ընտրիր խաղը (choose the game)")
		for i in reversed(range(self.grid.count())):
			self.grid.itemAt(i).widget().setParent(None)

		games = glob.glob("jsons/*.json")
		game_names = [self.extract_name(x) for x in games]
		positions = range(len(game_names))
		positions = [(0, p) for p in positions]
		for position, name in zip(positions, game_names):
			button = picButton(name)
			button.setText(name)
			button.answered.connect(self.load_game)
			path = f"pics/{name}/1"
			icon = QIcon(path)
			button.setIcon(icon)
			button.setIconSize(QSize(400, 400))
			self.grid.addWidget(button, *position)

	def initUI(self):
		self.grid = QGridLayout()
		self.vbox = QVBoxLayout()
		self.setLayout(self.vbox)
		self.question_lbl = QLabel("")
		self.question_lbl.setFont(QFont('Arial', 16))
		self.menu_btn = QPushButton("Մենյու (Menu)")
		self.menu_btn.clicked.connect(self.choose_game)

		self.choose_game()
		self.vbox.addWidget(self.question_lbl)
		self.vbox.addLayout(self.grid)
		self.vbox.addWidget(self.menu_btn)

		self.move(300, 300)
		self.setWindowTitle('Արարատ (Ararat)')
		self.show()

	def process(self):
		self.sample = random.sample(list(self.dictionary.keys()), 4)
		self.correct_answer = random.choice(self.sample)
		while self.correct_answer == self.last_correct_answer:
			self.correct_answer = random.choice(self.sample)
			self.last_correct_answer = self.correct_answer
		self.correct_answer_path = self.dictionary[self.correct_answer]
		self.question = f"Գտիր (Find) {self.correct_answer}"
		if self.correct_answer[-1] in self.vowels:
			self.question += "ն"
		else:
			self.question += "ը"

		self.question_lbl.setText(self.question)

		positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

		for position, name in zip(positions, self.sample):
			button = picButton(name)
			button.answered.connect(self.check_answer)
			path = self.dictionary[name]
			icon = QIcon(f'{self.image_paths}/{path}')
			button.setIcon(icon)
			button.setIconSize(QSize(400, 400))
			self.grid.addWidget(button, *position)

	def check_answer(self, answer):
		if answer == self.correct_answer:
			QTimer.singleShot(1, lambda: playsound("conf/Correct.mp3"))
			self.process()
		else:
			QTimer.singleShot(1, lambda: playsound("conf/Wrong.mp3"))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Main()
	sys.exit(app.exec_())

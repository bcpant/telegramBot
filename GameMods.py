import sqlite3
import random
import keyboard
class FourAnswClass:
    def __init__(self, dbPath: str):
        self.__dbPath = dbPath
        getTask = self.variantsPlay()
        self.__askedWord = getTask[0]
        self.__trueAnswer = getTask[1]
        self.__wrongAnswer1 = getTask[2]
        self.__wrongAnswer2 = getTask[3]
        self.__wrongAnswer3 = getTask[4]

    def __str__(self):
        return f'Word:{self.__askedWord}, variants:\n { self.__trueAnswer},{self.__wrongAnswer1}, {self.__wrongAnswer2}, {self.__wrongAnswer3}'

    @property
    def askedWord(self):
        return self.__askedWord
    @property
    def trueAnswer(self):
        return self.__trueAnswer
    @property
    def wrongAnswer1(self):
        return self.__wrongAnswer1
    @property
    def wrongAnswer2(self):
        return self.__wrongAnswer2
    @property
    def wrongAnswer3(self):
        return self.__wrongAnswer3

    @staticmethod
    def get_four_unique_random_numbers(start, end):
        return random.sample(range(start, end + 1), 4)

    def get_word_and_translation_by_id(self, word_id):
        dbConnection = sqlite3.connect(self.__dbPath)
        curs = dbConnection.cursor()
        curs.execute("SELECT word, translate FROM words WHERE id = ?", (word_id,))
        result = curs.fetchone()
        curs.close()
        dbConnection.close()

        if result:
            return {
                'word': result[0],
                'translate': result[1]
            }
        else:
            return "Слово не найдено."

    def variantsPlay(self):
        variants = []
        ansVariants = []
        variantsId = self.get_four_unique_random_numbers(1, 5000)
        for id in variantsId:
            variants.append(self.get_word_and_translation_by_id(id))
        mWord = variants[0]['word']
        ansWord = variants[0]['translate']
        wrongAns1 = variants[1]['translate']
        wrongAns2 = variants[2]['translate']
        wrongAns3 = variants[3]['translate']
        return mWord, ansWord, wrongAns1, wrongAns2, wrongAns3

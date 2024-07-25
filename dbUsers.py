import sqlite3


class Db:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `tguserid` FROM `user` WHERE `tguserid` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id, user_chat_id):
        self.cursor.execute("INSERT INTO `user` (`tguserid`, `tguserchatid`) VALUES (?, ?)", (user_id, user_chat_id))
        return self.conn.commit()

    def add_true_answer(self, user_id):
        self.cursor.execute("SELECT `rightAnswers` FROM `user` WHERE `tguserid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            oldValue = result[0]
            newValue = oldValue + 1
            self.cursor.execute("UPDATE `user` SET `rightAnswers` = ? WHERE `tguserid` = ?", (newValue, user_id))
            self.conn.commit()
        else:
            print(f"User with tguserid {user_id} not found in the database.")

    def add_wrong_answer(self, user_id):
        self.cursor.execute("SELECT `wrongAnswers` FROM `user` WHERE `tguserid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            oldValue = result[0]
            newValue = oldValue + 1
            self.cursor.execute("UPDATE `user` SET `wrongAnswers` = ? WHERE `tguserid` = ?", (newValue, user_id))
            self.conn.commit()
        else:
            print(f"User with tguserid {user_id} not found in the database.")

    def get_true_count(self, user_id):
        self.cursor.execute("SELECT `rightAnswers` FROM `user` WHERE `tguserid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"User with tguserid {user_id} not found in the database.")

    def get_wrong_count(self, user_id):
        self.cursor.execute("SELECT `wrongAnswers` FROM `user` WHERE `tguserid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"User with tguserid {user_id} not found in the database.")

    def refresh_the_stats(self, user_id):
        self.cursor.execute("UPDATE user SET `wrongAnswers` = 0, `rightAnswers` = 0 WHERE `tguserid` = ?", (user_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

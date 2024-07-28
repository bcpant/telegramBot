import sqlite3


class Db:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `usertgid` FROM `users` WHERE `usertgid` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id, user_chat_id):
        self.cursor.execute("INSERT INTO `users` (`usertgid`, `userchatid`) VALUES (?, ?)", (user_id, user_chat_id))
        return self.conn.commit()

    def add_true_survansw(self, user_id):
        self.cursor.execute("SELECT `survmodeRight` FROM `users` WHERE `usertgid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            oldValue = result[0]
            newValue = oldValue + 1
            self.cursor.execute("UPDATE `users` SET `survmodeRight` = ? WHERE `usertgid` = ?", (newValue, user_id))
            self.conn.commit()
        else:
            print(f"User with userId {user_id} not found in the database.")

    def add_wrong_surwansw(self, user_id):
        self.cursor.execute("SELECT `survModeWrong` FROM `users` WHERE `usertgid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            oldValue = result[0]
            newValue = oldValue + 1
            self.cursor.execute("UPDATE `users` SET `survModeWrong` = ? WHERE `usertgid` = ?", (newValue, user_id))
            self.conn.commit()
        else:
            print(f"User with userId {user_id} not found in the database.")

    def get_true_srvc(self, user_id):
        self.cursor.execute("SELECT `survmodeRight` FROM `users` WHERE `usertgid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"User with userId {user_id} not found in the database.")

    def get_wrong_srvc(self, user_id):
        self.cursor.execute("SELECT `survModeWrong` FROM `users` WHERE `usertgid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"User with userId {user_id} not found in the database.")

    def get_lives_mode(self, user_id):
        self.cursor.execute("SELECT `livesRecord` FROM `users` WHERE `usertgid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            print(f"User with userId {user_id} not found in the database.")

    def refresh_the_stats(self, user_id):
        self.cursor.execute("UPDATE users SET `survmodeRight` = 0, `survModeWrong` = 0, `livesRecord` = 0 WHERE `usertgid` = ?", (user_id,))
        self.conn.commit()

    def livesModeRecord(self, user_id, streakCount):
        self.cursor.execute("SELECT `livesRecord` FROM `users` WHERE `usertgid` = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            oldValue = result[0]
            if (oldValue < streakCount):
                self.cursor.execute("UPDATE `users` SET `livesRecord` = ? WHERE `usertgid` = ?", (streakCount, user_id))
                self.conn.commit()
                return True
        else:
            return False



    def close(self):
        self.conn.close()

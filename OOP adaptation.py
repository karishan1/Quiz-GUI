import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import numpy as np
import matplotlib.pyplot as plt


class LoginSystemMain(tk.Tk):  # This class holds all the frames for the login/registration system

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("GoPhysics")
        self.frames = dict()  # Dictionary holds all the frames within the login system

        container = ttk.Frame(self)  # The main container to place frames in the program
        container.grid(padx=15, pady=15, sticky="EW")

        account_frame = CreateAccount(container, self)  # Places the frame for creating an account into the container
        account_frame.grid(row=0, column=0, sticky="NSEW")

        login_frame = Login(container, self)  # Places the frame for Logging in into the container
        login_frame.grid(row=0, column=0, sticky="NSEW")

        self.frames[CreateAccount] = account_frame  # Places frame into the dictionary to allow switching between
        # frames
        self.frames[Login] = login_frame

    def show_frame(self, page_name):  # Module which allows frames in this class to be switched
        frame = self.frames[page_name]
        frame.tkraise()


class CreateAccount(ttk.Frame):  # Class which produces the registration screen

    def __init__(self, container, controller, **kwargs):  # Constructor produces all tkinter widgets for this class

        super().__init__(container, **kwargs)  # Inherits methods from the main frame

        self.u_name = tk.StringVar()  # StringVar type variables allowing variables to hold a string value from user
        # input
        self.p_word = tk.StringVar()
        self.p_word_two = tk.StringVar()

        self.heading = Label(self, text="Create new account", width=20, justify="center")  # Produces heading
        self.heading.config(font=("Arial Narrow Bold", 18), justify="center")
        self.heading.grid(column=0, row=0, padx=10, pady=10)

        self.username_label = Label(self, text="Username:")  # Produces the label to identify username entry widget
        self.username_label.config(font=("Arial Narrow", 14))
        self.username_label.grid(column=0, row=1, sticky="W", padx=10, pady=10)
        self.username_entry = Entry(self, textvariable=self.u_name)  # Produces entry widget for user input of username
        self.username_entry.grid(column=1, row=1, padx=10, pady=10, sticky="W")
        self.username_entry.config(width=35, font=("Arial Narrow", 14))

        self.password_label = Label(self, text="Password:")  # Produces the label to identify password entry widget
        self.password_label.grid(column=0, row=2, sticky="W", padx=10, pady=10)
        self.password_label.config(font=("Arial Narrow", 14))
        self.password_entry = Entry(self, show="*",
                                    textvariable=self.p_word)  # Produces entry widget for user input of password
        self.password_entry.grid(column=1, row=2, padx=10, pady=10, sticky="W")
        self.password_entry.config(width=35, font=("Arial Narrow", 14))

        self.password_label_two = Label(self,
                                        text="Re-enter Password:")  # Produces the label to identify password entry
        # widget
        self.password_label_two.grid(column=0, row=3, sticky="W", padx=10, pady=10)
        self.password_label_two.config(font=("Arial Narrow", 14))
        self.password_entry_two = Entry(self, show="*",
                                        textvariable=self.p_word_two)  # Produces entry widget for user input of
        # password to allow for double entry verification
        self.password_entry_two.config(width=35, font=("Arial Narrow", 14))
        self.password_entry_two.grid(column=1, row=3, padx=10, pady=10, sticky="W")

        self.label = Label(self, text="\n")
        self.label.grid(column=0, row=4)

        self.output_result_label = Label(self, text="",
                                         foreground="red")  # Produces label which outputs information to user
        self.output_result_label.config(font=("Arial Narrow bold", 14), justify="center")
        self.output_result_label.grid(column=0, row=5, padx=10, pady=10)

        self.submit_button = ttk.Button(self, text="Submit", command=self.new_user)  # Produces button which calls
        # new_user module to create their account
        self.submit_button.grid(column=0, row=6, sticky="W", padx=10, pady=10)

        self.switch_frame_button = ttk.Button(self, text="Login", command=lambda: controller.show_frame(
            Login))  # Produces button which uses parents method to switch frames
        self.switch_frame_button.grid(column=1, row=6, sticky="E", padx=10, pady=10)

    def new_user(self):  # Method which allows user to create new account

        u_name = self.u_name.get()  # Retrieves inputs on tkinter entry widgets
        p_word = self.p_word.get()
        p_word_two = self.p_word_two.get()

        if len(u_name) == 0 or len(p_word) == 0 or len(
                p_word_two) == 0:  # Presence check in retrieved entry values from tkinter entry widgets

            self.output_result_label.config(
                text="One or more Entry Fields Missing")  # Outputs an error message when presence check fails
        elif len(p_word) < 8:  # Performs length check on entered password
            self.output_result_label.config(
                text="Password is too short")  # Outputs an error message when length check fails
        elif p_word != p_word_two:  # ensures double entry verification check passes
            self.output_result_label.config(
                text="Passwords do not match")  # Outputs an error message if double entry verification fails

        else:  # Program goes to this path if all entry fields requirements are met
            sql = '''SELECT username FROM user
                     WHERE username = ?
                  '''
            # SQL statement returns all usernames with identical username input by user
            with sqlite3.connect("Quiz.db") as db:  # Opens database using sqlite library
                cursor = db.cursor()

            cursor.execute(sql, [u_name])
            db.commit()
            all_usernames = cursor.fetchall()  # returns values after performing SQL query

            if len(all_usernames) != 0:  # Checks whether an existing account with username input exists
                self.output_result_label.config(text="Username already exists", foreground="red")  # Outputs error
                # message if username entered exists within database
            else:

                with sqlite3.connect("Quiz.db") as db:  # Opens database using sqlite library

                    cursor = db.cursor()
                    values = (u_name, p_word)

                sql = ''' INSERT INTO user(username,password)
                          VALUES(?,?)
                      '''
                # SQL statement stores user credentials in database
                cursor.execute(sql, values)
                db.commit()

                self.output_result_label.config(text="Account Created", foreground="green")  # Outputs to user that
                # account has been created
                self.username_entry.delete(0, "end")  # Clears tkinter entry widgets
                self.password_entry.delete(0, "end")
                self.password_entry_two.delete(0, "end")


class Login(ttk.Frame):  # Class which produces the Login screen in the program

    def __init__(self, container, controller, **kwargs):  # Constructor produces all tkinter widgets for this class

        super().__init__(container, **kwargs)  # Inherits methods from the main frame

        self.u_name = tk.StringVar()  # StringVar type variables allowing variables to hold a string value from user
        # input
        self.p_word = tk.StringVar()

        self.heading = ttk.Label(self, text="Login")  # Produces heading for frame
        self.heading.config(font=("Arial Narrow Bold", 18))
        self.heading.grid(row=0, column=0, padx=10, pady=10)

        self.username_label = ttk.Label(self, text="Username:")  # Produces label which identifies the tkinter entry
        # widget for username entry
        self.username_label.config(font=("Arial Narrow", 14))
        self.username_label.grid(column=0, row=1, sticky="W", padx=10, pady=10)
        self.username_entry = ttk.Entry(self, textvariable=self.u_name)  # Produces entry widget for username entry
        self.username_entry.grid(column=0, row=2, sticky="W", padx=10, pady=10)
        self.username_entry.config(width=40, font=("Arial Narrow", 14))

        self.password_label = ttk.Label(self, text="Password:")  # Produces label which identifies the tkinter entry
        # for password entry
        self.password_label.config(font=("Arial Narrow", 14))
        self.password_label.grid(column=0, row=3, sticky="W", padx=10, pady=10)
        self.password_entry = ttk.Entry(self, show="*", textvariable=self.p_word)  # Produces entry widget for
        # password entry
        self.password_entry.grid(column=0, row=4, sticky="W", padx=10, pady=10)
        self.password_entry.config(width=40, font=("Arial Narrow", 14))

        self.output_result_label = ttk.Label(self, text="", foreground="red")  # Produces label used to output error
        # messages to user
        self.output_result_label.config(font=("Arial Narrow bold", 16), justify="center")
        self.output_result_label.grid(column=0, row=6, padx=10, pady=10)

        self.submit_button = ttk.Button(self, text="Submit", command=self.login_command)  # Produces button which
        # allows submission of entry fields
        self.submit_button.grid(column=0, row=7, sticky="W", padx=10, pady=10)

        self.switch_frame_button = ttk.Button(self, text="Create new Account",
                                              command=lambda: controller.show_frame(CreateAccount))  # Produces button
        # which uses parent's method to change frames
        self.switch_frame_button.grid(column=1, row=7, padx=10, pady=10, sticky="W")

    def login_command(self):  # Method which checks if login entries exists in the database

        with sqlite3.connect("Quiz.db") as db:  # Opens database using sqlite library
            cursor = db.cursor()

        username = self.u_name.get()  # Retrieves the inputs from tkinter widgets  for username and password
        password = self.p_word.get()

        sql = '''  SELECT * FROM user
                    WHERE username = ? AND password = ?
              '''
        # SQL statement which returns the matching username and password to user entry
        cursor.execute(sql, (username, password))
        db.commit()

        result = cursor.fetchall()  # returns values after performing SQL query

        if len(result) == 0:  # Select statement which checks if username and password entered exists
            self.output_result_label.config(text="Incorrect Username and or Password",
                                            foreground="red")  # Outputs error message

        else:
            self.output_result_label.config(text="Access Granted",
                                            foreground="Green")  # Outputs message stating login was successful
            global user_ID  # Creates global variable of user_ID
            user_ID = result[0][0]

            global menu_root  # Creates global variable of instance
            menu_root = MenuSystemMain()  # Produces instance of class which controls main menu frames
            login_root.destroy()  # Destroys login instance in turn destroying login/ registration window
            menu_root.columnconfigure(0, weight=1)
            menu_root.config(bg="#7393B3")
            menu_root.mainloop()


########################################################################################################################
########################################################################################################################
########################################################################################################################


class MenuSystemMain(tk.Tk):  # This class holds all the frames for the whole Menu system

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("GoPhysics")
        self.frames = dict()  # Dictionary holds all the frames within the login system

        container = ttk.Frame(self)  # The main container to place frames in the program
        container.grid(padx=15, pady=15, sticky="EW")

        quiz_details_frame = CreateQuizDetails(container,
                                               self)  # Places the frame for creating quiz details frame into the
        # container
        quiz_details_frame.grid(row=0, column=0, sticky="NSEW")

        choose_quiz_frame = QuizDisplay(container,
                                        self)  # Places the frame for creating quiz details frame into the container
        choose_quiz_frame.grid(row=0, column=0, sticky="NSEW")

        quiz_form_frame = CreateQuizQuestions(container, self)  # Places the frame for creating quiz questions
        # frame into the container
        quiz_form_frame.grid(row=0, column=0, sticky="NSEW")

        pass_change_frame = ChangePassword(container, self)  # Places the frame for changing password frame into the
        # container
        pass_change_frame.grid(row=0, column=0, sticky="NSEW")

        review_frame = ReviewProgress(container, self)  # Places the frame for reviewing progress frame into the
        # container
        review_frame.grid(row=0, column=0, sticky="NSEW")

        menu_frame = Menu(container, self)
        menu_frame.grid(row=0, column=0, sticky="NSEW")

        self.frames[Menu] = menu_frame  # Places frames into dictionary
        self.frames[QuizDisplay] = choose_quiz_frame
        self.frames[CreateQuizQuestions] = quiz_form_frame
        self.frames[CreateQuizDetails] = quiz_details_frame
        self.frames[ChangePassword] = pass_change_frame
        self.frames[ReviewProgress] = review_frame

    def show_frame(self, page_name):  # Module which allows frames in this class to be switched
        frame = self.frames[page_name]
        frame.tkraise()


class Menu(ttk.Frame):  # Class which produces the Menu screen

    def __init__(self, container, controller, **kwargs):  # Constructor produces all tkinter widgets for this class
        super().__init__(container, **kwargs)  # Inherits methods from the main frame

        self.quiz_button = Button(self, text="Earliest Quiz Set", font=("Arial Narrow Bold", 14), height=3,
                                  width=40,
                                  background="#32CD32", command=lambda: controller.show_frame(QuizDisplay))
        self.quiz_button.pack(expand=True)  # Button which takes user to Quiz display screen

        self.review_progress_button = Button(self, text="Review Progress", font=("Arial Narrow Bold", 14), height=3,
                                             width=40,
                                             command=lambda: controller.show_frame(ReviewProgress)
                                             , background="#EE4B2B")
        self.review_progress_button.pack(expand=True)  # Button which takes user to review progress screen

        self.create_quiz_button = Button(self, text="Create Quiz", font=("Arial Narrow Bold", 14), height=3, width=40,
                                         background="orange",
                                         command=lambda: controller.show_frame(CreateQuizDetails))
        self.create_quiz_button.pack(expand=True)  # Button which takes user to create quiz screen

        self.change_pass_button = Button(self, text="Change Password", font=("Arial Narrow Bold", 14), height=3,
                                         width=40,
                                         background="blue", command=lambda: controller.show_frame(ChangePassword))
        self.change_pass_button.pack(expand=True)  # Button which takes user to change password screen using parent
        # method

        self.exit_button = Button(self, text="Sign Out", font=("Arial Narrow", 14), height=2, width=10,
                                  background="#A9A9A9", command=self.login_page)
        self.exit_button.pack(expand=True)  # Button which sings user out of their account

    def login_page(self):  # Method which signs user out of their account
        global login_root  # Creates global variable of instance
        login_root = LoginSystemMain()  # Produces instance of class which controls login/registration frames

        menu_root.destroy()  # Destroys menu instance

        login_root.columnconfigure(0, weight=1)
        login_root.config(bg="#7393B3")

        login_root.mainloop()


class CreateQuizDetails(ttk.Frame):  # Class which produces the Create Quiz Details screen

    def __init__(self, container, controller, **kwargs):  # Constructor produces all tkinter widgets for this class
        super().__init__(container, **kwargs)  # Inherits methods from the main frame

        self.heading = Label(self, text="Create a quiz", width=20)  # Produces heading for frame
        self.heading.config(font=("Arial Narrow Bold", 18), justify="center")
        self.heading.grid(column=0, row=0, sticky="W", padx=10, pady=10)

        self.quiz_name_label = Label(self, text="Quiz name:")  # Produces label which identifies the tkinter entry
        # widget for quiz name entry
        self.quiz_name_label.config(font=("Arial Narrow", 14), justify="center")
        self.quiz_name_label.grid(column=0, row=1, padx=10, pady=10, sticky="w")
        self.quiz_name_entry = Entry(self)  # Produces entry widget for user input of quiz name
        self.quiz_name_entry.grid(column=1, row=1, padx=10, pady=10, sticky="w")
        self.quiz_name_entry.config(width=40, font=("Arial Narrow", 14))

        self.quiz_difficulty_label = Label(self, text="Difficulty:")  # Produces label which identifies the tkinter
        # entry widget for difficulty entry
        self.quiz_difficulty_label.config(font=("Arial Narrow", 14), justify="center")
        self.quiz_difficulty_label.grid(column=0, row=2, padx=10, pady=10, sticky="w")
        self.quiz_difficulty_entry = Entry(self)  # Produces entry widget for user input of quiz difficulty
        self.quiz_difficulty_entry.grid(column=1, row=2, padx=10, pady=10, sticky="W")
        self.quiz_difficulty_entry.config(width=40, font=("Arial Narrow", 14))

        self.quiz_topics_label = Label(self, text="Topics:")  # Produces label which identifies the tkinter entry
        # widget for topics entry
        self.quiz_topics_label.config(font=("Arial Narrow", 14), justify="center")
        self.quiz_topics_label.grid(column=0, row=3, padx=10, pady=10, sticky="w")
        self.quiz_topics_entry = Entry(self)  # Produces entry widget for user input of quiz topics
        self.quiz_topics_entry.grid(column=1, row=3, padx=10, pady=10, sticky="W")
        self.quiz_topics_entry.config(width=40, font=("Arial Narrow", 14))

        self.output_result_label = Label(self, text="", foreground="red")  # Produces label which allows output of
        # messages to user
        self.output_result_label.config(font=("Arial Narrow Bold", 14), justify="center")
        self.output_result_label.grid(column=0, row=5, padx=10, pady=10)

        self.submit_button = ttk.Button(self, text="Submit",
                                        command=self.quiz_name_check)  # Button which calls module quiz_name_check
        self.submit_button.grid(column=0, row=4, sticky="W", padx=10, pady=10)

        self.return_button = ttk.Button(self, text="return", command=lambda: controller.show_frame(Menu))
        self.return_button.grid(column=1, row=4, padx=10, pady=10, sticky="W")

    def quiz_name_check(self):  # Module in class which stores user entries onto database

        global quiz_name  # Quiz name is set as a global variable
        quiz_name = self.quiz_name_entry.get()  # Retrieves entry fields on tkinter widgets as variables
        quiz_difficulty = self.quiz_difficulty_entry.get()
        quiz_topics = self.quiz_topics_entry.get()

        if len(quiz_name) == 0 or len(quiz_difficulty) == 0 or len(quiz_topics) == 0:  # Performs presence check on
            # tkinter widgets
            self.output_result_label.config(text="Missing entry fields", foreground="red")  # Outputs error message
        else:  # Continues if presence check passes

            with sqlite3.connect("Quiz.db") as db:  # Opens database using sqlite library
                cursor = db.cursor()

            sql = '''
                  SELECT * from questions 
                  WHERE quizname = ?
                  '''
            # SQL statement which returns all records that have matching quiz names

            cursor.execute(sql, [quiz_name])  # Performs SQL query

            results = cursor.fetchall()  # returns values after performing SQL query

            if len(results) == 0:  # Select statement which checks whether an existing quiz name exists

                sql = '''
                         INSERT INTO quizzes(quizname,difficulty,topics)
                         VALUES(?,?,?)
                      '''
                # SQL statement which stores quiz details onto database

                values = [quiz_name, quiz_difficulty, quiz_topics]
                cursor.execute(sql, values)  # Performs SQL query
                db.commit()

                sql = '''
                         SELECT * FROM user
                      '''
                # SQL query which selects all exisiting accounts

                cursor.execute(sql)  # Performs SQL query
                number_of_users = cursor.fetchall()  # Returns value from SQL query

                for x in range(len(number_of_users)):  # Loop cycles through all userID's
                    values = [quiz_name, x + 1]

                    sql = '''
                            INSERT INTO pendingQuizzes(quizname,userID)
                            VALUES(?,?)
                            '''
                    # SQL statement which makes it so all users have created quiz as a 'pending quiz' on
                    # pendingQuizzes table

                    cursor.execute(sql, values)  # Performs SQL query

                    db.commit()

                menu_root.show_frame(CreateQuizQuestions)  # Changes frame to Create Quiz Questions frame

            else:
                self.output_result_label.config(text="Quiz already exists", foreground="red")  # Outputs error message
                # if matching quiz name is found on database


class CreateQuizQuestions(ttk.Frame):  # Class which produces the Create Quiz Questions screen

    def __init__(self, container, controller, **kwargs):  # Constructor produces all tkinter widgets for this class
        # and initial attribute values
        super().__init__(container, **kwargs)  # Inherits methods from the main frame

        self.counter = 0  # Initial value of counter set in constructor

        self.heading = Label(self, text="Create a quiz", width=20)  # Produce heading
        self.heading.config(font=("Arial Narrow", 18), justify="center")
        self.heading.grid(column=0, row=0, sticky="W", padx=10, pady=10)

        self.question_label = Label(self, text="Question:")  # Produces the label to identify question entry widget
        self.question_label.grid(column=0, row=2, sticky="W", padx=10, pady=10)
        self.question_label.config(font=("Arial Narrow", 14))
        self.question_entry = Entry(self)  # Produces entry widget for user input of question
        self.question_entry.grid(column=1, row=2, padx=10, pady=10, sticky="W")
        self.question_entry.config(width=40, font=("Arial Narrow", 14))

        self.option1_label = Label(self, text="Option 1:")  # Produces the label to identify option1 entry widget
        self.option1_label.grid(column=0, row=3, sticky="W", padx=10, pady=10)
        self.option1_label.config(font=("Arial Narrow", 14))
        self.option1_entry = Entry(self)  # Produces entry widget for user input of first option for question
        self.option1_entry.config(width=40, font=("Arial Narrow", 14))
        self.option1_entry.grid(column=1, row=3, padx=10, pady=10, sticky="W")

        self.option2_label = Label(self, text="Option 2:")  # Produces the label to identify option2 entry widget
        self.option2_label.grid(column=0, row=4, sticky="W", padx=10, pady=10)
        self.option2_label.config(font=("Arial Narrow", 14))
        self.option2_entry = Entry(self)  # Produces entry widget for user input of second option for question
        self.option2_entry.grid(column=1, row=4, padx=10, pady=10, sticky="W")
        self.option2_entry.config(width=40, font=("Arial Narrow", 14))

        self.option3_label = Label(self, text="Option 3:")  # Produces the label to identify option3 entry widget
        self.option3_label.grid(column=0, row=5, sticky="W", padx=10, pady=10)
        self.option3_label.config(font=("Arial Narrow", 14))
        self.option3_entry = Entry(self)  # Produces entry widget for user input of third option for question
        self.option3_entry.grid(column=1, row=5, padx=10, pady=10, sticky="W")
        self.option3_entry.config(width=40, font=("Arial Narrow", 14))

        self.option4_label = Label(self, text="Option 4:")  # Produces the label to identify option4 entry widget
        self.option4_label.grid(column=0, row=6, sticky="W", padx=10, pady=10)
        self.option4_label.config(font=("Arial Narrow", 14))
        self.option4_entry = Entry(self)  # Produces entry widget for user input of fourth option for question
        self.option4_entry.grid(column=1, row=6, padx=10, pady=10, sticky="W")
        self.option4_entry.config(width=40, font=("Arial Narrow", 14))

        self.answer_label = Label(self, text="Answer")  # Produces the label to identify answer entry widget
        self.answer_label.grid(column=0, row=7, sticky="W", padx=10, pady=10)
        self.answer_label.config(font=("Arial Narrow", 14))
        self.answer_entry = Entry(self)  # Produces entry widget for user input of answer for question
        self.answer_entry.grid(column=1, row=7, padx=10, pady=10, sticky="W")
        self.answer_entry.config(width=40, font=("Arial Narrow", 14))

        self.label = Label(self, text="")
        self.label.grid(column=0, row=8, rowspan=2)

        self.counter_label = Label(self, text="0 / 10", foreground="blue")  # Produces label to show values counter
        # variable to user
        self.counter_label.config(font=("Arial Narrow bold", 14), justify="center")
        self.counter_label.grid(column=0, row=10, padx=10, pady=10)

        self.output_result_label = Label(self, text="", foreground="red")  # Produces label which displays error
        # message to user
        self.output_result_label.config(font=("Arial Narrow bold", 14), justify="center")
        self.output_result_label.grid(column=0, row=11, padx=10, pady=10)

        self.submit_button = ttk.Button(self, text="Submit", command=self.quiz_creator)  # Produces button which
        # calls quiz_creator method to create quiz
        self.submit_button.grid(column=0, row=12, sticky="W", padx=10, pady=10)

        self.return_button = ttk.Button(self, text="return", command=self.switch_frame)  # Button which changes frame
        # to Menu frame
        self.return_button.grid(column=1, row=12, padx=10, pady=10, sticky="W")

    def switch_frame(self):  # Method which changes user frame
        self.counter = 0  # Counter attribute set to 0 in case user wants to create multiple quizzes in one sitting
        menu_root.show_frame(Menu)

    def quiz_creator(self):  # Method which creates quiz

        question_name = self.question_entry.get()  # Retrieves inputs on tkinter entry widgets
        option_1 = self.option1_entry.get()
        option_2 = self.option2_entry.get()
        option_3 = self.option3_entry.get()
        option_4 = self.option4_entry.get()
        answer = self.answer_entry.get()

        if len(question_name) == 0 or len(option_1) == 0 or len(option_2) == 0 or len(option_3) == 0 or len(
                option_4) == 0 or len(answer) == 0:  # Presence check in retrieved entry values from tkinter entry
            # widgets
            self.output_result_label.config(text="Entry fields missing", foreground="red")  # Outputs error message

        else:
            if self.counter > 9:  # Prevents user from creating more than 10 questions
                self.output_result_label.config(text="Maximum question number exceeded!", foreground="red")  # Outputs
                # error message
            else:

                try:

                    if int(answer) == 1 or int(answer) == 2 or int(answer) == 3 or int(answer) == 4:  # allows answer
                        # value to be only an integer between 1 and 4

                        with sqlite3.connect("Quiz.db") as db:
                            cursor = db.cursor()

                        values = [quiz_name, question_name, option_1, option_2, option_3, option_4, answer]

                        sql = '''  INSERT INTO questions(quizname,question,option1,option2,option3,option4,answer)
                                   VALUES(?,?,?,?,?,?,?)
                            '''
                        # SQL statement which updates saves question onto database
                        cursor.execute(sql, values)  # Performs SQL query
                        db.commit()
                        self.counter += 1  # Increments counter

                        self.answer_entry.delete(0, "end")  # Clears input on tkinter widgets allowing user to enter
                        # more questions easier
                        self.question_entry.delete(0, "end")
                        self.option1_entry.delete(0, "end")
                        self.option2_entry.delete(0, "end")
                        self.option3_entry.delete(0, "end")
                        self.option4_entry.delete(0, "end")

                        string = str(self.counter) + " / 10"

                        self.counter_label.config(text=string)  # Displays counter number to user
                        self.output_result_label.config(text="")  # clears output label after adding a question


                    else:

                        self.output_result_label.config(text="Wrong value for answer field", foreground="red")


                except ValueError:
                    # Value error may be caused by setting answer as an int type when user enters erroneous data; value
                    # error is accepted by program

                    self.output_result_label.config(text="Wrong value for answer field", foreground="red")


class QuizDisplay(ttk.Frame):  # Class which produces the Quiz display screen

    def __init__(self, container, controller, **kwargs):  # Constructor produces all tkinter widgets for this class
        super().__init__(container, **kwargs)  # Inherits methods from the main frame

        with sqlite3.connect("Quiz.db") as db:  # Opens database using sqlite library
            cursor = db.cursor()

        sql = ''' 
              SELECT quizname from pendingQuizzes
              WHERE userID == ?  
              '''
        # SQL statement selects pending quiz names of logged-in user

        values = [user_ID]
        cursor.execute(sql, values)  # Performs SQL query
        quiz_names = cursor.fetchall()  # Returns values after performing SQL query

        if len(quiz_names) != 0:  # Widgets produced if user has pending quizzes

            global earliest_quiz  # Sets earliest quiz name as global
            earliest_quiz = quiz_names[0][0]

            self.heading = Label(self, text="Latest Quiz", background="#cecece")  # Produce heading
            self.heading.config(font=("Arial Narrow Bold", 14), width=75, height=3)
            self.heading.grid(row=1)

            self.label = Label(self, text="")
            self.label.grid(row=2, rowspan=2)

            self.quiz_button = Button(self, text=earliest_quiz, font=("Arial Narrow", 14), height=3, width=20,
                                      background="#32CD32", command=self.quiz_description)  # Produces quiz button
            self.quiz_button.grid(column=0, row=4, padx=10, pady=10)

        else:  # Widgets produced if user does not have pending quizzes
            self.heading = Label(self, text="NO QUIZZES AVAILABLE!", background="#cecece")
            self.heading.config(font=("Arial Narrow Bold", 14), width=75, height=3)
            self.heading.grid(row=1)

            self.label = Label(self, text="")
            self.label.grid(row=2, rowspan=2)

        self.return_button = Button(self, text="return", font=("Arial Narrow", 14), height=1, width=10,
                                    background="red", command=lambda: controller.show_frame(Menu))
        self.return_button.grid(column=0, row=5, padx=10, pady=10)  # Button which transfers user back to Menu frame

    def quiz_description(self):  # Method which produces a pop-up message box containing quiz details to user

        with sqlite3.connect("Quiz.db") as db:
            cursor = db.cursor()

        sql = ''' 
                 SELECT * from quizzes 
                 WHERE quizname = ?
              '''
        # SQL statement which selects record with quiz name of selected quiz
        cursor.execute(sql, [earliest_quiz])  # Performs SQL query
        quiz_des = cursor.fetchall()  # Returns values after performing SQL query

        quiz_name = quiz_des[0][1]
        quiz_difficulty = quiz_des[0][2]
        quiz_topics = quiz_des[0][3]

        global description_root  # Sets message box instance as a global variable

        description_root = Tk()  # Declares variable as instance of Tk
        description_root.title("Quiz description")
        description_root.geometry("400x400")  # Sets size of window
        description_root.columnconfigure(0, weight=1)
        description_root.config(bg="#7393B3")

        label1 = Label(description_root, text="Quiz name : ", background="#cecece")
        label1.config(font=("Arial Narrow", 14), width=10)
        label1.grid(row=0, column=0, sticky="W", padx=10, pady=10)
        label_quiz_name = Label(description_root, text=quiz_name)  # Label to display quiz name
        label_quiz_name.config(font=("Arial Narrow", 14), width=25)
        label_quiz_name.grid(row=0, column=1, sticky="E", padx=10, pady=10)

        label2 = Label(description_root, text="Difficulty : ", background="#cecece")
        label2.config(font=("Arial Narrow", 14), width=10)
        label2.grid(row=1, column=0, sticky="W", padx=10, pady=10)
        label_difficulty = Label(description_root, text=quiz_difficulty)  # Label to display difficulty
        label_difficulty.config(font=("Arial Narrow", 14), width=25)
        label_difficulty.grid(row=1, column=1)

        label3 = Label(description_root, text="Topics : ", background="#cecece")
        label3.config(font=("Arial Narrow", 14), width=10)
        label3.grid(row=2, column=0, sticky="W", padx=10, pady=10)
        label_topics = Label(description_root, text=quiz_topics)  # Label to display topics
        label_topics.config(font=("Arial Narrow", 14), width=25)
        label_topics.grid(row=2, column=1)

        start_button = Button(description_root, text="START", font=("Arial Narrow", 14), height=1, width=15,
                              background="Green", command=self.change_frame, justify="center")  # Produce button to
        # start quiz
        start_button.grid(row=5, column=0, pady=10, padx=10, sticky="w")

        return_button = Button(description_root, text="RETURN", font=("Arial Narrow", 14), height=1, width=15,
                               background="red", command=self.close_mb, justify="center")  # Produce button to remove
        # message box by calling method in class
        return_button.grid(row=5, column=1, pady=10, padx=10, sticky="e")

    def change_frame(self):  # Method which changes frame for user to start quiz

        description_root.destroy()  # Destroy message box pop-up

        global quiz_root  # Sets instance as global
        quiz_root = QuizSystemMain()  # Produces instance of quiz system class - produces a new window

        menu_root.destroy()  # Destroys Menu window

        quiz_root.columnconfigure(0, weight=1)
        quiz_root.geometry("855x450")

        quiz_root.mainloop()

    def close_mb(self):  # Method to destroy message box

        description_root.destroy()  # Destroy message box


class ReviewProgress(ttk.Frame):  # Class to produce widgets for review progress screen

    def __init__(self, container, controller, **kwargs):  # Constructor produces all tkinter widgets for this class
        super().__init__(container, **kwargs)  # Inherits methods from the main frame

        with sqlite3.connect("Quiz.db") as db:  # Opens database using sqlite library
            cursor = db.cursor()

        sql = '''
                 SELECT * FROM scores 
                 WHERE userID = ?   
              '''
        # SQL statement which selects all scores with  matching userID
        cursor.execute(sql, [user_ID])  # Performs SQL query
        user_scores = cursor.fetchall()

        if len(user_scores) != 0:  # Widgets produced when no quizzes have been answered by user

            table_score = ttk.Treeview(self)  # Produces table of values on tkinter frame
            table_score["columns"] = ("Quiz name", "Percentage Score")  # Sets columns on table
            table_score.column("Quiz name", anchor="w", width=120)
            table_score.column("Percentage Score", anchor="center", width=120)
            table_score.grid(column=2)

            table_score.heading("Quiz name", text="Quiz name", anchor="w")
            table_score.heading("Percentage Score", text="Percentage Score", anchor="center")

            for i in range(0, len(user_scores)):  # Loop to produce scores on table
                table_score.insert(parent="", index="end", iid=i, text=" ",
                                   values=(user_scores[i][1], user_scores[i][2]))
                table_score.grid(column=3, row=1, padx=20, pady=20)

            self.graph_button = Button(self, text="Graph", command=self.produce_graph)  # Button to produce a line
            # graph using matplotlib  library
            self.graph_button.grid(column=2, row=6, padx=20, pady=20)
            self.graph_button.config(height=2, width=10, background="Green")

            self.return_button = Button(self, text="Return", command=lambda: controller.show_frame(Menu))  # Changes
            # frame to Menu frame
            self.return_button.grid(column=3, row=6, padx=20, pady=20)
            self.return_button.config(height=2, width=10, background="Red")
        else:
            self.heading = Label(self, text="NO DATA AVAILABLE", background="#cecece")  # Heading label when no data
            self.heading.config(font=("Arial Narrow Bold", 14), width=75, height=3)
            self.heading.grid(row=1)

            self.return_button = Button(self, text="Return", command=lambda: controller.show_frame(Menu))  # Changes
            # frame to Menu frame
            self.return_button.grid(column=0, row=2, padx=20, pady=20)
            self.return_button.config(height=2, width=10, background="Red")

    def produce_graph(self):  # Method which produces a graph of results from score

        with sqlite3.connect("Quiz.db") as db:  # Opens database using sqlite library
            cursor = db.cursor()

        sql = '''
                 SELECT * FROM scores
                 WHERE userID = ?
              '''
        #  SQL statement selects all record of scores with matching userID
        values = [user_ID]
        cursor.execute(sql, values)  # Performs SQL query
        results = cursor.fetchall()
        scores_list = []  # Y values list
        x_values = []  # X values list

        for x in range(0, len(results)):
            scores_list.append(results[x][2])
            x_values.append(x)

        x = np.array(x_values)  # X-axis points
        y = np.array(scores_list)  # Y-axis points

        plt.plot(x, y)  # Plot the chart
        plt.show()  # Shows chart


class ChangePassword(ttk.Frame):  # Class which produces the Change Password frame in the program

    def __init__(self, container, controller, **kwargs):  # Constructor produces all tkinter widgets for this class
        super().__init__(container, **kwargs)  # Inherits methods from the main frame

        self.heading = Label(self, text="Change Password", width=20)  # Produces Heading Label
        self.heading.config(font=("Arial Narrow Bold", 18), justify="center")
        self.heading.grid(column=0, row=0, sticky="W", padx=10, pady=10)

        self.current_pass_label = Label(self, text="Enter current password : ")  # Identifies password entry widget
        self.current_pass_label.config(font=("Arial Narrow", 14), justify="center")
        self.current_pass_label.grid(column=0, row=1, padx=10, pady=10, sticky="w")
        self.current_pass_entry = Entry(self, show="*")  # Produces entry widget for password entry
        self.current_pass_entry.grid(column=1, row=1, padx=10, pady=10, sticky="W")
        self.current_pass_entry.config(width=40, font=("Arial Narrow", 14))

        self.new_pass_label = Label(self, text="Enter new password : ")  # Identifies new password entry widget
        self.new_pass_label.config(font=("Arial Narrow", 14), justify="center")
        self.new_pass_label.grid(column=0, row=2, padx=10, pady=10, sticky="w")
        self.new_pass_entry = Entry(self, show="*")  # Produces entry widget for password entry
        self.new_pass_entry.grid(column=1, row=2, padx=10, pady=10, sticky="W")
        self.new_pass_entry.config(width=40, font=("Arial Narrow", 14))

        self.new_pass_label_two = Label(self, text="Enter new password again : ")  # Identifies password entry widget
        self.new_pass_label_two.config(font=("Arial Narrow", 14), justify="center")
        self.new_pass_label_two.grid(column=0, row=3, padx=10, pady=10, sticky="w")
        self.new_pass_entry_two = Entry(self, show="*")  # Produces entry widget for password entry
        self.new_pass_entry_two.grid(column=1, row=3, padx=10, pady=10, sticky="W")
        self.new_pass_entry_two.config(width=40, font=("Arial Narrow", 14))

        self.output_label = Label(self, text="")  # Label to output errors
        self.output_label.config(font=("Arial Narrow", 14), justify="center")
        self.output_label.grid(column=0, row=4, padx=10, pady=10)

        self.submit_button = ttk.Button(self, text="Submit", command=self.password_changer)  # Button which calls module
        self.submit_button.grid(column=0, row=5, sticky="W", padx=10, pady=10)

        self.return_button = ttk.Button(self, text="return", command=lambda: controller.show_frame(Menu))  # Button
        # which changes frame to Menu frame
        self.return_button.grid(column=1, row=5, padx=10, pady=10, sticky="W")

    def password_changer(self):  # Module which allows user to change password

        current_pass_guess = self.current_pass_entry.get()  # Retrieves entry widget inputs
        new_pass = self.new_pass_entry.get()
        new_pass_two = self.new_pass_entry_two.get()

        with sqlite3.connect("Quiz.db") as db:
            cursor = db.cursor()

        sql = ''' 
              SELECT password from user WHERE userID == ?  
              '''
        #  SQL statement which selects current password from user

        cursor.execute(sql, [user_ID])  # Runs SQL statement

        results = cursor.fetchall()  # Returns values from SQL query
        actual_pass = results[0][0]

        if str(actual_pass) == str(current_pass_guess):  # Checks if new password entered is the same as current
            if len(new_pass) >= 8:  # Checks if length password is greater than 8 characters
                if new_pass == new_pass_two:  # Checks if double entry verification is correct

                    sql = '''
                          UPDATE user
                          SET password = ?
                          WHERE userID = ?
                          '''
                    #  SQL statement which updates user password after requirements are fulfilled

                    cursor.execute(sql, [new_pass, user_ID])  # Runs SQL query
                    db.commit()

                    self.new_pass_entry.delete(0, "end")  # Removes entry widget inputs
                    self.new_pass_entry_two.delete(0, "end")
                    self.current_pass_entry.delete(0, "end")

                    self.output_label.config(text="Password Change Successful!", foreground="Green")  # Outputs to
                    # user when password change is successful

                else:
                    self.output_label.config(text="Passwords do not match", foreground="red")  # Error message
            else:
                self.output_label.config(text="Password not long enough", foreground="red")  # Error message

        else:
            self.output_label.config(text="Password Incorrect", foreground="red")  # Error message


########################################################################################################################
########################################################################################################################
########################################################################################################################


class QuizSystemMain(tk.Tk):  # This class holds all the frames for the Quiz system

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("GoPhysics")
        self.frames = dict()  # Dictionary holds all the frames within the login system

        container = ttk.Frame(self)  # The main container to place frames in the program
        container.grid(padx=1000, pady=1000, sticky="EW")

        quiz_frame = Quiz(self)  # Places the frame for quiz into the container
        quiz_frame.grid(row=0, column=0, sticky="NSEW")

        self.frames[Quiz] = quiz_frame  # Places frame into the dictionary to allow switching between

    def show_frame(self, page_name):  # Module which allows frames in this class to be switched
        frame = self.frames[page_name]
        frame.tkraise()


class Quiz(ttk.Frame):  # Class which produces the Quiz screen

    def __init__(self, controller, **kwargs):  # Runs the methods of the class to produce widgets and cycle through
        # questions
        super().__init__(**kwargs)

        with sqlite3.connect("Quiz.db") as db:  # Opens database using sqlite library
            cursor = db.cursor()

        sql = '''
                 SELECT * FROM questions
                 WHERE quizname = ?
              '''
        #  SQL statement selects all records from questions where the quiz name is the quiz name selected by user

        cursor.execute(sql, [earliest_quiz])  # Runs SQL query
        results = cursor.fetchall()  # Returns SQL query
        self.question = []  # Empty Lists
        self.options = []
        self.answer = []

        for x in range(0, len(results)):  # Appends items to list
            ques = [results[x][1]]  # Produces list containing all questions on database
            self.question.append(ques)

            opt = [results[x][2], results[x][3], results[x][4], results[x][5]]
            self.options.append(opt)  # Produces list containing all options on database

            ans = [results[x][6]]
            self.answer.append(ans)  # Produces list containing all answers on database

        self.qno = 0  # Sets initial value of question number
        self.disp_title()  # Runs disp_title method
        self.disp_ques()  # Runs disp_ques method
        self.opt_sel = IntVar()  # Declares variable as IntVar
        self.opts = self.radio_buttons()  # Runs radio_buttons method as variable opts
        self.disp_opt()  # Runs disp_opt method
        self.buttons()  # Runs buttons method
        self.total_size = len(self.question)  # Sets total question number as total_size
        self.correct = 0  # Sets initial value of correct attribute

    def disp_res(self):  # Method which displays score at end of quiz

        wrong_count = self.total_size - self.correct  # number of wrong answers stores
        correct = f"Correct: {self.correct}"  # number of correct answers displayed
        wrong = f"Wrong: {wrong_count}"  # number of wrong answers displayed

        score = int(self.correct / self.total_size * 100)  # Score stored as a percentage
        result = f"Score: {score}%"  # Displays the score

        mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")

        with sqlite3.connect("Quiz.db") as db:
            cursor = db.cursor()

        sql = '''
                 INSERT INTO scores(userID,quizname,score)
                 VALUES(?,?,?)
                 
              '''
        # SQL statement which updates score table based on what user got
        values = [user_ID, earliest_quiz, score]
        cursor.execute(sql, values)  # Performs SQL statement
        db.commit()

        values = [user_ID, earliest_quiz]

        sql = '''
              DELETE FROM PendingQuizzes
              WHERE userID == ? and quizname = ?
              '''
        # SQL statement which removes record from Pending Quiz table of the quiz answered by logged in user's account
        cursor.execute(sql, values)
        db.commit()

    def check_ans(self, qno):  # Method to check whether answer selected is correct

        if int(self.opt_sel.get()) == int(self.answer[qno][0]):
            return True

    def next_btn(self):  # Method which called other methods to change question after user clicks next btn

        if self.check_ans(self.qno):
            self.correct += 1

        self.qno += 1

        if self.qno == self.total_size:
            self.disp_res()
        else:
            self.disp_ques()
            self.disp_opt()

    def buttons(self):  # Method which produces the buttons

        next_button = Button(self, text="Next", command=self.next_btn, width=10, bg="#F2780C", fg="white",
                             font=("ariel", 16, "bold"))

        next_button.place(x=350, y=380)

        quit_button = Button(self, text="Quit", width=5, bg="black", fg="white", font=("ariel", 16, " bold"),
                             command=self.quit_btn)  # Allows user to quit quiz
        quit_button.config(font=("Arial Narrow", 12))

        quit_button.place(x=800, y=50)

        eqn_sheet_btn = Button(self, text="Equation sheet", width=15, bg="Purple", fg="white",
                               font=("ariel", 16, " bold"),
                               command=self.eqn_sheet_btn)
        eqn_sheet_btn.config(font=("Arial Narrow", 12))

        eqn_sheet_btn.place(x=600, y=50)

    def quit_btn(self):  # Method which allows user to quit quiz

        global menu_root
        menu_root = MenuSystemMain()

        quiz_root.destroy()

        menu_root.columnconfigure(0, weight=1)
        menu_root.config(bg="#7393B3")

        menu_root.mainloop()

    def eqn_sheet_btn(self):  # Method which produces an equation sheet pop up to user

        global description_root

        description_root = Tk()
        description_root.title("Physics Formulas")
        description_root.geometry("600x750")
        description_root.columnconfigure(0, weight=1)
        description_root.config(bg="#7393B3")

        heading = Label(description_root, text="Physics constants", width=100)
        heading.config(font=("Arial Narrow Bold", 18), justify="center")
        heading.grid(row=0, column=0, sticky="W", padx=10, pady=10)

        label1 = Label(description_root, text="acceleration of free fall  -  g  -  9.81ms–2", background="#cecece")
        label1.config(font=("Arial Narrow", 14))
        label1.grid(row=1, column=0, sticky="W", padx=10, pady=10)

        label2 = Label(description_root, text="elementary charge  -  e  -  1.60 × 10–19C", background="#cecece")
        label2.config(font=("Arial Narrow", 14))
        label2.grid(row=2, column=0, sticky="W", padx=10, pady=10)

        label3 = Label(description_root, text="speed of light in a vacuum  -  c  -  3.00 × 108ms–1",
                       background="#cecece")
        label3.config(font=("Arial Narrow", 14))
        label3.grid(row=3, column=0, sticky="W", padx=10, pady=10)

        label4 = Label(description_root, text="Planck constant  -  h  -  6.63 × 10–34 Js", background="#cecece")
        label4.config(font=("Arial Narrow", 14))
        label4.grid(row=4, column=0, sticky="W", padx=10, pady=10)

        label5 = Label(description_root, text="Avogadro constant  -  NA  -  6.02 × 1023mol–1", background="#cecece")
        label5.config(font=("Arial Narrow", 14))
        label5.grid(row=5, column=0, sticky="W", padx=10, pady=10)

        label6 = Label(description_root, text="molar gas constant  -  R  -  8.31Jmol–1K–1", background="#cecece")
        label6.config(font=("Arial Narrow", 14))
        label6.grid(row=6, column=0, sticky="W", padx=10, pady=10)

        label7 = Label(description_root, text="Boltzmann constant  -  k  -  1.38 × 10–23 JK–1", background="#cecece")
        label7.config(font=("Arial Narrow", 14))
        label7.grid(row=7, column=0, sticky="W", padx=10, pady=10)

        label8 = Label(description_root, text="gravitational constant  -  G  -  6.67 × 10–11Nm2 kg–2",
                       background="#cecece")
        label8.config(font=("Arial Narrow", 14))
        label8.grid(row=8, column=0, sticky="W", padx=10, pady=10)

        label9 = Label(description_root, text="permittivity of free space  -  ε0  -  8.85 × 10–12C2N–1m–2 (Fm–1)",
                       background="#cecece")
        label9.config(font=("Arial Narrow", 14))
        label9.grid(row=9, column=0, sticky="W", padx=10, pady=10)

        label10 = Label(description_root, text="electron rest mass  -  me  -  9.11 × 10–31 kg", background="#cecece")
        label10.config(font=("Arial Narrow", 14))
        label10.grid(row=10, column=0, sticky="W", padx=10, pady=10)

        label11 = Label(description_root, text="proton rest mass  -  mp  -  1.673 × 10–27 kg", background="#cecece")
        label11.config(font=("Arial Narrow", 14))
        label11.grid(row=11, column=0, sticky="W", padx=10, pady=10)

        label12 = Label(description_root, text="neutron rest mass  -  mn  -  1.675 × 10–27 kg", background="#cecece")
        label12.config(font=("Arial Narrow", 14))
        label12.grid(row=12, column=0, sticky="W", padx=10, pady=10)

        label13 = Label(description_root, text="alpha particle rest mass  -  mα  -  6.646 × 10–27 kg",
                        background="#cecece")
        label13.config(font=("Arial Narrow", 14))
        label13.grid(row=13, column=0, sticky="W", padx=10, pady=10)

        label14 = Label(description_root, text="Stefan constant  -  σ  -  5.67 × 10–8Wm–2K–4", background="#cecece")
        label14.config(font=("Arial Narrow", 14))
        label14.grid(row=14, column=0, sticky="W", padx=10, pady=10)

    def disp_opt(self):  # Method to produce options to user
        val = 0
        self.opt_sel.set(0)

        for option in self.options[self.qno]:
            self.opts[val]['text'] = option
            val += 1

    def disp_ques(self):  # Method to display question to user

        question = str(self.question[self.qno])  # uses question number to cycle through list
        question = question[:-2]
        question = question[2:]
        question = str(self.qno + 1) + ". " + str(question)

        qno = Label(self, text=question, width=60, font=('ariel', 16, 'bold'), anchor='w',
                    wraplength=700, justify='center')

        qno.place(x=70, y=100)  # places widget on user screen

    def disp_title(self):  # Displays title of quiz to user

        title = Label(self, text=earliest_quiz, width=50, bg="#7393B3", fg="white", font=("ariel", 20, "bold"))

        title.place(x=0, y=2)

    def radio_buttons(self):  # Displays the radio buttons to user

        q_list = []

        y_pos = 150

        while len(q_list) < 4:  # 4 radiobuttons are produced
            radio_btn = Radiobutton(self, text=" ", variable=self.opt_sel, value=len(q_list) + 1, font=("ariel", 14))
            q_list.append(radio_btn)  # Radio buttons stored in list

            radio_btn.place(x=100, y=y_pos)

            y_pos += 40

        return q_list  # Returns the list of radio buttons


login_root = LoginSystemMain()  # Instance of Login system class to open login system

login_root.columnconfigure(0, weight=1)
login_root.config(bg="#7393B3")

login_root.mainloop()

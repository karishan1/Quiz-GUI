import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import numpy as np
import matplotlib.pyplot as plt



class MenuSystemMain(tk.Tk):  # This class holds all the frames for the whole Menu system

    def __init__(self,user_num):
        super().__init__()
        global user_ID
        user_ID = user_num


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

        self.destroy()  # Destroys menu instance

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

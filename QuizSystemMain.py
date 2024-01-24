import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import numpy as np
import matplotlib.pyplot as plt


from LoginSystemMain import LoginSystemMain


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
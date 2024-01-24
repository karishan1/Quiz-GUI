import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

import numpy as np
import matplotlib.pyplot as plt

from MenuSystemMain import MenuSystemMain


class LoginSystemMain(tk.Tk):  # This class holds all the frames for the login/registration system

    def __init__(self):
        super().__init__()

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
            menu_root = MenuSystemMain(user_ID)  # Produces instance of class which controls main menu frames
            self.destroy() # Destroys login instance in turn destroying login/ registration window
            menu_root.columnconfigure(0, weight=1)
            menu_root.config(bg="#7393B3")
            menu_root.mainloop()



login_root = LoginSystemMain()  # Instance of Login system class to open login system

login_root.columnconfigure(0, weight=1)
login_root.config(bg="#7393B3")

login_root.mainloop()

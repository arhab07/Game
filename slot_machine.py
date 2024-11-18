import tkinter as tk
import re
from tkinter import Button, Entry, IntVar, Label, messagebox, simpledialog
import slot_funtion as slot
import sqlite3

class SlotMachineApp:
    def __init__(self, app):
        self.root = app
        self.root.title("Slot Machine Game")
        self.root.geometry("700x700")
        self.balance = 0
        self.total_bet = 0
        self.balance_var = IntVar()
        self.payout = 0
        self.initial_balance = 0
        self.player_name = self.ask_for_name()  
        self.conn = sqlite3.connect("slot_machine.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        
        self.dashboard_window = None 
        
        if self.player_name:  
            self.intromessage()
            self.enter_balance()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS player_data
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                initial_balance INTEGER,
                                total_bet INTEGER,
                                amount_won INTEGER)''')
        self.conn.commit()
    def insert_player_data(self, name, initial_balance, total_bet, amount_won):
        self.cursor.execute('''INSERT INTO player_data (name, initial_balance, total_bet, amount_won)
                            VALUES (?, ?, ?, ?)''', (name, initial_balance, total_bet, amount_won))
        self.conn.commit()
   


    def ask_for_name(self):
        name = None
        while not name:  
            name = simpledialog.askstring("Player Name", "Please enter your name:")
            if name is None:  
                messagebox.showinfo("Goodbye", "You cancelled the game. Exiting...")
                self.root.destroy()  
                return None
            elif not name.strip():  
                messagebox.showwarning("Invalid Input", "Name cannot be empty. Please enter your name.")
                name = None  
            elif not re.match("^[A-Za-z ]+$", name):  
                messagebox.showwarning("Invalid Input", "Name can only contain alphabets and spaces. No numbers or special symbols are allowed.")
                name = None  
            else:
                return name.upper() 

    def display_intro_message(self, parent_widget):
        bothDesign = "✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨"

        welcome_message = f"🎉✨ Welcome to the Heart Game, {self.player_name}! ✨🎉\n" \
                  f"Your adventure begins now! 🏆\n" \
                  f"Are you ready to spin for love and luck? 🍀❤️"

        desgin_top = Label(parent_widget, text=bothDesign, font=("arial", 20, "bold"))
        desgin_bottom = Label(parent_widget, text=bothDesign, font=("arial", 20, "bold"))
        welcome = Label(parent_widget, text=welcome_message, font=("arial", 20, "bold"))
        desgin_top.pack()
        welcome.pack()
        desgin_bottom.pack()
        if parent_widget == self.root:
            dashboard_button = Button(parent_widget, text="View Dashboard", command=self.open_dashboard, font=("arial", 14), bg="lightgreen")
            dashboard_button.place(x=400, y=280)

    def open_dashboard(self):
        if self.dashboard_window and self.dashboard_window.winfo_exists():
            self.dashboard_window.focus_set() 
            return
        self.dashboard_window = tk.Toplevel(self.root)
        self.dashboard_window.title("Player Dashboard")
        self.dashboard_window.geometry("500x500")
        dashboard_label = Label(self.dashboard_window, text="Player Dashboard", font=("arial", 16, "bold"))
        dashboard_label.pack(pady=20)
        self.cursor.execute("SELECT * FROM player_data")
        players_data = self.cursor.fetchall()
        if players_data:
            for  player in players_data:
                player_info = f"{player[0]}.  {player[1]} |  Total Bet: {player[3]}₹ |  Amount Won: {player[4]}₹ |  initial Amount: {player[2]} "
                player_label = Label(self.dashboard_window, text=player_info, font=("arial", 12))
                player_label.pack(pady=5)
        else:
            no_data_label = Label(self.dashboard_window, text="No player data available.", font=("arial", 12))
            no_data_label.pack(pady=20)


    def intromessage(self):
        self.display_intro_message(self.root)
        
    def enter_balance(self):
        self.balance_label = Label(self.root, text="Please enter the amount you have to bet: ", font=("arial", 14))
        self.balance_label.place(x=20, y=230)
        self.balance_entry = Entry(self.root, textvariable="", font=("arial", 14))
        self.balance_entry.place(x=350, y=230)
        self.submit_button = Button(self.root, text="Submit", command=self.get_balance, font=("arial", 14), bg="lightblue")
        self.submit_button.place(x=300, y=280)

    def get_balance(self):
        try:
            balance = int(self.balance_entry.get())  
            if balance >= 100:
                self.balance = balance
                self.initial_balance = balance  
                print(f"Initial Balance: {self.initial_balance}₹")  
                self.setup_gui() 
            else:
                messagebox.showerror("Error", "Please enter a valid amount greater than 0 and at least 100₹.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer amount.")
    def setup_gui(self):
        if hasattr(self, 'game_window') and self.game_window.winfo_exists():
            self.game_window.focus_set()
            return
        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Slot Machine Game")
        self.game_window.geometry("700x700")
        self.display_intro_message(self.game_window)
        self.quit_button = tk.Button(self.game_window, text="Quit Game", command=self.end_game, font=("arial", 14), bg="#000000")
        self.quit_button.pack(side="bottom", fill="x", pady=40)
        self.bet_label = tk.Label(self.game_window, text="Enter amount to bet:", font=("arial", 14))
        self.bet_label.place(x=20, y=230)
        self.bet_entry = tk.Entry(self.game_window, font=("arial", 14))
        self.slot_output = tk.Label(self.game_window, text="", font=("arial", 16))
        self.slot_output.place(x=300, y=350)
        self.bet_entry.place(x=350, y=230)
        self.bet_button = tk.Button(self.game_window, text="Spin", command=self.spin_slot, font=("arial", 14), bg="red")
        self.bet_button.place(x=300, y=280)

        self.balance_display = tk.Label(self.game_window, text=f"Your current balance: {self.balance}₹", font=("arial", 14))
        self.balance_display.place(x=250, y=400)

    def spin_slot(self):
        bet = self.bet_entry.get()
        if not bet.isdigit() or int(bet) <= 0:
            messagebox.showerror("Error", "Please enter a valid bet greater than 0.")
            return
        bet = int(bet)
        if bet > self.balance:
            messagebox.showerror("Error", "Insufficient balance.")
            return
        self.balance -= bet
        self.total_bet += bet
        row = slot.spin_row()
        single_row = slot.print_row(row)
        self.slot_output.config(text=single_row)
        self.payout = slot.get_payout(row, bet)
        if self.payout > 0:
            messagebox.showinfo("You Won!", f"You have won {self.payout}₹. \n \n   {single_row}")
        else:
            messagebox.showinfo("You Lost", f"You lost a total of {self.total_bet}₹. \n \n {single_row}")
        self.balance += self.payout
        self.update_balance_display()
        if self.balance < 10:
            self.ask_to_add_more_balance()

    def update_balance_display(self):
        self.balance_display.config(text=f"Your current balance: {self.balance}₹")

    def ask_to_add_more_balance(self):
        res = messagebox.askyesno("Low Balance", "Your balance is below 100₹. Do you want to add more?")
        if res:
            additional_amount = simpledialog.askinteger("Add Balance", "Enter amount to add:")
            if additional_amount and additional_amount > 0:
                self.balance += additional_amount
                self.initial_balance += additional_amount
                self.update_balance_display()
            else:
                messagebox.showerror("Error", "Please enter a valid amount.")
        else:
            self.end_game()

    def end_game(self):
        response = messagebox.askyesno("Quit Game", "Are you sure you want to quit?")
        if response:
            messagebox.showinfo("Game Over", f"Thank you for playing, {self.player_name}! Your remaining balance is {self.balance}₹. Amount you have betted {self.total_bet}₹. You won {self.payout}₹!")
            self.insert_player_data(self.player_name, self.initial_balance, self.total_bet, self.payout)  
            self.conn.close()  
            self.root.quit()
        else:
            if hasattr(self, 'game_window') and self.game_window.winfo_exists():
                self.game_window.focus_set() 


root = tk.Tk()
app = SlotMachineApp(root)
root.mainloop()

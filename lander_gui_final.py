import tkinter as tk
import keyboard
import pyodbc
import update_values

# SQL Connection
SERVER = '10.26.1.101'
DATABASE = 'STDB01'
USER = 'stavani001'
PWD = 'OIJ29r8e3f48$38d'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PWD};'
connection = pyodbc.connect(connection_string)
connection.autocommit = True
cursor = connection.cursor()
SQL_QUERY = f"delete from flightData"  # initially clears the table in the database
cursor.execute(SQL_QUERY)

# Pushing first display values to the DB and GUI
update_values.pushValues(0, 0, 0, 0, 0)


# Function to select a trial
def select_trial():
    trial_number = trial_var.get()
    if trial_number == 1:
        trial_1()
    elif trial_number == 2:
        trial_2()
    elif trial_number == 3:
        trial_3()


def trial_1():
    update_values.pushValues(1000, 6000, 12000, 0, 0)


def trial_2():
    update_values.pushValues(1000, 6000, 18000, 0, 0)


def trial_3():
    update_values.pushValues(1000, 6000, 20000, 0, 0)


# Prints start values
values = update_values.fetchValues()
print("Intitial values: ")
print(*values, sep='\t')
hasCrashed = False


# Main application Loop for updating the GUI and running the math
def run_gui():
    global hasCrashed
    if keyboard.is_pressed('w'):
        update_values.updateValuesThrusters()
        canvas.itemconfig(ship_id, image=thrust_image)
    else:
        update_values.updateValuesNormal()
        canvas.itemconfig(ship_id, image=ship)

    altitude = update_values.fetchValues()[0]
    fuel = update_values.fetchValues()[1]
    velocity = update_values.fetchValues()[3]
    time = str(update_values.fetchValues()[4])
    weight = update_values.fetchValues()[2]

    altitude_label.config(text="Altitude: {:.2f} m".format(altitude))
    fuel_label.config(text="Fuel remaining: {} kg".format(fuel))
    velocity_label.config(text="Velocity: {:.2f} m/s".format(velocity))
    time_label.config(text="Time: {} s".format(time))
    weight_label.config(text="Total Weight: {:.2f} kg".format(weight))

    if altitude > 0:
        screen_height = 780
        ship_y = screen_height - ((altitude / 1100) * screen_height)
        canvas.coords(ship_id, 400, ship_y)

    if altitude <= 0:
        if velocity > 5:
            hasCrashed = True
            canvas.itemconfig(ship_id, image=explo_image)
            print("You died :(")
        else:
            canvas.itemconfig(ship_id, image=complete_image)
            print("You completed the landing!")

    root.after(500, run_gui) if altitude > 0 else None


root = tk.Tk()
root.title("Crater: Lego Ship ")

canvas = tk.Canvas(root, width=800, height=800)
canvas.pack()

try:
    background_image = tk.PhotoImage(file="background.png")
    background_image_id = canvas.create_image(400, 400, image=background_image)
except tk.TclError as e:
    print(f"Error loading background image! Needs to be same location as file.")

explo_image = tk.PhotoImage(file="explosion.png")
thrust_image = tk.PhotoImage(file="thrusters.png")
complete_image = tk.PhotoImage(file="ship_1.png")
ship = tk.PhotoImage(file="ship.png")
ship_id = canvas.create_image(400, 70, image=ship)
canvas.tag_raise(ship_id)

font_size = 11

altitude_label = tk.Label(root, text="Altitude: {:.2f} m".format(update_values.fetchValues()[0]),
                          font=("Helvetica", font_size))
altitude_label.place(x=0, y=60)

fuel_label = tk.Label(root, text="Fuel Remaining: {} kg".format(update_values.fetchValues()[1]),
                      font=("Helvetica", font_size))
fuel_label.place(x=0, y=80)

velocity_label = tk.Label(root, text="Velocity: {:.2f} m/s".format(update_values.fetchValues()[3]),
                          font=("Helvetica", font_size))
velocity_label.place(x=0, y=100)

time_label = tk.Label(root, text="Time: {} s".format(update_values.fetchValues()[4]),
                      font=("Helvetica", font_size))
time_label.place(x=0, y=120)

weight_label = tk.Label(root, text="Total Weight: {} s".format(update_values.fetchValues()[2]),
                        font=("Helvetica", font_size))
weight_label.place(x=0, y=140)

start_button = tk.Button(root, text="Start Simulation!", command=run_gui)
start_button.place(x=0, y=165)

button = tk.Button(root, text="Thrusters Engaged!", width=27, height=3)
button.place(x=0, y=190)


def check_key_press():
    if keyboard.is_pressed('w'):
        button.config(bg='green')
    else:
        button.config(bg='yellow')
    root.after(10, check_key_press)


def about():
    about_window = tk.Toplevel(root)
    about_window.title("About!")
    about_window.geometry("250x150")
    about_window.resizable(False, False)
    about_text = "Team Crater Lego Ship Lander!\nCreated By:\n Michael Arend (Front End)\n David Born (Programmer)\n Sam Tavani (Back End)\n Daniel Randall (Programmer)\nLibraries Used: Tkinter and Pyodbc"
    about_label = tk.Label(about_window, text=about_text, padx=10, pady=10, font=("Helvetica", 10))
    about_label.pack()


def exit_app():
    root.destroy()


menu_bar = tk.Menu(root)

about_menu = tk.Menu(menu_bar, tearoff=0)
about_menu.add_command(label="Trial 1: Lightest Weight, Instruments Only!", command=trial_1)
about_menu.add_command(label="Trial 2: Medium Weight, Instruments & Astronaut!", command=trial_2)
about_menu.add_command(label="Trial 3: Heaviest Weight, Instruments, Astronaut, and Rover!", command=trial_3)
about_menu.add_separator()
about_menu.add_command(label="About", command=about)
about_menu.add_command(label="Exit", command=exit_app)

menu_bar.add_cascade(label="Menu", menu=about_menu)

trialmenu = tk.Menu(menu_bar, tearoff=0)

trial_menu = tk.Menu(trialmenu, tearoff=0)
trial_menu.add_command(label="Trial 1", command=trial_1)
trial_menu.add_command(label="Trial 2", command=trial_2)
trial_menu.add_command(label="Trial 3", command=trial_3)
trial_menu.add_cascade(label="Trials", menu=trial_menu)

trial_var = tk.IntVar()
trial_var.set(1)
root.config(menu=menu_bar)
check_key_press()
root.mainloop()
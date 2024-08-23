import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont


# Function to perform calculations
def calculate():
    try:
        # Retrieve values from the input fields
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = operation_var.get()

        # Perform the calculation based on the selected operation
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                raise ValueError("Cannot divide by zero.")
            result = num1 / num2
        else:
            raise ValueError("Invalid operation selected.")

        # Display the result
        label_result.config(text=f"Result: {result:.2f}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


# Create the main window
root = tk.Tk()
root.title("Advanced Calculator")

# Define custom fonts
title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
button_font = tkfont.Font(family="Helvetica", size=12)

# Set a background color for the window
root.configure(bg="#f0f0f0")

# Create and place the widgets
tk.Label(root, text="Advanced Calculator", font=title_font, bg="#f0f0f0").grid(row=0, column=0, columnspan=4, padx=20,
                                                                               pady=10)

tk.Label(root, text="Number 1:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_num1 = tk.Entry(root, width=15, font=button_font)
entry_num1.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Number 2:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_num2 = tk.Entry(root, width=15, font=button_font)
entry_num2.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Operation:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky="e")

operation_var = tk.StringVar(value='+')
operations = ['+', '-', '*', '/']
for i, op in enumerate(operations):
    tk.Radiobutton(root, text=op, variable=operation_var, value=op, font=button_font, bg="#f0f0f0").grid(row=3,
                                                                                                         column=1 + i,
                                                                                                         padx=5, pady=5)

tk.Button(root, text="Calculate", command=calculate, font=button_font, bg="#4CAF50", fg="white", relief="raised",
          width=20).grid(row=4, column=0, columnspan=4, pady=20)

label_result = tk.Label(root, text="Result: ", font=button_font, bg="#f0f0f0")
label_result.grid(row=5, column=0, columnspan=4, pady=10)

# Set window size and position
root.geometry("500x350")

# Run the application
root.mainloop()



import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import csv

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    else:
        return "Overweight"

def save_data(weight, height, bmi, category):
    with open("bmi_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([weight, height, bmi, category])

def visualize_data():
    bmi_data = []
    with open("bmi_data.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            bmi_data.append(float(row[2]))

    plt.plot(bmi_data)
    plt.xlabel("Entry Number")
    plt.ylabel("BMI")
    plt.title("BMI Trend")
    plt.show()

def main():
    root = tk.Tk()
    root.title("BMI Calculator")

    # Create input fields
    weight_label = tk.Label(root, text="Weight (kg):")
    weight_label.pack()
    weight_entry = tk.Entry(root)
    weight_entry.pack()

    height_label = tk.Label(root, text="Height (m):")
    height_label.pack()
    height_entry = tk.Entry(root)
    height_entry.pack()

    # Create calculate button
    calculate_button = tk.Button(root, text="Calculate BMI", command=lambda: calculate_bmi_callback())
    calculate_button.pack()

    # Create result display
    result_label = tk.Label(root, text="")
    result_label.pack()

    # Create visualize button
    visualize_button = tk.Button(root, text="Visualize BMI Trend", command=visualize_data)
    visualize_button.pack()

    def calculate_bmi_callback():
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Invalid input", "Please enter positive values.")
            return

        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)

        result_label.config(text=f"Your BMI is: {bmi:.2f}\nYour category is: {category}")
        save_data(weight, height, bmi, category)

    root.mainloop()

if __name__ == "__main__":
    main()
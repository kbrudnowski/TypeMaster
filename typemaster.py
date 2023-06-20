import tkinter as tk
import tkinter.messagebox as messagebox
import time
import random
import csv


""" Functions """

# Center the window on the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# Load the high score from file
def load_high_score():
    global high_score
    try:
        with open("high_score.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            high_score = float(next(reader)[0])

    except FileNotFoundError:
        high_score = 0.0

    high_score_label.config(text="High Score: {:.2f}".format(high_score))


# Start the timer
def start_timer():
    global start_time
    start_time = time.time()
    input_text.focus()


# Show message at the start of app
def show_start_message():
    load_high_score()
    messagebox.showinfo(
        "Let's begin",
        "Click OK whenever you are ready and start typing.\nPress Enter or click 'Done!' to stop the timer when you finish.",
    )
    start_timer()


# Stop the timer and show mismatches, disable buttons and display result
def stop_timer(event=None):
    global start_time, high_score
    if start_time > 0:
        end_time = time.time()
        elapsed_time = end_time - start_time
        user_input = input_text.get("1.0", tk.END).strip()
        input_words = user_input.split()
        sample_words = sample_text.split()

        input_text.tag_remove("mismatch", "1.0", tk.END)

        for i, word in enumerate(input_words):
            if i < len(sample_words):
                sample_word = sample_words[i]
                if word != sample_word:
                    start_index = input_text.search(word, "1.0", tk.END)
                    end_index = f"{start_index}+{len(word)}c"
                    input_text.tag_add("mismatch", start_index, end_index)

        input_text.tag_config("mismatch", background="red", foreground="white")

        wpm = calculate_wpm(user_input, elapsed_time)
        
        if wpm > high_score:
            high_score = wpm
            save_high_score()
            high_score_label.config(text="High Score: {:.2f}".format(high_score))
        
        done_button.config(state="disabled")
        window.unbind("<KeyRelease-Return>")

        display_result(wpm)


# Calculate the result
def calculate_wpm(user_input, elapsed_time):
    # Remove leading/trailing whitespaces and split the input into words
    words = user_input.strip().split()
    num_words = len(words)

    wpm = (num_words / elapsed_time) * 60

    return wpm


# Save the current high score to the file
def save_high_score():
    with open("high_score.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["High Score"])
        writer.writerow([high_score])


# Show the result on screen
def display_result(wpm):
    result = f"Words per minute: {wpm:.2f}"
    messagebox.showinfo("Result", result)


# Load new text-sample and refresh buttons
def next_text():
    global sample_text

    # Reset the input text
    input_text.delete("1.0", tk.END)
    
    # Generate a new random sample text
    sample_text = random.choice(samples)
    sample_label.config(text=sample_text, wraplength=400)

    # Reset the buttons and start time
    start_timer()
    done_button.config(state="normal")
    window.bind("<KeyRelease-Return>", stop_timer)


# Get samples of text from the file
samples = []
with open("samples.txt", "r") as file:
    for line in file:
        if '"' in line:
            samples.append(line.replace('"', "").strip())

# Variables
sample_text = random.choice(samples)
high_score = 0.0
start_time = 0

# Window
window = tk.Tk()
window.title("Expand Typing Skills")
window.geometry("500x550")
center_window(window)

# Labels
high_score_label = tk.Label(window, text="High Score: {:.2f}".format(high_score), font=("Arial", 12))
high_score_label.pack(side="bottom", anchor="center", pady=10)

sample_label = tk.Label(window, text=sample_text, wraplength=400, font=("Arial", 12))
sample_label.pack(pady=20)

label = tk.Label(window, text="Enter your text:", font=("Arial", 10))
label.pack()

input_text = tk.Text(window, height=10, width=50, wrap=tk.WORD)
input_text.pack(pady=10)

# Buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

done_button = tk.Button(button_frame, text="Done", command=stop_timer, font=("Arial", 12))
done_button.pack(side="left", padx=5, pady=10)

restart_button = tk.Button(button_frame, text="Next one", command=next_text, font=("Arial", 12))
restart_button.pack(side="left", padx=5, pady=10)

button_frame.pack_configure(anchor="center")

# Start message and start timer at the beginning
window.after(0, show_start_message)

# Bind the Enter key to stop the timer
window.bind("<KeyRelease-Return>", stop_timer)

window.mainloop()

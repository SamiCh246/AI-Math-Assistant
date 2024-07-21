import tkinter as tk
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="API KEY")

# Initialize the conversation history with the system message
conversation_history = [
    {"role": "system", "content": "You are an assistant that only answers math questions"}
]

# Function to handle the chat interaction
def chat_with_bot():
    user_input = user_entry.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + user_input + "\n")
    chat_log.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)

    if user_input.lower() in ["goodbye", "exit"]:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "Assistant: Have a great day! Goodbye!\n")
        chat_log.config(state=tk.DISABLED)
        root.quit()
    else:
        conversation_history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        assistant_response = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": assistant_response})
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "Assistant: " + assistant_response + "\n")
        chat_log.config(state=tk.DISABLED)

# Initialize the GUI window
root = tk.Tk()
root.title("Math Assistant Chat Bot")
root.geometry("400x500")
root.configure(bg='#f0f0f0')

# Chat log text area
chat_log = tk.Text(root, height=20, width=50, state=tk.DISABLED, wrap=tk.WORD, bg='#ffffff', fg='#000000', font=("Helvetica", 12))
chat_log.pack(pady=10, padx=10)

# Scrollbar for the chat log
scrollbar = tk.Scrollbar(root, command=chat_log.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
chat_log['yscrollcommand'] = scrollbar.set

# Entry widget for user input
user_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
user_entry.pack(pady=10, padx=10)

# Button to send the user input
send_button = tk.Button(root, text="Send", command=chat_with_bot, bg='#000000', fg='#000000', font=("Helvetica", 15), relief=tk.FLAT)
send_button.pack(pady=10, padx=10)

# Welcome message
chat_log.config(state=tk.NORMAL)
chat_log.insert(tk.END, "Welcome to the Math Assistant! Type 'goodbye' or 'exit' to end the conversation.\n")
chat_log.config(state=tk.DISABLED)

# Run the GUI event loop
root.mainloop()

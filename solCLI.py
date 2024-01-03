import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr

def grind_keys():
    vanity_start = vanity_start_entry.get()
    vanity_end = vanity_end_entry.get() if ends_with_var.get() else ''
    ignore_case_flag = '--ignore-case' if ignore_case_var.get() else ''
    quantity = quantity_entry.get()

    console_log.insert(tk.END, f"Grinding keys: Starts with '{vanity_start}', Ends with '{vanity_end}', Quantity: {quantity}...\n")
    
    starts_with_option = f"--starts-with {vanity_start}:{quantity}" if vanity_start else ''
    ends_with_option = f"--ends-with {vanity_end}:{quantity}" if vanity_end else ''

    command = f"solana-keygen grind {ignore_case_flag} {starts_with_option} {ends_with_option}"
    output = run_command(command)

    with open("wallets.txt", "a") as file:
        file.write(output)

    console_log.insert(tk.END, output)

def set_keypair():
    keypair_path = keypair_path_entry.get()
    console_log.insert(tk.END, f"Setting keypair: {keypair_path}\n")
    command = f"solana config set --keypair {keypair_path}"
    output = run_command(command)
    console_log.insert(tk.END, output)

def choose_keypair_file():
    filepath = filedialog.askopenfilename()
    keypair_path_entry.delete(0, tk.END)
    keypair_path_entry.insert(0, filepath)

def toggle_network():
    network = network_var.get()
    console_log.insert(tk.END, f"Switching to {network} network...\n")
    command = f"solana config set --url https://api.{network}.solana.com"
    output = run_command(command)
    console_log.insert(tk.END, output)

# Create the main window
root = tk.Tk()
root.title("Solana CLI Tools GUI")

# Console log
console_log = tk.Text(root, height=12, width=68)
console_log.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Vanity start entry for key grinding
vanity_start_label = ttk.Label(root, text="Starts With:")
vanity_start_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
vanity_start_entry = ttk.Entry(root)
vanity_start_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we')

# Ends with entry
ends_with_var = tk.BooleanVar()
ends_with_check = ttk.Checkbutton(root, text="Ends With:", variable=ends_with_var)
ends_with_check.grid(row=2, column=0, padx=5, pady=5, sticky='e')
vanity_end_entry = ttk.Entry(root)  # This line defines vanity_end_entry
vanity_end_entry.grid(row=2, column=1, padx=5, pady=5, sticky='we')

# Ignore case checkbox
ignore_case_var = tk.BooleanVar()
ignore_case_check = ttk.Checkbutton(root, text="Ignore Case", variable=ignore_case_var)
ignore_case_check.grid(row=3, column=0, padx=5, pady=5, sticky='e')

# Quantity entry
quantity_label = ttk.Label(root, text="Quantity:")
quantity_label.grid(row=4, column=0, padx=5, pady=5, sticky='e')
quantity_entry = ttk.Entry(root)
quantity_entry.grid(row=4, column=1, padx=5, pady=5, sticky='we')

grind_button = ttk.Button(root, text="Grind Keys", command=grind_keys)
grind_button.grid(row=1, column=3, padx=5, pady=5, sticky='w')

# Keypair selection
keypair_path_entry = ttk.Entry(root)
keypair_path_entry.grid(row=5, column=1, padx=5, pady=5, sticky='we')
choose_button = ttk.Button(root, text="Choose Keypair File", command=choose_keypair_file)
choose_button.grid(row=5, column=0, padx=5, pady=5, sticky='e')
set_button = ttk.Button(root, text="Set Keypair", command=set_keypair)
set_button.grid(row=5, column=3, padx=5, pady=5, sticky='w')

# Network selection
network_var = tk.StringVar(value="mainnet-beta")
testnet_radio = ttk.Radiobutton(root, text="Testnet", variable=network_var, value="testnet")
mainnet_radio = ttk.Radiobutton(root, text="Mainnet", variable=network_var, value="mainnet-beta")
testnet_radio.grid(row=6, column=1, padx=5, pady=5, sticky='w')
mainnet_radio.grid(row=6, column=1, padx=5, pady=5)
set_network_button = ttk.Button(root, text="Set Network", command=toggle_network)
set_network_button.grid(row=6, column=3, padx=5, pady=5, sticky='w')

# Start the application
root.mainloop()

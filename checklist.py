import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Function to load Pokémon data from pokedex.txt
def load_pokemon_data():
    try:
        with open("pokedex.txt", "r") as file:
            pokemons = [line.strip() for line in file.readlines()]
        return pokemons
    except FileNotFoundError:
        messagebox.showerror("Error", "pokedex.txt not found.")
        return []

# Function to update the listbox with search results
def update_pokemon_list(search_query):
    search_query = search_query.lower()
    filtered_pokemons = [pokemon for pokemon in pokemons if search_query in pokemon.lower()]
    
    # Clear current listbox entries
    listbox.delete(0, tk.END)
    
    # Insert filtered results
    for pokemon in filtered_pokemons:
        # Determine if the Pokémon is collected (saved)
        is_collected = pokemon in saved_pokemons
        # Insert with special styling if collected
        index = listbox.size()
        listbox.insert(tk.END, pokemon)
        if is_collected:
            listbox.itemconfig(index, {'bg': '#B6FF00'})  # Highlight with lime green

# Function to load the already saved Pokémon from selected_pokemons.txt
def load_saved_pokemons():
    try:
        with open("selected_pokemons.txt", "r") as file:
            saved_pokemons = set(line.strip() for line in file.readlines())
        return saved_pokemons
    except FileNotFoundError:
        return set()

# Function to save selected Pokémon to another file (avoids duplicates)
def save_selected_pokemons():
    selected_index = listbox.curselection()  # Get the index of the selected Pokémon
    if selected_index:
        selected_pokemon = listbox.get(selected_index)  # Retrieve the selected Pokémon using the index
        # Load already saved Pokémon
        saved_pokemons = load_saved_pokemons()
        
        if selected_pokemon not in saved_pokemons:
            try:
                # Save the selected Pokémon to the file
                with open("selected_pokemons.txt", "a") as file:
                    file.write(selected_pokemon + "\n")
                
                # Update the number of collected Pokémon
                update_collected_count(saved_pokemons.union({selected_pokemon}))
                
                # Refresh the listbox to highlight newly saved Pokémon
                index = listbox.get(0, tk.END).index(selected_pokemon)
                listbox.itemconfig(index, {'bg': '#B6FF00'})
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {e}")
    else:
        messagebox.showwarning("Warning", "No Pokémon selected.")

# Function to unsave selected Pokémon from the file
def unsave_selected_pokemons():
    selected_index = listbox.curselection()  # Get the index of the selected Pokémon
    if selected_index:
        selected_pokemon = listbox.get(selected_index)  # Retrieve the selected Pokémon using the index
        # Load already saved Pokémon
        saved_pokemons = load_saved_pokemons()
        
        if selected_pokemon in saved_pokemons:
            # Remove the Pokémon from the saved list and the file
            saved_pokemons.remove(selected_pokemon)
            try:
                with open("selected_pokemons.txt", "w") as file:
                    for pokemon in saved_pokemons:
                        file.write(pokemon + "\n")
                
                # Update the number of collected Pokémon
                update_collected_count(saved_pokemons)
                
                # Refresh the listbox to remove highlight (lime green)
                index = listbox.get(0, tk.END).index(selected_pokemon)
                listbox.itemconfig(index, {'bg': 'white'})
            except Exception as e:
                messagebox.showerror("Error", f"Error removing from file: {e}")
        else:
            messagebox.showwarning("Warning", f"{selected_pokemon} is not saved.")
    else:
        messagebox.showwarning("Warning", "No Pokémon selected.")

# Function to update the number of collected Pokémon
def update_collected_count(all_pokemons):
    collected_label.config(text=f"Collected Pokémon: {len(all_pokemons)}")

# Create main window
window = tk.Tk()
window.title("Pokémon Search and Selection")
window.geometry("310x455")  # Set window size to 310x455
window.resizable(False, False)  # Disable window resizing (both horizontally and vertically)

# Load Pokémon data from pokedex.txt
pokedex_data = load_pokemon_data()
pokemons = pd.Series(pokedex_data)

# Load already saved Pokémon
saved_pokemons = load_saved_pokemons()

# Collected Pokémon counter (before updating, make sure collected_label is created)
collected_label = tk.Label(window, text=f"Collected Pokémon: {len(saved_pokemons)}")
collected_label.pack(pady=5)

# Update the collected Pokémon count immediately after loading saved Pokémon
update_collected_count(saved_pokemons)

# Search bar
search_label = tk.Label(window, text="Search for Pokémon:")
search_label.pack(pady=5)
search_entry = tk.Entry(window, width=50)
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", lambda event: update_pokemon_list(search_entry.get()))

# Listbox to display Pokémon results (only single selection)
listbox_label = tk.Label(window, text="Pokémon List:")
listbox_label.pack(pady=5)
listbox = tk.Listbox(window, selectmode=tk.SINGLE, width=50, height=10)
listbox.pack(pady=5)

# Save button to save selected Pokémon
save_button = tk.Button(window, text="Save Selected Pokémon", command=save_selected_pokemons)
save_button.pack(pady=5)

# Unsave button to unsave selected Pokémon
unsave_button = tk.Button(window, text="Unsave Selected Pokémon", command=unsave_selected_pokemons)
unsave_button.pack(pady=10)

# Run the application
window.mainloop()

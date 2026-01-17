import pandas as pd
import os

class HistoryManager:
    """
    Manages calculation history using a Pandas DataFrame.
    Handles data storage, retrieval, and file I/O (CSV).
    """
    def __init__(self):
        self.history_df = pd.DataFrame(columns=['Expression', 'Result'])
        self.file_path = "calculation_history.csv"

    def add_entry(self, expression, result):
        """Adds a new calculation to the history DataFrame."""
        # Skip error messages
        if result.startswith("Error"):
            return
        
        new_entry = pd.DataFrame({'Expression': [expression], 'Result': [result]})
        self.history_df = pd.concat([new_entry, self.history_df], ignore_index=True)

    def get_history(self):
        """Returns the Pandas DataFrame containing the history."""
        return self.history_df

    def clear_history(self):
        """Clears all entries from the history."""
        self.history_df = pd.DataFrame(columns=['Expression', 'Result'])

    def save_to_file(self):
        """Saves the current history DataFrame to a CSV file."""
        try:
            self.history_df.to_csv(self.file_path, index=False)
            return True, f"History saved to {self.file_path}"
        except Exception as e:
            return False, f"Failed to save history: {e}"

    def load_from_file(self):
        """Loads history from a CSV file into the DataFrame."""
        if not os.path.exists(self.file_path):
            return False, "No history file found."
        
        try:
            self.history_df = pd.read_csv(self.file_path)
            return True, "History loaded successfully."
        except Exception as e:
            return False, f"Failed to load history: {e}"
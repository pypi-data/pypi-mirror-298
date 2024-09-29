import pandas as pd
import json
from abc import ABC, abstractmethod

class ConfigBase(ABC):
    def __init__(self, config_file, mode='append'):
        # Ensure the mode is either 'create' or 'append'
        if mode not in ['create', 'append']:
            raise ValueError("Invalid mode: mode should be either 'create' or 'append'")
        self.config = config_file
        self.df = self._init_df()
        self.mode = mode

    def _file_exists(self):
        """Check if the file exists."""
        try:
            pd.read_csv(self.config)
            return True
        except FileNotFoundError:
            return False

    @abstractmethod
    def _init_df(self):
        """Abstract method to initialize the DataFrame."""
        pass

    @abstractmethod
    def add_entry(self, *args, **kwargs):
        """Abstract method for adding a new row."""
        pass

    def _handle_create(self, new_row_df):
        """Handle 'create' mode by replacing the current DataFrame with the new row."""
        self.df = new_row_df

    def _handle_append(self, new_row_df):
        """Handle 'append' mode by appending the new row to the existing DataFrame."""
        self.df = pd.concat([self.df, new_row_df], ignore_index=True)


class Config(ConfigBase):
    def _init_df(self):
        """Initialize the DataFrame. Load from file if exists, otherwise create a new DataFrame."""
        if self._file_exists():
            return pd.read_csv(self.config)
        else:
            # Define the columns for this specific class
            return pd.DataFrame(columns=['dataset_file_name', 'dataset_name', 'label_name_definition', 'source', 'language', 'text'])

    def add_entry(self, dataset_file_name, dataset_name, label_name_definition, source, language, text):
        """Add a new row to the DataFrame based on the mode (create or append)."""
        # Ensure label_name_definition is a dictionary
        assert isinstance(label_name_definition, dict), f"Expected label_name_definition to be a dictionary, got {type(label_name_definition)}"

        # Create a dictionary representing the new row
        new_row = {
            'dataset_file_name': dataset_file_name,
            'dataset_name': dataset_name,
            'label_name_definition': json.dumps(label_name_definition),
            'source': source,
            'language': language,
            'text': text
        }

        # Convert the dictionary to a DataFrame
        new_row_df = pd.DataFrame([new_row])

        # Handle different modes
        if self.mode == 'create':
            self._handle_create(new_row_df)
        elif self.mode == 'append':
            self._handle_append(new_row_df)

        # Save the updated DataFrame to the config file
        self.df.to_csv(self.config, index=False)

    def switch_mode(self, mode_name):
        assert mode_name in ['create', 'append'], "There are only 'create' or 'append' mode"
        self.mode = mode_name
        return

# Example usage
if __name__ == "__main__":
    # Using 'create' mode to initialize the file with a new row
    config = Config('config.csv', mode='create')
    config.add_entry(
        dataset_file_name='file1.csv',
        dataset_name='Dataset1',
        label_name_definition={'label1': 'definition1'},
        source='source',
        language='@eng',
        text='text'
    )

    # Switch to 'append' mode and add another row
    config = Config('config.csv', mode='append')
    config.add_entry(
        dataset_file_name='file2.csv',
        dataset_name='Dataset2',
        label_name_definition={'label2': 'definition2'},
        source='source',
        language='@eng',
        text='text'
    )
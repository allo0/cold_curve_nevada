import pickle
import os



class DataHandler:
    def __init__(self, filename: str):
        self.filename = filename

    def file_exists(self) -> bool:
        return os.path.exists(self.filename)

    def write_data(self, data):
        existing_data = self.read_data() or []
        if not isinstance(existing_data, list):
            existing_data = [existing_data]  # Ensure existing_data is a list
        updated_data = [data] + existing_data
        try:
            with open(self.filename, 'wb+') as file:
                pickle.dump(updated_data, file)
        except IOError as e:
            print(f"IOError occurred while trying to write to '{self.filename}': {e}")
        except pickle.PicklingError as e:
            print(f"PicklingError occurred while trying to serialize data: {e}")

    def read_data(self):
        if not self.file_exists():
            print(f"File '{self.filename}' does not exist.")
            return None

        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except IOError as e:
            print(f"IOError occurred while trying to read from '{self.filename}': {e}")
            return None
        except pickle.UnpicklingError as e:
            print(f"UnpicklingError occurred while trying to deserialize data from '{self.filename}': {e}")
            return None
        except EOFError as e:
            print(f"EOFError: End of file reached for '{self.filename}' without reading any data: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None





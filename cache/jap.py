import json
import os
import time
from datetime import datetime



if __name__ == "__main__":

    data = [
        {'name': 'John', 'age': 30},
        {'name': 'Jane', 'age': 25},
        {'name': 'Michael', 'age': 35}
    ]
    news = []
    with open(generate_file_name(), "w") as file:
        for d in data:
            try:
                file.write(f"{d}\n")
            except Exception as e:
                print(f"{e}")
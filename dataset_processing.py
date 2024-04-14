import os

folder_path = "dataset/FINAL_BOX/train/labelTxt"

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        # Read the content of the file
        with open(file_path, "r") as file:
            lines = file.readlines()
        # Rewrite the file with text removed after the 8th number
        with open(file_path, "w") as file:
            for line in lines:
                # Split the line by whitespace
                parts = line.strip().split()
                # If there are more than 8 parts, keep only the first 8
                if len(parts) > 8:
                    line = " ".join(parts[:8]) + "\n"
                file.write(line)
        print(f"Processed: {filename}")

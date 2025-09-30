import numpy as np
import pandas as pd
import os

def load_uid_list(csv_path):
    # Peek at the first row to determine if it's a header
    with open(csv_path, 'r') as f:
        first_line = f.readline().strip()

    # If first line contains non-digit characters, assume it's a header
    if not first_line.split(',')[0].isdigit():
        df = pd.read_csv(csv_path, header=0)  # Header is present
        uid_column = df.columns[0]
    else:
        df = pd.read_csv(csv_path, header=None)  # No header
        uid_column = df.columns[0]

    return df[uid_column].astype(np.uint64).values

def filter_cs(cs_path, uid_list):
    # Load CS file, filtering only by 'uid'
    cs_array = np.load(cs_path, allow_pickle=False)
    if "uid" in cs_array.dtype.names:
        mask = np.isin(cs_array["uid"], uid_list)
    else:
        raise KeyError("'uid' field not found in the CS file.")
    return cs_array[mask]

def save_cs(filtered_array, output_name="filtered_particles.cs"):
    # Save the filtered array to a .cs file
    output_path = os.path.join(os.getcwd(), output_name)
    with open(output_path, "wb") as f:
        np.save(f, filtered_array, allow_pickle=False)
    print(f"\n✅ Filtered CS file saved to: {output_path}")

def prompt_for_file(prompt_text, file_ext):
    while True:
        path = input(f"{prompt_text} ({file_ext}): ").strip()
        if os.path.isfile(path) and path.endswith(file_ext):
            return path
        print(f"❌ Invalid file. Please enter a valid {file_ext} file path.")

def main():
    print("🧊 CS File Filter Tool")
    cs_file = prompt_for_file("Enter path to the .cs file", ".cs")
    csv_file = prompt_for_file("Enter path to the .csv file with UIDs", ".csv")

    uids = load_uid_list(csv_file)
    filtered = filter_cs(cs_file, uids)
    save_cs(filtered)

if __name__ == "__main__":
    main()

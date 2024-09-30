import glob
import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import platform
import subprocess

def open_xlsx(file_path):
    try:
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', file_path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(file_path)
        elif platform.system() == 'Linux':  # Linux
            subprocess.call(('xdg-open', file_path))
        else:
            print("Unsupported OS")
    except Exception as e:
        print(f"Error opening file: {e}")

def main():
    try:
        # Create a simple GUI to ask for folder and suffix
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Start the script
        initialize = messagebox.askokcancel("Message", "Please select the folder containing the files to rename!")

        if initialize:
            # Ask for folder
            folder = filedialog.askdirectory(title="Select Folder")
            folder = Path(folder)

            # Ask for suffix
            suffix = simpledialog.askstring("Input", "Enter the file suffix (e.g., .fastq.gz):", initialvalue=".fastq.gz")

            # Collect files
            files = Path(f'{folder}/*{suffix}')
            files = glob.glob(str(files))

            # Create rename sheet
            df_lst = []
            for i, file in enumerate(files):
                file = Path(file)
                stem = Path(str(file).replace(suffix, '')).stem
                parent = file.parent

                lst = [str(file), str(parent), stem, suffix, f'=B{i+2}&"/"&C{i+2}&D{i+2}']
                df_lst.append(lst)

            df = pd.DataFrame(df_lst, columns=['Old file', 'File path', 'File name (ADJUST)', 'File suffix', 'New file'])
            rename_sheet = folder.joinpath('rename_sheet.xlsx')
            df.to_excel(rename_sheet, index=False)

            # Ask for suffix
            response = messagebox.askokcancel("Question", "A new Excel sheet will now open.\n\nPlease fill out this rename sheet.")

            if response:
                open_xlsx(rename_sheet)
                response = messagebox.askokcancel("Question", "Adjust the Excel sheet and leave this window open!\n\nThen, save and close the Excel sheet and click OK to rename samples.\n\nMake sure to have a backup of your data!\nNever rename the original files!")

                if response:
                    rename_df = pd.read_excel(rename_sheet)

                    for file in rename_df.values.tolist():
                        old = file[0]
                        new = file[-1]
                        try:
                            os.rename(old, new)
                        except Exception as e:
                            print(f"Error renaming file {old} to {new}: {e}")

                    messagebox.showinfo("Message", "All files were renamed!\n\nHave a nice day!")
            else:
                messagebox.showinfo("Message", "Have a nice day!")
        else:
            messagebox.showinfo("Message", "Have a nice day!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

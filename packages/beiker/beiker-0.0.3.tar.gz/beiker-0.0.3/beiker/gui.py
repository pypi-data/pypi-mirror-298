
from.files import check_create_folder,truncate_string
import os
from tkinter import filedialog

recent_folder=None
def open_folder_dialog(folder_path_var,format_folder_path_var):
    global recent_folder
    if recent_folder is not None:
        selected_folder = filedialog.askdirectory(initialdir=recent_folder)
    else:
        folder_path=check_create_folder(folder_path_var.get())
        # 默认打开桌面文件夹
        selected_folder = filedialog.askdirectory(initialdir=folder_path)
    if selected_folder:
        folder_path_var.set(selected_folder)
        format_folder_path_var.set(truncate_string(selected_folder,40))
        recent_folder=selected_folder
def open_file_dialog(filePath,formatFilePath):
    global recent_folder
    if recent_folder is not None:
        selectedFile = filedialog.askopenfilename(title="选择文件", initialdir=recent_folder)
    else:
        file_path=check_create_folder(filePath.get())
        # 默认打开桌面文件夹
        selectedFile = filedialog.askopenfilename(title="选择文件", initialdir=file_path)
    if selectedFile:
        filePath.set(selectedFile)
        formatFilePath.set(truncate_string(selectedFile,40))
        recent_folder=os.path.dirname(selectedFile)
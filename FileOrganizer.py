import os
import shutil

FilesExtension = {
    "wav": "Music/wav",
    "mp4": "Videos/mp4",
    "jpg": "Photos/jpg",
    "jpeg": "Photos/jpeg",
    "svg": "Photos/svg",
    "pdf": "Documents/pdf",
    "ppt": "Powerpoints",
    "pptx": "Powerpoints",
    "zip": "Compressed/zips",
    "rar": "Compressed/rar",
    "mp3": "Music/mp3",
    "exe": "Programs",
    "txt": "Text Files",    
    "csv": "Documents",     
    "xlsx": "Spreadsheets", 
    "png": "Photos",        
    "gif": "Photos",        
    "html": "Web Pages",    
    "json": "Data",
    "cdr": "Corel Draw",
    "sql": "Server Query Language",
    "drawio": "Diagrams",
    "cs": "CSharp",
    "torrent": "Miscilanious",
    "py": "Python"
}

separator = '\n' + '-' * 150 + '\n'

def scan_directory(directory):
    files = [entry.name for entry in os.scandir(directory) if entry.is_file()]
    return files

def organize_files(directory, files_extension_mapping):
    files = scan_directory(directory)
    if not files:
        return "No files found to organize."

    extensions = {file.split('.')[-1] for file in files if '.' in file}
    for ext in extensions:
        if ext in files_extension_mapping:
            os.makedirs(os.path.join(directory, files_extension_mapping[ext]), exist_ok=True)
        else:
            print(f"Warning: No folder category defined for the '{ext}' extension.")

    moved_files_count = 0
    for file in files:
        ext = file.split('.')[-1]
        destination_folder = files_extension_mapping.get(ext, "Miscilanious")
        full_destination_folder = os.path.join(directory, destination_folder)
        os.makedirs(full_destination_folder, exist_ok=True)
        source_path = os.path.join(directory, file)
        destination_path = os.path.join(full_destination_folder, file)
        shutil.move(source_path, destination_path)
        moved_files_count += 1

    return f"File organization complete. {moved_files_count} files moved."

def organize_selected_files(files_list, files_extension_mapping):
    moved_files_count = 0
    for file_path in files_list:
        if os.path.isfile(file_path):
            directory, filename = os.path.split(file_path)
            ext = filename.split('.')[-1]
            destination_folder = files_extension_mapping.get(ext, "Miscilanious")
            full_destination_folder = os.path.join(directory, destination_folder)
            os.makedirs(full_destination_folder, exist_ok=True)
            destination_path = os.path.join(full_destination_folder, filename)
            shutil.move(file_path, destination_path)
            moved_files_count += 1
        else:
            print(f"File not found: {file_path}")
    return f"File organization complete. {moved_files_count} files moved."

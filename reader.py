import pathlib
import os
import shutil

# Define the encoding to use for non-ASCII characters
ENCODING = "utf-8"

# Dictionary mapping file signatures to their corresponding file extensions
file_headers = {
    b"\x89PNG\r\n\x1a\n": "png",    # PNG file
    b"OggS": "ogg",                 # OGG file
    b"<roblox!‰ÿ".encode(ENCODING): "rbxl",  # Roblox place file (encoded to bytes)
    b"GIF87a": "gif",               # GIF file (version 87a)
    b"GIF89a": "gif",               # GIF file (version 89a)
    b"ID3": "mp3",                  # MP3 file with ID3 tag
    b"RIFF": "wav",                 # WAV file
    b"PK\x03\x04": "zip",           # ZIP file
    b"%PDF": "pdf",                 # PDF file
    b"II*\x00": "tif",              # TIFF file (little-endian)
    b"MM\x00*": "tif",              # TIFF file (big-endian)
    b"\x1A\x45\xDF\xA3": "webm",    # WebM file
}

def do_dir_checks(folder_path: str) -> bool:
    """
    Check if the provided folder path is valid.

    Parameters:
    folder_path (str): The path to the folder.

    Returns:
    bool: True if the folder path is valid, False otherwise.
    """
    if not folder_path:
        return False

    if not os.path.exists(folder_path):
        return False

    if not os.path.isdir(folder_path):
        return False
    
    return True

def get_file_extension(file_data: bytes) -> dict:
    """
    Determine the file extension based on the file's signature.

    Parameters:
    file_data (bytes): The data read from the file.

    Returns:
    dict: A dictionary containing the file extension and the position of the signature if found, None otherwise.
    """
    for header, ext in file_headers.items():
        found_index = file_data.find(header)

        if found_index != -1:
            return {"extension": ext, "position": found_index}

def move_file(file_path: str, folder_name: str):
    """
    Move a file to a specified folder.

    Parameters:
    file_path (str): Path to the file to be moved.
    folder_name (str): Name of the destination folder.
    """
    dest_folder = os.path.join(os.path.dirname(file_path), folder_name)
    os.makedirs(dest_folder, exist_ok=True)
    shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))

def get_files_from_folder(folder_path: str):
    """
    Process all files in the specified folder, identify their file type by signature,
    and move them to the appropriate folders based on their types.

    Parameters:
    folder_path (str): The path to the folder containing the files to process.
    """
    if not do_dir_checks(folder_path):
        print("Invalid folder!")
        exit(-1)

    path = pathlib.Path(folder_path)
    
    for filename in path.iterdir():
        if filename.is_file():
            with open(filename, "rb") as file:
                file_data = file.read()

                data = get_file_extension(file_data)
                
                if not data:
                    continue
                
                file_extension = data['extension']
                
                if file_extension in ["png", "tif"]:
                    move_file(filename, "Photos")
                elif file_extension in ["ogg", "mp3", "wav"]:
                    move_file(filename, "Sounds")
                elif file_extension in ["gif", "webm"]:
                    move_file(filename, "Video")
                else:
                    print(f"Unknown file type: {file_extension}")

def main():
    get_files_from_folder("C:\\Users\\build\\AppData\\Local\\Temp\\Roblox\\http")

if __name__ == "__main__":
    main()

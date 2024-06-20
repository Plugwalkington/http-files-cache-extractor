import threading
import requests
import pathlib
import re
import os

# Had to rewrite this script

# WHY:
# So i realized that in the http cache files haves a header
# it looks something like this: RBXH [Null Bytes] https://[roblox cdn].rbxcdn.com/[hash]
# the link is the actual file and i didn't realized this until just now
# so here's a more simpler script since im a dumbass and didn't put any
# attention to those files and only the contents

# NOTE: This is way slower since it does requests to roblox's CDN and has 
# to wait for a response

file_headers = {
    b"\x89PNG\r\n\x1a\n": "png",    # PNG file
    b"OggS": "ogg",                 # OGG file
    b"<roblox!\x2030\xFF": "rbxl",  # Roblox place file (encoded to bytes)
    b"GIF87a": "gif",               # GIF file (version 87a)
    b"GIF89a": "gif",               # GIF file (version 89a)
    b"ID3": "mp3",                  # MP3 file with ID3 tag
    b"RIFF": "wav",                 # WAV file
    b"PK\x03\x04": "zip",           # ZIP file
    b"II*\x00": "tif",              # TIFF file (little-endian)
    b"MM\x00*": "tif",              # TIFF file (big-endian)
    b"\x1A\x45\xDF\xA3": "webm",    # WebM file
}

def get_and_save_file(link: str, link_name: str, save_to: str):
    data = requests.get(link)

    if data.status_code == 403:
        return False
    
    extension = get_extension(data.text[0:32])

    if not extension:
        extension = "unknown"

    with open(os.path.join(save_to, f"{link_name[0]}.{extension}"), "wb+") as write_to:
        write_to.write(data.content)
        write_to.close()
        print(f"{link}: {link_name[0]}.{extension}")

    data.close()


def get_extension(str):
    for header, ext in file_headers.items():
        index = str.find(header.decode(errors="replace"))

        if index != -1:
            return ext

def start_getting_files(extract_path: str, out_path: str):
    for filename in pathlib.Path(extract_path).iterdir():
        file = open(filename, "rb")
        header = file.read(92)

        link = re.findall("https:\\/\\/[a-zA-Z0-9]*\\.rbxcdn\\.com\\/[a-z0-9]*", header.decode(errors="ignore"))
        file.close()

        if not link:
            continue

        link_name = re.findall("[a-f0-9]{32}", link[0]) # hash

        if not link_name:
            continue
        
        do_thread = threading.Thread(target=get_and_save_file, args=(link[0], link_name, out_path))
        do_thread.start()

def main():
    extract_path = input("Path to extract files: ")
    out_path = input("Output path: ")

    print("This process may take a long time")

    start_getting_files(extract_path, out_path)


if __name__ == "__main__":
    main()
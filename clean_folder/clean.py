import shutil
import sys
import re
import os
from pathlib import Path

FOLDER_PROCESS = sys.argv[1]
#FOLDER_PROCESS = Path(r'C:\Users\User\Desktop\Мотлох')
#FILE_DICT = {file.name: file.suffix for file in FOLDER_PROCESS.iterdir()}

#    ////___NORMALIZE.PY___\\\\
CYRILLIC_SYMBOLS = [*"абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"]
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()



def normalize_file(file: Path)-> str: 
    translate_name = re.sub('\W', '_', file.name.translate(TRANS))[:-len(file.suffix)] + file.suffix
    return translate_name

def normalize_archiv(name: str)-> str: 
    translate_name = re.sub('\W', '_', name.translate(TRANS))
    return translate_name

#     ////____PARSER____\\\\
IMAGES = []
VIDEO = []
AUDIO = []
DOCUMENTS = []
ARCHIVES = []

REGISTER_EXTRENTIONS = {
'JPEG': IMAGES,
'JPG': IMAGES,
'PNG': IMAGES,
'SVG': IMAGES,

'AVI': VIDEO, 
'MP4': VIDEO,
'MOV': VIDEO, 
'MKV': VIDEO,

'DOC': DOCUMENTS,
'DOCX': DOCUMENTS,
'TXT': DOCUMENTS,
'PDF': DOCUMENTS, 
'XLSX': DOCUMENTS, 
'PPTX': DOCUMENTS,

'MP3': AUDIO,
'OGG': AUDIO,
'WAV': AUDIO, 
'AMR': AUDIO,

'ZIP': ARCHIVES,
'GZ': ARCHIVES,
'TAR': ARCHIVES
}


MY_OTHER = []
FOLDERS = []
EXTENTIONS = set()
UNKNOWN = set()

def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('images', 'archives', 'video', 'audio', 'documents', 'MY_OTHER'):
                FOLDERS.append(item)
                try:
                    item.rmdir()
                except:
                    scan(item)
            continue
        extention = get_extension(item.name)   #беремо розширення
        full_name = folder / item.name         #беремо повний шлях до файлу
        if not extention:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTRENTIONS[extention]
                ext_reg.append(full_name)
                EXTENTIONS.add(extention)
            except KeyError:
                UNKNOWN.add(extention)
                MY_OTHER.append(full_name)

'''
if __name__ == '__main__':
    #folder_process = sys.argv[1]
    scan(Path(FOLDER_PROCESS))

    print(f'IMAGES:      {[im.name for im in IMAGES]}')
    print(f'VIDEO:       {[vd.name for vd in VIDEO]}')
    print(f'AUDIO:       {[au.name for au in AUDIO]}')
    print(f'DOCUMENTS:   {[dc.name for dc in DOCUMENTS]}')

    print(f'Archives:    {[arch.name for arch in ARCHIVES]}')
    print(f'EXTENTIONS:  {EXTENTIONS}')
    print(f'UNKNOWN:     {UNKNOWN}')
    print(f'FOLDERS:     {[fold.name for fold in FOLDERS]}')
'''

# ////____MAIN____\\\\
def handle_file(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True)
    file_name.replace(target_folder / normalize_file(file_name))

def handle_archive(file_name: Path, target_folder: Path, archive_format):
    target_folder.mkdir(exist_ok=True)
    folder_for_file = target_folder / normalize_archiv(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True)
    try:
        if archive_format == 'gz':
            archive_format = 'gztar'
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()), archive_format)
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

def main():
    for file in IMAGES:  
        handle_file(file, Path(FOLDER_PROCESS) / 'images')
    for file in VIDEO:  
        handle_file(file, Path(FOLDER_PROCESS) / 'video')
    for file in AUDIO:  
        handle_file(file, Path(FOLDER_PROCESS) / 'audio')
    for file in DOCUMENTS:  
        handle_file(file, Path(FOLDER_PROCESS) / 'documents')
    for file in MY_OTHER:  
        handle_file(file, Path(FOLDER_PROCESS) / 'MY_OTHER')       
    for file in ARCHIVES:  
        handle_archive(file, Path(FOLDER_PROCESS) / 'archives', file.suffix[1:])

def start():
    if sys.argv[1]:
        FOLDER_PROCESS = sys.argv[1]
        scan(Path(FOLDER_PROCESS))
        main()


if __name__ == '__main__':
    start()



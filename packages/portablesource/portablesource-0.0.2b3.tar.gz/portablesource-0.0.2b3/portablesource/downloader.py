import os
import requests
import subprocess
from tqdm import tqdm
from urllib.parse import urlparse
import winreg
import locale
from .get_gpu import get_gpu

links = [
    "https://huggingface.co/datasets/NeuroDonu/PortableSource/resolve/main/python.7z",
    "https://huggingface.co/datasets/NeuroDonu/PortableSource/resolve/main/ffmpeg.7z",
    "https://huggingface.co/datasets/NeuroDonu/PortableSource/resolve/main/git.7z",
    "https://huggingface.co/datasets/NeuroDonu/PortableSource/resolve/main/CUDA.7z",
    "https://huggingface.co/datasets/NeuroDonu/PortableSource/resolve/main/7z.exe",
]

gpu = get_gpu()

def set_path(cuda_path):
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_ALL_ACCESS)
        current_path = winreg.QueryValueEx(key, "Path")[0]
        if cuda_path not in current_path:
            new_path = current_path + ";" + cuda_path
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        os.environ["PATH"] = new_path
        return True

def get_localized_text(language, key):
    texts = {
        "en": {
            "which_path": "Select a installation path or enter your reference, default C:\ :",
            "error_creating_directory": "Error creating directory!",
        },
        "ru": {
            "which_path": "Выберите путь установки, дефолтный C:\ :",
            "error_creating_directory": "Ошибка создания директории!",
        }
    }
    return texts[language].get(key, "")

def get_system_language():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International")
        language = winreg.QueryValueEx(key, "LocaleName")[0]
        winreg.CloseKey(key)
        lang_code = language.split('-')[0].lower()
        return "ru" if lang_code == "ru" else "en"
    except WindowsError:
        lang_code = locale.getdefaultlocale()[0].split('_')[0].lower()
        return "ru" if lang_code == "ru" else "en"

def add_to_user_path(path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
        current_path, _ = winreg.QueryValueEx(key, "Path")
        if path not in current_path:
            new_path = current_path + ";" + path if current_path else path
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        os.environ['PATH'] = os.environ['PATH'] + ";" + path
        return True
    except Exception as e:
        return False

def get_installed_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ)
        path, _ = winreg.QueryValueEx(key, "Path")
        winreg.CloseKey(key)
        paths = path.split(';')
        for p in paths:
            if 'portablesource' in p:
                if os.path.exists(os.path.join(p, 'installed.txt')):
                    return p
        env_path = os.environ.get('PATH', '')
        env_paths = env_path.split(os.pathsep)
        for p in env_paths:
            if 'portablesource' in p:
                if os.path.exists(os.path.join(p, 'installed.txt')):
                    return p
        return None
    except Exception as e:
        return None

def get_path_for_install():
    language = get_system_language()
    if language not in ["en", "ru"]:
        language = "en"
    default_path = "C:\\"
    user_input = input(get_localized_text(language, "which_path")).strip()
    install_path = user_input if user_input else default_path

    full_path = os.path.join(install_path, 'portablesource')
    if not os.path.exists(full_path):
        try:
            os.makedirs(full_path)
        except OSError:
            print(get_localized_text(language, "error_creating_directory"))
            return get_path_for_install()

    with open(os.path.join(full_path, 'installed.txt'), 'w') as f:
        f.write('installed')

    return full_path

def get_install_path():
    tested_path = get_installed_path()
    if tested_path is None:
        full_path = get_path_for_install()
        add_to_user_path(full_path)
        install_path = full_path
    else:
        install_path = tested_path
    return install_path

def download_file(url, output_dir='system'):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(urlparse(url).path)
    output_path = os.path.join(output_dir, filename)
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get('content-length', 0))

    with open(output_path, 'wb') as out_file, tqdm(
        desc=filename,
        total=file_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=16384):
            size = out_file.write(data)
            pbar.update(size)
    return output_path

def extract_7z(archive_path, output_dir, seven_zip_path):
    command = [seven_zip_path, 'x', archive_path, f'-o{output_dir}', '-y']
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError as e:
        return False

def download_extract_and_cleanup(links, output_dir='system'):
    #if gpu == "NVIDIA": #maybe
        #required_folders = ['python', 'ffmpeg', 'git', 'CUDA']
    #else:
        #required_folders = ['python', 'ffmpeg', 'git']

    required_folders = ['python', 'ffmpeg', 'git']

    missing_folders = [folder for folder in required_folders if not os.path.exists(os.path.join(output_dir, folder))]

    if not missing_folders:
            return

    seven_zip_path = os.path.join(output_dir, '7z.exe')
    if not os.path.exists(seven_zip_path):
        seven_zip_path = download_file(links[-1], output_dir)

    archives_to_extract = []

    for link in links[:-1]:
        folder_name = os.path.splitext(os.path.basename(link))[0]
        if folder_name in missing_folders:
            file_path = download_file(link, output_dir)
            archives_to_extract.append(file_path)

    for archive in archives_to_extract:
        if extract_7z(archive, output_dir, seven_zip_path):
            os.remove(archive)

def download_for_main():
    path = get_install_path()
    system = os.path.join(path, "system")
    download_extract_and_cleanup(links, output_dir=system)
    #if gpu == "NVIDIA":
        #cuda_path = os.path.join(system, "CUDA")
        #if os.path.exists(cuda_path):
            #set_path(cuda_path)
import os
import subprocess
import re
import locale
import winreg
from .downloader import get_install_path, download_for_main
from tqdm import tqdm
import requests
import time

install_path = get_install_path()
git_exe = os.path.join(install_path, 'system', 'git', 'cmd', 'git.exe')
python = os.path.join(install_path, 'system', 'python', 'python.exe')
ffmpeg = os.path.join(install_path, 'system', 'ffmpeg')
git_cmd = os.path.join(install_path, 'system', 'git', 'cmd')
python_scripts = os.path.join(install_path, 'system', 'python', 'Scripts')

repos = [
    "https://github.com/facefusion/facefusion",
    "https://github.com/KwaiVGI/LivePortrait",
    "https://github.com/lllyasviel/stable-diffusion-webui-forge",
    "https://github.com/comfyanonymous/ComfyUI",
    "https://github.com/hacksider/Deep-Live-Cam",
    "https://github.com/argenspin/Rope-Live",
]

for i, repo in enumerate(repos, 1):
    print(f"{i}. {repo}")

def create_venv(repo_path, python):
    venv_path = os.path.join(repo_path, "venv")
    if not os.path.exists(venv_path):
        subprocess.run([python, "-m", "venv", venv_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
    return venv_path, activate_script

def get_uv_path():
    scripts_dir = os.path.join(os.path.dirname(python), 'Scripts')
    uv_executable = os.path.join(scripts_dir, "uv.exe")
    return uv_executable

def install_uv():
    try:
        subprocess.run([python, "-m", "pip", "install", "uv"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None
    
    uv_executable = get_uv_path()
    if os.path.exists(uv_executable):
        return uv_executable
    else:
        return None


def get_localized_text(language, key):
    texts = {
        "en": {
            "installed" : "Installed! Try to use.",
            "select_repo": "Select a repository number or enter your reference:",
            "enter_requirements_filename": "Enter the name of the requirements file (press Enter for 'requirements.txt'): ",
        },
        "ru": {
            "installed" : "Установлено! Надеюсь вам понравится.",
            "select_repo": "Выберите номер репозитория или введите свою ссылку: ",
            "enter_requirements_filename": "Введите имя файла с библиотеками (нажмите Enter для 'requirements.txt'): ",
             
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

def install_from_source(language):
    language = get_system_language()
    if not language:
        language = input(get_localized_text("en", "choose_language")).strip().lower()
        if language not in ["en", "ru"]:
            language = "en"
    choice = input(get_localized_text(language, "select_repo")).strip()

    if choice.isdigit() and 1 <= int(choice) <= len(repos):
        repo_url = repos[int(choice) - 1]
    else:
        repo_url = choice

    download_for_main()

    repo_name = repo_url.split('/')[-1].replace('.git', '')
    abs_path = get_install_path()
    sources_path = os.path.join(abs_path, "sources")
    os.makedirs(sources_path, exist_ok=True)
    repo_home = os.path.join(sources_path, repo_name)
    os.makedirs(repo_home, exist_ok=True)

    if not os.path.exists(repo_home) and not repo_name=="facefusion":
        os.chdir(sources_path)
        repo_abs = os.path.join(sources_path, repo_name)
        if not os.path.exists(repo_abs):
            subprocess.run([git_exe, "clone", repo_url, repo_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.chdir(repo_abs)
            subprocess.run([git_exe, "pull", "origin"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        ff_path = os.path.join(abs_path, "sources","facefusion")
        ff_master = os.path.join(ff_path, "master")
        if not os.path.exists(ff_path):
            os.makedirs(ff_path)
        if not os.path.exists(ff_master):
            os.chdir(ff_path)
            subprocess.run([git_exe, "clone", repo_url, "-b", "master", "master"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.chdir(ff_master)
            subprocess.run([git_exe, "pull", "origin", "master"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    repo_path = os.path.join(abs_path, "sources", repo_name)
    venv_path, activate_script = create_venv(repo_path, python)
    uv_executable = install_uv()

    if repo_name == "facefusion":
        requirements_file = os.path.join(repo_path, "master", "requirements.txt")
    else:
        requirements_file = os.path.join(repo_path, "requirements.txt")

    python_venv = os.path.join(install_path, 'system', repo_name, 'venv', 'Scripts', 'python.exe')
    python_facefusion = os.path.join(install_path, 'system', 'facefusion', 'venv', 'Scripts', 'python.exe')

    if repo_name == "facefusion":
        app_name = "updater_facefusion.py"
    elif repo_name == "Rope-Live":
        app_name == "Rope.py"
    elif repo_name == "LivePortrait":
        app_name = "app.py"
    elif repo_name == "ComfyUI":
        app_name == "main.py"
    elif repo_name == "Deep-Live-Cam":
        app_name == "run.py"
    elif repo_name == "stable-diffusion-webui-forge":
        app_name == "webui.py"

    if repo_name == "facefusion":
        os.chdir(repo_home)
        tmp = os.path.join(repo_home, "tmp")
        if not os.path.exists(tmp):
            os.makedirs(tmp)
        bat_content = f'''@echo off
setlocal enabledelayedexpansion
for /d %%i in (tmp\\tmp*,tmp\\pip*) do rd /s /q "%%i" 2>nul || ("%%i" && exit /b 1) & del /q tmp\\tmp* > nul 2>&1 & rd /s /q pip\\cache 2>nul

set "appdata={tmp}"
set "userprofile={tmp}"
set "temp={tmp}"
set "PATH=%PATH%;{git_cmd};{python_facefusion};{python_scripts};{ffmpeg};%PATH%"

set "CUDA_MODULE_LOADING=LAZY"

"{python_facefusion}" {app_name}
pause
endlocal
REM by dony
'''

        with open('start_nvidia.bat', 'w') as bat_file:
            bat_file.write(bat_content)
        updater_facefusion_url = "https://huggingface.co/datasets/NeuroDonu/PortableSource/resolve/main/updater_facefusion.py"
        updater_facefusion_name = "updater_facefusion.py"
        response = requests.get(updater_facefusion_url, stream=True)
        with open(updater_facefusion_name, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    out_file.write(chunk)
    else:
        os.chdir(repo_home)
        tmp = os.path.join(repo_home, "tmp")
        if not os.path.exists(tmp):
            os.makedirs(tmp)
        app_path = os.path.join(repo_home, "app.py")
        if not os.path.exists(app_path):
            print("not found app.py! please check correctly start_nvidia.bat! maybe he dont work.")
        else:
            bat_content = f'''@echo off
setlocal enabledelayedexpansion
for /d %%i in (tmp\\tmp*,tmp\\pip*) do rd /s /q "%%i" 2>nul || ("%%i" && exit /b 1) & del /q tmp\\tmp* > nul 2>&1 & rd /s /q pip\\cache 2>nul

set "appdata={tmp}"
set "userprofile={tmp}"
set "temp={tmp}"
set "PATH=%PATH%;{git_cmd};{python_venv};{python_scripts};{ffmpeg};%PATH%"

set "CUDA_MODULE_LOADING=LAZY"

"{python_venv}" {app_name}
pause
endlocal
REM by dony
'''
            with open('start_nvidia.bat', 'w') as bat_file:
                bat_file.write(bat_content)
    
    if os.path.exists(requirements_file):
        installed_flag = os.path.join(venv_path, ".libraries_installed")
        if not os.path.exists(installed_flag):
            with open(requirements_file, 'r') as f:
                requirements = f.read()
    
        requirements = re.sub(r'(insightface).*\n', '', requirements)
        torch_packages = re.findall(r'(torch)', requirements)
        onnx_fix = re.findall(r'(onnx)', requirements)
        cuda_version = re.search(r'\+cu(\d+)', requirements)
        cuda_version = cuda_version.group(1) if cuda_version else None
        onnx_gpu = re.search(r'onnxruntime-gpu', requirements)
        onnxruntime = re.search(r'onnxruntime(?!-gpu)', requirements)

        with open(requirements_file, 'w') as f:
            f.write(requirements)

        install_cmd = f'"{activate_script}" && "{uv_executable}" pip install -r "{requirements_file}"'
        subprocess.run(install_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        insightface_cmd = f'"{activate_script}" && "{uv_executable}" pip install https://huggingface.co/hanamizuki-ai/insightface-releases/resolve/main/insightface-0.7.3-cp310-cp310-win_amd64.whl"'
        subprocess.run(insightface_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if torch_packages:
            torch_cmd = f'"{activate_script}" && "{uv_executable}" pip install torch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/{cuda_version}'
            subprocess.run(torch_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if onnx_fix and repo_name!="facefusion":
            onnx_cmd = f'"{activate_script}" && "{uv_executable}" pip install onnx==1.16.1'
            subprocess.run(onnx_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


        if onnx_gpu or onnxruntime:
            requirements = re.sub(r'onnxruntime(?!-gpu)', 'onnxruntime-gpu', requirements)
            ort_lib_path = os.path.join(repo_path, "venv", "Lib", "site-packages", "onnxruntime")
            for item in os.listdir(ort_lib_path):
                if item.endswith('dll'):
                    item_path = os.path.join(ort_lib_path, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
            
            ort_dll_files = ["onnxruntime.dll", "onnxruntime_providers_cuda.dll", "onnxruntime_providers_shared.dll", "onnxruntime_providers_tensorrt.dll"]

            for file_name in ort_dll_files:
                file_url = f"https://huggingface.co/datasets/NeuroDonu/PortableSource/resolve/main/{file_name}"
                file_path = os.path.join(ort_lib_path, file_name)
    
                response = requests.get(file_url, stream=True)
                total_size = int(response.headers.get('content-length', 0))

                with open(file_path, 'wb') as file, tqdm(
                desc=file_name,
                total=total_size,
                unit='kB',
                unit_scale=True,
                unit_divisor=1024,
                ) as progress_bar:
                    for data in response.iter_content(chunk_size=16384):
                        size = file.write(data)
                        progress_bar.update(size)
    
                        time.sleep(1)

        open(installed_flag, 'w').close()

    if repo_name == "Deep-Live-Cam":
        models_dir = os.path.join(repo_name, "models")
        os.makedirs(models_dir, exist_ok=True)
        model_to_download_urls = [
            "https://huggingface.co/hacksider/deep-live-cam/resolve/main/GFPGANv1.4.pth",
            "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128_fp16.onnx"
        ]
        for url in model_to_download_urls:
            filename = url.split('/')[-1]
            local_path = os.path.join(models_dir, filename)
            if not os.path.exists(local_path):
                response = requests.get(url, stream=True)
                with open(local_path, 'wb') as out_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            out_file.write(chunk)

def installed():
    language = get_system_language()
    if language not in ["en", "ru"]:
        language = "en"
    install_from_source(language)
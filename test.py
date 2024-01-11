import os.path
import unicodedata
import re
import subprocess


def recursive_run(path):
    change_compatible_name(path)
    unzip_file(path)

def change_compatible_name(path):
    for (root, dirs, files) in os.walk(path):
        for file_name in files:
            src = os.path.join(root, file_name)
            filename, _ext = os.path.splitext(file_name)
            if not unicodedata.is_normalized('NFC', filename):
                normalized_name = unicodedata.normalize('NFC', filename)
                filename = normalized_name
            if not check_compatible_filename(filename):
                fixed_file_name = fix_compatible_filename(filename) + _ext
                dst = os.path.join(root, fixed_file_name)
                os.rename(src=src, dst=dst)
        for dir_name in dirs:
            _dir_name = dir_name.copy()
            if not unicodedata.is_normalized('NFC', _dir_name):
                _dir_name = unicodedata.normalize('NFC', _dir_name)
            if not check_compatible_filename(_dir_name):
                src = os.path.join(root, _dir_name)
                fixed_dir_name = fix_compatible_filename(_dir_name)
                dst = os.path.join(root, fixed_dir_name)
                os.rename(src=src, dst=dst)

def unzip_file(path):
    for (root, dirs, files) in os.walk(path):
        for file_name in files:
            src = os.path.join(root, file_name)
            filename, _ext = os.path.splitext(file_name)
            if _ext == "zip":
                extract_dir_name = f"{filename}_tmp"
                extract_dir_path = os.path.join(root, extract_dir_name)
                if os.path.exists(extract_dir_path):
                    FileExistsError("이미 존재하는 tmp 폴더 입니다.")
                os.mkdir(extract_dir_path)
                bandizip_unzip(src_path=src,dst_path=f"{extract_dir_path}/")
                recursive_run(extract_dir_path)
                bandizip_zip(src_path=root, dst_file_path=src)


def bandizip_zip(src_path, dst_file_path):
    try:
        subprocess.call(f"Bandizip c -y {dst_file_path} {src_path}\\")
        return True
    except Exception as e:
        print(e, src_path, dst_file_path)
        return False


def bandizip_unzip(src_path, dst_path):
    try:
        subprocess.call(f"Bandizip bx -y -o:{dst_path} {src_path}")
        return True
    except Exception as e:
        print(e, src_path, dst_path)
        return False


def check_compatible_filename(filename):
    # 윈도우에서 불가능한 문자 및 제어 문자를 포함하는 정규식 패턴
    pattern = r'[\<>:"/\|?*\x00-\x1f\x7f]'

    # 파일명에 비호환 문자가 있는지 검사
    if re.search(pattern, filename):
        return False  # 비호환 문자가 있음
    return True  # 호환 가능한 파일명


def fix_compatible_filename(filename):
    # 윈도우에서 불가능한 문자 제거 및 치환
    filename = re.sub(r'[<>:"/|?*]', '_', filename)
    # 제어 문자 제거
    filename = re.sub(r'[\x00-\x1f\x7f]', '', filename)
    # 리눅스/유닉스에서 불가능한 문자 제거 (경로 구분자 '/')
    filename = filename.replace('/', '-')

    # 파일명 길이 제한 (예시: 255자)
    filename = filename[:255]
    return filename


# def check_unicode(string):
#     try:
#         string.encode('latin1').decode('euc-kr')
#     except UnicodeDecodeError:
#         string.encode('latin1').decode('cp949')

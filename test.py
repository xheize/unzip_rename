import os.path
import stat
import unicodedata
import re
# import subprocess
import shutil
import datetime
from multiprocessing import Pool

from bandizip_modules import bandizip_unzip, bandizip_zip

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
            _dir_name = dir_name
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
            if _ext == ".zip":
                extract_dir_name = f"{filename}_tmp"
                extract_dir_path = os.path.join(root, extract_dir_name)
                if os.path.exists(extract_dir_path):
                    shutil.rmtree(extract_dir_path, onexc=remove_readonly)
                os.mkdir(extract_dir_path)
                if not bandizip_unzip(src_path=src,dst_path=f"{extract_dir_path}\\"):
                    FileNotFoundError("압축해제 에러 발생")
                    return
                recursive_run(extract_dir_path)
                if not bandizip_zip(src_path=extract_dir_path, dst_file_path=src):
                    FileNotFoundError("압축하기 에러 발생")
                    shutil.rmtree(extract_dir_path, onexc=remove_readonly)
                    return


def check_compatible_filename(filename):
    # 윈도우에서 불가능한 문자 및 제어 문자를 포함하는 정규식 패턴
    pattern = r'[\<>:"/\|?*\x00-\x1f\x7f]'

    # 파일명에 비호환 문자가 있는지 검사
    if re.search(pattern, filename):
        return False  # 비호환 문자가 있음
    return True  # 호환 가능한 파일명


def fix_compatible_filename(filename):
    # 윈도우에서 불가능한 문자 제거 및 치환
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 응용프로그램 불가능한 문자 제거 및 치환
    filename = re.sub(r'[@#%]', '_', filename)
    # 제어 문자 제거
    filename = re.sub(r'[\x00-\x1f\x7f]', '', filename)
    # 리눅스/유닉스에서 불가능한 문자 제거 (경로 구분자 '/')
    filename = filename.replace('/', '_')

    # 파일명 길이 제한 (예시: 255자)
    filename = filename[:255]
    return filename

def remove_readonly(func, path, _):
   "Clear the readonly bit and reattempt the removal"
   os.chmod(path, stat.S_IWRITE)
   func(path)

# def check_unicode(string):
#     try:
#         string.encode('latin1').decode('euc-kr')
#     except UnicodeDecodeError:
#         string.encode('latin1').decode('cp949')

def multiprocess_run():
    path = "C:\\webudding_test"
    prod_list = os.listdir(path)
    prod_path_list = map(lambda x: os.path.join(path, x), prod_list)
    prod_path_list = list(prod_path_list)
    
    with Pool(processes=32) as pool:
        result = pool.map(recursive_run, prod_path_list)
        
def test_run():
    path = "C:\\webudding_test"
    prod_list = os.listdir(path)
    prod_path_list = map(lambda x: os.path.join(path, x), prod_list)
    prod_path_list = list(prod_path_list)
    
    for prod_path in prod_path_list:
        recursive_run(prod_path)
        tmp = input()
        if not tmp == "y":
            break


if __name__ == "__main__":
    start = datetime.datetime.now()
    print("시작시간 : ", start)
    multiprocess_run()
    end = datetime.datetime.now()
    print("종료 시간 : ", end)
    count = end - start
    print("소요 시간 : ", count)


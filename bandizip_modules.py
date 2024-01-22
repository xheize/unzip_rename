import subprocess

def bandizip_zip(src_path, dst_file_path):
    command = ["bz.exe","c","-y", f"{dst_file_path}", f"{src_path}"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    # result = subprocess.run(f"bz.exe c -y {dst_file_path} {src_path}/", shell=True, check=True)
    if result.returncode != 0:
        print("압축하기 에러")
        print(result.stdout)
        print(result.stderr)
        return False
    else:
        return True
    try:
        command = ["bz.exe","c","-y", f"{dst_file_path}", f"{src_path}"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', check=True)
        # result = subprocess.run(f"bz.exe c -y {dst_file_path} {src_path}/", shell=True, check=True)
        print(result.stdout)
        if result.returncode != 0:
            print("압축하기 에러")
            print(result.stdout)
            print(result.stderr)
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False


def bandizip_unzip(src_path, dst_path):
    command = ["bz.exe","x","-y", f"-o:{dst_path}", f"{src_path}"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8',)
    if result.returncode != 0:
        print("압축해제 에러")
        print(result.stdout)
        print(result.stderr)
        return False
    else:
        return True
    try:
        command = ["bz.exe","x","-y", f"-o:{dst_path}", f"{src_path}"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', check=True)
        print(result.stdout)
        if result.returncode != 0:
            print("압축해제 에러")
            print(result.stdout)
            print(result.stderr)
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False
    
    
# Origin Code
# def bandizip_zip(src_path, dst_file_path):
#     try:
#         result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         subprocess.run(f"bz.exe c -y {dst_file_path} {src_path}/", shell=True, check=True)
#         return True
#     except Exception as e:
#         print(e, src_path, dst_file_path)
#         return False


# def bandizip_unzip(src_path, dst_path):
#     try:
#         subprocess.run(f"bz.exe x -y -o:{dst_path} {src_path}", shell=True, check=True)
#         return True
#     except Exception as e:
#         print(e, src_path, dst_path)
#         return False
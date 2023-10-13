import os
import zipfile


def compress_folder(folder_path, save_path, save_name):
    zip_filename = save_path + save_name
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))


def split_zip_with_structure(input_zip, output_prefix, chunk_size):
    with zipfile.ZipFile(input_zip, 'r') as zip_file:
        file_list = zip_file.namelist()
        chunk_num = 1
        while file_list:
            chunk_files = file_list[:chunk_size]
            with zipfile.ZipFile(f'{output_prefix}_{chunk_num}.zip', 'w') as chunk_zip:
                for file in chunk_files:
                    with zip_file.open(file) as original_file:
                        chunk_zip.writestr(file, original_file.read())
            file_list = file_list[chunk_size:]
            chunk_num += 1


def scan(path, my_dir, basepath, i):
    files = os.listdir(path)

    for file in files:
        tmp = os.path.join(path, file)
        if os.path.isfile(tmp):
            name = tmp[len(basepath):]
            i = i + 1
            my_dir[i] = name
            print(my_dir)
        if os.path.isdir(tmp):
            scan(tmp, my_dir, basepath, i)

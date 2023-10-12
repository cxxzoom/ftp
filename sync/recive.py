# import os
# import zipfile
#
#
# # 合并分割文件
# def merge_split_files(split_dir, merged_file):
#     with open(merged_file, 'wb') as output_file:
#         for root, dirs, files in os.walk(split_dir):
#             for file in sorted(files):
#                 chunk_file = os.path.join(root, file)
#                 with open(chunk_file, 'rb') as chunk_f:
#                     output_file.write(chunk_f.read())
#
#
# # 解压文件
# def unzip_file(zip_file, target_dir):
#     with zipfile.ZipFile(zip_file, 'r') as zipf:
#         zipf.extractall(target_dir)
#
#
# # 解压和合并应该是在另一个文件夹下
# chunk_dir = "F:\\cxxzoom\\ftp\\save\\1"
#
# # merge_split_files('F:\\cxxzoom\\ftp\\sync\\slice', 'F:\\cxxzoom\\ftp\\sync\\merge.zip')
# # unzip_file('F:\\cxxzoom\\ftp\\sync\\merge.zip', 'F:\\cxxzoom\\ftp\\sync\\merge_', )
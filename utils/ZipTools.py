"""
copy from https://blog.csdn.net/zy0412326/article/details/136272749
"""
import os
import pyzipper
import zipfile

class ZipTools:
    @staticmethod
    def extract_zip(zip_file, extract_folder, password):
        with pyzipper.AESZipFile(zip_file) as z:
            try:
                z.extractall(extract_folder, pwd=password.encode('utf-8'))
                print(f"Successfully extracted {zip_file} to {extract_folder}")
            except Exception as e:
                print(f"Extraction failed: {e}")
    @staticmethod
    def zip_folder(folder_path, zip_path, password = None):
        if password is None:
            with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as zf:
                for file_i in os.listdir(folder_path):
                    zf.write(os.path.join(folder_path,file_i),os.path.relpath(os.path.join(folder_path,file_i),os.path.dirname(folder_path)))
        else:
            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
                # 将密码转换为字节类型
                password_bytes = password.encode('utf-8')
                zf.setpassword(password_bytes)
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        abs_path = os.path.join(root, file)
                        rel_path = os.path.relpath(abs_path, os.path.dirname(folder_path))
                        zf.write(abs_path, rel_path)
if __name__ == "__main__":
    folder_to_zip = '/root/workspace/nicegui_payment_shop/assets/uploads/1720766619.7633362/org'
    zip_file_path = '/root/workspace/nicegui_payment_shop/assets/uploads/1720766619.7633362/org.zip'
    password = '123123'
    ZipTools.zip_folder(folder_to_zip, zip_file_path, password)
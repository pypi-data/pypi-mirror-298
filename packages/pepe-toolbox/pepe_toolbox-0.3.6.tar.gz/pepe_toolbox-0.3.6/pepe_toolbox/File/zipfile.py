import os
import zipfile
import shutil
from typing import Optional

class ZipFile:
    @staticmethod
    def extract_zip(zip_path: str, extract_to: Optional[str] = None, delete_original: bool = False) -> None:
        """
        단일 ZIP 파일을 해제하는 함수입니다.
        Function to extract a single ZIP file.

        Args:
            zip_path (str): 압축 파일의 경로 / Path to the ZIP file
            extract_to (Optional[str]): 압축 해제할 디렉토리 경로. 기본값은 None으로, ZIP 파일이 있는 폴더에 추출합니다.
                                        Path to extract the contents. If None, extracts to a folder with the same name as the ZIP file.
            delete_original (bool): 압축 해제 후 원본 파일 삭제 여부. 기본값은 False입니다.
                                    Whether to delete the original file after extraction. Defaults to False.

        Raises:
            zipfile.BadZipFile: 잘못된 ZIP 파일일 경우 / If the ZIP file is invalid
            FileNotFoundError: ZIP 파일을 찾을 수 없는 경우 / If the ZIP file is not found
        """
        try:
            if extract_to is None:
                # ZIP 파일 이름과 같은 이름의 폴더 생성
                zip_name = os.path.splitext(os.path.basename(zip_path))[0]
                extract_to = os.path.join(os.path.dirname(zip_path), zip_name)

            # 같은 이름의 폴더가 있으면 삭제
            if os.path.exists(extract_to):
                shutil.rmtree(extract_to)

            # 폴더 생성
            os.makedirs(extract_to)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)

            if delete_original:
                os.remove(zip_path)
                print(f"원본 파일이 삭제되었습니다: {zip_path} / Original file deleted: {zip_path}")
        except zipfile.BadZipFile:
            print(f"잘못된 ZIP 파일입니다: {zip_path} / Invalid ZIP file: {zip_path}")
        except FileNotFoundError:
            print(f"ZIP 파일을 찾을 수 없습니다: {zip_path} / ZIP file not found: {zip_path}")

    @staticmethod
    def extract_all(path: str, delete_original: bool = False) -> None:
        """
        폴더 내의 모든 ZIP 파일을 전부 압축 해제하는 함수입니다.
        Function to recursively extract all ZIP files in a folder.

        Args:
            path (str): 처리할 폴더 또는 ZIP 파일의 경로 / Path to the folder or ZIP file to process
            delete_original (bool): 압축 해제 후 원본 파일 삭제 여부. 기본값은 False입니다.
                                    Whether to delete the original files after extraction. Defaults to False.
        """
        if os.path.isfile(path) and path.lower().endswith(".zip"):
            # ZIP 파일인 경우 압축 해제
            ZipFile.extract_zip(path, delete_original=delete_original)
        elif os.path.isdir(path):
            # 디렉토리 내의 모든 항목을 처리
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path) and item_path.lower().endswith(".zip"):
                    # ZIP 파일인 경우 압축 해제
                    ZipFile.extract_zip(item_path, delete_original=delete_original)
                elif os.path.isdir(item_path):
                    # 하위 디렉토리인 경우 재귀적으로 처리
                    ZipFile.extract_all(item_path, delete_original)

        # 현재 디렉토리에서 새로 생성된 ZIP 파일 처리
        if os.path.isdir(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path) and item_path.lower().endswith(".zip"):
                    ZipFile.extract_zip(item_path, delete_original=delete_original)
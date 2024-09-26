import os
from typing import Optional, List
from PIL import Image
from pdf2image import convert_from_path
import io
from enum import Enum
from tqdm import tqdm
import multiprocessing

# PIL의 이미지 크기 제한을 늘립니다.
Image.MAX_IMAGE_PIXELS = 933120000  # 기본값의 2배

class FileFormat(Enum):
    """지원되는 파일 포맷"""
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    PDF = ".pdf"
    WEBP = ".webp"

class ImageConverter:
    """이미지 변환을 위한 클래스"""

    @staticmethod
    def convert_image(image_path: str,
                      max_size: Optional[int] = None,
                      output_format: FileFormat = FileFormat.JPEG,
                      output_path: Optional[str] = None,
                      keep_original: bool = True) -> str:
        """
        이미지 변환 메서드

        Args:
            image_path (str): 변환할 이미지 파일 경로
            output_format (FileFormat): 출력 파일 형식 (기본값: JPEG)
            output_path (Optional[str]): 출력 파일 경로 (기본값: None)
            keep_original (bool): 원본 파일 유지 여부 (기본값: True)
            max_size (Optional[int]): 최대 파일 크기 (KB) (기본값: None)

        Returns:
            str: 변환된 이미지 파일 경로 또는 여러 파일 경로를 쉼표로 구분한 문자열
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {image_path}")

        input_format = ImageConverter._from_extension(os.path.splitext(image_path)[1])

        if input_format == FileFormat.PDF:
            output_dir = os.path.dirname(output_path) if output_path else os.path.dirname(image_path)
            output_paths = ImageConverter.__convert_pdf_to_images(image_path, output_format, output_dir)
            if not keep_original:
                os.remove(image_path)
            return output_paths[0] if len(output_paths) == 1 else ", ".join(output_paths)

        if output_path is None:
            directory, filename = os.path.split(image_path)
            name, _ = os.path.splitext(filename)
            output_base = os.path.join(directory, name)
            output_path = ImageConverter._get_unique_filename(output_base, output_format.value)
        else:
            output_path = ImageConverter._get_unique_filename(output_path, output_format.value)

        with Image.open(image_path) as img:
            if max_size:
                img = ImageConverter._resize_image(img, max_size)
            ImageConverter._process_image(img, output_format, output_path, keep_original, image_path)

        return output_path

    @staticmethod
    def convert_images_in_folder(folder_path: str,
                                 output_format: FileFormat = FileFormat.JPEG,
                                 max_size: Optional[int] = None,
                                 keep_original: bool = True) -> None:
        """폴더 내 이미지 변환 메서드"""
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"유효한 디렉토리가 아닙니다: {folder_path}")

        files_to_convert = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        total_files = len(files_to_convert)

        print(f"총 {total_files}개의 파일을 처리합니다.")

        success_count = 0
        fail_count = 0

        with tqdm(total=total_files, desc="이미지 변환 중", unit="파일") as pbar:
            for filename in files_to_convert:
                file_path = os.path.join(folder_path, filename)
                try:
                    ImageConverter.convert_image(file_path, max_size=max_size, output_format=output_format, keep_original=keep_original)
                    success_count += 1
                    pbar.set_postfix({"성공": success_count, "실패": fail_count})
                except ValueError as e:
                    print(f"\n변환 실패 ({filename}): {str(e)}")
                    fail_count += 1
                except Exception as e:
                    print(f"\n예상치 못한 오류 발생 ({filename}): {str(e)}")
                    fail_count += 1
                pbar.update(1)

        print(f"\n변환 완료: 총 {total_files}개 중 {success_count}개 성공, {fail_count}개 실패")
        print(f"성공률: {success_count/total_files*100:.2f}%")

    @staticmethod
    def _from_extension(extension: str) -> FileFormat:
        """파일 확장자로부터 FileFormat을 반환"""
        normalized_ext = extension.lower()
        for format in FileFormat:
            if format.value == normalized_ext:
                return format
        raise ValueError(f"지원되지 않는 파일 형식입니다: {extension}")

    @staticmethod
    def _get_unique_filename(base_path: str, extension: str) -> str:
        """중복되지 않는 파일명 생성"""
        directory, filename = os.path.split(base_path)
        name, _ = os.path.splitext(filename)
        counter = 1
        new_path = os.path.join(directory, f"{name}{extension}")
        while os.path.exists(new_path):
            new_path = os.path.join(directory, f"{name}_{counter}{extension}")
            counter += 1
        return new_path

    @staticmethod
    def _process_image(img: Image.Image,
                       output_format: FileFormat,
                       output_path: str,
                       keep_original: bool,
                       image_path: str) -> None:
        """이미지 처리를 위한 내부 함수"""
        save_format = output_format.name if output_format != FileFormat.JPG else "JPEG"
        img.save(output_path, format=save_format)
        if not keep_original and output_path != image_path:
            os.remove(image_path)

    @staticmethod
    def _convert_single_pdf(args):
        pdf_path, page_num, output_format, output_dir, dpi = args
        images = convert_from_path(pdf_path, dpi=dpi, first_page=page_num, last_page=page_num)
        if images:
            base_name, _ = os.path.splitext(os.path.basename(pdf_path))
            output_base = os.path.join(output_dir, f"{base_name}_page_{page_num}")
            output_path = ImageConverter._get_unique_filename(output_base, output_format.value)
            images[0].save(output_path, format=output_format.name)
            return output_path
        return None

    @staticmethod
    def __convert_pdf_to_images(pdf_path: str, output_format: FileFormat, output_dir: str) -> List[str]:
        """PDF를 이미지로 변환하는 함수 (멀티프로세싱 적용)"""
        try:
            info = convert_from_path(pdf_path, dpi=300, first_page=1, last_page=1)
            num_pages = len(info)
            cpu_count = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=cpu_count)
            dpi = 300
            tasks = [(pdf_path, i, output_format, output_dir, dpi) for i in range(1, num_pages + 1)]
            output_paths = pool.map(ImageConverter._convert_single_pdf, tasks)
            pool.close()
            pool.join()
            return [path for path in output_paths if path]
        except Exception as e:
            print(f"PDF 변환 중 오류 발생: {str(e)}")
            return []

    @staticmethod
    def _resize_image(img: Image.Image, max_size: int) -> Image.Image:
        """이미지 크기를 효율적으로 조정하여 max_size 이하로 만드는 함수"""
        def get_size(image: Image.Image) -> float:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="JPEG", quality=95)
            return img_byte_arr.tell() / 1024

        original_size = get_size(img)
        if original_size <= max_size:
            return img

        scale = (max_size / original_size) ** 0.5
        while True:
            new_size = tuple(int(dim * scale) for dim in img.size)
            resized_img = img.resize(new_size, Image.LANCZOS)
            current_size = get_size(resized_img)
            if current_size <= max_size:
                return resized_img
            scale *= 0.9
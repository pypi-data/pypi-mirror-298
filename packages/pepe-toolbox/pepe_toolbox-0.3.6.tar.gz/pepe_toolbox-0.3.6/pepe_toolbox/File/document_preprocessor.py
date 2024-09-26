import cv2
import numpy as np

class DocumentPreprocessor:
    """
    문서 전처리를 위한 클래스
    """

    @staticmethod
    def remove_noise(image):
        """
        이미지에서 노이즈를 제거합니다.
        :param image: 입력 이미지
        :return: 노이즈가 제거된 이미지
        """
        # 그레이스케일 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # GaussianBlur를 사용하여 노이즈 제거
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)
        return denoised


    @staticmethod
    def deskew(image):
        """
        이미지의 기울기를 보정합니다.
        :param image: 입력 이미지
        :return: 기울기가 보정된 이미지
        """
        # 그레이스케일 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 이진화
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # 좌표 추출
        coords = np.column_stack(np.where(thresh > 0))
        # 최소 외접 사각형으로 각도 계산
        angle = cv2.minAreaRect(coords)[-1]
        # 각도 보정
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        # 회전 매트릭스 생성 및 이미지 회전
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC,
                                borderMode=cv2.BORDER_REPLICATE)
        return rotated


    @staticmethod
    def binarize_image(image):
        """
        이미지를 이진화합니다.
        :param image: 입력 이미지
        :return: 이진화된 이미지
        """
        # 그레이스케일 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Otsu 이진화를 사용하여 이미지 이진화
        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary


    @staticmethod
    def resize_image(image, width=None, height=None):
        """
        이미지의 크기를 조정합니다.
        :param image: 입력 이미지
        :param width: 새로운 폭 (옵션)
        :param height: 새로운 높이 (옵션)
        :return: 크기가 조정된 이미지
        """
        if width is None and height is None:
            return image
        (h, w) = image.shape[:2]
        if width is None:
            ratio = height / float(h)
            dimension = (int(w * ratio), height)
        else:
            ratio = width / float(w)
            dimension = (width, int(h * ratio))
        resized = cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)
        return resized


    @staticmethod
    def adjust_contrast_brightness(image, contrast=1.0, brightness=0):
        """
        이미지의 대비와 밝기를 조정합니다.
        :param image: 입력 이미지
        :param contrast: 대비 비율
        :param brightness: 밝기 값
        :return: 조정된 이미지
        """
        adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
        return adjusted


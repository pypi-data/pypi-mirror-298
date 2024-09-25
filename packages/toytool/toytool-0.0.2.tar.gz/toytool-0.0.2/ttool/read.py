import cv2
import typing
from PIL import Image

def ReadImage(ImagePath: str, Mode: str = 'cv2') -> typing.Any:
    """Read image in one manner of opencv or pillow.

    Args:
        ImagePath: img file path.
        Mode: one of ['pillow', 'cv2'].
    """
    if mode == 'pillow':
        img = Image.open(ImagePath)
    elif mode == "opencv":
        img = cv2.imread(ImagePath)
    return img
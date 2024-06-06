from PIL import Image


def process_image(image):
    if not image:
        return None

    try:
        img = Image.open(image)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img = img.resize((500, 500))

        return img
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")

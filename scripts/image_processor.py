from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image

processor = AutoProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = AutoModelForVision2Seq.from_pretrained("microsoft/trocr-base-handwritten")

def extract_text_from_image(image_path):
    """Извлечение текста из изображения с помощью TrOCR"""
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

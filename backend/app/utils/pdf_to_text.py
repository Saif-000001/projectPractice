import easyocr
import fitz
import numpy as np
from app.utils.language_detection import detect_language

def pdf_to_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    full_text = ""
    
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        
        # Detect language of the page
        page_text = " ".join([word[4] for word in page.get_text("words")])
        lang = detect_language(page_text)
        
        # Choose appropriate reader based on detected language
        if lang in ['bn']:
            reader = easyocr.Reader(['bn', 'en'])
        elif lang in ['zh-cn', 'zh-tw', 'ja', 'ko']:
            reader = easyocr.Reader(['ch_sim', 'ch_tra', 'ja', 'ko', 'en'])
        elif lang in ['ru', 'bg', 'be', 'uk']:
            reader = easyocr.Reader(['ru', 'bg', 'be', 'uk', 'en'])
        elif lang in ['cs', 'pl', 'sk']:
            reader = easyocr.Reader(['cs', 'pl', 'sk', 'en'])
        elif lang in ['da', 'no', 'sv']:
            reader = easyocr.Reader(['da', 'no', 'sv', 'en'])
        elif lang in ['nl', 'de']:
            reader = easyocr.Reader(['nl', 'de', 'en'])
        elif lang in ['fr', 'it', 'es', 'pt']:
            reader = easyocr.Reader(['fr', 'it', 'es', 'pt', 'en'])
        else:
            reader = easyocr.Reader(['en', 'fr', 'es', 'de', 'it', 'pt', 'nl'])
        
        result = reader.readtext(img)
        page_text = " ".join([text[1] for text in result])
        full_text += page_text + "\n\n"
    
    pdf_document.close()
    return full_text

# Example usage
p = pdf_to_text('Bn.pdf')
print(p)
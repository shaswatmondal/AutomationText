import os
import time
from PIL import Image
import pywhatkit
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# class AIImageGenerator:
#     def __init__(self):
#         self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#     def generate_image(self, prompt):
#         print("Generating image via Gemini 3 Pro Image (Nano Banana)...")
        
#         try:
#             response = self.client.models.generate_content(
#                 model='gemini-3-pro-image-preview',
#                 contents=prompt,
#                 config=types.GenerateContentConfig(
#                     response_modalities=["IMAGE"],
#                 )
#             )

#             image_path = "generated_image.png"
#             found_image = False
            
#             for part in response.parts:
#                 if part.inline_data:
#                     img = part.as_image()
#                     img.save(image_path)
#                     found_image = True
#                     break
            
#             if found_image:
#                 print("Image saved successfully!")
#                 return image_path
#             else:
#                 print("Model responded but no image was found (check safety filters).")
#                 return None
                
#         except Exception as e:
#             print(f"Error: {e}")
#             return None

# class ImageConverter:
#     def convert_to_jpg(self, png_path):
#         if not png_path: return None
#         print("Converting to JPG...")
#         img = Image.open(png_path)
#         rgb_img = img.convert('RGB')
#         jpg_path = "final_image.jpg"
#         rgb_img.save(jpg_path)
#         print("Converted to JPG")
#         return jpg_path

class WhatsAppSender:
    def send_text(self,prompt,phone):
    
        
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=prompt,
            wait_time=20,
            tab_close=True  # Automatically closes the browser tab after sending
        )
        print("Text sent successfully!")

if __name__ == "__main__":
    prompt = input("Enter Text prompt: ")
    phone = input("Enter phone number (+91xxxxxxxxxx): ")

    # generator = AIImageGenerator()
    # converter = ImageConverter()
    sender = WhatsAppSender()
    sender.send_text(prompt,phone)

    # png_file = generator.generate_image(prompt)
    
    # if png_file:
        # jpg_file = converter.convert_to_jpg(png_file)
        # time.sleep(2) 
        # sender.send_image(phone, jpg_file)
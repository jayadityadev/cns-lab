import os
from PIL import Image, ImageDraw

os.makedirs('report/figures/code', exist_ok=True)
os.makedirs('report/figures/screenshots', exist_ok=True)

def create_placeholder(path, width, height, title, subtitle=''):
    img = Image.new('RGB', (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)
    # Draw double border with KSIT maroon accent
    draw.rectangle([(2, 2), (width-3, height-3)], outline=(128, 0, 0), width=3)
    draw.rectangle([(8, 8), (width-9, height-9)], outline=(180, 190, 200), width=1)
    
    # Text
    draw.text((width // 2, height // 2 - 20), title, fill=(40, 50, 60), anchor='mm')
    if subtitle:
        draw.text((width // 2, height // 2 + 20), subtitle, fill=(100, 110, 120), anchor='mm')
    
    img.save(path)
    print(f'Created: {path}')

if __name__ == '__main__':
    # 1. Team Presentation
    create_placeholder('report/figures/team_presentation.jpg', 1200, 750, 
                       'PROJECT PRESENTATION PHOTOGRAPH', 
                       'Drop presentation photo (JPEG/PNG) here')

    # 2. Code Snippets
    code_snippets = [
        ('report/figures/code/listing4_1_caesar.jpg', 'Listing 4.1: Caesar Cipher Core Logic (JPEG)'),
        ('report/figures/code/listing4_2_vigenere.jpg', 'Listing 4.2: Vigenere Cipher Core Logic (JPEG)'),
        ('report/figures/code/listing4_3_otp.jpg', 'Listing 4.3: One-Time Pad Stream Logic (JPEG)'),
        ('report/figures/code/listing4_4_rsa.jpg', 'Listing 4.4: RSA-PSS Digital Signature Logic (JPEG)'),
    ]
    for p, t in code_snippets:
        create_placeholder(p, 900, 550, t, 'Drop Code Snippet Screenshot Here')

    # 3. Execution Screenshots
    screenshots = [
        ('report/figures/screenshots/screenshot_01_tui_main.png', 'Figure 5.1: Interactive TUI Menu (main.py)', 'Drop Terminal Screenshot Here'),
        ('report/figures/screenshots/screenshot_02_caesar.png', 'Figure 5.2: Caesar Cipher CLI Execution', 'Drop Terminal Screenshot Here'),
        ('report/figures/screenshots/screenshot_03_vigenere.png', 'Figure 5.3: Vigenere Cipher CLI Execution', 'Drop Terminal Screenshot Here'),
        ('report/figures/screenshots/screenshot_04_otp.png', 'Figure 5.4: One-Time Pad & Two-Time Pad Attack', 'Drop Terminal Screenshot Here'),
        ('report/figures/screenshots/screenshot_05_signature.png', 'Figure 5.5: RSA-PSS Digital Signature & Tamper Detection', 'Drop Terminal Screenshot Here'),
    ]
    for p, t, s in screenshots:
        create_placeholder(p, 1100, 500, t, s)

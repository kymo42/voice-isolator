from PIL import Image
import os

# Convert SL.png to SpeakerLove.ico
if os.path.exists('SL.png'):
    # Open the PNG file
    img = Image.open('SL.png')
    
    # Convert to RGB if necessary (remove alpha channel)
    if img.mode in ('RGBA', 'LA'):
        # Create a white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
        else:
            background.paste(img, mask=img.split()[-1])
        img = background
    
    # Resize to standard icon sizes
    sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    img_resized = []
    
    for size in sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        img_resized.append(resized)
    
    # Save as ICO file
    img_resized[0].save('SpeakerLove.ico', format='ICO', 
                       sizes=[(s.width, s.height) for s in img_resized],
                       append_images=img_resized[1:])
    
    print("Successfully created SpeakerLove.ico from SL.png")
else:
    print("SL.png not found in current directory")
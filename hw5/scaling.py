from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def bilinear_resize(img_array, new_height, new_width):
    height, width = img_array.shape[:2]
    channels = img_array.shape[2] if len(img_array.shape) == 3 else 1
    
    resized = np.zeros((new_height, new_width, channels), dtype=img_array.dtype)
    
    for i in range(new_height):
        for j in range(new_width):
            if new_height > 1:
                x = (i / (new_height - 1)) * (height - 1)
            else:
                x = 0
            if new_width > 1:
                y = (j / (new_width - 1)) * (width - 1)
            else:
                y = 0
            
            x0 = int(x)
            y0 = int(y)
            x1 = min(x0 + 1, height - 1)
            y1 = min(y0 + 1, width - 1)
            
            wx = x - x0
            wy = y - y0
            
            for c in range(channels):
                resized[i, j, c] = (1 - wx) * (1 - wy) * img_array[x0, y0, c] + \
                                   wx * (1 - wy) * img_array[x1, y0, c] + \
                                   (1 - wx) * wy * img_array[x0, y1, c] + \
                                   wx * wy * img_array[x1, y1, c]
    
    return resized.astype(np.uint8)

def scale_image(input_path, new_width, new_height):
    img = Image.open(input_path)
    img_array = np.array(img)
    
    resized_array = bilinear_resize(img_array, new_height, new_width)
    resized_img = Image.fromarray(resized_array)
    
    plt.imshow(resized_img)
    plt.title(f"Resized Image ({new_width}x{new_height})")
    plt.axis('off')
    plt.show()
    
    print(f"Resized image displayed. Original size: {img.size}, New size: {resized_img.size}")

if __name__ == "__main__":
    input_file = "image.jpeg"
    new_width = 360
    new_height = 240
    
    scale_image(input_file, new_width, new_height)

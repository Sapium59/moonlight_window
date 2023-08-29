from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os


# config
pix_per_char = 300
font = ImageFont.truetype("simhei.ttf" , pix_per_char)  # Font type
bg_color = (255, 255, 255)      # white
ans_color = (0, 0, 0)           # black
char_color = (0, 0, 255)        # blue
split_color = (127, 127, 127)   # gray

os.makedirs("output", exist_ok=True)


while True:
    chars = input("月照纱窗:\n")
    # chars = "月照纱窗"

    if len(chars) >= 10:
        print(f"Fail! {chars} is too long!")
        

    char_num = len(chars)
    image = Image.new('RGB', (char_num * pix_per_char, pix_per_char), ans_color)
    draw = ImageDraw.Draw(image)


    # get answer image step 1: write characters on answer color
    for idx, char in enumerate(chars):
        position = (idx * pix_per_char, 0)
        draw.text(position, char, font=font, fill=char_color)

    # get answer image step 2: make the characters bi-valued (preperation for flood)
    img_arr = np.array(image)
    mask = (img_arr==char_color).astype(np.uint8).sum(axis=-1)==3
    mask3 = np.dstack([mask.astype(np.uint8)]*3)
    img_arr_dyed = np.array(char_color).astype(np.uint8).reshape((1, 1, 3)) * mask3
    image = Image.fromarray(img_arr_dyed)
    draw = ImageDraw.Draw(image)

    # get answer image step 3: dye background with flood
    ImageDraw.floodfill(image, (0, 0), value=bg_color)

    # get answer image step 4: split characters from each other
    for idx in range(1, char_num):
        xy = (idx * pix_per_char, 0, idx * pix_per_char, pix_per_char)
        draw.line(xy, fill=split_color)
    image.save(f"output/{chars}_A.png")


    # get question image step 1: dye background
    img_arr = np.array(image)
    mask = (img_arr!=ans_color).astype(np.uint8).sum(axis=-1)!=0
    mask3 = np.dstack([mask.astype(np.uint8)]*3)
    img_arr_dyed = np.array(bg_color).astype(np.uint8).reshape((1, 1, 3)) * mask3
    image = Image.fromarray(img_arr_dyed)
    draw = ImageDraw.Draw(image)

    # get question image step 2: split characters from each other
    for idx in range(1, char_num):
        xy = (idx * pix_per_char, 0, idx * pix_per_char, pix_per_char)
        draw.line(xy, fill=split_color)
    image.save(f"output/{chars}_Q.png")


    print(f"Success! Please refer to output/{chars}_Q.png and output/{chars}_A.png")
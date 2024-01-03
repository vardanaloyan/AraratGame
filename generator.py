from PIL import Image, ImageFont

text = "Hello world!"
font_size = 36
font_filepath = "/Library/Fonts/TheSansSwisscom_37_TT.ttf"
color = (0, 255, 0, 155)

def gen_image_from_text(text):
    font = ImageFont.truetype(font_filepath, size=font_size)
    mask_image = font.getmask(text, "L")
    img = Image.new("RGBA", mask_image.size)
    img.im.paste(color, (0, 0) + mask_image.size, mask_image)  # need to use the inner `img.im.paste` due to `getmask` returning a core
    img.save(f"{i}.png")
    
for i in range(30, 31):
    gen_image_from_text(str(i))
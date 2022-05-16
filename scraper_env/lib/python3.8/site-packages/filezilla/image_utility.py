from PIL import Image

def image_resizer(input_path,h,w,output_path):
    img = Image.open(input_path)
    if h==None and w==None:
        img.save(output_path)
    elif h==None:
        wpercent = (w/float(img.size[0]))
        hsize = int(float(wpercent)*(float(img.size[1])))
        img = img.resize((w,hsize),Image.ANTIALIAS)
        img.save(output_path)
    elif w==None:
        hpercent = (h/float(img.size[1]))
        wsize = int(float(hpercent)*(float(img.size[0])))
        img = img.resize((wsize,h),Image.ANTIALIAS)
        img.save(output_path)
    else:
        img = img.resize((w,h),Image.ANTIALIAS)
        img.save(output_path)

def image_compressor(input_path,output_path):
    img = Image.open(input_path)
    img.save(output_path,optimize=True,quality=75)

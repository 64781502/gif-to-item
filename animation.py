from PIL import Image
from enum import Enum
import os, sys, glob, shutil

class Message(Enum):
    SUCCESS = f"[+] "
    INFO = f"[+] "
    WARNING = f"[!] "
    ERROR = f"[-] "
    

if len(sys.argv) <= 1:
    print(Message.ERROR.value + "Didn't specify a file")
    
    input()
    exit()

FILE = sys.argv[1].split('\\')[-1]

def gif_frames(gif_path):
    with Image.open(gif_path) as img:
        try:
            img.seek(1)
        except EOFError:
            return None

        frames = img.n_frames

        return frames


def gen_mcmeta():
    frames = gif_frames(FILE)

    frame_data = ""

    for x in range(frames):
        frame_data += f"{x}"
    
        if x != frames - 1:
            frame_data += ","

    json_string = '{"animation":{"frametime":1,"frames":[' + frame_data + ']}}'

    f = open(FILE.split('.')[0] + '.png.mcmeta', 'w')
    f.write(json_string)
    f.close()

def cleanup():
    shutil.rmtree("temp")


def combine_images():
    input_files = []
    
    for x in glob.glob('temp/*.png'):
        input_files.append(x)

    images = [Image.open(path) for path in input_files]

    width, height = images[0].size

    combined_image = Image.new('RGBA', (width, height * len(images)))

    for i, img in enumerate(images):
        combined_image.paste(img, (0, i * height))

    combined_image.save(FILE.split('.')[0] + '.png')


def gif_to_images():
    if not os.path.exists("temp"): 
        os.makedirs("temp") 
    
    digit = len(str(gif_frames(FILE)))
    
    os.system(f"ffmpeg -i {FILE} temp/{FILE.split('.')[0]}_%0{digit}d.png -hide_banner -loglevel error")


def main():
    gif = Image.open(FILE)
    
    if gif.width != gif.height:
        print(Message.ERROR.value + "Input gif is not square (1x1)")
        input()
        exit()

    gen_mcmeta()
    gif_to_images()
    combine_images()
    cleanup()


if __name__ == "__main__":
    main()

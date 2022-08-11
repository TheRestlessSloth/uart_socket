from PIL import Image, ImageFile, ImageOps
import numpy as np
import scipy.fftpack as fp


class PictureModule:
    def read_pic(self, path):
        file = Image.open(path)
        file.show()
        print(file.format)
        print(file.mode)

    def send_pic(self, path, send_to):
        file = open(path, "rb")
        p = ImageFile.Parser()
        while 1:
            s = file.read(1024)
            if not s:
                break
            p.feed(s)
            send_to.tx(s)
        p.close()

    def send_pic_fft(self, path, send):
        with Image.open(path) as im:
            im = ImageOps.grayscale(im)
            im = np.fft.fft(im)
            p = ImageFile.Parser()
            while 1:
                s = im.read(1024)
                if not s:
                    break
                p.feed(s)
                send.tx(s)
            p.close()
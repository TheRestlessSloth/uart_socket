from PIL import Image, ImageFile

class PictureModule:
    def read_pic(self, path):
        file = Image.open(path)
        file.show()
        print(file.format)
        print(file.mode)

    def send_pic(self, path, send):
        file = open(path, "rb")
        p = ImageFile.Parser()
        while 1:
            s = file.read(1024)
            if not s:
                break
            p.feed(s)
            send(s)
        p.close()
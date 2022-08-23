encoding = "ascii"

class ComModule: 
    def hash_sum(self,data):
        bytearr = bytearray(data.encode("ascii"))
        hs = bytearr[0]
        for byte in bytearr[1:len(bytearr)]: hs = hs^byte
        hs = hex(hs)
        return hs[2:4].upper()

    def str2hex(self,data):
        mes = "0x"
        bytearr = bytearray(data.encode("ascii"))
        for byte in bytearr: mes += hex(byte)[2:4]
        return mes

    def command(self,id,body):
        id = id
        body = body
        mes_body = f"PUWV{id},{body}"
        hs = self.hash_sum(mes_body)
        return f"${mes_body}*{hs}"
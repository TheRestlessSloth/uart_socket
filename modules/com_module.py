encoding = "ascii"

class ComModule: 
    def hash_sum(self,data):
        bytearr = bytearray(data.encode("ascii"))
        hs = bytearr[0]
        for byte in bytearr[1:len(bytearr)]:
            hs = hs^byte
        hs = hex(hs)
        return hs[2:4]

    def command(self,id,body):
        id = id
        body = body
        mes_body = f"PUVW{id},{body}"
        hs = self.hash_sum(mes_body) 
        print(f"${mes_body}*{hs}<CR><LF>")
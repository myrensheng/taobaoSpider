class Login():
    def __init__(self):
        self.name = "zs"


class Userinfos(Login):
    useronfo = {}
    def __init__(self):
        Login.__init__(self)
        self.parse()
    def parse(self):
        self.useronfo["sex"]="man"


a = Login()
print(a.name)

b = Userinfos()
print(b.useronfo)

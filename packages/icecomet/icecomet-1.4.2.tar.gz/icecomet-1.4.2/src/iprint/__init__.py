import os
import inspect

class color_text:
    def __init__(self) -> None:
        self.gray = '\033[90m'
        self.red = '\033[91m'
        self.green = '\033[92m'
        self.yello = '\033[93m'
        self.blue = '\033[94m'
        self.magenta = '\033[95m'
        self.sky = '\033[96m'
        self.white = '\033[97m'


        self.grayk = '\033[100m'
        self.redk = '\033[101m'
        self.greenk = '\033[102m'
        self.yellok = '\033[103m'
        self.bluek = '\033[104m'
        self.magentak = '\033[105m'
        self.skyk = '\033[106m'
        self.whitek = '\033[107m'

        self.set = '\033[0m'
        self.ijset = '\033[92m'
        self.jiset = '\033[93m'
    def show(self):
        print(f"{self.gray}gray {self.red}red {self.green}green {self.yello}yello {self.blue}blue {self.magenta}magenta {self.sky}sky {self.white}white {self.set}")
        print(f"{self.grayk}gray {self.redk}red {self.greenk}green {self.yellok}yello {self.bluek}blue {self.magentak}magenta {self.skyk}sky {self.whitek}white {self.set}")
ct = color_text()

class ij_status:
    def __init__(self,tag=0,len=0,type=0,line=0,path=0,round=0,var=0,color=ct.green,end='\n'):
        self.tag = tag
        self.len = len
        self.type = type
        self.line = line
        self.path = path
        self.round = round
        self.var = var
        self.color = color
        self.end = end
        self.npass = 0

class base_color:
    def __init__(self):
        self.cprint = ct.green
        self.ij=ct.green
        self.ji=ct.yello
        self.jk=ct.red
        self.set=ct.set

cb = base_color()

def oncode():
    current_file_path = os.path.abspath(__file__)
    directory = os.path.dirname(current_file_path)
    os.chdir(directory)


def cprint(*arg,color=cb.cprint):
    string = ' '.join([str(i) for i in arg])
    print(f'{color}{string}{ct.set}')


ij_global = {}
def ij(tag='',mode='',c=cb.ij,end='\n'):
    global ij_global
    if tag not in ij_global.keys():
        if mode=='full':mode='iltaprv'
        ij_global[tag] = ij_status(color=c,end=end)
        if 'i' in mode:ij_global[tag].tag = 1
        if 'l' in mode:ij_global[tag].len = 1
        if 't' in mode:ij_global[tag].type = 1
        if 'a' in mode:ij_global[tag].line = 1
        if 'p' in mode:ij_global[tag].path = 1
        if 'r' in mode:ij_global[tag].round = 1
        if 'v' in mode:ij_global[tag].var = 1
    if tag=='':#ถ้าใช้ ij()
        string=f'Passed : {ij_global[tag].npass}'
    elif mode=='':string=f'{tag}'
    elif 's' in mode:return None
    else :
        string=f''
        if ij_global[tag].tag : string=string+f'{tag}  \n'
        if ij_global[tag].len : string=string+f'[len : {len(tag)}  ]'
        if ij_global[tag].type :string=string+f'[type : {type(tag)}  ]'
        if ij_global[tag].round :string=string+f'[Passed : {ij_global[tag].npass}  ]'
        if ij_global[tag].line :
            frame = inspect.currentframe().f_back
            info = inspect.getframeinfo(frame)
            string+=f'[At Line {info.lineno}  ]'
        if ij_global[tag].path :
            current_file_path = os.path.abspath(__file__)
            string+=f'\n{current_file_path}  '
    ij_global[tag].npass+=1
    print(c+string+cb.set)
    return tag


ji_global = {}
def ji(tag='',mode='',c=cb.ji,end='\n'):
    global ji_global
    if tag not in ji_global.keys():
        if mode=='full':mode='iltaprv'
        ji_global[tag] = ij_status(color=c,end=end)
        if 'i' in mode:ji_global[tag].tag = 1
        if 'l' in mode:ji_global[tag].len = 1
        if 't' in mode:ji_global[tag].type = 1
        if 'a' in mode:ji_global[tag].line = 1
        if 'p' in mode:ji_global[tag].path = 1
        if 'r' in mode:ji_global[tag].round = 1
        if 'v' in mode:ji_global[tag].var = 1
    if tag=='':#ถ้าใช้ ji()
        string=f'Passed : {ji_global[tag].npass}'
    elif mode=='':string=f'{tag}'
    elif 's' in mode:return None
    else :
        string=f''
        if ji_global[tag].tag : string=string+f'{tag}  \n'
        if ji_global[tag].len : string=string+f'[len : {len(tag)}  ]'
        if ji_global[tag].type :string=string+f'[type : {type(tag)}  ]'
        if ji_global[tag].round :string=string+f'[Passed : {ji_global[tag].npass}  ]'
        if ji_global[tag].line :
            frame = inspect.currentframe().f_back
            info = inspect.getframeinfo(frame)
            string+=f'[At Line {info.lineno}  ]'
        if ji_global[tag].path :
            current_file_path = os.path.abspath(__file__)
            string+=f'\n{current_file_path}  '
    ji_global[tag].npass+=1
    print(c+string+cb.set)
    return tag

jk_global = {}
def jk(tag='',mode='',c=cb.jk,end='\n'):
    global jk_global
    if tag not in jk_global.keys():
        if mode=='full':mode='iltaprv'
        jk_global[tag] = ij_status(color=c,end=end)
        if 'i' in mode:jk_global[tag].tag = 1
        if 'l' in mode:jk_global[tag].len = 1
        if 't' in mode:jk_global[tag].type = 1
        if 'a' in mode:jk_global[tag].line = 1
        if 'p' in mode:jk_global[tag].path = 1
        if 'r' in mode:jk_global[tag].round = 1
        if 'v' in mode:jk_global[tag].var = 1
    if tag=='':#ถ้าใช้ jk()
        string=f'Passed : {jk_global[tag].npass}'
    elif mode=='':string=f'{tag}'
    elif 's' in mode:return None
    else :
        string=f''
        if jk_global[tag].tag : string=string+f'{tag}  \n'
        if jk_global[tag].len : string=string+f'[len : {len(tag)}  ]'
        if jk_global[tag].type :string=string+f'[type : {type(tag)}  ]'
        if jk_global[tag].round :string=string+f'[Passed : {jk_global[tag].npass}  ]'
        if jk_global[tag].line :
            frame = inspect.currentframe().f_back
            info = inspect.getframeinfo(frame)
            string+=f'[At Line {info.lineno}  ]'
        if jk_global[tag].path :
            current_file_path = os.path.abspath(__file__)
            string+=f'\n{current_file_path}  '
    jk_global[tag].npass+=1
    print(c+string+cb.set)
    return tag






def iprint():
    print('value len type line path round isvar')
    print('i     l   t    a    p    r     v')









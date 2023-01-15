import getpass
import os
import keyboard

class File():
    def __init__(self):
        self.name=""
        self.size=0
        self.permission=""
        self.owner=""
        self.use=""
        
    def setName(self,name):
        self.name=name
    
    def getName(self):
        return self.name

    def setSize(self,size):
        self.size=size
    
    def getSize(self):
        return self.size
    
    def setPermission(self,permission):
        self.permission=permission
        
    def getPermission(self):
        return self.permission
    
    def setOwner(self,owner):
        self.owner=owner
        
    def getOwner(self):
        return self.owner
    
    def setUse(self,use):
        self.use=use    
    
    def getUse(self):
        return self.use

class MyDir():
    def __init__(self):
        self.Name = ""
        self.Size = 0
        self.fileList = []
        self.permission = ""
        self.owner = ""
    
    def setName(self,Name):
        self.Name = Name
    
    def getName(self):
        return self.Name
    
    def setSize(self,Size):
        self.Size = Size
        
    def getSize(self):
        self.dirSize = os.path.getsize("F:\\Desktop_From_C\\OSCourseDesign\\"+self.Name.replace('/','\\'))
        return self.dirSize
    
    def setFileList(self,fileList):
        self.fileList = fileList
        
    def getFileList(self):
        # self.fileList = os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.Name.replace('/','\\'))
        return self.fileList
    
    def setPermission(self,permission):
        self.permission = permission
    
    def getPermission(self):
        return self.permission

    def setOwner(self,owner):
        self.owner = owner
    
    def getOwner(self):
        return self.owner
    
class User():
    def __init__(self):
        f=open("F:\\Desktop_From_C\\OSCourseDesign\\root\\user.txt","r")
        string=f.readline()
        self.userName=string.split(" ")[0]
        self.pw=string.split(" ")[1].split("\n")[0]
        
    def setName(self,Name):
        self.name = Name
    
    def getName(self):
        return self.name
    
    def setPassword(self,Password):
        self.pw = Password
    
    def getPassword(self):
        return self.pw
    
    def setType(self,Type):
        self.type = Type
    
    def getType(self):
        return self.type
    
class FileSys():
    user = User()
    currentDir = MyDir()
    
    def __init__(self):
        self.user.setName("root")
        self.user.setPassword("123456")
        self.user.setType("root")
        
        self.currentDir.setName(self.user.getName())
        self.currentDir.setFileList(os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\root"))
        self.currentDir.setPermission("77")
        
    def login(self,pw):
        if pw == self.user.getPassword():
            print("Login successfully!")
            return True
        else:
            print("Login failed!")
            return False
    
    # 是否有权限    
    def matchPermission(self,permission:str,num:str):
        if self.user.getType() == "root" and permission[0] == num:
            return True
        elif self.user.getType() == "user" and permission[1] == num:
            return True
        else:
            return False
    
    # 创建文件
    def createFile(self,kw:str):
        try:
            name = kw.split(" ")[1]
        except:
            print("Incomplete command!")
            return
        if self.matchPermission(self.currentDir.getPermission(),"7") or self.matchPermission(self.currentDir.getPermission(),"3"):
            if "/" not in name:
                if name not in self.currentDir.getFileList():
                    permission = "76"
                    f = File()
                    f.setName(name)
                    f.setOwner(self.user.getName())
                    f.setPermission(permission)
                    self.currentDir.fileList.append(f)
                    open(f.getName(),"w")
                    self.currentDir.setFileList(os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')))
                else:
                    print("File already exists!")
            else:
                print("Invalid file name!")
        else:
            print("Permission denied!")
    
    # 删除文件        
    def delFile(self,kw:str):
        try:
            name = kw.split(" ")[1]
        except:
            print("Incomplete command!")
            return
        flag=False
        if self.matchPermission(self.currentDir.getPermission(),"7"):
            for f in self.currentDir.getFileList():
                if name == f:
                    self.currentDir.fileList.remove(f)
                    os.remove("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name)
                    flag=True
                    break
            if flag==False:
                print("No such file!")
        else:
            print("Permission denied!")
    
    # 重命名文件
    def renameFile(self,kw:str):
        try:
            name = kw.split(" ")[1]
            newName = kw.split(" ")[2]
        except:
            print("Incomplete command!")
            return
        flag=False
        for f in self.currentDir.getFileList():
            if name == f:
                if "/" not in newName:
                    if newName in self.currentDir.getFileList():
                        print("File already exists!")
                        flag=True
                        break
                    else:
                        self.currentDir.fileList.remove(name)
                        self.currentDir.fileList.append(newName)
                        os.rename("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name,"F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+newName)
                        flag=True
                        break
                else:
                    print("Invalid file new name!")
                    break
        if flag==False:
            print("No such file!")
    
    # 复制文件    
    def copyFile(self,kw:str):
        try:
            name = kw.split(" ")[1]
            newName = kw.split(" ")[2]
        except:
            print("Incomplete command!")
            return
        if self.matchPermission(self.currentDir.getPermission(),"7" or "2" or "3"):
            flag=False
            for f in self.currentDir.fileList:
                if name == f:
                    if "/" not in newName:
                        if newName in self.currentDir.fileList:
                            print("File already exists!")
                            flag=True
                            break
                        else:
                            self.currentDir.fileList.append(newName)
                            f1 = open("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name,"r",encoding="utf-8")
                            f2 = open("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+newName,"w",encoding="utf-8")
                            f2.write(f1.read()) 
                            f2.close()  
                            f1.close()
                            flag=True
                            break
                    else:
                        print("Invalid file new name!")
                        break
            if flag==False:
                    print("No such file!")
        else:
            print("Permission denied!")

    # 读取文件
    def readFile(self,kw:str):
        flag=False
        try:
            name = kw.split(" ")[1]
        except:
            print("Incomplete command!")
            return
        path="F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name
        for f in self.currentDir.fileList:
            if name == f:
                if os.access(path,os.R_OK):
                    print("文件名："+name+" 文件大小："+str(os.path.getsize("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name))+" 字节")
                    os.system("pause")
                    os.system("cls")
                    f = open("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name,"r")
                    print(f.read())
                    f.close()
                    flag=True
                    break
                else:
                    print("Permission denied!")    
        if flag==False:
            print("No such file!")

    # 编辑文件
    def editFile(self,kw:str):
        try:
            name = kw.split(" ")[1]
        except:
            print("Incomplete command!")
            return
        flag=False
        if os.access("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name,os.W_OK):
            for f in self.currentDir.fileList:
                if name == f and name.getUse() == False:
                    name.setUse(True)
                    os.system("cls")
                    f = open("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name,"a+")
                    f1 = open("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name,"r")
                    print(f1.read())
                    content=""
                    while True:
                        temp=input()
                        if temp == ":wq":
                            break
                        elif temp == ":q":
                            content=""
                            break
                        else:
                            content += temp+"\n"
                    f.write(content)
                    f.close()
                    name.setUse(False)
                    flag=True
                    break
                else:
                    print("File is being used!")
            if flag==False:
                print("No such file!")
        else:
            print("Permission denied!")
    
    # 创建目录
    def createDir(self,kw:str):
        try:
            name = kw.split(" ")[1]
        except:
            print("Incomplete command!")
            return
        if self.matchPermission(self.currentDir.getPermission(),"7") or self.matchPermission(self.currentDir.getPermission(),"3"):
            if "/" not in name:
                if name in self.currentDir.getFileList():
                    print("Dir already exists!")
                    return
                else:
                    dir = MyDir()
                    dir.setName(name)
                    dir.setOwner(self.user.getName())
                    dir.setPermission("76")
                    self.currentDir.fileList.append(dir)
                    os.mkdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name)
                    self.currentDir.setFileList(os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')))
            else:
                print("Invalid dir name!")
        else:
            print("Permission denied!")
    
    # 删除目录
    def delDir(self,kw:str):
        flag=False
        try:
            name = kw.split(" ")[1]
        except:
            print("Incomplete command!")
            return
        if self.matchPermission(self.currentDir.getPermission(),"7"):
            for f in self.currentDir.fileList:
                if name == f:
                    self.currentDir.fileList.remove(f)
                    os.rmdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name)
                    flag=True
                    break
            if flag==False:
                print("No such dir!")
        else:
            print("Permission denied!")

    # 罗列文件
    def listFile(self):
        if self.matchPermission(self.currentDir.getPermission(),"7" or "4" or "5"):
            if self.currentDir.fileList==[]:
                print()
            else:
                for f in self.currentDir.fileList:
                    if f == self.currentDir.fileList[-1]:
                        if "." in f and f[0] !=".":
                            print(f)
                        else:
                            print("\033[1;34;40m"+f+"\033[0m")
                    else:
                        if "." in f and f[0]!=".":
                            print(f,end=" ")
                        else:
                            print("\033[1;34;40m"+f+"\033[0m",end=" ")
        else:
            print("Permission denied!")

    # 进入目录
    def intoDir(self,kw:str):
        try:
            name = kw.split(" ")[1]
        except:
            print("Incomplete command!")
            return
        if name == "" or name == " ":
            print("Incomplete command!")
            return
        flag=False
        if self.matchPermission(self.currentDir.getPermission(),"7" or "3" or "5" or "1"):
            for f in self.currentDir.fileList:
                if name == f:
                    self.currentDir.setName(self.currentDir.getName()+"/"+f)
                    self.currentDir.setFileList(os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')))
                    flag=True
                    break
            if flag==False:
                print("No such dir!")
        else:
            print("Permission denied!")

    # 返回上一级目录
    def backDir(self):
        if self.matchPermission(self.currentDir.getPermission(),"7" or "3" or "5" or "1"):
            if self.currentDir.getName()=="root":
                print("You are in the root dir!")
            else:
                self.currentDir.setName(self.currentDir.getName()[0:self.currentDir.getName().rfind("/")])
                self.currentDir.setFileList(os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')))
        else:
            print("Permission denied!") 
    
    # 树形目录
    def treeDir(self,kw):
        try:
            name = kw.split(" ")[1]
        except:
            name = ""
        if self.matchPermission(self.currentDir.getPermission(),"7" or "5"):
            if name == "":
                rootDir = 'F:\\Desktop_From_C\\OSCourseDesign\\'+self.currentDir.getName().replace('/','\\')
            else:
                Dir = 'F:\\Desktop_From_C\\OSCourseDesign\\'+self.currentDir.getName().replace('/','\\')
                existed=False
                for parent,dirnames,filenames in os.walk(Dir):
                    for d in dirnames:
                        if d == name:
                            rootDir = parent+"\\"+d
                            existed=True
                            break
                if existed==False:
                    print("No such file!")
                    return
            count=1
            if self.currentDir.getName()=="root":
                print("root")
            else:
                print("\033[1;34;40m"+"+"+self.currentDir.getName()[self.currentDir.getName().rfind("/")+1:]+"\033[0m")
            for parent,dirnames,filenames in os.walk(rootDir):
                for f in filenames:
                    if os.access(parent+"\\"+f,os.R_OK):
                        print("     "*count+"|"+f)
                for d in dirnames:
                    if os.access(parent+"\\"+d,os.R_OK):
                        print("     "*count+"\033[1;34;40m"+"+"+d+"\033[0m")
                count+=1
        else:
            print("Permission denied!")
    
    # 查找文件
    def findFile(self,kw:str):
        if self.matchPermission(self.currentDir.getPermission(),"7" or "5"):
            name = kw.split(" ")[1]
            rootDir = 'F:\\Desktop_From_C\\OSCourseDesign\\'+self.currentDir.getName().replace('/','\\')
            existed=False
            for parent,dirnames,filenames in os.walk(rootDir):
                for f in filenames:
                    if f == name:
                        print(parent.replace("F:\\Desktop_From_C\\OSCourseDesign\\","")+"\\"+f)
                        existed=True
                for d in dirnames:
                    if d == name:
                        print(parent.replace("F:\\Desktop_From_C\\OSCourseDesign\\","")+"\\"+d)
                        existed=True
            if existed==False:
                print("No such file!")
        else:
            print("Permission denied!")             

    # 清除
    def clear(self):
        os.system("cls")
    
    # 帮助
    def menu(self):
        os.system("cls") # 清屏
        print("================================================")
        print("      功能              |          指令")
        print("================================================")
        print("     创建文件           |          touch")
        print("     删除文件           |          rm")
        print("     文件改名           |          mv")
        print("     复制文件           |          cp")
        print("     读取文件           |          cat")
        print("     编辑文件           |          vi")
        print("     创建文件夹         |          mkdir")
        print("     删除文件夹         |          rmdir")
        print("     罗列文件           |          ls")
        print("     进入文件夹         |          cd")
        print("     返回上一级         |          cd ..")
        print("     树形目录           |          tree")
        print("     查找文件           |          find")
        print("     清屏               |          clear")
        print("     退出               |          exit")
        print("================================================")
        
    # 选择功能
    def choose(self):
        while True:
            kw = input("\033[1;32;40m"+self.currentDir.getName()+"\033[0m"+">")
            # 创建文件
            if "touch" in kw:
                self.createFile(kw)
            
            # 删除文件夹， rmdir 必须在 rm 之前，否则会先执行rm
            elif "rmdir" in kw:
                self.delDir(kw)
                
            # 删除文件
            elif "rm" in kw:
                self.delFile(kw)
            
            # 文件改名
            elif "mv" in kw:
                self.renameFile(kw)
                
            # 复制文件
            elif "cp" in kw:
                self.copyFile(kw)
        
            # 读取文件
            elif "cat" in kw:
                self.readFile(kw)
                
            # 编辑文件
            elif "vi" in kw:
                self.editFile(kw)
                
            # 创建文件夹
            elif "mkdir" in kw:
                self.createDir(kw)
                
            # 罗列文件
            elif kw == "ls":
                self.listFile()
                
            # 返回上一级，同理，cd .. 必须在 cd 之前
            elif kw == "cd ..":
                self.backDir()
                
            # 进入文件夹
            elif "cd" in kw:
                self.intoDir(kw)
            
            # 文件系统的树状图
            elif "tree" in kw:
                self.treeDir(kw)
                
            # 查找文件
            elif "find" in kw:
                self.findFile(kw)
                
            # 清屏
            elif kw == "clear":
                self.clear()
                
            # 退出
            elif kw == "exit":
                break
            
            # 帮助
            elif kw == "help" or kw == "?":
                self.menu()
                
            # 未识别的指令
            else:
                print("未识别的指令: "+kw+" 请重新输入！")

    # 运行    
    def run(self):
        
        # getpass可隐藏输入的密码
        pw=getpass.getpass("请输入"+self.user.getName()+"的密码：")
        
        # 输入密码的过程中，如果输入q则表示退出
        while pw != "q":
            if self.login(pw) == 1:
                break
            else:
                pw=getpass.getpass("密码错误，请重新输入：")
        if pw == "q":
            return
        
        # 登录成功后，进入系统
        os.system("pause")        
        os.system("cls")
        self.choose()
        
if __name__ == '__main__':
    fs = FileSys()
    fs.run()
import getpass
import os
import keyboard
import copy

class File():
    def __init__(self):
        self.name=""
        self.size=0
        self.permission=""
        self.owner=""
        self.use=False
        self.content=""
        
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
    
    def setContent(self,content):
        self.content=content
        
    def getContent(self):
        return self.content      
    
    def __del__(self):
        del self

class MyDir():
    def __init__(self):
        self.Name = ""
        self.Size = 0
        self.fileList = []
        self.permission = ""
        self.owner = ""
        self.wholeName=""
    
    def setName(self,Name):
        self.Name = Name
    
    def getName(self):
        return self.Name
    
    def setSize(self,Size):
        self.Size = Size
        
    def getSize(self):
        return self.Size
    
    def setFileList(self,fileList):
        self.fileList = fileList
        
    def addfile(self,file):
        self.fileList.append(file)
        
    def delfile(self,file):
        self.fileList.remove(file)
        file.__del__()
        
    def delDir(self,file):
        for f in file.getFileList():
            if isinstance(f,MyDir):
                self.delDir(f)
            else:
                self.delfile(f)
        
    def getFileList(self):
        return self.fileList
    
    def setPermission(self,permission):
        self.permission = permission
    
    def getPermission(self):
        return self.permission

    def setOwner(self,owner):
        self.owner = owner
    
    def getOwner(self):
        return self.owner
    
    def setParent(self,parent):
        self.parent = parent
    
    def getParent(self):
        return self.parent
    
    def setWholeName(self,wholeName):
        self.wholeName = wholeName
        
    def getWholeName(self):
        return self.wholeName
    
    def __del__(self):
        del self
    
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
        
        self.currentDir.setWholeName(self.user.getName())
        self.currentDir.setName(self.user.getName())
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
    
    def findDir(self,dirName:str):
        if dirName == self.currentDir.getName():
            return self.currentDir
        else:
            for f in self.currentDir.getFileList():
                if isinstance(f,MyDir):
                    if f.getName() == dirName:
                        return f
                    else:
                        self.findDir(f,dirName)
            return None
    
    def displayDir(self,file,count):
        if isinstance(file,MyDir):
            for f in file.getFileList():
                if isinstance(f,MyDir) and self.matchPermission(f.getPermission(),"7" or "5" or "3" or "1"):
                    print("     "*count+"\033[1;34;40m"+"+"+f.getName()+"\033[0m")
                    self.displayDir(f,count+1)
                else:
                    print("     "*count+"|"+f.getName())
                    
        else:
            print("     "*count+"|"+file.getName())
    
    # 创建文件
    def createFile(self,kw:str):
        try:
            name = kw.split(" ")[1]
        except:
            print("Incomplete command!")
            return
        if self.matchPermission(self.currentDir.getPermission(),"7") or self.matchPermission(self.currentDir.getPermission(),"3"):
            if "/" not in name:
                flag=False
                for n in self.currentDir.getFileList():
                    if name == n.getName():
                        print("File already exists!")
                        flag=True
                        break
                if flag == False:
                    permission = "76"
                    f = File()
                    f.setName(name)
                    f.setOwner(self.user.getName())
                    f.setPermission(permission)
                    self.currentDir.addfile(f)
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
                if name == f.getName():
                    self.currentDir.delfile(f)
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
            if newName == f.getName():
                print("File already exists!")
                flag=True
                return
        
        for f in self.currentDir.getFileList():
            if name == f.getName():
                if "/" not in newName:
                    if newName in self.currentDir.getFileList():
                        print("File already exists!")
                        flag=True
                        break
                    else:
                        f.setName(newName)
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
                if newName == f.getName():
                    print("File already exists!")
                    flag=True
                    return
            
            for f in self.currentDir.fileList:
                if name == f.getName():
                    if "/" not in newName:
                        if newName in self.currentDir.fileList:
                            print("File already exists!")
                            flag=True
                            break
                        else:
                            f1=File()
                            f1=copy.deepcopy(f)
                            f1.setName(newName)
                            self.currentDir.addfile(f1)
                            print(self.currentDir.fileList)
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
        for f in self.currentDir.fileList:
            if name == f.getName():
                if self.matchPermission(f.getPermission(),"7" or "4" or "5" or "6"):
                    print("文件名："+name+" 文件大小："+str(f.getSize())+" 字节")
                    os.system("pause")
                    os.system("cls")
                    print(f.getContent())
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
        if self.matchPermission(self.currentDir.getPermission(),"7" or "2" or "3" or "6"):
            for f in self.currentDir.fileList:
                if name == f.getName():
                    if f.getUse() == False:
                        f.setUse(True)
                        os.system("cls")
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
                        f.setContent(content)
                        f.setSize(len(content.encode("utf-8")))
                        f.setUse(False)
                        flag=True
                        break
                    else:
                        print("File is being used!")
                        return
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
                flag=False
                for n in self.currentDir.getFileList():
                    if name == n.getName():
                        flag=True
                        print("Dir already exists!")
                        return
                if flag==False:
                    dir = MyDir()
                    dir.setName(name)
                    dir.setOwner(self.user.getName())
                    dir.setPermission("76")
                    dir.setParent(self.currentDir)
                    dir.setWholeName(self.currentDir.getWholeName()+"/"+name)
                    self.currentDir.addfile(dir)
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
            for f in self.currentDir.getFileList():
                if name == f.getName():
                    self.currentDir.delDir(f)
                    self.currentDir.delfile(f)
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
                for f in self.currentDir.getFileList():
                    if f == self.currentDir.fileList[-1]:
                        if "." in f.getName() and f.getName()[0] !=".":
                            print(f.getName())
                        else:
                            print("\033[1;34;40m"+f.getName()+"\033[0m")
                    else:
                        if "." in f.getName() and f.getName()[0]!=".":
                            print(f.getName(),end=" ")
                        else:
                            print("\033[1;34;40m"+f.getName()+"\033[0m",end=" ")
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
                if name == f.getName() and self.matchPermission(f.getPermission()[0],"7" or "3" or "5" or "1"):
                    self.currentDir = f
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
                self.currentDir = self.currentDir.getParent()
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
                rootDir = self.currentDir
            else:
                rootDir = self.findDir(name)
                if rootDir == None:
                    print("No such file!")
                    return
            count=1
            print("\033[1;34;40m"+"+"+rootDir.getName()+"\033[0m")
            self.displayDir(rootDir,count)
        else:
            print("Permission denied!")
    
    # 查找文件
    def findFile(self,kw:str):
        name = kw.split(" ")[1]
        self.recurFind(self.currentDir,name)     
    
    # 递归查找文件
    def recurFind(self,dir:MyDir,name):
        if self.matchPermission(dir.getPermission(),"7" or "5"):
            if dir.getFileList()==[]:
                print("No such file!")  
            else:        
                for f in dir.getFileList():
                    if isinstance(f,MyDir):
                        if f.getName() == name:
                            print(f.getWholeName().replace('/','\\')+"\\")
                        else:    
                            self.recurFind(f,name)
                    else:
                        if f.getName() == name:
                            print(dir.getWholeName().replace('/','\\')+"\\"+f.getName())
                        else:
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
            kw = input("\033[1;32;40m"+self.currentDir.getWholeName()+"\033[0m"+">")
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
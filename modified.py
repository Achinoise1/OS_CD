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
    
    # ???????????????    
    def matchPermission(self,permission:str,num:str):
        if self.user.getType() == "root" and permission[0] == num:
            return True
        elif self.user.getType() == "user" and permission[1] == num:
            return True
        else:
            return False
    
    # ????????????
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
    
    # ????????????        
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
    
    # ???????????????
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
    
    # ????????????    
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

    # ????????????
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
                    print("????????????"+name+" ???????????????"+str(os.path.getsize("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')+"\\"+name))+" ??????")
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

    # ????????????
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
    
    # ????????????
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
    
    # ????????????
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

    # ????????????
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

    # ????????????
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

    # ?????????????????????
    def backDir(self):
        if self.matchPermission(self.currentDir.getPermission(),"7" or "3" or "5" or "1"):
            if self.currentDir.getName()=="root":
                print("You are in the root dir!")
            else:
                self.currentDir.setName(self.currentDir.getName()[0:self.currentDir.getName().rfind("/")])
                self.currentDir.setFileList(os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.getName().replace('/','\\')))
        else:
            print("Permission denied!") 
    
    # ????????????
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
    
    # ????????????
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

    # ??????
    def clear(self):
        os.system("cls")
    
    # ??????
    def menu(self):
        os.system("cls") # ??????
        print("================================================")
        print("      ??????              |          ??????")
        print("================================================")
        print("     ????????????           |          touch")
        print("     ????????????           |          rm")
        print("     ????????????           |          mv")
        print("     ????????????           |          cp")
        print("     ????????????           |          cat")
        print("     ????????????           |          vi")
        print("     ???????????????         |          mkdir")
        print("     ???????????????         |          rmdir")
        print("     ????????????           |          ls")
        print("     ???????????????         |          cd")
        print("     ???????????????         |          cd ..")
        print("     ????????????           |          tree")
        print("     ????????????           |          find")
        print("     ??????               |          clear")
        print("     ??????               |          exit")
        print("================================================")
        
    # ????????????
    def choose(self):
        while True:
            kw = input("\033[1;32;40m"+self.currentDir.getName()+"\033[0m"+">")
            # ????????????
            if "touch" in kw:
                self.createFile(kw)
            
            # ?????????????????? rmdir ????????? rm ???????????????????????????rm
            elif "rmdir" in kw:
                self.delDir(kw)
                
            # ????????????
            elif "rm" in kw:
                self.delFile(kw)
            
            # ????????????
            elif "mv" in kw:
                self.renameFile(kw)
                
            # ????????????
            elif "cp" in kw:
                self.copyFile(kw)
        
            # ????????????
            elif "cat" in kw:
                self.readFile(kw)
                
            # ????????????
            elif "vi" in kw:
                self.editFile(kw)
                
            # ???????????????
            elif "mkdir" in kw:
                self.createDir(kw)
                
            # ????????????
            elif kw == "ls":
                self.listFile()
                
            # ???????????????????????????cd .. ????????? cd ??????
            elif kw == "cd ..":
                self.backDir()
                
            # ???????????????
            elif "cd" in kw:
                self.intoDir(kw)
            
            # ????????????????????????
            elif "tree" in kw:
                self.treeDir(kw)
                
            # ????????????
            elif "find" in kw:
                self.findFile(kw)
                
            # ??????
            elif kw == "clear":
                self.clear()
                
            # ??????
            elif kw == "exit":
                break
            
            # ??????
            elif kw == "help" or kw == "?":
                self.menu()
                
            # ??????????????????
            else:
                print("??????????????????: "+kw+" ??????????????????")

    # ??????    
    def run(self):
        
        # getpass????????????????????????
        pw=getpass.getpass("?????????"+self.user.getName()+"????????????")
        
        # ???????????????????????????????????????q???????????????
        while pw != "q":
            if self.login(pw) == 1:
                break
            else:
                pw=getpass.getpass("?????????????????????????????????")
        if pw == "q":
            return
        
        # ??????????????????????????????
        os.system("pause")        
        os.system("cls")
        self.choose()
        
if __name__ == '__main__':
    fs = FileSys()
    fs.run()
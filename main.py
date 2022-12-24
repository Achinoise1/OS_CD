import getpass
import os
import keyboard

class MyFile():
    def __init__(self):
        self.fileName = ""
        self.fileSize = 0
        self.content = ""
        self.fileType = ""
    
    def setFileName(self,fileName):
        self.fileName = fileName
    
    def getFileName(self):
        return self.fileName
    
    def setFileSize(self,fileSize):
        self.fileSize = fileSize
    
    def getFileSize(self):
        return self.fileSize
    
    def setContent(self,content):
        self.content = content
    
    def getContent(self):
        return self.content
    
    def setFileType(self,fileType):
        self.fileType = fileType
    
    def getFileType(self):
        return self.fileType
    
    def setPermission(self,permission):
        self.permission = permission
    
    def getPermission(self):
        return self.permission

  
class MyDir():
    def __init__(self):
        self.dirName = ""
        self.dirSize = 0
        self.fileList = []
    
    def setDirName(self,dirName):
        self.dirName = dirName
    
    def getDirName(self):
        return self.dirName
    
    def setDirSize(self,dirSize):
        self.dirSize = dirSize
        
    def getDirSize(self):
        self.dirSize = os.path.getsize("F:\\Desktop_From_C\\OSCourseDesign\\"+self.dirName.replace('/','\\'))
        return self.dirSize
    
    def setFileList(self,fileList):
        self.fileList = fileList
        
    def getFileList(self):
        self.fileList = os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.dirName.replace('/','\\'))
        return self.fileList
    
    def setLastDir(self,lastDir):
        self.lastDir = lastDir
    
    def getLastDir(self):
        return self.lastDir
    
    def setNextDir(self,nextDir):
        self.nextDir = nextDir
        
    def getNextDir(self):
        return self.nextDir

class FileSys():
    root= MyDir()
    currentDir = root
    
    def __init__(self):
        self.userName="root"
        self.pw="123456"
        self.root.dirName = "root"
        self.currentDir.fileList = self.currentDir.getFileList()
    
    # 登录
    def login(self,pw):
        if pw == self.pw:
            print("登录成功！")
            return 1
        else:
            return 0
    
    # 创建文件
    def createFile(self,kw):
        fileName = kw.split(" ")[1]
        try:
            fileType = kw.split(".")[1]
        except:
            fileType = "txt"        #默认为文本文件
        if "/" in fileName:
            print("文件名不能包含/字符！")
        else:
            file = MyFile()
            file.setFileName(fileName)
            file.setFileType(fileType)
            self.currentDir.fileList.append(fileName)
            open(kw.split(" ")[1],"w")
    
    # 删除文件    
    def delFile(self,kw):
        fileName = kw.split(" ")[1]
        if fileName in self.currentDir.fileList:
            self.currentDir.fileList.remove(fileName)
            os.remove(kw.split(" ")[1])
        else:
            print("文件不存在！")
    
    # 读取文件
    def readFile(self,kw):
        fileName = kw.split(" ")[1]
        print("文件名："+fileName+" 文件大小："+str(os.path.getsize("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.dirName.replace('/','\\')+"\\"+fileName))+" 字节")
        os.system("pause")
        os.system("cls")
        if fileName in self.currentDir.fileList:
            f = open(kw.split(" ")[1],"r",encoding="utf-8")
            print(f.read())
            f.close()
        else:
            print("文件不存在！")
    
    # 编辑文件 -- 默认队尾追加
    def editFile(self,kw):
        fileName = kw.split(" ")[1]
        if fileName in self.currentDir.fileList:
            os.system("cls")
            f = open(kw.split(" ")[1],"a+",encoding="utf-8")
            f1 = open(kw.split(" ")[1],"r",encoding="utf-8")
            print(f1.read())
            string=""
            while True:
                temp = input()
                if temp == ":wq":
                    break
                else:
                    string = string + temp + "\n"
            f.write(string)
            f.close()       
    
    # 创建文件夹
    def createDir(self,kw):
        try:
            dirName = kw.split(" ")[1]
            if "/" in dirName:
                print("文件夹名不能包含/字符！")
            else:
                dir = MyDir()
                dir.setDirName(dirName)
                self.currentDir.fileList.append(dirName)
                os.mkdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.dirName.replace('/','\\')+"\\"+kw.split(" ")[1])
        except:
            print("请输入完整的指令")
    
    # 删除文件夹
    def delDir(self,kw):
        try:
            dirName = kw.split(" ")[1]
            if dirName in self.currentDir.fileList:
                self.currentDir.fileList.remove(dirName)
                os.rmdir(kw.split(" ")[1])
            else:
                print("文件夹不存在！")
        except:
            print("请输入完整的指令")
            
    # 罗列文件
    def listFile(self):
        # 没有文件时输出一个空行
        if self.currentDir.fileList == []:
            print()
        else:
            for f in self.currentDir.fileList:
                if f == self.currentDir.fileList[-1]:
                    print(f)
                else:
                    print(f,end=" ")
    
    # 进入文件夹
    def intoDir(self,kw):
        # 确保文件夹存在才能进入
        if kw in self.currentDir.fileList:
            self.currentDir.dirName += "/"+kw
            
            # 重新获取当前目录下的文件列表
            self.currentDir.fileList = os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.dirName.replace('/','\\'))
        else:
            print("文件夹不存在！")
    
    # 返回上一级
    def backDir(self):
        if self.currentDir.dirName != "root":
            # 从右往左找到第一个/，然后截取到它的左边，即为上一级目录
            self.currentDir.dirName = self.currentDir.dirName[0:self.currentDir.dirName.rfind("/")]
            
            # 重新获取当前目录下的文件列表
            self.currentDir.fileList = os.listdir("F:\\Desktop_From_C\\OSCourseDesign\\"+self.currentDir.dirName.replace('/','\\'))
        else:
            print("已经是根目录！")
 
    # 树形目录
    def treeDir(self):
        rootDir = 'F:\\Desktop_From_C\\OSCourseDesign\\'+self.currentDir.dirName.replace('/','\\')
        count=1
        if self.currentDir.dirName == "root":
            print("root")
        else:
            print("+"+self.currentDir.dirName[self.currentDir.dirName.rfind("/")+1:])
        for parent,dirnames,filenames in os.walk(rootDir):
            for f in filenames:
                print("     "*count+"|"+f)
            for d in dirnames:
                print("     "*count+"+"+d)
            count+=1
       
    # 查找文件
    def findFile(self,kw):
        fileName = kw.split(" ")[1]
        rootDir = 'F:\\Desktop_From_C\\OSCourseDesign\\'+self.currentDir.dirName.replace('/','\\')
        for parent,dirnames,filenames in os.walk(rootDir):
            for f in filenames:
                if f == fileName:
                    print(parent.replace("F:\\Desktop_From_C\\OSCourseDesign\\","")+"\\"+f)
            for d in dirnames:
                if d == fileName:
                    print(parent.replace("F:\\Desktop_From_C\\OSCourseDesign\\","")+"\\"+d)        
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
        print("     读取文件           |          cat")
        print("     编辑文件           |          vi")
        print("     创建文件夹         |          mkdir")
        print("     删除文件夹         |          rmdir")
        print("     罗列文件           |          ls")
        print("     进入文件夹         |          cd")
        print("     返回上一级         |          cd ..")
        print("     树形目录           |          tree")
        print("     清屏               |          clear")
        print("     退出               |          exit")
        print("================================================")

    # 选择功能
    def choose(self):
        while True:
            kw = input(self.currentDir.dirName+">")
            # 创建文件
            if "touch" in kw:
                self.createFile(kw)
                
            # rmdir 必须在 rm 之前，否则会先执行rm
            # 删除文件夹
            elif "rmdir" in kw:
                self.delDir(kw)
            # 删除文件
            elif "rm" in kw:
                self.delFile(kw)
            
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
                
            # 同理，cd .. 必须在 cd 之前
            # 返回上一级
            elif kw == "cd ..":
                self.backDir()
            # 进入文件夹
            elif "cd " in kw:
                self.intoDir(kw.split(" ")[1])
            
            # 文件系统的树状图
            elif kw == "tree":
                self.treeDir()
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
            elif kw == "help":
                self.menu()
            # 未识别的指令
            else:
                print("未识别的指令: "+kw+"请重新输入！")
       
    # 运行    
    def run(self):
        
        # getpass可隐藏输入的密码
        pw=getpass.getpass("请输入"+self.userName+"的密码：")
        
        # 输入密码的过程中，如果输入q则表示退出
        while pw != "q":
            if self.login(pw) == 1:
                break
            else:
                pw=getpass.getpass("密码错误，请重新输入：")
        if pw == "q":
            self.Exit()
        
        # 登录成功后，进入系统
        os.system("pause")        
        os.system("cls")
        self.choose()

     
if __name__ == '__main__':
    fs = FileSys()
    fs.run()
    
from util import * 

if Aset.get("april.speech_recognition"):
    import speech_recognition as sr

if Aset.get("april.pyttsx3"):
    import pyttsx3

class AprilFind:
    def __init__(self):
        pass

    def docmd(self, cmdlist):
        dst = cmdlist[0]
        by = " ".join(cmdlist[1:])
        if by == "in local":
            os.system("find ./ -name "+dst)

class AprilBuild:
    def __init__(self):
        pass
    
    def docmd(self,  cmdlist):
        if cmdlist[0] == "1":
            pass
        else:
            os.system("ycmd.py web info")
class AprilInfo:
    def __init__(self, root):
        pass
    
    def docmd(self, cmdlist):
        self._console(self._getroot())
        self._getroot().info.summay()

class HostInfo:
    def __init__(self, root):
        pass
    
    def docmd(self, cmdlist):
        self._console(self._getroot())
        self._getroot().host.summay()

class April(YModule):
    def __init__(self):
        super().__init__()
        pass

    def docmd(self, cmdstr):
        cmdlist = cmdstr.split(' ')
        cmd = cmdlist[0]
        if cmd == "m":
            self.now = eval("self.now."+cmdlist[1])
            self.now.summay()
        elif cmd == "b":
            self.now = self.now.parent
            self.now.summay()
        elif cmd == "root":
            self.now = self._getroot()
            self.now.summay()
        elif cmd == "run":
            arg=" ".join(cmdlist[2:])
            self._console(arg)
            allcmd = "self.now"+"."+cmdlist[1]+"("+arg+")"
            self._console(allcmd)
            eval(allcmd)
        pass

    def run(self, arg):
        self._console("april run "+ arg)
        if arg == "test":
            self.docmd("build test in local")
        elif arg == "1":
            self.run1()
        elif arg == "2":
            self.run2()
        else:
            self.docmd(arg)
        pass 

    def run2(self):
        self.now = self._getroot()
        self._console("welcome use april cmd line")
        self.now.summay()
        while 1:
            cmd = input()
            self.docmd(cmd)
            self._console("finsh cmd ======")

    def run1(self):
        
        r = sr.Recognizer()
        harvard = sr.AudioFile('hello.wav')

        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            self._console("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

        self._console("=======================================")

        mp=sr.Microphone() 

        speaker= pyttsx3.init()
        self._console("my name is april")
        speaker.say("my name is april")
        speaker.runAndWait()

        with mp as source:
            while 1:
                try:
                    self._console("waiting...")
                    audio = r.listen(source)
                    self._console("try to study ...")
                    local = "local:"+r.recognize_sphinx(audio)
                    google = "google:"+r.recognize_google(audio)
                    self._console(local)
                    speaker.say(local)
                    speaker.runAndWait()
                    self._console(google)
                    speaker.say(google)
                    speaker.runAndWait()
                    speaker.say("this is april")
                    speaker.runAndWait()

                except KeyboardInterrupt:
                    self._console("exit")
                    break 
                except:
                    self._console("except")


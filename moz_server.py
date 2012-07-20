#!/usr/bin/python
# coding: utf-8 

import BaseHTTPServer
import  re, telnetlib
import os

# The program requires xvkbd. If you don't need, then False
XVKBDP = True

class Moz():
    """"이 크래스의 목적은 mozlab에 접속하여 원하는 결과를 가져오는 것이다.
    moz 함수를 이용하여 결과를 가져올 수 있다.
    """
        #moz에 연결하였을 때 이미 연결된 연결이 있다면, 새로운 연결은 repl1>,
        # repl2> 같은 식으로 연결된다. 이 연결을 끊기 위해서는 repl1.quit(),
        # repl2.quit() 같이 명령을 주어야 한다. 하지만 현재 cmd 함수는
        # repl.quit() 명령만을 내린다. 그래서 tn.read_all() 함수는 제대로
        # 동작하지 않게 된다. 이제 repl 의 연결이 끊어진 상태이므로 다시 연결하여
        # 결과를 받아오자.
    
    def __init__(self):
        self.host = "localhost"
        self.port = "4242"
        self.content=None

    def __call__(self, cmd):

        return self.cmd(cmd)
        
    # interaction with moz
    def moztest(self, cmd):
        ""
        tn = telnetlib.Telnet(self.host,self.port)
        

    def cmd(self, cmd):
        ""

        ## connect
        try:
            tn = telnetlib.Telnet(self.host,self.port)
        except:
            "Your firefox/mozlab opened? Check that."
        # quit()가 없어도 함수가 끝나면 연결이 자동으로 끊긴다.
        #tn.write("repl.quit()")

        #content=tn.read_until('syntax\n\n')
        content = tn.expect(["repl[0-9]*> "])[2]

        # 이미 열려진 port가 있으면 prompt는 repl1, repl2 식으로 된다.
        # repl.quit() 같은 명령어를 보낼 때 repl1 에서는 repl1.quit() 식으로
        # 명령한다.
        prompt = self.parse("(repl[0-9]*)> ", content).group(1)

        ## send command
        cmd=cmd+"\n"
        tn.write(cmd)

        ## read respone
        content = tn.read_until(prompt).replace('"',"").replace('\n','').replace(prompt, '')

        tn.close() 
        return content


    def mozQuit(self):
        ""
        tn = telnetlib.Telnet(self.host,self.port)
        tn.write("repl.quit()")
        tn.close()

    def parse(self, regex, content):
        "Re turns a search object."
        regobj = re.compile(regex)
        seaobj = regobj.search(content)
        return seaobj



class MozServer():
    ""
    def __init__(self):
        ""
        # If True, you can execute any moz command
        self.server_commandp = False
        # If True, server will respones any message for request
        self.server_responsep = False
        # If True, server only allow the requests from localhost
        self.server_localp = True

        self.port = 8090

    def start(self, port=None):
        "Start the server."
        if port == None:
            port = self.port
        server_address = ('', self.port)
        httpd = BaseHTTPServer.HTTPServer(server_address, MozServerRequest)

        sa = httpd.socket.getsockname()
        print "Serving HTTP on", sa[0], "port", sa[1], "..."
        try:
            httpd.serve_forever()
        except: print "end server"

    
class MozServerRequest(BaseHTTPServer.BaseHTTPRequestHandler):
    ""
    def do_GET(self):
        "The function will be executed when the server has GET request."
        cmd = self.path.replace('/','')

        # for configuration
        serverCof= MozServer()
        
        try:
            # execute the command
            getattr(MozCmds(), cmd)()
            if serverCof.server_responsep:
                self.send_header('Content-Type', 'text/html')
                self.wfile.write('200')
        except AttributeError:
            if serverCof.server_responsep:
                self.send_header('Content-Type', 'text/html')
                self.send_error(400)



class MozCmds:
    ""

    def cmdList(self):
        ""
        pass

    def openEmacs(self, new_position=False):
        ""
        mozobj = Moz()
        if new_position:
            mozobj.cmd('moveTo(0,0)')

        # The position
        sw = mozobj.cmd('screen.width')
        ww = mozobj.cmd('outerWidth')
        wl = mozobj.cmd('screenX')
        wr = str(int(sw)-int(wl)-int(ww))

        #print sw+'|'+ww+'|'+wl+'|'+wr+'|'
        # open eamcs
        if (int(wr) < int(wl)):
            # open to left side
            cmd = 'emacsclient -c -e "(d-moz-open-worknote \\"91x100+0\\")"'
        else:
            #open to right side = wl + ww
            x = str(int(wl) + int(ww) + 7)
            cmd = 'emacsclient -c -e "(d-moz-open-worknote \\"91x100+'+x+'\\")"'
        os.popen2(cmd)

        #fixme
        # Do not work
#        if XVKBDP:
#            os.popen2('/usr/bin/xvkbd -sendevent -text "\[Alt_L]\[Tab]"')




if __name__ == '__main__':
    ms = MozServer()
    ms.start()
    

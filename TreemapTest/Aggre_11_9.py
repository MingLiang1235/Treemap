#-*- encoding:UTF-8 -*-
"""version 11.9_03.01.06.01 : 
双击按钮直接进入钻取。改文件颜色为浅蓝色。
清理窗口内容 通过获取获取窗口变化大小，重绘页面组件。
不用重新获取，OnWindowResize而是重新计算，升级后窗口变化即自动重算，以及调整细度。"""
import wx
import win32con,win32api,os,sys
from stat import *
from os.path import join, getsize
import codecs
import re
import os
import sys
import ctypes.wintypes
import win32gui
import DevideModule
import ChoiceRandomLs
import StackWithPoint
from Progress import *
import getAllSizeThread
import threading
from MyStatusBar import *
import DialogConfig
try:
	import cPickle as pickle
except ImportError:
	import pickle
import images
import webbrowser
#import DialogConsole
# class singletonFutureCall(wx.FutureCall):
# 	def __init__(self):
# 		super.__init__(self)

# 	instance = singletonFutureCall()
# 	def getInstance():
# 		return instance

class MyFrame(wx.Frame):
	"""MyFrame clas treat with the config files"""
	def __init__(self):
		win32all_mode = ((win32con.FILE_ATTRIBUTE_DIRECTORY,  'd'),
                         (win32con.FILE_ATTRIBUTE_ARCHIVE,    'A'),
                         (win32con.FILE_ATTRIBUTE_COMPRESSED, 'C'),
						 (win32con.FILE_ATTRIBUTE_HIDDEN,     'H'),
						 (win32con.FILE_ATTRIBUTE_NORMAL,     'N'),
						 (win32con.FILE_ATTRIBUTE_READONLY,   'R'),
						 (win32con.FILE_ATTRIBUTE_SYSTEM,     'S'))
		UNAVAILABLE   = "Unavailable"
		global updateFile
		global medviewFile
		global prideFile
		
		prideFile=''
		updateFile=''
		medviewFile=''
			
		def prepareTwoConfigFile():
			global updateFile
			global medviewFile
			updateFile=openFile(updateFPath)
			updateFile=subFile(updateFile)
			medviewFile=openFile(medviewFPath)
			medviewFile=subFile(medviewFile)
		def SaveConfig(text,filePath):
			#print 'text=' + text
			#print 'path=' + filePath
			if not (text==""):
				fopen = codecs.open(filePath,'w',encoding='utf8')
				fopen.write(text)
				consoleText.AppendText(filePath+" saved.\n")
			else:
				consoleText.AppendText("Cant save because text "+filePath+" is empty.\n")
				#pass
				#print "cant save because text is empty"
		def OpenTheFile(event):
			global prideFile
			filePath = configFPath
			fopen = codecs.open(filePath,'r',encoding='utf8')
			prideFile = fopen.read()
			#contentsText.SetValue(prideFile)
			#contentsText.SetEditable(False)
		def SaveFile(event):
			global prideFile
			contents = prideFile
			if len(contents) > 0:
				filePath = configFPath
				fopen = codecs.open(filePath,'w',encoding='utf8')
				fopen.write(prideFile)
				#consoleText.AppendText(contents)
				consoleText.AppendText(filePath+" saved.\n")
			else:
				consoleText.AppendText("the config is empty.\n")
			global updateFile
			global medviewFile
			#print 'updatefile=' + updateFile
			if (updateCheck.GetValue() == True and len(updateFile)!=0):
				#print "want to save updateconfig"
				SaveConfig(updateFile,updateFPath)
			if (medviewCheck.GetValue() == True and len(medviewFile)!=0):
				#print "want to save medviewconfig"
				SaveConfig(medviewFile,medviewFPath)
		#def MatchText(event):
			#contentsText.SetDefaultStyle(wx.TextAttr("red","blue"))
			#consoleText.SetDefaultStyle(wx.TextAttr(wx.RED))
			#consoleText.AppendText("Red text\n")
			#consoleText.SetValue(candidate+'Regex match?\n')
			#text = contentsText.GetValue()
			#reg = conditionText.GetValue()  # default use : r"getted value"
			#print reg +'\n'
			#m = re.search(reg, text)
			#if m:
				#consoleText.AppendText('Match onece!\n')
				#print  m.group(0)+"::"+m.group(1)+'\n'
				#print  m.group(0)+"::"+'\n'
			#else:
				#consoleText.AppendText('not match\n')
				#print "not match (search)"
		def SubTheText(event):
			global prideFile
			text = prideFile
			#reg = r' *<endpoint address="[a-zA-Z0-9<>:.]+//([a-zA-Z0-9_.:]+)'
			reg = strconditionText  # default use : r"getted value"  r mean raw string (failure escape charater)
			p = re.compile(reg)
			#m = p.sub('hello', text)
			#print m			
			def func(m):
				return m.group(1)+replText.GetValue()
			repledText = p.sub(func,text)
			#consoleText.SetValue(candidate+'Regex match.\n')
			#consoleText.SetValue(candidate+'Content replaced..\n')
			consoleText.AppendText('Content has been replaced..\n')
			prideFile = repledText
			#contentsText.SetValue(repledText)
			#print reg
			prepareTwoConfigFile()
		def verModify(event):
			versionFPath = workPath + '\MeDSysUpdate\MedSysUpdate.ini'
			fopen = codecs.open(versionFPath,'r',encoding='utf8')
			text=fopen.read()
			fopen.close()
			
			reg = '(AppVer=)([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)'
			s = re.compile(reg)
			match = s.search(text)
			if match:
				consoleText.AppendText(match.group(0)+'\n'+'<<------------------------>>\n')
			def func(m):
				return m.group(1)+updateVersionText.GetValue()
			repledText = s.sub(func,text,1)
			match = s.search(repledText)
			if match:
				consoleText.AppendText(match.group(0)+'\n')
			
			def getModes(fn):
				#print fn
				modlen = len(win32all_mode)
				#print modlen
				try:
					#print 'be in try'
					win32stat = win32api.GetFileAttributes(fn)
					#print 'getFileAttributes'
					mode = ""
					#print 'mode='+mode
				except:
					mode = UNAVAILABLE
  
				if not mode:
  
				# Test each attribute and set symbol in respective
				# position, if attribute is true.
					for i in range(modlen):
						mask, sym = win32all_mode[i]
						if win32stat & mask:
							mode += sym
						else:
							mode += '-'
				return mode
			mode = getModes(versionFPath)
			consoleText.AppendText(mode+'\n')
			for c in mode:
				if c == 'H':
					win32api.SetFileAttributes(versionFPath, win32con.FILE_ATTRIBUTE_NORMAL) 
			fsave = codecs.open(versionFPath,'w',encoding='utf8')
			fsave.write(repledText)
			win32api.SetFileAttributes(versionFPath, win32con.FILE_ATTRIBUTE_HIDDEN)
		def openFile(path):
			fopen = codecs.open(path,'r',encoding='utf8')
			text = fopen.read()
			return text
		def subFile(text):
			reg = strconditionText
			p = re.compile(reg)
			def func(m):
				return m.group(1)+replText.GetValue()
			repledText = p.sub(func,text)
			return repledText
		def initFifo():
			try:
				with open('abc.pkl', 'rb') as f:
					self.fifo = pickle.load(f)
				#dlg = wx.MessageDialog(None,"I'm in initPickle","A Message",wx.OK | wx.ICON_INFORMATION)
				#retCode = dlg.ShowModal()
			except Exception,err:
				self.showMsg(str(Exception)+str(err))



				
		self.width = 900     #程序视窗宽度
		self.height = 535    #程序视窗高度

		self.ls = []
		self.currDir = os.getcwd()  #获得当前工作目录
		wx.Frame.__init__(self,None,-1,u"DirCubie 3",size=(self.width,self.height))
		self.panel = wx.Panel(self ,-1)		

		self.panel.Bind(wx.EVT_SIZE,self.OnMyResize)
		
		self.timer = wx.Timer(owner=None, id=-1)
		self.timer.Bind(wx.EVT_TIMER, self.OnTimer)

		#self.timerProgress = wx.Timer(owner=None,id=-1)
		#self.timerProgress.Bind(wx.EVT_TIMER,self.OnProgressTimer)

		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		#self.dialog = DialogConsole.ConsoleDialog("===For Aggregation 1.0.9 === \n")
		#self.dialog.Show()
		
		#panel.Bind(wx.EVT_BUTTON, self.OnMove)
		#wx.StaticText(panel,-1,"Pos:",pos=(10,12))
		#self.posCtrl = wx.TextCtrl(panel,-1,"",pos=(40,10))
		loadButton = wx.Button(self.panel,label = u'扫描当前目录', pos=(225,5),size=(130,25))
		#saveButton = wx.Button(panel,label = 'save', pos=(315,5),size=(80,25))
		#matchButton = wx.Button(panel,label = 'search', pos=(315,5),size=(80,25))
		#verModifyButton = wx.Button(panel,label = 'modify', pos=(355,5),size=(80,25))
		#subButton = wx.Button(panel,label = 'Sub', pos=(385,5),size=(80,25))
		
		self.locationText = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER,pos=(5,5),size=(200,25))
		self.consoleText = wx.TextCtrl(self.panel,pos =(0,435),size=(200,100),style=wx.TE_MULTILINE)
		#mainConfigText = wx.TextCtrl(panel, pos=(5,5),size=(210,25))
		#versionText = wx.TextCtrl(panel, pos=(5,5),size=(120,25))
		#updateVersionText = wx.TextCtrl(panel, pos=(5,5),size=(120,25))
		#workLocalLabel = wx.StaticText(panel, -1, u":*当前位置*")
		try:
			self.Icon = wx.Icon('config_256.ico',wx.BITMAP_TYPE_ICO)   #config对话框的图标
			self.IconBundle = wx.IconBundle()
			self.IconBundle.AddIcon(self.Icon)
		except Exception as err:
			dlg = wx.MessageDialog(None,"I'm in init,"+str(Exception)+str(err),"A Note",wx.OK | wx.ICON_INFORMATION)
			dlg.ShowModal()
		try:
			#bmp_config = wx.Image('config_.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()  #位图按钮的图标
			bmp_config = images._rt_open.GetBitmap()
			BtnOpen = wx.BitmapButton(self.panel,-1,bmp_config,size=(25,25))
		except Exception as err:
			dlg = wx.MessageDialog(None,"I'm in init,build bmp_config,"+str(Exception)+str(err),"A Note",wx.OK|wx.ICON_INFORMATION)
			dlg.ShowModal()
			BtnOpen = wx.Button(self.panel,label='*',size=(25,25))
		self.prevButton = wx.Button(self.panel,label='<',size=(35,25))
		self.nextButton = wx.Button(self.panel,label='>',size=(35,25))
		#mainConfigLabel = wx.StaticText(panel, -1, u"主配置文件:")
		#versionLabel = wx.StaticText(panel, -1, u"文件版本号:")
		#updateVersionLabel = wx.StaticText(panel, -1, u"版本升级号:")
		#conditionText = wx.TextCtrl(panel, size=(300,25))
		#replText = wx.TextCtrl(panel, size=(300,25))
		#updateCheck = wx.CheckBox(panel,-1,"UpdateDir",(35,40),(80,25))
		#medviewCheck = wx.CheckBox(panel,-1,"MedviewDir",(35,60),(80,25))
		#contentsText = wx.TextCtrl(panel,pos=(5,35),size=(395,260),style=wx.TE_MULTILINE|wx.HSCROLL)
		#self.consoleText = wx.TextCtrl(self.panel,pos =(0,435),size=(200,100),style=wx.TE_MULTILINE)
		
		#这里定义buttons的数量没有任何意义，因为还没有scan，不知道具体的按钮数量呢。
		#除非从序列化（硬盘）取得记录，会有意义，因为要建立初始图形，那么也不能用以下方式建立。
		if self.maxButtons != -1:
			self.buttons = [None]*self.maxButtons   #一维数组初始法，二维初始法：A = [[None] * 2 for x in range(3)]  （这个是2×3的数组）
		else:
			#self.buttons = [None]*self.currBtnNum
			self.buttons = [None]*0  #[]
		# for i in range(maxButtons):
			# buttons[i]=wx.Button(panel,id=i,label = str(i),pos = (100,100*i),size=(180,55))
			# tip = wx.ToolTip('TEST')
			# buttons[i].SetToolTip(tip)
			# tip.SetTip(buttons[i].GetLabel())
		#firstButton = wx.Button(panel,label = 'first',pos=(100,100),size=(180,55))
		#secondButton = wx.Button(panel,label = 'second',pos=(100,200),size=(180,55))
		#thirdButton = wx.Button(panel,label = 'third',pos=(100,300),size=(180,55))
		
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(BtnOpen,proportion=0,flag=wx.LEFT,border=2)
		hbox.Add(self.locationText,proportion=1,flag=wx.EXPAND|wx.LEFT,border=5)
		hbox.Add(self.prevButton,proportion=0,flag=wx.LEFT,border=2)
		hbox.Add(self.nextButton,proportion=0,flag=wx.LEFT,border=2)
		hbox.Add(loadButton,proportion=0,flag=wx.LEFT,border=5)
		
		vbox0 = wx.BoxSizer(wx.VERTICAL)
		
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		hbox3.Add(vbox0,proportion=1,flag=wx.EXPAND|wx.LEFT,border=5)
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(hbox,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
		vbox.Add(hbox3,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=5)
		vbox.Add(self.consoleText,0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
		
		self.panel.SetSizer(vbox)

		loadButton.Bind(wx.EVT_BUTTON,self.OnClickScan)
		self.prevButton.Bind(wx.EVT_BUTTON,self.GetPrevious)
		self.nextButton.Bind(wx.EVT_BUTTON,self.GetNext)
		BtnOpen.Bind(wx.EVT_BUTTON,self.OnDirOpen)

		self.Bind(wx.EVT_KEY_DOWN,self.enterDown,self)
		self.Bind(wx.EVT_TEXT_ENTER,self.textEnterDown,self.locationText)

		#saveButton.Bind(wx.EVT_BUTTON,SaveFile)
		#matchButton.Bind(wx.EVT_BUTTON,MatchText)
		#verModifyButton.Bind(wx.EVT_BUTTON,verModify)
		#subButton.Bind(wx.EVT_BUTTON,SubTheText)
		# for i in buttons:
			# i.Bind(wx.EVT_BUTTON,goThrough)
		# firstButton.Bind(wx.EVT_BUTTON,goThrough)
		# secondButton.Bind(wx.EVT_BUTTON,goThrough)
		# thirdButton.Bind(wx.EVT_BUTTON,goThrough)

		# self.statusbar = self.CreateStatusBar(2,wx.ST_SIZEGRIP) # 创建状态栏
		# self.statusbar.SetStatusWidths([-4,-3])
		# self.statusbar.SetStatusText("Unicodes gearmaster @ 23 Mar 2015", 0)
		# self.statusbar.SetStatusText("Welcome to wxPython!", 1)
		self.statusbar = MyStatusBar(self)
		self.SetStatusBar(self.statusbar)


		#contentsText.SetDefaultStyle(wxTextAttr(wxRED,wxWHITE))  #why does this not work
		#candidate =  r"(\w+)\s"
		#candidate += "\n"
		#candidate += r" *[a-zA-z_0-9<>]+"
		#candidate += "\n"
		#candidate += r' *<endpoint address="(net.tcp)'
		#candidate += "\n"
		#candidate += r' *<endpoint address="[a-zA-Z0-9<>:.]+//([a-zA-Z0-9_.:]+)'
		#candidate += "\n=====================\n"
		candidate = 'Console\n'
		#candidate += 'D:\\oracle\\product\\10.2.0\\db_1\n'
		#candidate += 'E:\\s_c\Python\\aggregatit\\test\\test_data\n'
		#candidate += 'D:\\Life\n'
		#candidate += 'E:\\s_c\Python\\aggregatit\\test\\test_data\n'
		candidate += '=======================\n'
		#candidate += "self.wf_dir:"+ self.wf_dir+"\n"
		self.consoleText.SetValue(candidate)
		
		#repl = "172.17.0.87:8080"
		#replText.SetValue(repl)
		workPath = r'D:'
		
		#try:
		#	GetFileVersionInfoPath = workPath + '\pride\PRIDE.exe'
		#	info = win32api.GetFileVersionInfo(GetFileVersionInfoPath, "\\")
		#	ms = info['FileVersionMS']
		#	ls = info['FileVersionLS']
		#	__version__ = "%d.%d.%d.%d" % (win32api.HIWORD(ms), win32api.LOWORD (ms),win32api.HIWORD (ls), win32api.LOWORD (ls))
		#except:
		#	__version__ = '5.1.1.000' # some appropriate default here.
		#
		#try:
		#	versionFPath = workPath + '\MeDSysUpdate\MedSysUpdate.ini'
		#	fopen = codecs.open(versionFPath,'r',encoding='utf-8')
		#	reg = 'AppVer=([0-9]+.[0-9]+.[0-9]+.[0-9]+)'
		#	s = re.search(reg,fopen.read())
		#	#updateVersionText.SetValue(s.group(1))
		#except:
		#	#updateVersionText.SetValue('not found')
		#	pass
		
		#configFPath = workPath + '\pride\PRIDE.exe.config'
		#updateFPath = workPath + '\MeDSysUpdate\MeDSysUpdate.exe.config'
		#medviewFPath = workPath + '\MeDViewer\MeDViewer.exe.config'
		self.locationText.SetValue(workPath)
		#self.currDir = workPath
		#mainConfigText.SetValue(configFPath)
		#versionText.SetValue(__version__)
		#versionText.SetEditable(False)
		#strconditionText='( *<endpoint address="[a-zA-Z0-9<>:.]+//)([a-zA-Z0-9_.:]+)'	#[a-zA-z_0-9]*
		self.doMakeMenu()  #这一句要提前执行
		#-----------------------------------------
		#读取配置参数,每次启动必须执行
		self.configFile = "configs.xml"
		xmldom = self.readXML(self.configFile)
		try:
			if xmldom :
				vals = self.getXMLStructure(xmldom)
				self.maxButtons = int(vals[0])
				self.continueFromLast = int(vals[1])
				#self.showMsg("xml has maxButtons value is : "+str(self.maxButtons))
				#self.showMsg("xml has continueFromLast value is : "+str(self.continueFromLast)) 
		except Exception,err:
			self.showMsg(str(Exception)+str(err))
			self.showMsg("Can not get value from xml or value is invalidate.")
		#-----------------------------------------
		#self.clickPrevButton()   #手动触发prevButton的onclick事件。
		#self.Bind(wx.EVT_IDLE, self.OnIdle)
		if self.continueFromLast == 1:          #需要从上次关闭的地方继续
			initFifo()			#read from abc.pkl
		self.Bind(wx.EVT_ACTIVATE,self.OnMyActive)

		
		"""debuging"""
		#self.act_count = 0

	def doMakeMenu(self):
		def doBind(item, handler, updateUI=None):
			self.Bind(wx.EVT_MENU, handler, item)
			if updateUI is not None:
				self.Bind(wx.EVT_UPDATE_UI, updateUI, item)
		
		dirMenu = wx.Menu()
		doBind( dirMenu.Append(-1, u"打开(&O)\tCtrl+O", "Open a Dir"),
				self.OnDirOpen )
		dirMenu.AppendSeparator()
		doBind( dirMenu.Append(-1, u"退出(&Q)\tCtrl+Q", "Quit this program"),
				self.OnFileExit )
		
		toolMenu = wx.Menu()
		doBind( toolMenu.Append(-1,u"选项(&P)\tCtrl+P","Options"),
				self.Config )

		helpMenu = wx.Menu()
		doBind( helpMenu.Append(-1,u"查看帮助(&H)\tCtrl+H","Helps"),
				self.OnHelp )
		doBind( helpMenu.Append(-1,u"购买(&P)\tCtrl+P","Perchase"),
				self.OnPerchase )
		helpMenu.AppendSeparator()
		doBind( helpMenu.Append(-1,u"关于DirCube(&A)\tCtrl+A","About Dir Cubie"),
				self.OnAbout )

		Menu = wx.MenuBar()
		Menu.Append(dirMenu,u"文件(&F)")
		Menu.Append(toolMenu,u"工具(&T)")
		Menu.Append(helpMenu,u"帮助(&H)")
		self.SetMenuBar(Menu)
	def OnAbout(self,evt):
		info = wx.AboutDialogInfo()
		info.SetName("DirCubie")
		info.SetVersion("3.1.6.5")
		info.SetDescription(u"这个程序帮助您对硬盘使用情况有一个整体的认识。通过本程序可用直观的方式找到占硬盘空间最多的文件和文件夹等。")
		info.SetCopyright("(c) 2019 Unicoder <unicoder@jishan.asuscomm.com>")
		wx.AboutBox(info)
	def OnHelp(self,evt):
		webbrowser.open_new_tab('https://jishan.asuscomm.com:6001/DirCubie/help.html')
	def OnPerchase(self,evt):
		webbrowser.open_new_tab('https://jishan.asuscomm.com:6001/Donate/')
	def OnFileExit(self,evt):
		self.Close(True)
	def OnDirOpen(self,evt):
		#dlg = wx.FileDialog(self,style=wx.FD_CHANGE_DIR ,message="Choose a Dir")
		dlg = wx.DirDialog(self,style=wx.DD_CHANGE_DIR,size = (300,300))  #DD_CHANGE_DIR:Change the current working directory to the directory chosen by the user.
		if dlg.ShowModal() == wx.ID_OK:
			path=dlg.GetPath()
			if path:
				self.locationText.SetValue(path)
	def readXML(self,conFile):
		from xml.dom import minidom
		import pprint

		doc = None
		filePath = conFile
		try:
			with open(filePath,'rt') as f:
				doc = minidom.parse(f)
				#f.Close()
		except:
			self.showMsg('in readXML can not with open('+ filePath + ",'rt') as f: .")
		
		return doc
	def getXMLStructure(self,doc):
		xmlList = []
		for entity in doc.getElementsByTagName('maxButtons'):
			maxNode = entity.getElementsByTagName('val')[0]
			maxNum = maxNode.firstChild.data.strip()
			xmlList.append(maxNum)
		for entity in doc.getElementsByTagName('continueFromLast'):
			conNode = entity.getElementsByTagName('val')[0]
			conFL = conNode.firstChild.data.strip()
			xmlList.append(conFL)
		return xmlList
	def Config(self,evt):
		useMetal = False
		dlg = DialogConfig.TestDialog(self,-1,u"设置",size=(360,300),pos=self.GetFramePosition(),style=wx.DEFAULT_DIALOG_STYLE,useMetal=useMetal,\
				maxButtons=self.maxButtons,conti=self.continueFromLast,icon=self.Icon)
		dlg.CenterOnScreen()
		val=dlg.ShowModal()
		if val == wx.ID_OK:
			#self.showMsg("You pressed OK.")
			maxButtons = dlg.GetSliderValue()
			continueFromLast = dlg.GetRadioValue()
			if maxButtons != self.maxButtons or continueFromLast != self.continueFromLast:    #数值有改动
				self.maxButtons = maxButtons
				self.continueFromLast = continueFromLast
				#self.showMsg("You modify the maxButtons,the new value is : "+str(self.maxButtons))
				self.saveXML(self.maxButtons,self.continueFromLast)        #每次关闭config对话框之前，将改变写入配置文件。
		else:
			#self.showMsg("You pressed CANCEL.")
			pass
		dlg.Destroy()
	def saveXML(self,val,conVal):
		from xml.dom import minidom
		dom = minidom.Document()
		stri = '请不要手工修改配置的值，否则可能产生问题'
		#stri = 'oooyyy'
		#stri = self.to_unicode_or_bust(stri)
		comment = dom.createComment(stri)   #添加中文注释
		dom.appendChild(comment)
		root_node = dom.createElement('selector')
		dom.appendChild(root_node)
		max_node = dom.createElement('maxButtons')
		root_node.appendChild(max_node)
		max_val_node = dom.createElement('val')
		max_node.appendChild(max_val_node)
		max_val = dom.createTextNode(str(val))
		max_val_node.appendChild(max_val)
		cont_node = dom.createElement('continueFromLast')
		root_node.appendChild(cont_node)
		cont_val_node = dom.createElement('val')
		cont_node.appendChild(cont_val_node)
		cont_val = dom.createTextNode(str(conVal))
		cont_val_node.appendChild(cont_val) 
		try:
			with open('configs.xml','w+') as f:
				dom.writexml(f,indent='',addindent='\t',newl='\n',encoding='UTF-8')
				self.showMsg("Write config file ok.")
		except Exception as err:
			self.showMsg('Error when write configs.xml: {0}'.format(err))

	def to_unicode_or_bust(obj,encoding='utf-8'):
		if isinstance(obj,basestring):
			if not isinstance(obj,unicode):
				obj = unicode(obj,encoding)
		return obj
	def showMsg(self,msg):
		self.consoleText.AppendText(msg+'\n')
	def OnMyResize(self,event):               #一个隐藏的bug，系统初始化的时候，也会运行一次OnMyResize().
		if self.resizedTwice >=2:        #执行过2次以后  ,初始化为第一次执行，添加菜单项为第二次执行，这两者要去掉
			self.resizedTwice = 2
			self.width,self.height = event.Size
			#print self.size
			# if ls!=[]:
				#showButtons(ls,size.width,size.height)

			self.timer.Start(milliseconds=200,oneShot=True)      #new Start erase old ones
			#self.winWidth,self.winHeight = getWindowSize()
			#self.consoleText.AppendText(str(self.winWidth)+' '+str(self.winHeight))
			#self.consoleText.AppendText(str(self.size.width)+' '+str(self.size.height))
		self.resizedTwice += 1
		event.Skip()
	def OnTimer(self,event):	
		#print size
		if self.ls!=[]:
			try:
				self.caculatelsCondition(self.ls,self.width,self.height+self.titleHeight) #这里要去掉标题栏的高度（39）
			except Exception,err:
				self.showMsg(str(Exception)+str(err))
	def cleanWapper(self,string):
		try:
			while string[-1] == "\\":
				string = string[0:-1]
			return string
		except Exception,err:
			self.showMsg(str(Exception)+str(err))
			return None


	###################################################################################################
	#   工作流： 处理scan，prev，next，获取list并划分、产生buttons
	###################################################################################################
	def CopyTheWorkFlowArgs(self):					#初始化工作流参数，拷贝自myframe实例成员，并在此刻固定其值
		#self.showMsg("Im in CopyTheWorkFlowArgs.")
		#self.showMsg(str(self.fifo))
		self.wf_MaxBtnNum = self.maxButtons
		self.wf_dir = self.locationText.GetValue()
		self.wf_dir = self.cleanWapper(self.wf_dir)
		self.wf_dir = self.wf_dir+"\\"
	# def clickPrevButton(self):
	# 	iRet = wx.PostEvent(self,wx.CommandEvent(wx.EVT_BUTTON,self.prevButton.GetId()))
	# 	return iRet
	def OnMyActive(self,evt):
		#self.act_count += 1
		if not self.activedOnce:                    #第一次运行
			self.activedOnce = True                 #已经运行过一次为True,表示下次运行不是第一次运行了
			if self.continueFromLast == 1:          #需要从上次关闭的地方继续
				#self.showMsg("fifo.curr(): "+str(self.fifo.getCurr()))
				if (evt.GetActive() == True) and self.fifo.getCurr():         #onActive确实准备好了,并且fifo有值(fifo.curr!= None)
					try:
						#self.showMsg("I'm in OnMyActive,"+str(self.act_count))
						self.locationText.SetValue(self.fifo.getCurr()[0])
						self.CopyTheWorkFlowArgs()                #注意这个初始化的位置。
						self.caculatels(self.fifo.getCurr()[1])
					except Exception,err:
						self.showMsg(str(Exception)+str(err))
						self.showMsg("Can not open or use stored data.")
		evt.Skip()          #or it will be wirld
	# def OnIdle(self, evt):# 空闲时的处理
	# 	if not self.initIdle:
	# 		self.initIdle = True
	# 		try:
				
	# 			#self.showMsg(str(self.fifo))
	# 			#dlg = wx.MessageDialog(None,"I'm in Idle,"+self.fifo[1][0],"A Message",wx.OK | wx.ICON_INFORMATION)
	# 			#retCode = dlg.ShowModal()
	# 			#iRet = wx.PostEvent(self,wx.CommandEvent(wx.EVT_BUTTON.typeId,self.prevButton.GetId()))
	# 			#self.showMsg(str(self.fifo.getPoint()))
	# 			#self.showMsg(str(self.fifo.getCurr()))
	# 			self.locationText.SetValue(self.fifo.getCurr()[0])
	# 			self.CopyTheWorkFlowArgs()                #注意这个初始化的位置。
	# 			self.caculatels(self.fifo.getCurr()[1])
	# 			evt.Skip()
	# 			#self.Refresh(False)
	# 			#self.Update()

	# 		except Exception,err:
	# 			self.showMsg(str(Exception)+str(err))
	# 			self.showMsg("Can not open or use stored data.")
	def GetPrevious(self,event):
		if self.fifo and not self.thread:
			self.CopyTheWorkFlowArgs()					#拷贝工作流需要的初始化参数，三个入口scan(包括按钮DKlick)，prev，next都要执行此函数
			self.consoleText.AppendText("\n===============\n")
			self.consoleText.AppendText("currDir is:"+ self.wf_dir +"\n")
			#self.consoleText.AppendText("fifo:" + str(self.fifo) + "\n")
			try:
				left = self.fifo.getLeft()
				if left:
					#self.showMsg("self.fifo.left has value: "+str(left))
					text,self.ls = left
					if text != self.wf_dir:
						self.wf_dir = text
						self.locationText.SetValue(text)
						#self.consoleText.AppendText("the Prev is:" + str(left) + "\n")
						self.caculatels(self.ls)
					# elif self.buttons[0] == None:
					# 	self.caculatels(self.ls)
			except Exception,err:
				self.showMsg(str(Exception)+str(err))
	def GetNext(self,event):
		if self.fifo and not self.thread:
			self.CopyTheWorkFlowArgs()					#拷贝工作流需要的初始化参数
			self.consoleText.AppendText("\n===============\n")
			self.consoleText.AppendText("currDir is:"+ self.wf_dir +"\n")
			#self.consoleText.AppendText("fifo:" + str(self.fifo) + "\n")
			try:
				right = self.fifo.getRight()
				if right:
					text,self.ls = right					
					if text != self.wf_dir:
						self.wf_dir = text 
						self.locationText.SetValue(text)
						#self.consoleText.AppendText("the Next is:" + str(right) + "\n")
						self.caculatels(self.ls)
			except Exception,err:
				self.showMsg(str(Exception)+str(err))
	def caculatels(self,ls):
		theWidth,theHeight = self.getWindowSize()
		self.ls = self.myDevide(ls,theWidth,theHeight-39)   #使用魔数减去状态栏和菜单的高度
		self.showButtons(self.ls)
	#--------------------------------------------------------------------------------------
	#  处理扫描硬盘从新获取数据的情况
	#--------------------------------------------------------------------------------------
	def OnClickScan(self,event):    #单击scan按钮
		if not self.thread:
			self.showMsg("Press scan btn.")
			self.doScanPress = True
			self.doOpenTheLocation()    
	def enterDown(self,evt):            #对frame直接调用回车
		key = evt.GetKeyCode()
		if key == wx.WXK_RETURN:
			self.doScanPress = True     #相当于按下了doScan按钮
			self.doOpenTheLocation()
		evt.Skip()
	def textEnterDown(self,evt):        #在地址录入栏按回车
		if not self.thread:
			self.doScanPress = True     #相当于按下了doScan按钮
			self.doOpenTheLocation()
		else:
			showMsg(u"工作进程运行当中，不能打开新的地址。")
	def btnDClick(self,evt):            #双击方块按钮
		#self.showMsg("btn double clicked.")
		self.btnPress = True
		if not self.thread:                #工作进程运行当中，不能双击新的按钮。或可改为可以执行新的工作进程，但需要析构当前工作进程并析构进度条。
			self.doOpenTheLocation()
	def btnKeyDown(self,evt):            #焦点在每个按钮上，按F5刷新
		#self.showMsg("when forcus on btn,key enter down.")
		if not self.thread:
			key = evt.GetKeyCode()
			if key == wx.WXK_F5:
				self.doScanPress = True     #相当于按下了doScan按钮
				self.doOpenTheLocation()
			evt.Skip()
	#--------------------------------------------------------------------------------------
	#   以上是触发扫描硬盘的几个命令
	#--------------------------------------------------------------------------------------
	def doOpenTheLocation(self):
		'''
		Procedure:打开工作位置,获取目录下递归工作结构（ls）
		Input:事件触发
		Notice:ls 数据结构[{'Name':name,'isDir':True,'size':size,'pos':0,'w':0,'h':0},{'Name':name2,'isDir':False...},...]'''
		if not self.thread: 
			self.CopyTheWorkFlowArgs()					#拷贝工作流需要的初始化参数
			#self.showMsg('in doOpenTheLocation, self.wf_dir is '+self.wf_dir)
			#dir_ = self.locationText.GetValue()+'\\'
			#dir_ = self.to_unicode_or_bust(dir_)       #转化成unicode
			#print dir_
			#consoleText.AppendText(dir_)
			#self.ShowProgress()
			self.width,self.height = self.getWindowSize()
			################################
			if not self.pro:                                                        #如果未建立进度条
				self.pro = Progress(self,(self.width,self.height))              #建立进度条
			################################
			#timerProgress.Start(milliseconds=1000,oneShot=False)
			self.thread = getAllSizeThread.GetAllSizeThread(self.wf_dir,self)     #创建一个工作进程
			self.thread.start()    #启动进程
			"""try:
				fileNameList= os.listdir(dir_)
				
				for fname in fileNameList:
					pathName = dir_+fname
					#print pathName
					pathStat = os.stat(pathName)
					#entity_fileName = {'fileName':pathName}
					if S_ISDIR(pathStat.st_mode):
						size=getdirsize(pathName)
						isDir = True
						#entity_fileName['isDir']=True
						#dict_fileNamesOneLevel.append(entity_fileName)
					else :
						size=os.path.getsize(pathName)
						isDir = False
						#entity_fileName['isDir']=False
						#dict_fileNamesOneLevel.append(entity_fileName)
					dictSize={'name':pathName,'size':size,'isDir':isDir,'pos':0,'w':0,'h':0}
					sizes.append(dictSize)
				"""	
				#dialog.Add("NOW OPEN THE LOC:::::::::")
				#dialog.Add("the row of origin dir is :"+str(len(sizes))+'\n')
				
				#for i in range(len(sizes)):
					#dialog.Add(sizes[i]['name']+"->"+str(sizes[i]['size'])+'\n')
			#dialog.Add("---------------\n")
	def SimpleStopThread(self):
		self.showMsg("Work thread stopped.")
		self.thread.stop()         #停止进程
		self.thread = None
		if self.pro:               #停止进度条
			self.pro.stopProgress()
			self.pro = None
	def DoneWithGetAllSize(self,sizes):
		#self.sizes = sizes
		#self.consoleText.AppendText("the thread call main thread "+str(self.sizes)+"\n")
		self.showMsg("Work thread invoke main.")
		self.thread.stop()  #停止进程
		self.thread = None
		self.ls = self.getMaxs(sizes)  #得到排序后的前n大size。
			#sizes[:]=sizes[:maxButtons]
		self.showMsg("---------------")
		for i in range(len(self.ls)):
			self.showMsg(self.ls[i]['name'] + "->" + self.HowMuchM(self.ls[i]['size'])) 
		self.showMsg("---------------")
		#--------------------------------------------
		# Treemap  需要的，去除之就是Treemap顺序执行。
		#self.ls = ChoiceRandomLs.ReUnitLs(self.ls)  #将ls乱序重排。
		#--------------------------------------------
			#for i in range(len(ls)):
				#dialog.Add("ReUnit ls["+str(i)+"] is : "+ str(ls[i]['size']))
			#dialog.Add("ReUnited ls is :  "+str(ls)+'\n')
			
			# self.d = DevideModule.DevideRec()
			# theWindwoSize= getWindowSize()
			# theWidth = theWindwoSize[0]
			# theHeight = theWindwoSize[1]

		self.width,self.height = self.getWindowSize()
		"""except:
			consoleText.AppendText("\n The work object Is a File,or invalide, can't open it.")
			#pass"""
		#self.destroyProgress()
		################################
		if self.pro:
			self.pro.stopProgress()              #删除进度条
			self.pro = None
		################################
		try:
			#self.consoleText.AppendText(str(self.ls)+'   '+str(theWidth)+' '+str(theHeight))
			#self.showMsg(str(theWidth)+' '+str(theHeight))
			self.caculatelsCondition(self.ls,self.width,self.height-20)    #这里使用魔数凑够下边的空白
		except Exception,err:
			self.consoleText.AppendText("Run devide failure.\n")
			self.consoleText.AppendText(str(Exception)+str(err))
	def getMaxs(self,ls):
		"""ls:list,in,return: ls,has 3 items,top 3 large size.
		To getMaxs the ls[i]['level'] which is larger
		"""
		#print "I'm in sort!"
		for i in range(len(ls)):
			max=ls[i]['size']
			for j in range(i+1,len(ls)):
				curr=ls[j]['size']  # from 1 :...
				if curr>max:
					max=curr
					temp=ls[i]
					ls[i]=ls[j]
					ls[j]=temp
		#print ls
		if self.wf_MaxBtnNum > -1:
			ls=ls[:self.wf_MaxBtnNum]
		return ls
	def caculatelsCondition(self,ls,theW,theH):
		#self.currDir=self.locationText.GetValue()
		if self.fifo == []:      #新建一个工作目录，工作目录原记录为空
			self.consoleText.AppendText("\n===============\n")
			#self.consoleText.AppendText("the fifo is empty.\n")
			self.ls = self.myDevide(ls,theW,theH)    #按贪心算法算出需排布的按钮长宽和位置。
			self.consoleText.AppendText("The currDir:"+ self.wf_dir +"\n") 
			self.fifo.push((self.wf_dir,self.ls))

		elif self.fifo != [] and self.wf_dir != self.fifo.getCurr()[0]:	#打开一个工作目录，和当前工作目录记录不同																	 
				
			self.consoleText.AppendText("\n===============\n")
			#self.consoleText.AppendText("theWidth."+ str(theW) +"\ntheHeight."+str(theH)+"\n---------------\n")
			#self.consoleText.AppendText("The fifo has value ,but not equal to TextCtrl.\n")
			#self.consoleText.AppendText("The Original ls before devide is :\n"+ str(ls)+"\n---------------\n")
			self.ls = self.myDevide(ls,theW,theH)    #按贪心算法算出需排布的按钮长宽和位置。 
			self.consoleText.AppendText("The currDir:"+ self.wf_dir +"\n")
			if self.doScanPress and not self.btnPress:     #直接修改地址栏后单击doScan按钮，而非点击Btn后单击doScan按钮，注意按钮直接双击这句也不执行
				self.fifo.popit()
				self.doScanPress = False
			self.fifo.push((self.wf_dir,self.ls))
		else:                                     #刷新一个工作目录，和工作目录记录相同
			self.consoleText.AppendText("\n===============\n")
			#self.consoleText.AppendText("The same with textDIR:\n")	
			#self.ls = fifo.getCurr()[1]
			#self.ls = DevideModule.devide(self.ls,theWidth,theHeight)
			self.ls = self.myDevide(ls,theW,theH)    #按贪心算法算出需排布的按钮长宽和位置。
			self.fifo.update((self.wf_dir,self.ls))     #替换当前的文件路径和列表
		self.btnPress = False         # 判断完了是否按钮点击，恢复原值。
		self.doScanPress = False
		self.showButtons(self.ls)
	
	def myDevide(self,ls,theW,theH):
		self.showMsg("=====ls=====")
		self.showMsg(str(ls))
		myls = DevideModule.devide(ls,theW,theH-self.toolHeight-self.titleHeight-100)  #theWidth/2  只占界面的左边一半  toolHeight  Y轴起始位置  titleHeight 标题栏的高度
		self.showMsg("=====Devided=====")
		self.showMsg(str(myls))
		return myls

	def showButtons(self,ls):
		'''
		Procedure: 按获取的区域和按钮列表，排布按键。
		Input:ls:数据结构[{'fileName':name,'isDir':True},{'fileName':name2,'isDir':False},...]
			  theWidth: 画布宽度
			  theHeight:画布高度'''
		#global buttons
		#for i in range(len(ls)):
			#dialog.Add('L['+ str(i) +']: '+ str(ls[i])+"\n")
			#dialog.Add("---------------\n")
		#dialog.Add("in OpenLocation,before destroy Buttons is : "+str(buttons)+"\n")
		self.destroyButtons(self.buttons)
		#self.consoleText.AppendText("\nThe devided ls(to generate buttton) 's len() is "+ str(len(ls)) +" \n---------------\n")
		j = self.generateButton(ls)  #排布按钮
		self.consoleText.AppendText("Generated "+ str(j) +" buttons.\n---------------\n")

		self.setButtonLabels(j,ls)

		#vbox0.Clear()
		#panel.Refresh()
	def generateButton(self,L):
		"""  
		Function:从保有按钮长宽和坐标的列表L描绘出所有按钮
		Input: L is the list with coordinate value
		Output: 生成的按钮数
		Date:  2014-01-10 
		"""
		if len(L) == 0:
			return 0
		#pass
		#vbox0.Clear(True)
		#global buttons
		i=0
		#vbox0= wx.BoxSizer(wx.VERTICAL)
		#if self.buttons == None:
		# if self.wf_MaxBtnNum != -1:
		# 	self.buttons = [None]*self.wf_MaxBtnNum  # 重新初始化按钮列表，使用工作流参数
		# else:
		btnNum = len(L)
		self.buttons = [None]*btnNum            #这里不能用currBtnNum。因为不scan该值就没有初始化，在prev和next时就会出问题
		#self.consoleText.AppendText("in generate button,initaial Buttons is : "+str(self.buttons)+"\n")
		self.panel.ClearBackground() 
		self.panel.Refresh()
		self.Refresh()
		#self.consoleText.AppendText("len(L): "+str(len(L))+"\n")
		#self.showMsg("before Generate buttons , len(L) is :")
		#self.showMsg(str(len(L)))
		for i in range(btnNum):
			position=(int(L[i]['pos'][0]),int(L[i]['pos'][1]))
			sizeofB = (int(L[i]['w']),int(L[i]['h']))
			self.buttons[i]=wx.Button(self.panel,id=i,label = str(i),pos = position,size=sizeofB)
			tip = wx.ToolTip('TEST')
			self.buttons[i].SetToolTip(tip)
			tip.SetTip(self.buttons[i].GetLabel())
			self.buttons[i].Bind(wx.EVT_BUTTON,self.goThrough)    #统一事件处理程序 
			self.buttons[i].Bind(wx.EVT_LEFT_DCLICK,self.btnDClick)   ##鼠标双击，直接进入下一层目录。
			self.Bind(wx.EVT_KEY_DOWN,self.btnKeyDown,self.buttons[i])
			#self.buttons[i].Bind(wx.EVT_KEY_DOWN,self.btnKeyDown)                          
			#self.consoleText.AppendText("\nbutton("+str(i)+")):" + str(position) + "  "+str(sizeofB))
		#self.consoleText.AppendText("\n---------------\n")
		# hbox3.Add(vbox0,proportion=1,flag=wx.EXPAND|wx.LEFT,border=5)
		# hbox3.ShowItems(True)
		# vbox.ShowItems(True)
		
		return i+1   #生成了i+1个按钮

	def setButtonLabels(self,j,ls):
		'''Procedure:给所有的button配置标签
		   Input：NONE'''
		#global buttons
		if self.buttons:
			#for i in range(len(buttons)):    #len(ls) == maxButtons refer to getMaxs(ls). 不能用len(buttons)，因为当有空目录或文件时它比L多
			for i in range(j):
				# if i < len(ls):
					#self.consoleText.AppendText(ls[i]['name']+'->'+str(ls[i]['size'])+'\n')
					self.buttons[i].SetLabel(ls[i]['name']+' '+self.HowMuchM(ls[i]['size'])+(' isDir'if (ls[i]['isDir']) else ' isFile'))  #如果是File，则不可以goThrough下一步了，这个要处理。另外如果是File为何没有name和size值？
					if not ls[i]['isDir']:
						self.buttons[i].SetBackgroundColour(self.color)
						self.buttons[i].SetOwnForegroundColour('#000000')
					else:
						self.buttons[i].SetBackgroundColour(self.dirColor)
						self.buttons[i].SetOwnForegroundColour('#000000')
					#self.buttons[i].SetLabel(ls[i]['name']+' '+self.HowMuchM(ls[i]['size'])+(' isDir'if (ls[i]['isDir']) else ' isFile'))  #如果是File，则不可以goThrough下一步了，这个要处理。另外如果是File为何没有name和size值？
					
					tip = self.buttons[i].GetToolTip()
					tip.SetTip(self.buttons[i].GetLabel())
				# else:
					# buttons[i].SetLabel("None")
					# tip = buttons[i].GetToolTip()
					# tip.SetTip(buttons[i].GetLabel())
			self.consoleText.AppendText("\n===============\n")
		else:
			pass

	def destroyButtons(self,buttons):
		for i in buttons:
			#self.consoleText.AppendText("Before DestroyButton,Button[i] is : "+str(i)+'\n')
			if i:
				i.Destroy()
				#self.consoleText.AppendText(" --and it destroyed .\n")
	###################################################################################################
	#  工作流结束
	###################################################################################################
	def goThrough(self,event):
		'''
		Procedure： 单击按钮的事件处理程序，找到按钮的序号，将ls同序号的name写入地址栏。
		Input:event of button onClick
		Date: 2013-11-16'''
		self.btnPress = True
		if self.ls:
			for i in range(len(self.ls)):
				if event.GetEventObject()==self.buttons[i]:
					if not self.thread:         #没有工作进程，可以点击新的按钮       
						self.locationText.SetValue(self.ls[i]['name'])
					else:						#工作进程运行当中，不能点击新的按钮
						if (self.locationText.GetValue() != self.ls[i]['name']):
							self.showMsg(u"工作进程运行当中，点击新的按钮不起作用")
		#触发一个open按钮的点击，用以触发打开工作位置的动作：
		#	。。。
		event.Skip()
	# def ShowProgress(self):
	# 	self.timerProgress.Start(milliseconds=1000,oneShot=False)
	# 	#w,h = getWindowSize()
	# 	self.txtProgress = wx.StaticText(self.panel, -1, "|",(self.winWidth/2, self.winHeight/2)) 
	# def OnProgressTimer(self,event):
	# 	if (self.iProgress < 3 ):
	# 		self.iProgress += 1
	# 	else:
	# 		self.iProgress = 0
	# 	#self.consoleText.AppendText(self.lsProgress[self.iProgress]+' '+str(self.winWidth)+' '+str(self.winHeight)+'\n')
	# 	if self.txtProgress:
	# 		self.txtProgress.setLabel(self.lsProgress[self.iProgress])
	# def destroyProgress(self):
	# 	if self.timerProgress:
	# 		self.showMsg(str(self.timerProgress))
	# 		self.timerProgress.Destroy()			
	# 	if self.txtProgress:
	# 		self.showMsg(str(self.txtProgress))
	# 		self.txtProgress.Destroy()

	def getWindowSize(self):
		'''
		Function:获取当前程序窗口大小 
		Input：NONE 
		Output: tuple(width,height)  tuple 窗口大小 
		author: SamJi 
		blog:http://blog.csdn.net/cava15 
		date:2014-03-12'''
		#窗口结构         
		class RECT(ctypes.Structure):  
			_fields_ = [('left', ctypes.c_long),  
					('top', ctypes.c_long),  
					('right', ctypes.c_long),  
					('bottom', ctypes.c_long)]  
			def __str__(self):  
				return str((self.left, self.top, self.right, self.bottom))
		rect = RECT()
		#获取当前窗口句柄  
		HWND = win32gui.GetForegroundWindow()
		
		#取当前窗口坐标  
		ctypes.windll.user32.GetWindowRect(HWND,ctypes.byref(rect))
		
		#global width,height
		width = rect.right-rect.left
		height = rect.bottom-rect.top
		return (width,height)
	def GetFramePosition(self):
		w,h = self.GetScreenPosition()
		return (w+self.width/2,h+self.height/2)
	def HowMuchM(self,i):
		if i>1024*1024*1024:
			i=round(i/1024.00/1024.00/1024.00,2)
			return str(i)+'G'
		if i>1024*1024:
			i=round(i/1024.00/1024.00,2)
			return str(i)+'M'
		if i>1024:
			i=round(i/1024.00,2)
			return str(i)+'K'
		return str(i)+'Byte'

	def OnCloseWindow(self,evt):
		if self.continueFromLast == 1:  #下次从本次记录的地方开始
			try:
				with open(self.currDir+'\\abc.pkl', 'wb+') as f:
					pickle.dump(self.fifo,f)
				#f.close()
				#dlg = wx.MessageDialog(None,"I'm in savePickle","A Message",wx.OK | wx.ICON_INFORMATION)
				#retCode = dlg.ShowModal()
			except:
				dlg = wx.MessageDialog(None,u"无法保存查询记录，建议程序使用系统管理员权限启动。","A Message",wx.OK | wx.ICON_INFORMATION)
				retCode = dlg.ShowModal()
		#self.Destroy()
		evt.Skip()	


	ls = []         #记录各个方框的数据 myFrame.property
	#currDir = u""    #记录当前目录
	#sizes = []      #记录工作目录的所有项目（所有项目大小）
	#width = 0        #窗口宽度
	#height = 0		 #窗口高度
	#txtProgress = None
	#lsProgress = ["|","/","-","\\"]
	#iProgress = 0

	pro = None
	thread = None

	wf_dir = u""				#工作流参数，只用于工作流，当前工作目录
	wf_MaxBtnNum = 0			#工作流参数，只用于工作流，最大按钮数

	fifo = StackWithPoint.FIFOWithPoint([])
	
	#color = wx.Colour(red=0,green=246,blue=169)  #file按钮的颜色    亮绿色荧光色
	color = wx.Colour(red=173,green=223,blue=250)  #file按钮的颜色  浅蓝色
	dirColor = wx.NamedColour('#E3E3E3')            #dir按钮的颜色   浅灰色   LIGHT GREY '#C0C0C0'
	#color = wx.Colour(red=0,green=76,blue=115)  #file按钮的颜色    深蓝色
	toolHeight = 39	       #原值为65：Y轴起始位置(工具栏的高度)
	titleHeight = 39	   #标题栏的高度
	maxButtons = 24		   #最大按钮数	
	continueFromLast = 0   #表示使用全新界面
	#currBtnNum = 0        #当前按钮数量，根据检索来的数据变化，当maxButtons==-1时启用	
	activedOnce = False    #OnActive初次执行过没	   
	resizedTwice = 0       #OnResize初次执行过两次没
	doScanPress = False    #没有点击doScan按钮
	btnPress = False       #没有点击任何一个生成的按钮

	Icon = None            #“设置”对话框的图标
	IconBundle = None      #图标群
	#def OnDestroy(self):
		#self.dialog.Destroy()
	#def OnMove(self,event):
     #   pos = event.GetPosition()
      #  self.posCtrl.SetValue("%s,%s" % (pos.x,pos.y))
	  
class MyApp(wx.App):
	"""MyApp class is an application class"""
	def OnInit(self):
		self.frame = MyFrame()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True
	def OnExit(self):
		#self.frame.savePickle()
		pass
	def OnDestroy(self):
		#self.frame.savePickle()
		self.frame.Destroy()
		# self.frame.dialog.Destroy()
		# return True
def main():
	app = MyApp()
	try:
		app.MainLoop()
		
	except:
		raw_input('Press any key to terminate the app')
	
if __name__=='__main__': 
	main()
				
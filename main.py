
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from database import Db

import sqlite3
import hashlib
import subprocess

## TODO
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SHOULD ONLY ALLOW ONE TO OPEN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!





class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.titles=""" 
        [anchor=title1][size=24]Forest-Biotech[/size]  
        [anchor=subtitle][size=20]Nanodrop usage logger[/size] 
        """

        self.content="""
        [anchor=content]
        Be sure to clean the equipment before and after each usage.

        To request a login to use this equipment please send an email to: brunovasquescosta@gmail.com 
        For a fast addition respect the following structure:
        - Subject: account nanodrop 
        - Text: Desired login, name & group name.
        """
        self.cols = 1
        self.padding=[100,10,100,10]
        self.add_widget(Label(text=self.titles,markup=True,halign="center"))
        self.add_widget(Label(text=self.content,markup=True,halign="justify"))

        self.username = TextInput(multiline=False)
        self.password = TextInput(password=True, multiline=False)
        self.button = Button(text="Login",size_hint_x=None, width=100)
        self.button.bind(on_press=self.callback)
        
        self.loginGrid=GridLayout(cols=3,row_force_default=True,row_default_height=40)
        self.loginGrid.add_widget(Label(text='username',halign="right"))
        self.loginGrid.add_widget(self.username)
        self.loginGrid.add_widget(Label(text=''))
        self.loginGrid.add_widget(Label(text='password',halign="right"))
        self.loginGrid.add_widget(self.password)
        self.loginGrid.add_widget(self.button)

        self.add_widget(self.loginGrid)

        ###### REMOVE #################
        ##self.db=Db()
        ##self.loadLoggedMenu()
        ###### ###### #################


    def makePopup(self,content):
        popupGrid=GridLayout(cols=1)
        popupGrid.add_widget(Label(text=content,halign="justify"))
        popupButton=Button(text='OK')
        popupGrid.add_widget(popupButton)
        

        self.popup = Popup(title='Authentication',
                content=popupGrid,
                size_hint=(None,None),
                size=(200,200))

        popupButton.bind(on_press=self.popup.dismiss)

    def callback(self,instance):
        self.passHash=hashlib.sha256()
        self.passHash.update(bytes(self.password.text, 'utf-8'))
        self.validateLogin()

    def validateLogin(self):
        self.db=Db()        
        userdata=self.db.getUser(self.username.text)

        if ( type(userdata)==tuple and len(userdata)>4):
            self.ID=str(userdata[0])
            self.USERNAME=userdata[1]
            self.NAME=userdata[2]
            dbHash=userdata[4]
            self.USERNAME
        else:
            dbHash=None
        
        passwordHash=self.passHash.hexdigest()
        if ( passwordHash == dbHash ):
            self.makePopup("Login succeeded!")
            self.loadLoggedMenu()
        else:
            self.makePopup("Login Error!\n Wrong login or password!")
        self.popup.open()


    def loadLoggedMenu(self,instance=None):
        self.clear_widgets()
        self.btn1 = Button(text="Start Nanodrop")
        self.btn1.bind(on_press=self.startProgram)             
        self.btn2 = Button(text="settings") #Set nanodrop path
        self.btn2.bind(on_press=self.loadSettingsMenu)
        self.btn3 = Button(text="admin") #Create user, Change password, see all users
        self.btn3.bind(on_press=self.loadAdminMenu)             
        self.btn4 = Button(text="show activity") #Table, export data
        self.btn4.bind(on_press=self.showActivity)   

        self.add_widget(Label(text=self.titles,markup=True,halign="center"))
        #Login name and logout button
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)
        self.add_widget(self.btn4)


    def userPanel(self,instance):
        userGrid=GridLayout(cols=4,row_force_default=True,row_default_height=40)
        #Label User: Label(Name), button(logout), button(main menu) 
        userGrid.add_widget(Label(text="User: ",font_size="20sp",halign="left",size_hint_x=None, width=80))
        userGrid.add_widget(Label(text=self.NAME,font_size="20sp",halign="left",size_hint_x=None, width=150))
        btnLogout=Button(text="logout",size_hint_x=None, width=100)
        #btnLogout.bint(on_press=)
        btnMainMenu=Button(text="main menu")
        btnMainMenu.bind(on_press=self.loadLoggedMenu)   
        userGrid.add_widget(btnLogout)
        userGrid.add_widget(btnMainMenu)


        instance.add_widget(userGrid)


    def startProgram(self,instance):
        self.makePopup("Simulating Nanodrop!")
        self.popup.open()
        #subprocess.call(["c:\\"])

        self.db.logActivity(self.ID) 

    def loadAdminMenu(self,instance):
        self.clear_widgets()
        self.add_widget(Label(text=self.titles,markup=True,halign="center"))
        self.btn1 = Button(text="create user")
        self.btn1.bind(on_press=self.loadCreateUserMenu)   
        self.btn2 = Button(text="change password") #Set nanodrop path
        self.btn2.bind(on_press=self.loadChangePasswordMenu)
        self.btn3 = Button(text="see users") #Create user, Change password, see all users
        self.btn3.bind(on_press=self.loadShowUsers)
        self.btn4 = Button(text="back to main menu") #Table, export data
        self.btn4.bind(on_press=self.loadLoggedMenu)


        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)
        self.add_widget(self.btn4)


    def loadSettingsMenu(self,instance):
        self.clear_widgets()
        self.add_widget(Label(text=self.titles,markup=True,halign="center"))
        

        #uix.filechooser https://kivy.org/doc/stable/api-kivy.uix.filechooser.html

        pathValue=self.db.getPath()
        if( type(pathValue) == tuple ):
            pathValue=pathValue[0]
        else:
            pathValue=""

        self.path=TextInput(text=pathValue,multiline=False)
        settingsGrid=GridLayout(cols=2,row_force_default=True,row_default_height=40)
        settingsGrid.add_widget(Label(text="path",halign="left",size_hint_x=None, width=100))
        settingsGrid.add_widget(self.path)
        settingsGrid.add_widget(Label(text="",halign="left",size_hint_x=None, width=100))
        self.btn1 = Button(text="save path")
        self.btn1.bind(on_press=self.savePath)
        settingsGrid.add_widget(self.btn1)

        self.btn2 = Button(text="back to main menu")
        self.btn2.bind(on_press=self.loadLoggedMenu)

        self.add_widget(settingsGrid)
        self.add_widget(self.btn2)


    def showActivity(self,instance):
        TABLE_HEADER="30sp"

        self.clear_widgets()
        self.add_widget(Label(text=self.titles,markup=True,halign="center"))
        self.userPanel(self)
        settingsGrid=GridLayout(cols=4,row_force_default=True,row_default_height=40)
        settingsGrid.add_widget(Label(text="Group",font_size=TABLE_HEADER,halign="center",size_hint_x=None, width=100))
        settingsGrid.add_widget(Label(text="Name",font_size=TABLE_HEADER,halign="center",size_hint_x=None, width=100))
        settingsGrid.add_widget(Label(text="Date",font_size=TABLE_HEADER,halign="center",size_hint_x=None, width=200))
        settingsGrid.add_widget(Label(text="Samples",font_size=TABLE_HEADER,halign="center",size_hint_x=None, width=100))
        
        self.scrollView=ScrollView(size_hint_x=1, size_hint_y=None)
        self.scrollView.add_widget(settingsGrid)
        self.add_widget(self.scrollView)
        
        for row in self.db.getLogs(4):
            for cell in row:
                settingsGrid.add_widget(Label(text=str(cell),halign="center"))


    def savePath(self,instance):    
        #Check that path exists
        self.db.setPath(self.path.text)    
        self.makePopup("Path added")
        self.popup.open()


    def loadCreateUserMenu(self,instance):
        self.clear_widgets()

        self.username=TextInput(multiline=False)
        self.name=TextInput(multiline=False)
        self.password=TextInput(password=True,multiline=False)
        self.passwordRep=TextInput(password=True,multiline=False)
        self.group=TextInput(multiline=False)
        self.admin=Switch(active=False)
        self.enabled=Switch(active=True)
        self.pb = ProgressBar(max=100,size_hint_x=None, width=120)

        self.passwordRep.bind(text=self.on_password)

        settingsGrid=GridLayout(cols=2,row_force_default=True,row_default_height=40)
        settingsGrid.add_widget(Label(text="username",halign="left",size_hint_x=None, width=120))
        settingsGrid.add_widget(self.username)
        settingsGrid.add_widget(Label(text="name",halign="left",size_hint_x=None, width=120))
        settingsGrid.add_widget(self.name)        
        settingsGrid.add_widget(Label(text="password",halign="left",size_hint_x=None, width=120))
        settingsGrid.add_widget(self.password)
        settingsGrid.add_widget(Label(text="repeat password",halign="left",size_hint_x=None, width=120))
        settingsGrid.add_widget(self.passwordRep)        
        settingsGrid.add_widget(Label(text="group",halign="left",size_hint_x=None, width=120))
        settingsGrid.add_widget(self.group)
        settingsGrid.add_widget(Label(text="admin",halign="left",size_hint_x=None, width=120))
        settingsGrid.add_widget(self.admin)
        settingsGrid.add_widget(self.pb) 
        self.btn1 = Button(text="add user")
        self.btn1.bind(on_press=self.createUser)
        settingsGrid.add_widget(self.btn1)
        
        self.add_widget(settingsGrid)
        self.btn4 = Button(text="back to main menu") #Table, export data
        self.btn4.bind(on_press=self.loadLoggedMenu)

        self.add_widget(self.btn4)



    def on_password(self,instance,value):
        score=0
        if(len(value)<=8):
            score=len(value)*10
        
        if(len(value)>8):
            score=80

        if(value==self.password.text):
            score=score*1
        else:
            score=score*0

        self.pb.value= score


    def loadChangePasswordMenu(self,instance):
        self.clear_widgets()

        self.username=TextInput(multiline=False)
        self.password=TextInput(password=True,multiline=False)
        self.passwordRep=TextInput(password=True,multiline=False)
        self.pb = ProgressBar(max=100,size_hint_x=None, width=120)
        
        settingsGrid=GridLayout(cols=2,row_force_default=True,row_default_height=40)
        settingsGrid.add_widget(Label(text="username",halign="left",size_hint_x=None, width=120))
        settingsGrid.add_widget(Label(text=self.USERNAME,halign="left")) #### SET THIS TO user
        settingsGrid.add_widget(Label(text="password",halign="left",size_hint_x=None, width=120))
        settingsGrid.add_widget(self.password)
        settingsGrid.add_widget(Label(text="repeat password",halign="left",size_hint_x=None, width=120))
        settingsGrid.add_widget(self.passwordRep)        
        settingsGrid.add_widget(self.pb)
        self.passwordRep.bind(text=self.on_password)

        self.btn1 = Button(text="change password")
        self.btn1.bind(on_press=self.changePassword)
        settingsGrid.add_widget(self.btn1)


        self.add_widget(settingsGrid)

        self.btn4 = Button(text="back to main menu") #Table, export data
        self.btn4.bind(on_press=self.loadLoggedMenu)

        self.add_widget(self.btn4)

    
    def createUser(self,instance):
        self.passHash=hashlib.sha256()
        self.passHash.update(bytes(self.passwordRep.text, 'utf-8'))
        hash=self.passHash.hexdigest()
        admin=0
        print(self.admin.active)
        if(self.admin.active):
            admin=1

        if( self.pb.value > 50 ):
            if (self.username is None or self.name is None or self.group is None):
                self.makePopup("Error: Not all fields were filled!")
                self.popup.open()  
            else:
                try:
                    self.db.setUser(self.username.text,self.name.text,self.group.text,hash,admin)
                    self.makePopup("User created")
                    self.popup.open()
                except sqlite3.OperationalError as err:
                    self.makePopup("Error: "+err)
                    self.popup.open()                


    def changePassword(self,instance):
        self.passHash=hashlib.sha256()
        self.passHash.update(bytes(self.passwordRep.text, 'utf-8'))
        hash=self.passHash.hexdigest()
        if( self.pb.value > 50 ):
            try:
                self.db.setPassword(self.ID,hash)
                self.makePopup("Password changed")
                self.popup.open()
            except sqlite3.OperationalError as err:
                self.makePopup("Error: "+err)
                self.popup.open()

    def loadShowUsers(self, instance):
        TABLE_HEADER="30sp"

        self.clear_widgets()
        self.add_widget(Label(text=self.titles,markup=True,halign="center"))
        self.userPanel(self)
        settingsGrid=GridLayout(cols=5,row_force_default=True,row_default_height=40)
        settingsGrid.add_widget(Label(text="User",font_size=TABLE_HEADER,halign="center",size_hint_x=None, width=100))
        settingsGrid.add_widget(Label(text="Name",font_size=TABLE_HEADER,halign="center",size_hint_x=None, width=100))
        settingsGrid.add_widget(Label(text="Group",font_size=TABLE_HEADER,halign="center",size_hint_x=None, width=200))
        settingsGrid.add_widget(Label(text="admin",font_size=TABLE_HEADER,halign="center",size_hint_x=None, width=100))
        settingsGrid.add_widget(Label(text="enabled",font_size=TABLE_HEADER,halign="center",size_hint_x=None, width=100))
        

        self.add_widget(settingsGrid)
        
        for row in self.db.listUsers():
            for cell in row:
                settingsGrid.add_widget(Label(text=str(cell),halign="center"))



class MainMenu(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MainMenu().run()
    









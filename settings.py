class Settings:
    def __init__(self,this):
        self=this

    def loadSettingsMenu(self,instance):
        self.clearWindow()
        self.add_widget(Label(text=self.titles,markup=True,halign="center"))
        
        pathValue=self.db.getPath()
        print(pathValue)
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
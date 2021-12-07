from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, DictProperty, BooleanProperty, NumericProperty
from kivy.utils import rgba as RGBA
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import platform
from CustomModalView import CustomModalView
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from security import *
import os

app = None
Window.clearcolor = RGBA('#292B2F')

if platform == 'win':
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Screen_Manager(ScreenManager):
    pass

class SignUp(Screen):
    def signup_and_verify(self):
        if self.ids.password.text == self.ids.cpassword.text:
            if len(self.ids.password.text) > 8:
                if len(self.ids.username.text) > 4:
                    print("Signup Success")
                    global app
                    username_hash = blake(self.ids.username.text)                
                    password_hash = blake(self.ids.password.text)                
                    credentials = username_hash + password_hash
                    credentials = credentials.encode("utf-8")
                    os.mkdir("../SuperUserData/")
                    app.write_file("Credentials.bin", credentials)
                    app.generate_key_pair()
                    self.manager.transition = SlideTransition(direction="right")
                    self.manager.current = "login"
                else:
                    self.ids.message.text = "Username must be greater than 4 characters."
            else:
                self.ids.message.text = "Password should be greater than 8 characters."
        else:
            self.ids.message.text = "The passwords do not match, try again."
            print("passwords do not match")

class Login(Screen):
    def auth(self):
        username_hash = blake(self.ids.username.text)                
        password_hash = blake(self.ids.password.text)                
        credentials = username_hash + password_hash
        try:
            stored_hash = app.read_file("Credentials.bin").decode("utf-8")
            if stored_hash == credentials:
                global app
                app.credentials = credentials
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = "sendblock"
            else:
                self.ids.message.text = "Login Failed"
        except:
            self.ids.message.text = "You need to SignUp first!"
        
    def signup(self):
        global app
        if app.checkUser():
            self.ids.message.text = "User Exists Already."
        else:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "signup"

class LoadPopupDesign(BoxLayout):
    pass

class SendBlock(Screen):
    def send(self):
        global app
        design = LoadPopupDesign()
        loadPopup = CustomModalView(
                                size_hint = (0.7, 0.8),
                                size_hint_max = (dp(450),dp(550)),
                                size_hint_min = (dp(325),dp(400)),
                                custom_color = app.theme["primary"],
                                opacity = 0,
                                pos_hint = {'center_x': -2, 'center_y':0.5 }
                           )
        loadPopup.add_widget(design)
        loadPopup.open(loadPopup.pos_hint, {'center_x': 0.5, 'center_y': 0.5}, "out_expo")
        # read medical record
        medical_record = app.read_json_file("medical_record.json") 

        


class RecieveBlocks(Screen):
    pass

class superNodeApp(App):
    fonts = DictProperty({"main": "Fonts/Montserrat-SemiBold.ttf", "regular": "Fonts/Montserrat-Regular.ttf"})
    theme = DictProperty({"primary_dark": RGBA("#292B2F"), "primary": RGBA("#2F3136"), 
                          "secondary_dark": RGBA("#36393F"), "secondary": RGBA("#40444B"),
                          "font1": RGBA("#697279"), "font2": RGBA("#ffffff")
                        })
    home = StringProperty('../SuperUserData/')

    def read_file(self, file):
        with open(self.home+file, 'rb') as f:
            return f.read()

    def write_file(self, file, content):
        with open(self.home+file, 'wb') as f:
            f.write(content)
    
    def write_json_file(self, file, content):
        with open(self.home+file, 'w') as f:
            json.dump(content, f, indent=2)

    def read_json_file(self, file):
        with open(self.home+file, 'w') as f:
            return json.load(f)

    def checkUser(self):
        try:
            if os.path.isfile("../SuperUserData/Credentials.bin"):
                return True
            return False
        except:
            return False
    def generate_key_pair():
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()

    def on_start(self):
        Window.clearcolor = self.theme["primary"]
    def build(self):
        global app
        app = self

if __name__ == "__main__":
    superNodeApp().run()

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, DictProperty, BooleanProperty, NumericProperty
from kivy.utils import rgba as RGBA
from kivy.core.window import Window
from security import *
import os

app = None
Window.clearcolor = RGBA('#292B2F')

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
                    os.mkdir("../UserData/")
                    app.write_file("Credentials.bin", credentials)
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
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = "sendblocks"
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

class SendBlocks(Screen):
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
        fileName = self.ids.medical_record_path.text
        medical_record = app.read_json_file(fileName) 
        private_key = app.fetch_private_key()
        # create a block for user block chain 
        block = Block()
        block.medical_data = medical_record
        block.signer_hash = app.credentials
        block.signature = pkcs1_15.new(signerPrivateKey).sign(hashObj)
        # send it to user 
        serializedBlockList = [pickle.dumps(block)]
        server_connect(self.ids.ip.text, self.ids.port.text, serializedBlockList)
        


class RecieveBlock(Screen):
    pass

class LoadPopupDesign(BoxLayout):
    pass

class nodeApp(App):
    fonts = DictProperty({"main": "Fonts/Montserrat-SemiBold.ttf", "regular": "Fonts/Montserrat-Regular.ttf"})
    theme = DictProperty({"primary_dark": RGBA("#292B2F"), "primary": RGBA("#2F3136"), 
                          "secondary_dark": RGBA("#36393F"), "secondary": RGBA("#40444B"),
                          "font1": RGBA("#697279"), "font2": RGBA("#ffffff")
                        })
    home = StringProperty('../UserData/')

    def read_file(self, file):
        with open(self.home+file, 'rb') as f:
            return f.read()

    def write_file(self, file, content):
        with open(self.home+file, 'wb') as f:
            f.write(content)
    
    def write_json_file(self, file, content):
        with open(self.home+file, 'w') as f:
            json.dump(content, f, indent=2)

    def read_json_file(self, file, content):
        with open(self.home+file, 'w') as f:
            return json.load(f)

    def checkUser(self):
        try:
            if os.path.isfile("../UserData/Credentials.bin"):
                return True
            return False
        except:
            return False

    def on_start(self):
        Window.clearcolor = self.theme["primary_dark"]
    def build(self):
        global app
        app = self

if __name__ == "__main__":
    nodeApp().run()

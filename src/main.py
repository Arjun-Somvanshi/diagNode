from kivy.app import App
from kivy.lang import Builder

kv = Builder.load_string('''
BoxLayout:
    Button:
        text: "hello"
        ''')

class healthNodeApp(App):
    #This is the instance of the app object
    def build(self):
        #This functions runs when the app is lauched
        return kv

if __name__ == "__main__":
    healthNodeApp().run()

from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import ListProperty

Builder.load_string('''
<CustomModalView>:
    canvas:
        Color:
            rgba: root.custom_color 
        Rectangle:
            size: self.size
            pos: self.pos
    background: '' 

''')

class CustomModalView(ModalView): # here I have made a custom modal view so that it can handle animations 
                                  # instead of typing the whole deal over and over, the open and dismiss are new                  
    custom_color = ListProperty([1,1,1,1])
    def open(self, pos_hint_initial = {}, pos_hint_final = {}, 
             t = '', d1=0.7, d2=0.7, animate = True, *largs, **kwargs):
        if animate: # we have to parameters to decide whether animation should occur or
        # not, incase, the user decides to not use animations on slow hardware, app.animations will be set to false, 
        # if the developer doen't wanna use the animation then he/she can set animate to false
            self.disabled = True
            self.pos_hint = pos_hint_initial
            anim = Animation(pos_hint = pos_hint_final, t = t, duration = d1)
            anim &= Animation(opacity = 1, t=t, duration=d2)
            anim.start(self)
            anim.bind(on_complete=self.enable_popup)
        else: 
            self.opacity = 1
            self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        super(CustomModalView, self).open(*largs, **kwargs)
    
    def enable_popup(self, *args):
        self.disabled = False
    
    def dismiss(self, pos_hint_final = {}, t = '', d1=0.7, d2=0.75, animate = True, *largs, **kwargs):
        #print('dismissing')
        self.disabled = True
        if animate:
            anim = Animation(pos_hint = pos_hint_final, t = t, duration = d1)
            anim &= Animation(opacity = 0, t=t, duration = d2)
            anim.start(self)
            anim.bind(on_complete = self.finish_dismiss) # binding the on_complete callback, to finish dismiss()
        else:
            super(CustomModalView, self).dismiss()

    def finish_dismiss(self, *args):
        super(CustomModalView, self).dismiss()

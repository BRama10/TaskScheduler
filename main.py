from kivy.app import App

from kivy.config import Config
Config.set('graphics', 'width',  800)
Config.set('graphics', 'height', 600)

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.graphics import Color, Rectangle

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.floatlayout import MDFloatLayout

import time
from datetime import datetime


#colorScheme = {'choice 1' : { 'background' : , 'foreground' : },
#               'choice 2' : { 'background' : , 'foreground' : },
#               }
with open('settings.txt', 'r+') as file:
    contents=file.read().splitlines()

colorScheme = contents[3][1:]


def getInterval(c):
    hour = c[0:2]
    minute = int(c[3:5])
    interval_minute = None

    if minute - 30 >= 0:
        interval_minute = '30'
    else:
        interval_minute = '00'

    return hour+':'+interval_minute
        
def getColor(timeDict, time):
    global colorScheme

    if colorScheme == 'black-red':
        if(timeDict.get(time) == []):
            return [1,1,1,0.5] #kinda default grey
        return 'black'
    elif colorScheme == 'purple-green':
        if(timeDict.get(time) == []):
            return [1,1,1,0.5] #kinda default grey
        return 'purple'
    elif colorScheme == 'yellow-grey':
        if(timeDict.get(time) == []):
            return [1,1,1,0.5] #kinda default grey
        return 'yellow'    
    elif colorScheme == 'blue-pink':
        if(timeDict.get(time) == []):
            return [1,1,1,0.5] #kinda default grey
        return 'blue'

def getButtonColor():
    global colorScheme

    if colorScheme == 'black-red':
        return 'black'
    elif colorScheme == 'purple-green':
        return 'purple'
    elif colorScheme == 'yellow-grey':
        return 'yellow'    
    elif colorScheme == 'blue-pink':
        return 'blue'

    
class TimeReader():
    def __init__(self, filename='times.txt'):
        self.filename = filename
        self.times = []
        self.readFile = dict()

    def ReadFile(self):
        with open(self.filename, 'r+') as file:
            lst = file.read().splitlines()

        thisDict, currTimeIndex = dict(), 0

        for n in range(len(lst)):
            if '#' in lst[n]:
                if not(lst[n] in thisDict.keys()):
                    thisDict[lst[n][1:]] = []
                currTimeIndex = n

            if '$' in lst[n]:
                thisDict[lst[currTimeIndex][1:]].append(lst[n][1:])

        self.times = list(thisDict.keys())
        self.readFile = thisDict

    def WriteFile(self):
        with open(self.filename, 'w+') as file:
            for x in self.times:
                file.write('#'+x+'\n')
                
                for y in self.readFile.get(x):
                    file.write('$'+y+'\n')

                file.write('\n\n')

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class ChoiceWindow(Screen):
        def __init__(self, **kwargs):
            super(ChoiceWindow, self).__init__(**kwargs)

        def screen_transition_curr_it(self, *args):
            self.manager.current = 'today'

        def screen_transition_settings(self, *args):
            self.manager.current = 'settings'

        def screen_transition_scratch_pad(self, *args):
            self.manager.current = 'scratch'

        def screen_transition_future(self, *args):
            self.manager.current = 'future'
        
        def on_enter(self):
            with self.canvas:
                if colorScheme == 'black-red':
                    Color(255, 0, 0)
                elif colorScheme == 'purple-green':
                    Color(0, 255, 0)
                elif colorScheme == 'yellow-grey':
                    Color(0.502,0.502,0.502)
                elif colorScheme == 'blue-pink':
                    print('here')
                    Color(1., 0.753, 0.796)
                
                Rectangle(pos=(0, 0), size=(2000, 2000))
            
            self.btn1 = Button(text='Modify Today\'s Itinerary',pos=(0,380), size_hint=(.5,.5), background_color=getButtonColor())
            self.btn2 = Button(text='Modify Later Itineraries', pos=(400,380), size_hint=(.5,.5), background_color=getButtonColor())
            self.btn3 = Button(text='Alerts',pos=(0,100), size_hint=(.5,.3), background_color=getButtonColor())
            self.btn4 = Button(text='Scratchpad',pos=(400,100), size_hint=(.5,.3), background_color=getButtonColor())
            self.btn5 = Button(text='Settings',pos=(720,0), size_hint=(.1,.1), background_color=getButtonColor())

            self.btn1.bind(on_press=self.screen_transition_curr_it)
            self.btn2.bind(on_press=self.screen_transition_future)
            self.btn4.bind(on_press=self.screen_transition_scratch_pad)
            self.btn5.bind(on_press=self.screen_transition_settings)
        
            self.layout=FloatLayout()
            self.layout.add_widget(self.btn1)
            self.layout.add_widget(self.btn2)
            self.layout.add_widget(self.btn3)
            self.layout.add_widget(self.btn4)
            self.layout.add_widget(self.btn5)
            
            
            self.add_widget(self.layout)
            
class ItineraryWindow(Screen):
        def __init__(self,TYPE=None, **kwargs):
            super(ItineraryWindow, self).__init__(**kwargs)
            self.type = TYPE

        def on_enter(self):

            time_btn_list = []

            tr = TimeReader()
            tr.ReadFile()
            if self.type == 'today':
                now = datetime.now()

                now_str = now.strftime("%m/%d/%Y %H:%M:%S")
    
                date = now_str[0:10]
                time = now_str[11:]

                curr_interval = getInterval(time)
                timeIndex = tr.times.index(curr_interval)
    
           
                for x in range(timeIndex, len(tr.times)):
                    time_btn_list.append(Button(text=tr.times[x],background_color=getColor(timeDict=tr.readFile, time=tr.times[x])))
                    print(tr.times[x], getColor(timeDict=tr.readFile, time=tr.times[x]))

            

                self.layout = GridLayout(cols=4)
            
                for x in time_btn_list:
                    x.bind(state=self.callback)
                    self.layout.add_widget(x)

                self.back_btn = Button(text ='Back')
                self.back_btn.bind(on_press = self.move_back)

                self.layout.add_widget(self.back_btn)
                
            self.add_widget(self.layout)

        def callback(self, instance, value):
            self.screen_transition_x(name=instance.text)

        def screen_transition_x(self, name, *args):
            self.manager.current = name

        def move_back(self, *args):
            self.manager.current = 'choice'
            
class TimeWindow(Screen):
        def __init__(self, **kwargs):
            super(TimeWindow, self).__init__(**kwargs)

        

        def on_enter(self):
            tr = TimeReader()
            tr.ReadFile()
            notes = '\n'.join(tr.readFile.get(self.name))
            
            self.viewer = TextInput(text=notes)
            self.save_btn = Button(text='Save',pos=(720,0), size_hint=(.1,.1))
            self.back_btn = Button(text='Back',pos=(0,0), size_hint=(.1,.1))

            self.save_btn.bind(on_press = self.save_entry)
            self.back_btn.bind(on_press = self.move_back)

            self.layout = BoxLayout()
            self.layout.add_widget(self.viewer)
            self.layout.add_widget(self.save_btn)
            self.layout.add_widget(self.back_btn)

            self.add_widget(self.layout)

        def move_back(self, *args):
            self.manager.current = 'today'

        def save_entry(self, *args):
            entries_temp = self.viewer.text.split('\n')
            entries = []

            for x in entries_temp:
                if not(x == '' or x == ' ' or x == '  '):
                    entries.append(x)
            
            tr = TimeReader()
            tr.ReadFile()
            tr.readFile[self.name] = entries
            tr.WriteFile()

class SettingWindow(Screen):
        def __init__(self, **kwargs):
            super(SettingWindow, self).__init__(**kwargs)

        def on_enter(self):
            with open('settings.txt', 'r+') as file:
                contents = file.read().splitlines()
            
            with self.canvas:
                if colorScheme == 'black-red':
                    Color(255, 0, 0)
                elif colorScheme == 'purple-green':
                    Color(0, 255, 0)
                elif colorScheme == 'yellow-grey':
                    Color(0.502,0.502,0.502)
                elif colorScheme == 'blue-pink':
                    Color(1., 0.753, 0.796)

                Rectangle(pos=(0, 0), size=(2000, 2000))

            with self.canvas:
                Color(1, 1, 1)

                Rectangle(pos=(60, 540), size=(150, 20))

            with self.canvas:
                Color(1, 1, 1)

                Rectangle(pos=(270, 380), size=(250, 30))
            
            self.name_label = Label(text='Enter your name: ', pos=(-50,460), size_hint=(.5,.3),color='blue')
            self.name_input = TextInput(text=contents[1][1:], pos=(250,540), size_hint=(.5,.06), multiline=False)
            self.name_input.bind(text=self.on_enter_key)
            self.color_choice_title = Label(text='Choose Your Color Scheme Below', pos=(200, 300), size_hint=(.5, .3), color='blue')

            self.layout=FloatLayout()
            self.layout.add_widget(self.name_label)
            self.layout.add_widget(self.name_input)
            self.layout.add_widget(self.color_choice_title)

            self.choice1_btn = Button(text='Blue/Pink', size_hint=(.2, .2), pos=(0,80))
            self.choice2_btn = Button(text='Yellow/Grey', size_hint=(.2, .2), pos=(200,80))
            self.choice3_btn = Button(text='Purple/Green', size_hint=(.2, .2), pos=(400,80))
            self.choice4_btn = Button(text='Black/Red', size_hint=(.2, .2), pos=(600,80))

            self.choice1_btn.bind(state=self.callback)
            self.choice2_btn.bind(state=self.callback)
            self.choice3_btn.bind(state=self.callback)
            self.choice4_btn.bind(state=self.callback)

            self.layout.add_widget(self.choice1_btn)
            self.layout.add_widget(self.choice2_btn)
            self.layout.add_widget(self.choice3_btn)
            self.layout.add_widget(self.choice4_btn)

            self.back_btn = Button(text='Back',pos=(0,0), size_hint=(.1,.1), background_color=getButtonColor())
            self.back_btn.bind(on_press=self.move_back)
            
            self.layout.add_widget(self.back_btn)

            self.add_widget(self.layout)

        def on_enter_key(self, instance, value):
            with open('settings.txt', 'r+') as file:
                contents = file.read().splitlines()
                contents[1] = '*'+instance.text

            with open('settings.txt', 'w+') as file:
                for x in contents:
                    file.write(x + '\n')

        def callback(self, instance, value):
            global colorScheme
            
            with open('settings.txt', 'r+') as file:
                contents = file.read().splitlines()
            if instance.text == 'Blue/Pink':
                contents[3] = '*'+'blue-pink'
            elif instance.text == 'Yellow/Grey':
                contents[3] = '*'+'yellow-grey'
            elif instance.text == 'Purple/Green':
                contents[3] = '*'+'purple-green'
            elif instance.text == 'Black/Red':
                contents[3] = '*'+'black-red'

            colorScheme = contents[3][1:]
            
            with open('settings.txt', 'w+') as file:
                for x in contents:
                    file.write(x + '\n')
                    
            self.manager.current = 'choice'

        def move_back(self, *args):
            self.manager.current = 'choice'

    
        
class ScratchPadWindow(Screen):
        def __init__(self, **kwargs):
            super(ScratchPadWindow, self).__init__(**kwargs)

        def on_enter(self):
            self.back_btn = Button(text='Back',pos=(0,0), size_hint=(.1,.1), background_color=getButtonColor())
            self.back_btn.bind(on_press=self.move_back)

            with open('scratchpad_text.txt', 'r+') as file:
                self.pad = TextInput(text=file.read())
                self.pad.bind(text=self.constant_save)

            self.layout = BoxLayout()
            self.layout.add_widget(self.pad)
            self.layout.add_widget(self.back_btn)

            self.add_widget(self.layout)
            
        def move_back(self, *args):
            self.manager.current = 'choice'

        def constant_save(self, instance, value):
            with open('scratchpad_text.txt', 'w+') as file:
                file.write(instance.text)

class FutureItineraryWindow(Screen):
        def __init__(self, **kwargs):
            super(FutureItineraryWindow, self).__init__(**kwargs)
            if self.name == 'future':
                self.btn = MDRaisedButton(text='Choose Date', pos=(100,500), size_hint=(.3,.1), on_press = self.show_date_picker)
                self.name_label = Label(text='', pos=(280,440), size_hint=(.5,.3),color='blue', font_size=('32sp'))
                
                self.layout = MDFloatLayout()
                self.layout.add_widget(self.btn)
                self.layout.add_widget(self.name_label)

                self.add_widget(self.layout)

        def on_enter(self):
            if self.name == 'future_detail':
                #self.add_widget(
                pass

        def show_date_picker(self, *args, **kwargs):
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
            date_dialog.open()

        def on_cancel(self, instance, value):
            tempvar=5

        def on_save(self, instance, value, datePicker):
            self.chosen_date = value
            #self.manager.current = 'future_detail'
            date_str = self.chosen_date.strftime("%m/%d/%Y")
            self.name_label.text = date_str
            
            #self.value_itinerary = TextInput()
            
            

class Application(MDApp):
    def build(self):
        sm = ScreenManagement(transition=FadeTransition())
        sm.add_widget(ChoiceWindow(name='choice'))
        sm.add_widget(ItineraryWindow(name='today', TYPE='today'))
        sm.add_widget(SettingWindow(name='settings'))
        sm.add_widget(ScratchPadWindow(name='scratch'))
        sm.add_widget(FutureItineraryWindow(name='future'))
        sm.add_widget(FutureItineraryWindow(name='future_detail'))

        tr = TimeReader()
        tr.ReadFile()

        
        for x in tr.readFile:
            sm.add_widget(TimeWindow(name = x))
        return sm


if __name__ == "__main__":
    Application().run()

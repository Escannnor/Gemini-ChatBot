from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from tools import Gemini

class ChatInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        chat_box = BoxLayout(orientation='horizontal', size_hint_y=0.9)

        self.scroll_view = ScrollView()
        self.chat_history = Label(text='', size_hint_y=None, halign='left', valign='top')
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.scroll_view.add_widget(self.chat_history)
        chat_box.add_widget(self.scroll_view)

        self.user_input = TextInput(multiline=False, size_hint_x=0.9)

        send_button = Button(text='Send', size_hint_x=0.2)
        send_button.bind(on_press=self.send_message)
        
        input_box = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        input_box.add_widget(self.user_input)
        input_box.add_widget(send_button)

        self.add_widget(chat_box)
        self.add_widget(input_box)
        
    def send_message(self, instance):
        gemini_instance = Gemini(api_key='AIzaSyDcDjyhSdWPNuMxoi_iNPM58TTBGvHsscQ')
        message = self.user_input.text
        if message == '':
            message = "end of message"
        response = gemini_instance.response(message=message)
        self.chat_history.text += f'You: {message}\n'
        self.chat_history.text += f'Gemini: {response}\n\n' 
        self.user_input.text = ''
        self.chat_history.parent.scroll_y = 0  

class ChatApp(App):
    def build(self):
        return ChatInterface()

if __name__ == '__main__':
    ChatApp().run()
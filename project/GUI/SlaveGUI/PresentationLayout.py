from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

from Constants.ContentType import ContentType
from Domain.PresentationElement import PresentationElement


class PresentationLayout(Screen):
    """
    Fullscreen layout for presenting content
    """
    image_source = StringProperty('')
    text_element = StringProperty('')
    video_source = StringProperty('')

    def __init__(self, **kwargs):
        """
        In the constructor the class and instance are passed
        to the superclass' __init__ function
        """
        super(PresentationLayout, self).__init__(**kwargs)
        self.slave = None
        self.presentation_type = None
        self.start_screen = PresentationElement(ContentType.Image, "background/black_as_kivys_soul.png")

    def on_pre_enter(self, *args):
        self.hide_widgets()

    def on_enter(self, *args):
        self.slave = App.get_running_app().servicemode
        self.slave.set_layout(self)
        self.set_visible_widget(self.start_screen)
        self.slave.reset_presentation()

    def init_presentation(self):
        """
        Do not delete! Called when starting presentation if the slave is already in presentation
        :return: Nothing
        """
        pass

    def set_visible_widget(self, element):
        """
        Sets the visible widget according to the presentation's type

        Hides the "picture" widget if TextPresentation
        Hides the "text_field" widget if PicPresentation

        presentation_type:  a PresentationType object
        """
        self.hide_widgets()

        if element.element_type == ContentType.Text:
            self.text_element = element.get_content()
            self.show_widget(self.ids.text_field)
        elif element.element_type == ContentType.Image:
            self.image_source = element.get_content()
            self.show_widget(self.ids.picture)
        elif element.element_type == ContentType.Video:
            self.video_source = element.get_content()
            self.show_widget(self.ids.video)
            self.ids.video.state = 'play'

    def show_widget(self, widget):
        """
        Shows a given widget. Unlike in the hiding, height doesn't need to be modified when showing widget. Otherwise
        acts as a counter-method for the hide_widget method.
        :param widget:
        :return: Nothing
        """
        widget.opacity = 1
        widget.size_hint_y = 1

    def hide_widgets(self):
        """
        Hides all of the different type of widgets.
        :return: Nothing
        """
        self.hide_widget(self.ids.picture)
        self.hide_widget(self.ids.text_field)
        self.hide_widget(self.ids.video)

    def hide_widget(self, widget):
        """
        Hides a widget. Size_hint_y and height are set to zero, so that the widgets do not take up space in the screen.
        Opacity is also set to zero, in case the widget would be still visible (text-elements need this to be hidden
        properly)
        :param widget:
        :return: Nothing
        """
        widget.opacity = 0
        widget.size_hint_y = 0
        widget.height = '0dp'

    def show(self, content):
        """
        Shows the next element of the show
        """
        if self.presentation_type == ContentType.Image:
            self.image_source = content
        elif self.presentation_type == ContentType.Text:
            self.text_element = content

    def reset_presentation(self):
        """
        Resets the presentation to the starting state
        """
        self.ids.picture.source = ''
        self.get_root_window().show_cursor = True
        self.slave.reset_presentation()
        self.parent.get_screen('slave_gui_layout').set_info_text("Presentation ended\nCurrently in slave mode")
        App.get_running_app().root.change_screen_to("slave_gui_layout")

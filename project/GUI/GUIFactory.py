from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from Domain.Command import Notification
from Domain.ContentType import ContentType
from Domain.MessageKeys import MessageKeys
from Domain.PresentationElement import PresentationElement
from kivy.app import App

"""
CLASS LIBRARY TO HANDLE THE FUNCTIONALITY OF GUI LAYOUTS

The layouts' components, administrative information (such as
ids and names) and functions to perform on triggered events
are defined in the layout file:

project/GUI/remu.kv
"""


class SwitchLayout(Screen):
    """
    Produces the GUI-layout that allows the user to choose
    between Master- and Slave-mode.

    Inherits kivy.uix.screenmanager.Screen
    """
    text = StringProperty('')

    def add_address(self, address):
        self.text = address

class MasterGUILayout(Screen):
    """
    Produces the Master-mode's GUI-layout that allows the
    user to communicate with Slave-devices.

    Inherits kivy.uix.screenmanager.Screen
    """

    label_text = StringProperty('')
    slave_presentation = {}

    def __init__(self, **kwargs):
        super(MasterGUILayout, self).__init__(**kwargs)
        self.presentation = None
        self.hide_button(self.ids.show_next)

    def on_pre_enter(self):
        self.master = App.get_running_app().get_master(self)

    def set_address_to_gui(self, address):
        """
        Sets the address for GUI purposes, but does not control the actual connection
        """
        self.label_text = address

    def add_slave_connection(self, address):
        self.master.add_slave(address)

    def send_message_to_slave(self):
        self.master.request_next()

    def start_presentation(self):
        self.hide_button(self.ids.start_pres)
        self.show_button(self.ids.show_next)
        self.master.send_presentations_to_slaves()

    def hide_button(self, widget):
        widget.opacity = 0
        widget.size_hint_y = 0
        widget.size_hint_x = 0
        widget.width = '0dp'

    def show_button(self, widget):
        widget.opacity = 1
        widget.size_hint_y = 1
        widget.size_hint_x = 1

    def show_master_back_popup(self):
        """
        Opens the warning pop-up to master, asking if they are sure they want to go back
        """
        MasterBackPopUp().open()

    def generate_presentation(self, data):
        """
        Generate the presentation information on the layout on connection to a slave.
        """
        self.remove_slave_presentation(data)
        print("Creating a new slave presentation widget")
        slave_widget = SlavePresentation(data)
        self.slave_presentation[data.full_address] = slave_widget
        self.ids.middle.add_widget(slave_widget)

    def remove_slave_presentation(self, data):
        """
        Remove possibly existing SlavePresentation widget based on the
        SlaveConnection object
        """
        if data.full_address in self.slave_presentation:
            self.ids.middle.remove_widget(self.slave_presentation[data.full_address])

    def update_presentation_status(self, data=None):
        """
        Update the presentation status on the layout
        """
        print("päivitetään")
        for slave_connection in self.slave_presentation.values():
            slave_connection.update_status()

    def update_connection_to_gui(self, data):
        """
        Sets the slave address to be shown in the gui
        """
        self.set_address_to_gui(str(data))

    def notify(self, notification, data):
        """
        Handles the received notification from master

        notification:   a Notification enum
        data:           an object
        """
        return self.messagehandler[notification](self, data)

    """
    A dictionary of Notification-Function pairs for the purpose of
    updating the layout on predefined events.
    """
    messagehandler = {Notification.PRESENTATION_UPDATE: generate_presentation,
                      Notification.PRESENTATION_STATUS_CHANGE: update_presentation_status,
                      Notification.CONNECTION_FAILED: update_connection_to_gui,
                      Notification.CONNECTION_ESTABLISHED: update_connection_to_gui,
                      Notification.CONNECTION_TERMINATED: remove_slave_presentation}


class SlaveGUILayout(Screen):
    """
    Produces the Slave-mode's GUI-layout that reacts to
    the Master-devices commands.

    Inherits kivy.uix.screenmanager.Screen
    """

    # layout uses this StringProperty to show current service mode
    info_text = StringProperty('Currently in slave mode')

    def __init__(self, **kwargs):
        """
        In the constructor the class and instance are passed
        to the superclass' __init__ function
        """
        super(SlaveGUILayout, self).__init__(**kwargs)
        self.slave = None

    def on_pre_enter(self, *args):
        if self.slave is None:
            self.slave = App.get_running_app().get_slave(self)

    def init_presentation(self):
        App.get_running_app().init_presentation()
        self.prepare_for_presentation_mode()

    def prepare_for_presentation_mode(self):
        """
        Sets the app's main window to full screen and hides the
        mouse cursor.
        """
        window = self.get_root_window()
        window.show_cursor = False

    def show_slave_back_popup(self):
        """
        Opens the warning pop-up to slave, asking if they are sure they want to go back
        """
        SlaveBackPopUp().open()

    def set_info_text(self, info_text):
        self.info_text = info_text


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

    def set_presentation_mode(self, presentation_type):
        """
        Sets the right media widget based on the presentation mode.

        presentation_type:  a PresentationType object
        """
        self.set_visible_widget(presentation_type)
        self.presentation_type = presentation_type
        print(self.presentation_type)

    def set_visible_widget(self, element):
        """
        Sets the visible widget according to the presentation's type

        Hides the "picture" widget if TextPresentation
        Hides the "text_field" widget if PicPresentation

        presentation_type:  a PresentationType object
        """
        self.hide_widgets()

        if element.type == ContentType.Text:
            self.text_element = element.get_content()
            self.show_widget(self.ids.text_field)
        elif element.type == ContentType.Image:
            self.image_source = element.get_content()
            self.show_widget(self.ids.picture)
        elif element.type == ContentType.Video:
            self.video_source = element.get_content()
            self.show_widget(self.ids.video)
            self.ids.video.state = 'play'

    def show_widget(self, widget):
        widget.opacity = 1
        widget.size_hint_y = 1

    def hide_widgets(self):
        self.hide_widget(self.ids.picture)
        self.hide_widget(self.ids.text_field)
        self.hide_widget(self.ids.video)

    def hide_widget(self, widget):
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
        App.get_running_app().root.current = "slave_gui_layout"


"""
MasterBackPopUp and SlaveBackPopUp classes represent the popups that take the master or slave back to the switch layout 
if they decide to break the connection
"""


class MasterBackPopUp(Popup):
    pass


class SlaveBackPopUp(Popup):
    pass


class SlavePresentation(BoxLayout):
    """
    SlavePresentation is the visual presentation of the slave in the master view. It contains information about the slave's
    state and visuals associated with it
    """
    presentation_data = None

    def __init__(self, data):
        super(SlavePresentation, self).__init__()
        self.slave = data
        self.ids["btn_address"].text = data.full_address
        self.presentation_data = data.presentation
        self.visuals = []
        self.current_active = data.currently_showing
        self.create_visual_widgets()

    def create_visual_widgets(self):
        """
        Creates the visual widgets for the slave's visuals
        """
        for i in range(0, len(self.presentation_data)):
            filename = self.presentation_data[i][:100] #[0][:100]
            if len(filename) == 100:
                filename += "..."
            visual = SlaveVisualProperty(filename)
            self.visuals.append(visual)
            self.ids.visuals.add_widget(visual)
        self.show_next()

    def show_next(self):
        """
        Highlights the next visual, indicating it is the currently active visual
        """
        self.visuals[self.current_active].set_inactive()
        self.current_active = self.slave.currently_showing
        if self.current_active is not -1:
            self.visuals[self.current_active].set_active()

    def update_status(self):
        """
        Checks if the tracked SlaveConnection has updated; updates the widget if needed
        """
        if not self.slave.connected:
            self.ids["btn_address"].background_color = [0.94, 0.025, 0.15, 1]
        self.show_next()

    def get_address(self):
        return self.ids["btn_address"].text


class SlaveVisualProperty(Button):
    """
    SlaveVisualProperty is the class of the slave's visuals. It represents a single visual property of the slave's properties
    """

    visual_name = StringProperty('')

    def __init__(self, image_source):
        super(SlaveVisualProperty, self).__init__()
        self.visual_name = image_source
        self.background_normal = ''
        self.background_color = [0.5, 0.5, 0.5, 1]

    def on_press(self):
        print("Showing visual property information not yet implemented!")

    def set_active(self):
        self.background_color = [0.3, 0.6, 0.3, 1]

    def set_inactive(self):
        self.background_color = [0.5, 0.5, 0.5, 1]


from kivy.uix.behaviors import DragBehavior
from Domain.Presentation import Presentation

class DraggablePresentationElement(DragBehavior, Button):

    ELEMENT_WIDTH = 40
    ELEMENT_HEIGHT = 0

    def __init__(self, pres, parent):
        super(DraggablePresentationElement, self).__init__()
        self.text = pres
        self.pseudoparent = parent
        self.updating = False
        self.old_x = self.x

    def on_y(self, *largs):
        self.y = self.parent.y

    def on_x(self, *largs):
        pass
        """
        if not self.updating and abs(self.x-self.old_x) > self.ELEMENT_WIDTH:
            self.old_x = self.x
            self.pseudoparent.update_us(self)
            self.x = self.old_x
        """

    def on_touch_up(self, touch):
        super(DraggablePresentationElement, self).on_touch_up(touch)
        self.pseudoparent.update_us(self)

    def __lt__(self, other):
        return self.x > other.x


class RobustPresentationEditView(BoxLayout):

    def __init__(self, **kwargs):
        super(RobustPresentationEditView, self).__init__(**kwargs)
        self.content = []

    def create_dynamically_editable_presentation_view_that_works_like_kivy(self):
        pres = Presentation()
        pres.load()
        for prescontent in pres.get_presentation_content():
            print(prescontent)
            temp = DraggablePresentationElement(prescontent, self)
            self.ids.presentation_elements.add_widget(temp)
            self.content.append(temp)

    def update_us(self, element=None):
        self.content.sort()
        self.ids.presentation_elements.children.sort()
        """
        for i in range(len(self.content)):
            self.content[i].old_x = self.content[i].x
            if element and element.text == self.content[i].text:
                continue
            self.content[i].updating = True
            #self.content[i].y = DraggablePresentationElement.ELEMENT_HEIGHT
            self.content[i].x = i*DraggablePresentationElement.ELEMENT_WIDTH+40
            self.content[i].updating = False
        """
        print("updated!")

    def create_presentation(self):
        presentation = Presentation()
        for i in range(len(self.content)):
            presentation.presentation_filenames.append(self.content[i].text)
        print(presentation.get_presentation_content())
        return presentation



class PresentationCreationLayout(Screen):


    def on_pre_enter(self, *args):
        self.edit_views = []
        view = RobustPresentationEditView()
        view.create_dynamically_editable_presentation_view_that_works_like_kivy()
        self.ids.views.add_widget(view)
        self.edit_views.append(view)

    def create_a_new_presentation_to_edit(self):
        view = RobustPresentationEditView()
        view.create_dynamically_editable_presentation_view_that_works_like_kivy()
        self.ids.views.add_widget(view)
        self.edit_views.append(view)





class RemuSM(ScreenManager):
    """
    Handles changing the GUI-layouts as different screens for the
    application, and also acts as the root widget

    Inherits kivy.uix.screenmanager.ScreenManager
    """

    def __init__(self, **kwargs):
        """
        Initializes references to differents screens as 'None'
        """
        super(RemuSM, self).__init__(**kwargs)
        self.master_screen = None
        self.slave_screen = None
        self.presentation_screen = None
        self.presentation_creation_screen = None

    def add_master_layout(self):
        """
        Creates a new master layout, and sets it to be the current screen
        """
        if self.master_screen is None:
            self.master_screen = MasterGUILayout(name='master_gui_layout')
            self.add_widget(self.master_screen)
        self.current = 'master_gui_layout'

    def add_slave_layout(self):
        """
        Creates a new slave layout and a presentation layout, and sets the slave layout
        to be the current screen
        """
        if self.slave_screen is None:
            self.slave_screen = SlaveGUILayout(name='slave_gui_layout')
            self.presentation_screen = PresentationLayout(name='presentation_layout')
            self.add_widget(self.slave_screen)
            self.add_widget(self.presentation_screen)
        self.current = 'slave_gui_layout'

    def add_presentation_creation_layout(self):
        if self.presentation_creation_screen is None:
            self.presentation_creation_screen = PresentationCreationLayout(name='presentation_creation_layout')
            self.add_widget(self.presentation_creation_screen)
        self.current = 'presentation_creation_layout'

    """
    Changes the screen according to the screen name parameter
    """
    def change_screen_to(self, name):
        """
        Changes the screen according to the screen name parameter
        """
        self.current = name

    def rm_master_layout(self):
        """
        Removes the master layout from screenmanager's screens
        """
        self.remove_widget(self.master_screen)
        self.change_screen_to("switch_layout")

    def rm_slave_layout(self):
        """
        Removes the slave layout and the presentation layout from screenmanager's screens
        """
        self.remove_widget(self.slave_screen)
        self.remove_widget(self.presentation_screen)
        self.change_screen_to("switch_layout")


class GUIFactory:
    """
    GUIFactory defines the functions for the layout components
    The current running app is set as the GUIFactory instance's
    parent in Main.py
    """
    remuapp = None

    def __init__(self):
        pass

    def set_parent(self, remuapp):
        """
        Sets the current running app as the GUIFactory instance's
        parent
        """
        self.remuapp = remuapp

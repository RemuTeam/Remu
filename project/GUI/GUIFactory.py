from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout

from Domain.ContentType import ContentType
from Domain.PresentationElement import PresentationElement
from GUI.MasterGUILayout import MasterGUILayout
from GUI.PopUps import ExceptionAlertPopUp, SlaveBackPopUp
from GUI.ProjectOverview import ProjectOverview

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

    def goto_master_mode(self):
        """
        Setups the app to be used in the master mode
        :return: ExceptionAlertPopup if adding master not possible
        """
        app = App.get_running_app()
        try:
            app.root.add_master_layout()
        except Exception as ex:
            app.reset_servicemode()
            app.root.rm_master_layout()
            ExceptionAlertPopUp("Error going to master mode:", ex).open()


    def add_address(self, address):
        self.text = address

class InfoLayout(Screen):
    with open('infotext.txt') as f:
        t = f.read()
    text = t


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
            self.slave.set_layout(self)

    def init_presentation(self):
        self.prepare_for_presentation_mode()

    def prepare_for_presentation_mode(self):
        """
        Sets the app's main window to full screen and hides the
        mouse cursor.
        """
        window = self.get_root_window()
        window.show_cursor = False
        App.get_running_app().root.change_screen_to("presentation_layout")

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

    def init_presentation(self):
        """
        Do not delete! Called when starting presentation if the slave is already in presentation
        :return: Nothing
        """
        pass

    def set_presentation_mode(self, presentation_type):
        """
        Sets the right media widget based on the presentation mode.

        presentation_type:  a PresentationType object
        """
        self.set_visible_widget(presentation_type)
        self.presentation_type = presentation_type

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


class SlavePresentation(StackLayout):
    """
    SlavePresentation represents slave's presentation in the master view. It contains information about the visuals it
    holds, as well as the current state of the presentation
    """

    def __init__(self, presentation):
        super(SlavePresentation, self).__init__()
        self.presentation_data = presentation
        self.visuals = []
        self.current_active = -1
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
            self.add_widget(visual)
        self.visualize_next()

    def update_presentation_content(self, import_list):
        """
        Adds SlaveVisualProperties to the SlavePresentation object
        :param import_list: list of presentation elements' filenames to be added to the presentation
        :return:
        """
        self.current_active = -1
        self.create_visual_widgets()
        self.presentation_data = import_list

    def get_presentation_from_widgets(self):
        self.visuals.sort()
        self.visuals = self.visuals[::-1]
        presentation_content = []
        for i in range(len(self.children)):
            presentation_content.append(self.children[i].visual_name.split("/")[-1])
        return presentation_content[::-1]

    def visualize_next(self):
        """
        Highlights the next visual, indicating it is the currently active visual
        """
        if self.current_active == -1:
            self.current_active += 1
            return -1
        self.visuals[self.current_active - 1].set_inactive()
        if self.current_active == len(self.visuals):
            self.current_active = -1
        if -1 < self.current_active < len(self.visuals):
            self.visuals[self.current_active].set_active()
            self.current_active += 1
        return self.current_active

    def reset(self):
        self.current_active = 0
        for visual in self.visuals:
            visual.set_inactive()

    def update_status(self):
        """
        Checks if the tracked SlaveConnection has updated; updates the widget if needed
        """
        #if not self.slave.connected:
        #    self.ids["btn_address"].background_color = [0.94, 0.025, 0.15, 1]
        return self.visualize_next()

    def get_address(self):
        return self.ids["btn_address"].text

    def get_presentation_size(self):
        return len(self.presentation_data)


from kivy.uix.behaviors import DragBehavior

class SlaveVisualProperty(DragBehavior, Button):
    """
    SlaveVisualProperty is the class of the slave's visuals. It represents a single visual property of the slave's properties
    """

    visual_name = StringProperty('')

    def __init__(self, image_source):
        super(SlaveVisualProperty, self).__init__()
        self.visual_name = image_source
        self.background_normal = ''
        self.background_color = [0.5, 0.5, 0.5, 1]
        self.old_x = self.x
        self.being_moved = False
        self.going_forward = True

    def on_press(self):
        print("Showing visual property information not yet implemented!")

    def set_active(self):
        self.background_color = [0.3, 0.6, 0.3, 1]

    def set_inactive(self):
        self.background_color = [0.5, 0.5, 0.5, 1]

    def on_y(self, *largs):
        """
        Keeps the object on the same y coordinate as its parent.
        :param largs:
        :return:
        """
        self.y = self.parent.y

    def on_touch_down(self, touch):
        """
        Called when you start dragging the object around. Updates that the object is, in fact, being dragged which is
        used in the method on_x to determine whether updating is necessary.
        :param touch:
        :return:
        """
        super(SlaveVisualProperty, self).on_touch_down(touch)
        self.old_x = self.x
        self.being_moved = True

    def __lt__(self, other):
        """
        Compares the object's x coordinate with another object's and for some reason returns if the object's x is greater than rather than less than;
        it just works this way
        :param other: Another SlaveVisualProperty object
        :return: boolean whether the object is greater than other.
        """
        return self.x > other.x

    def on_touch_up(self, touch):
        """
        Cleans up the list of visuals after you release a dragged presentation element.
        :param touch:
        :return:
        """
        super(SlaveVisualProperty, self).on_touch_up(touch)
        self.being_moved = False
        self.parent.children.sort()

    def is_update_required(self):
        """
        Determines if the button has been moved far enough that it would require rearrangement.
        Caller on_x
        :return: boolean of whether the rearrangement is in order
        """
        if self.going_forward:
            return self.x-self.old_x > self.width + 5 or abs(self.x-self.old_x) > self.width + 20
        return self.old_x-self.x < self.width + 5 or abs(self.x-self.old_x) > self.width + 20

    def on_x(self, *largs):
        if self.is_update_required() and self.being_moved:
            self.going_forward = self.x - self.old_x > 0
            self.old_x = self.x
            self.parent.children.sort()
            temp = self.x
            self.x = self.old_x
            self.old_x = temp


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
        self.info_screen = None

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

    def add_info_layout(self):
        if self.info_screen is None:
            self.info_screen = InfoLayout(name='info_gui_layout')
            self.add_widget(self.info_screen)
        self.current = 'info_gui_layout'

    def change_screen_to(self, name):
        """
        Changes the screen according to the screen name parameter
        """
        self.current = name

    def rm_master_layout(self):
        """
        Removes the master layout from screenmanager's screens
        """
        #self.remove_widget(self.master_screen)
        self.master_screen=None
        self.change_screen_to("switch_layout")

    def rm_slave_layout(self):
        """
        Removes the slave layout and the presentation layout from screenmanager's screens
        """
        self.remove_widget(self.slave_screen)
        self.remove_widget(self.presentation_screen)
        self.slave_screen=None
        self.presentation_screen=None
        self.change_screen_to("switch_layout")

    def get_current_layout(self):
        return self.current_screen


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

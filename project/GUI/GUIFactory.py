from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, BoundedNumericProperty, BooleanProperty
from kivy.properties import ListProperty, NumericProperty
from kivy.event import EventDispatcher
from Domain.SupportedFileTypes import AllSupportedFormats
from Domain.Command import Notification
from Domain.ContentType import ContentType
from Domain.MessageKeys import MessageKeys
from Domain.TestReturnValue import TestReturnValue
from Domain.PathConstants import PathConstants
from Domain.PresentationElement import PresentationElement
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
from shutil import copyfile
from shutil import copy
import os

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

from Domain.SlaveConnection import SlaveConnection

class MasterGUILayout(Screen, EventDispatcher):
    """
    Produces the Master-mode's GUI-layout that allows the
    user to communicate with Slave-devices.

    Inherits kivy.uix.screenmanager.Screen
    """

    label_text = StringProperty('')
    presenting_disabled = BooleanProperty(True)
    debug_text = StringProperty('Use this text space for debug')

    """
    The import counter is used to keep track on imported files on a
    single importation event.
    
    Values and their effects:
    -1      Handled as "the counter is reset and no imports are incomplete".
     0      The import is complete, the list of imported files is up to date.
            The list of files should be processed and the counter reset.
    1...n   The amount of files still to be imported.
    """
    import_counter = NumericProperty()
    import_list = ListProperty([])
    import_to_presentations = ListProperty([])

    def __init__(self, **kwargs):
        super(MasterGUILayout, self).__init__(**kwargs)
        self.presentation = None
        self.change_visibility_of_multiple_elements([self.ids.show_next, self.ids.stop_pres], True)
        self.bind(import_counter=self.import_counter_update)
        self.reset_import_counter()
        self.import_list = []
        self.import_to_presentations = []

    def notify_file_import(self):
        """
        Notifies the layout for a single file import
        :return: None
        """
        self.import_counter -= 1

    def reset_import_counter(self):
        """
        Resets the import counter.
        :return: None
        """
        self.import_counter = -1

    def import_started(self, value):
        """
        Updates the import counter's value.
        :param value: an integer, the new value
        :return: None
        """
        self.import_counter = value

    def import_counter_update(self, instance, value):
        """
        A callback function to call when the import counter's value changes.
        :return: None
        """
        if value == 0:
            for presentation_name in self.import_to_presentations:
                self.ids.slave_overview.add_files_to_a_presentation(presentation_name, self.import_list)
            del self.import_list[:]
            del self.import_to_presentations[:]
            self.reset_import_counter()

    def on_pre_enter(self):
        self.master = App.get_running_app().get_master(self)

    def check_text(self, text):
        self.ids.new_presentation_button.disabled = not text

    def set_address_to_gui(self, address):
        """
        Sets the address for GUI purposes, but does not control the actual connection
        """
        self.label_text = address

    def add_slave_connection(self, address):
        self.master.add_slave(address)

    def new_presentation(self, name):
        self.ids.slave_overview.new_presentation_to_overview(name)
        self.ids.txt_input.text = ""

    def send_message_to_slave(self):
        self.master.request_next()

    def start_presentation(self):
        self.change_visibility_of_multiple_elements([self.ids.start_pres, self.ids.back_button], True)
        self.change_visibility_of_multiple_elements([self.ids.show_next, self.ids.stop_pres], False)
        self.master.send_presentations_to_slaves()

    def stop_presentation(self):
        """
        Changes the editor mode into presentation mode. This method should lock the presentation
        :return:
        """
        self.change_visibility_of_multiple_elements([self.ids.show_next, self.ids.stop_pres], True)
        self.change_visibility_of_multiple_elements([self.ids.start_pres, self.ids.back_button], False)
        self.master.end_presentation()
        self.ids.slave_overview.reset_all_presentations()

    def change_visibility_of_multiple_elements(self, list, hide):
        """
        Uses the hide_widget and show widget to change visibility of multiple elements with a single method call
        :param list: Widgets that are hidden or shown
        :param hide: Boolean, true if you want to hide the widget
        :return: Nothing
        """
        for element in list:
            if hide:
                self.hide_widget(element)
            else:
                self.show_widget(element)

    def hide_widget(self, widget):
        """
        Hides the widget. Duhh.
        :param widget: Widget to be hidden
        :return: Nothing
        """
        widget.opacity = 0
        widget.size_hint_y = 0
        widget.size_hint_x = 0
        widget.width = '0dp'

    def show_widget(self, widget):
        """
        See the method above
        :param widget: Widget to be shown
        :return: Nothing
        """
        widget.opacity = 1
        widget.size_hint_y = 1
        widget.size_hint_x = 1

    def show_master_back_popup(self):
        """
        Opens the warning pop-up to master, asking if they are sure they want to go back
        """
        MasterBackPopUp().open()

    def show_open_file_popup(self):
        """
        Opens a Filechooser to load files
        :return: None
        """
        presentation_names = []
        for key, value in self.ids.slave_overview.slave_presentations.items():
            presentation_names.append(key)

        ImportFilesPopUp(self, self.import_list, presentation_names, self.import_to_presentations,
                         PathConstants.ABSOLUTE_MEDIA_FOLDER).open()

    def generate_presentation(self, slave_connection):
        """
        Generate the presentation information on the layout on connection to a slave.
        """
        self.ids.slave_overview.update_slave_to_overview(slave_connection)

    def remove_slave_presentation(self, data):
        """
        Remove possibly existing SlavePresentation widget based on the
        SlaveConnection object
        """
        self.ids.slave_overview.remove_slave_from_overview(data.full_address)

    def update_presentation_status(self, data=None):
        """
        Update the presentation status on the layout
        """
        self.ids.slave_overview.update_presentation_state()

    def update_connection_to_gui(self, data):
        """
        Sets the slave address to be shown in the gui
        """
        self.set_address_to_gui(str(data))

    def start_presentation_button_disabled(self, is_disabled):
        """
        Enables the start_pres button, enabling starting of the presentation.
        :param data:
        :return:
        """
        self.presenting_disabled = is_disabled

    def notify(self, notification, data=None):
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
                      Notification.CONNECTION_TERMINATED: remove_slave_presentation,
                      Notification.PRESENTING_DISABLED: start_presentation_button_disabled
                      }


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


"""
MasterBackPopUp and SlaveBackPopUp classes represent the popups that take the master or slave back to the switch layout 
if they decide to break the connection
"""


class MasterBackPopUp(Popup):
    pass


class SlaveBackPopUp(Popup):
    pass

from kivy.effects.scroll import ScrollEffect

class SlaveOverview(BoxLayout):
    """
    SlaveOverview class is used in the master GUI, to keep track of the slaves in the presentation. It maintains two
    lists: slave_buttons and slave_presentations. For each slave, SlaveOverview has a button in slave_buttons and a
    SlavePresentation in slave_presentations.
    """

    def __init__(self, **kwargs):
        super(SlaveOverview, self).__init__(**kwargs)
        self.slave_buttons = {}
        self.slave_presentations = {}
        self.effect_cls = ScrollEffect
        self.max = 0

    def new_presentation_to_overview(self, name):
        self.slave_buttons[name] = Button(text=name,
                                                   size_hint=(1, 0.2),
                                                   on_press=lambda a: print("kamehamehaaaaa"))
        self.slave_presentations[name] = SlavePresentation([])
        self.ids.slave_names.add_widget(self.slave_buttons[name])
        self.ids.slave_presentations.add_widget(self.slave_presentations[name])

    def add_files_to_a_presentation(self, presentation_name, import_list):
        self.slave_presentations[presentation_name].update_presentation_content(import_list)
        self.max = 5
        self.update_presentation_widths()

    def update_slave_to_overview(self, slave_connection):
        """
        Updates the SlaveOverview in the master's GUI. If a slave with an IP is already in the list, it is still deleted
        so that all changes in the slave's presentation will show.
        :param slave_connection: Slave's presentation data
        :return:
        """
        #slave_connection, "slave" + str(self.presentation_counter)
        self.remove_slave_from_overview(slave_connection.full_address)
        self.max = max(self.max, len(slave_connection.presentation))
        self.slave_buttons[slave_connection.full_address] = Button(text=slave_connection.full_address,
                                                                   size_hint=(1, 0.2),
                                                                   on_press=lambda a: slave_connection.show_next())
        self.slave_presentations[slave_connection.full_address] = SlavePresentation(slave_connection.presentation)
        self.ids.slave_presentations.width = len(slave_connection.presentation)*self.width/5 if len(slave_connection.presentation) > self.ids.slave_presentations.width/150 else self.width
        self.ids.slave_names.add_widget(self.slave_buttons[slave_connection.full_address])
        self.ids.slave_presentations.add_widget(self.slave_presentations[slave_connection.full_address])
        self.update_presentation_widths()

    def update_presentation_widths(self):
        for sp in self.slave_presentations.values():
            for budons in sp.children:
                budons.size_hint_x = 1/self.max

    def remove_slave_from_overview(self, address):
        """
        Removes the slave's information from the slave_buttons and slave_presentations list, and removes the widgets
        associated with it.
        :param address: The key which is used for deleting
        :return: Nothing
        """
        if address in self.slave_buttons.keys() or address in self.slave_presentations.keys():
            self.ids.slave_names.remove_widget(self.slave_buttons[address])
            self.ids.slave_presentations.remove_widget(self.slave_presentations[address])
            del self.slave_buttons[address]
            del self.slave_presentations[address]

    def update_presentation_state(self):
        current = 9999
        for slave_presentation in self.slave_presentations.values():
            current = min(current, slave_presentation.update_status())
        self.ids.scrollview.scroll_x = current/self.max

    def reset_all_presentations(self):
        for presentation in self.slave_presentations.values():
            presentation.reset()


class CheckBoxBonanza(BoxLayout):
    """
    A kivy widget class to hold a Checkbox and a Label
    """
    presentation_name = StringProperty('')

    def __init__(self, presentation_name, size_hint_y, callback):
        """
        Constructor function

        :param presentation_name: a string, the presentation's name
        :param size_hint_y: a floating-point number x, where 0 < x <= 1,
                defines the proportion the element occupies of the layout's height
        :param callback: the callback function to call when a checkbox is checked
        """
        super(CheckBoxBonanza, self).__init__()
        self.presentation_name = presentation_name
        self.size_hint_y = size_hint_y
        self.ids.checker.bind(active=callback)


class ImportFilesPopUp(Popup, EventDispatcher):
    """
    A file selection and opening popup
    """
    media_path = StringProperty('')
    supportedFormats = ListProperty([])
    local_presentation_selection = ListProperty([])

    def __init__(self, listener, imported_files, presentations,
                 selected_presentations, media_path, test_mode=False):
        """
        Constructor

        :param listener: the component to inform about file imports
        :param imported_files: a kivy ListProperty to store files that are imported
        :param presentations: a list of Presentation names
        :param
        """
        super(ImportFilesPopUp, self).__init__()
        self.supportedFormats = AllSupportedFormats
        self.imported_files = imported_files
        self.listener = listener
        self.populate_presentation_list(presentations)
        self.selected_presentations = selected_presentations
        self.ids.filechooser.bind(selection=self.check_selections)
        self.bind(local_presentation_selection=self.check_selections)
        self.media_path = media_path
        self.test_mode = test_mode

    def on_dismiss(self):
        self.ids.filechooser.unbind(selection=self.check_selections)
        self.unbind(local_presentation_selection=self.check_selections)

    def check_selections(self, instance, value):
        selection = self.ids.filechooser.selection
        import_button = self.ids.import_button
        if len(selection) == 0 or len(self.selected_presentations) == 0:
            import_button.disabled = True
        else:
            import_button.disabled = False

    def populate_presentation_list(self, presentations):
        presentation_list = self.ids.presentation_list
        for p in presentations:
            presentation_list.add_widget(CheckBoxBonanza(p, 0.05, self.on_checkbox_active))

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.selected_presentations.append(checkbox.label)
            self.local_presentation_selection.append(checkbox.label)
        else:
            self.selected_presentations.remove(checkbox.label)
            self.local_presentation_selection.remove(checkbox.label)


    def import_files_for_presentation(self, path, selection):
        """
        Opens one or multiple files from a path
        :param path: the path to open files from
        :param selection: a list the selected files in the path
        :param presentation: the presentation to open the files to
        :return: None
        """
        self.listener.import_started(len(selection))
        if not self.test_mode:
            self.import_files_from_media_folder(path, selection, self.listener)

    def import_files_from_media_folder(self, path, selected_files, listener):
        """
        Get the selected files from media folder.
        If the file doesn't exists in the media folder,
        it will be copied there first.

        :param path: the path of the files to import from
        :param selected_files: the files selected from some path
        :param callback: the function to call when importation is ready
        :return: a list of files copied to media folder
        """
        for filee in selected_files:
            separated_paths = filee.split(os.sep)
            file_to_write = os.path.join(self.media_path, separated_paths[len(separated_paths) - 1])
            self.copy_file(path, filee, file_to_write, self.imported_files, listener)

    def copy_file(self, path, source, destination, filename_list, listener):
        """
        Copies the source file as the destination file
        and returns the file with complete path.
        If the destination file exists, it will not be
        overwritten.

        :param path: the path of the files to import from
        :param source: a string, the source file with path
        :param destination: a string, the derstination file with path
        :param filename_list: the list to append the created filename
        :return: the destination file
        """
        if path != self.media_path and os.path.isfile(destination):
            if self.test_mode:
                return TestReturnValue.FileSavingDialogPopUp
            FileSavingDialogPopUp(source, destination, filename_list, listener, self.media_path).open()
        elif path != self.media_path:
            copyfile(source, destination)
            filename_list.append(destination)
            listener.notify_file_import()
        else:
            filename_list.append(destination)
            listener.notify_file_import()


class FileSavingDialogPopUp(Popup):
    """
    A popup functionality to confirm actions
    when copying a file that already exists.
    """
    COPY_EXTENSION = "_copy"    # the string to use when prefilling
                                # the name for copied file
    destination = StringProperty('')
    new_filename = StringProperty('')
    original_destination_filename_only = StringProperty('')

    """
    This list contains all characters that are reserved when naming a file
    either in Unix or Windows
    """
    RESERVED_FILENAME_CHARS = ["/", "\\", "?", "%", "*", ":", "|", '"', "<", ">"]

    def __init__(self, source, destination, filename_list, listener, media_path):
        """
        The source and destination files are passed as arguments
        :param source: a string, the source file with path
        :param destination: a string, the destination file with path
        :param filename_list: the list to append the created filename
        """
        super(FileSavingDialogPopUp, self).__init__()
        self.source = source
        self.destination_name = destination
        self.destination = destination
        self.media_path = media_path
        self.media_files = [file for file in os.listdir(self.media_path) if
                            os.path.isfile(os.path.join(self.media_path, file))]
        self.new_filename = self.__prefilled_new_file_name(destination)
        self.original_destination_filename_only = self.__parse_filename_only(destination)
        self.ids.save_as.bind(text=self.on_text)
        self.filename_list = filename_list
        self.listener = listener

    def __parse_filename_only(self, filepath):
        """
        A private helper method to return the file name from a
        "path1/path2/path3/filename.ext" string.
        :param filepath: a string, the pathpathpathfile-thingy
        :return: a string the file name only
        """
        paths_and_file_list = filepath.split(os.sep)
        return paths_and_file_list[len(paths_and_file_list) - 1]

    def on_text(self, instance, filename):
        """
        This function is called every time the bound widget's text-property changes
        :param instance: the instance of the Widget
        :param filename: the value in the text property
        :return:
        """
        copy_file_btn = self.ids.copy_file_button
        if not filename or filename in self.media_files \
                or self.__contains_reserved_chars(filename):
            copy_file_btn.disabled = not False
        else:
            copy_file_btn.disabled = not True

    def __contains_reserved_chars(self, filename):
        """
        Checks if the given filename contains any reserved characters
        :param filename: a string, the file's name
        :return: a boolean, True if reserved characters were encountered, False otherwise
        """
        for reserved_char in self.RESERVED_FILENAME_CHARS:
            if reserved_char in filename:
                return True

        return False

    def __prefilled_new_file_name(self, destination):
        """
        A private method to create a prefilled filename based on
        the original destination filename. The filename will differ
        from all the file names currently in the app's media folder
        :param destination: a string, the destination as "path1/path2/filename.ext"
        :return: a string, prefilled filename
        """
        separated_path_list = destination.split(os.sep)
        filename_and_extension = separated_path_list[len(separated_path_list) - 1].split('.')
        filename_copy = ''
        if len(filename_and_extension) > 1:
            filename_copy = self.__create_filename_with_extensions(filename_and_extension)
        else:
            filename_copy += filename_and_extension[0] + self.COPY_EXTENSION
        return filename_copy

    def __create_filename_with_extensions(self, filename_and_extensions):
        """
        A private helper methos. Creates a file name based on the filename
        and its extensions
        :param filename_and_extensions: a list, first element is the filename, the rest are its extensions
        :return: a string, a filename with extensions
        """
        extensions = filename_and_extensions[1:len(filename_and_extensions)]
        filename_with_extensions = filename_and_extensions[0]
        while self.__current_filename_with_extensions(filename_with_extensions, extensions) in self.media_files:
            filename_with_extensions += self.COPY_EXTENSION
        for i in range(0, len(extensions)):
            filename_with_extensions += '.' + extensions[i]
        return filename_with_extensions

    def __current_filename_with_extensions(self, filename, extensions):
        """
        A private helper method. Returns the filename and its extensions.
        :param filename: a string, the file's name
        :param extensions: a list, the extensions
        :return: a string, a filename with extensions
        """
        filename_with_extensions = filename
        for i in range(0, len(extensions)):
            filename_with_extensions += '.' + extensions[i]
        return filename_with_extensions

    def replace_file(self):
        """
        Replaces the original destination file.
        :return: None
        """
        self.copy_file_as(self.destination_name)

    def create_new_file(self):
        """
        Creates a new file.
        :return: None
        """
        separated_path_list = self.destination_name.split(os.sep)
        separated_path_list[len(separated_path_list) - 1] = self.ids.save_as.text
        file_to_save = separated_path_list[0]
        for i in range(1, len(separated_path_list)):
            file_to_save += os.sep + separated_path_list[i]
        self.copy_file_as(file_to_save)

    def copy_file_as(self, filename):
        """
        Copies the source file to to another location.
        :param filename: the file to write
        :return: None
        """
        try:
            copy(self.source, filename)
            self.filename_list.append(filename)
            self.listener.notify_file_import()
        except Exception as ex:
            ExceptionAlertPopUp("Error writing file", ex).open()


class ExceptionAlertPopUp(Popup):
    error_msg = StringProperty('')
    error_title = StringProperty('')

    def __init__(self, title, exception):
        super(ExceptionAlertPopUp, self).__init__()
        self.error_title = title
        self.error_msg = exception.__class__.__name__ + ": " + str(exception)


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
        self.presentation_data = import_list
        self.create_visual_widgets()

    def visualize_next(self):
        """
        Highlights the next visual, indicating it is the currently active visual
        """
        if self.current_active == -1:
            self.current_active += 1
            return -1
        self.visuals[self.current_active-1].set_inactive()
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
        self.y = self.parent.y

    def on_touch_down(self, touch):
        super(SlaveVisualProperty, self).on_touch_down(touch)
        self.old_x = self.x
        self.being_moved = True

    def __lt__(self, other):
        return self.x > other.x

    def on_touch_up(self, touch):
        super(SlaveVisualProperty, self).on_touch_up(touch)
        self.being_moved = False
        self.parent.children.sort()

    def do_i_have_to(self):
        if self.going_forward:
            return self.x-self.old_x > self.width + 5 or abs(self.x-self.old_x) > self.width + 20
        return self.old_x-self.x < self.width + 5 or abs(self.x-self.old_x) > self.width + 20

    def on_x(self, *largs):
        if self.do_i_have_to() and self.being_moved:
            self.going_forward = self.x - self.old_x > 0
            self.old_x = self.x
            self.parent.children.sort()
            temp = self.x
            self.x = self.old_x
            self.old_x = temp


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

    def create_presentation(self):
        presentation = Presentation()
        for i in range(len(self.content)):
            presentation.presentation_filenames.append(self.content[i].text)
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
        self.info_screen = None
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

    def add_info_layout(self):
        if self.info_screen is None:
            self.info_screen = InfoLayout(name='info_gui_layout')
            self.add_widget(self.info_screen)
        self.current = 'info_gui_layout'

    def add_presentation_creation_layout(self):
        if self.presentation_creation_screen is None:
            self.presentation_creation_screen = PresentationCreationLayout(name='presentation_creation_layout')
            self.add_widget(self.presentation_creation_screen)
        self.current = 'presentation_creation_layout'

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

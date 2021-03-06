from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.effects.scroll import ScrollEffect
from GUI.MasterGUI.SlavePresentation import SlavePresentation
from Domain.Presentation import Presentation
from Domain.Project import Project
from GUI.MasterGUI.SlavePresentationButton import SlavePresentationButton
from GUI.PopUps.BindPresentationToSlavePopUp import BindPresentationToSlavePopUp

class ProjectOverview(BoxLayout):
    """
    ProjectOverview class is used in the master GUI, to keep track of the slaves in the presentation. It maintains two
    lists: slave_buttons and slave_presentations. For each slave, ProjectOverview has a button in slave_buttons and a
    SlavePresentation in slave_presentations.
    """

    def __init__(self, **kwargs):
        super(ProjectOverview, self).__init__(**kwargs)
        self.slave_buttons = {}
        self.slave_presentations = {}
        self.project = Project()
        self.effect_cls = ScrollEffect
        self.max = 1
        self.in_editor_mode = True

    def new_presentation_to_overview(self, name, given_presentation=None):
        """
        Creates a new GUI element for a single presentation. Is used when creating a new presentation and when loading
        a saved presentation
        :param name:
        :return: Nothing
        """
        master = App.get_running_app().servicemode
        if given_presentation is None:
            given_presentation = Presentation(name)
            self.project.presentations.append((name, given_presentation))
        new_slave_presentation = SlavePresentation(given_presentation)
        #button = Button(text=name, size_hint=(1, 0.2))
        #lf = lambda a: BindPresentationToSlavePopUp(master.slave_connections.keys(), new_presentation.get_presentation_from_widgets(), master, button).open()
        #button.on_press = lf
        self.slave_buttons[name] = SlavePresentationButton(text=name,
                                                   size_hint=(1, 0.2))
        self.slave_buttons[name].bind(on_press=lambda a: self.slave_button_action(new_slave_presentation.get_presentation_from_widgets(), self.slave_buttons[name]))
        self.slave_presentations[name] = new_slave_presentation
        #self.project.presentations.append((name, given_presentation))
        self.ids.slave_names.add_widget(self.slave_buttons[name])
        self.ids.slave_presentations.add_widget(self.slave_presentations[name])
        self.max = max(self.max, len(given_presentation))
        self.update_presentation_widths()

    def slave_button_action(self, presentation, button):
        master = App.get_running_app().servicemode
        if self.in_editor_mode:
            BindPresentationToSlavePopUp(master.slave_connections.keys(), presentation, master, button).open()
        else:
            button.slave_connection.show_next()

    def add_files_to_a_presentation(self, presentation_name, import_list):
        """
        Adds files to a single presentation based on the filenames given in the import list
        :param presentation_name: presentation to be added to
        :param import_list: filenames to be added to presentation
        :return:
        """
        self.slave_presentations[presentation_name].update_presentation_content(import_list)
        self.max = max(self.max, len(self.slave_presentations[presentation_name].visuals))
        self.ids.slave_presentations.width = self.width/6*self.max
        self.update_presentation_widths()

    def update_slave_to_overview(self, slave_connection):
        """
        Updates the ProjectOverview in the master's GUI. If a slave with an IP is already in the list, it is still deleted
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
        self.ids.slave_presentations.width = len(slave_connection.presentation)*self.width/6
        """if len(slave_connection.presentation) > self.ids.slave_presentations.width/150 else self.width --- was in the statement above, not sure if necessary :^)"""
        self.ids.slave_names.add_widget(self.slave_buttons[slave_connection.full_address])
        self.ids.slave_presentations.add_widget(self.slave_presentations[slave_connection.full_address])
        self.update_presentation_widths()

    def setup_presentation(self):
        self.in_editor_mode = False
        self.disable_rearrangement_of_buttons()

    def end_presentation(self):
        self.in_editor_mode = True
        self.reset_all_presentations()

    def update_presentation_widths(self):
        """
        Scales the SlaveVisualProperties in proportion to the longest presentation.
        :return:
        """
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
        """
        Automatically progresses the scrollview forward based on where the presentation is at
        :return:
        """
        current = 9999
        for slave_presentation in self.slave_presentations.values():
            current = min(current, slave_presentation.update_status())
        self.ids.scrollview.scroll_x = (current+1)/self.max if current >= 1 else 0

    def reset_all_presentations(self):
        """
        Resets the presentations to their starting states and allows their
        elements to be rearranged.
        :return:
        """
        for presentation in self.slave_presentations.values():
            presentation.change_draggability(True)
            presentation.reset()

    def disable_rearrangement_of_buttons(self):
        """
        Called when Master starts the presentation so that the
        presentation elements won't be out of sync with what the
        slaves are showing.
        :return:
        """
        for presentation in self.slave_presentations.values():
            presentation.change_draggability(False)

    def notify_connection_lost(self, slave_connection):
        if slave_connection.presentation is not None:
            try:
                button = self.slave_buttons[slave_connection.presentation.name]
                button.background_color = (1, 0, 0, 0.8)
            except:
                pass

    def remove_presentation(self, name):
        """
        Masterlayout calls this method for all presentations that are to be removed from master_layout
        :param name:
        :return:
        """
        self.project.remove_from_presentations(name)
        self.ids.slave_presentations.remove_widget(self.slave_presentations[name])
        self.ids.slave_names.remove_widget(self.slave_buttons[name])
        del self.slave_buttons[name]
        del self.slave_presentations[name]

    def remove_presentations(self):
        """
        Clears all presentations in the ProjectOverview. Called when
        opening an existing project.
        :return:
        """
        self.ids.slave_presentations.clear_widgets()
        self.ids.slave_names.clear_widgets()
        self.slave_buttons = {}
        self.slave_presentations = {}

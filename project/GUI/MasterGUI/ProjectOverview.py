from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.effects.scroll import ScrollEffect
from GUI.MasterGUI.SlavePresentation import SlavePresentation
from Domain.Presentation import Presentation
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
        self.effect_cls = ScrollEffect
        self.max = 0

    def new_presentation_to_overview(self, name):
        """
        Creates a new empty presentation to the ProjectOverview, sets the key with name parameter.
        :param name:
        :return:
        """
        master = App.get_running_app().servicemode
        new_presentation = SlavePresentation(Presentation())
        #button = Button(text=name, size_hint=(1, 0.2))
        #lf = lambda a: BindPresentationToSlavePopUp(master.slave_connections.keys(), new_presentation.get_presentation_from_widgets(), master, button).open()
        #button.on_press = lf
        self.slave_buttons[name] = Button(text=name,
                                                   size_hint=(1, 0.2),
                                                   on_press=lambda a: BindPresentationToSlavePopUp(master.slave_connections.keys(), new_presentation.get_presentation_from_widgets(), master, a).open())
        self.slave_presentations[name] = new_presentation
        self.ids.slave_names.add_widget(self.slave_buttons[name])
        self.ids.slave_presentations.add_widget(self.slave_presentations[name])

    def add_files_to_a_presentation(self, presentation_name, import_list):
        """
        Adds files to a single presentation based on the filenames given in the import list
        :param presentation_name: presentation to be added to
        :param import_list: filenames to be added to presentation
        :return:
        """
        self.slave_presentations[presentation_name].update_presentation_content(import_list)
        self.max = max(self.max, len(self.slave_presentations[presentation_name].visuals))
        self.ids.slave_presentations.width = self.max * self.width / 6
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
        self.ids.scrollview.scroll_x = current/self.max if current >= 0 else 0

    def reset_all_presentations(self):
        for presentation in self.slave_presentations.values():
            presentation.reset()

    def remove_presentation(self,name):
        """
        masterlayout calls this method for all presentations that are to be removed from master_layout
        :param name:
        :return:
        """
        self.ids.slave_presentations.remove_widget(self.slave_presentations[name])
        self.ids.slave_names.remove_widget(self.slave_buttons[name])
        del self.slave_buttons[name]
        del self.slave_presentations[name]
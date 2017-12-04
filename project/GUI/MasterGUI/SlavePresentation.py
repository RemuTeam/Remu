from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.properties import StringProperty

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
        self.create_visual_widgets(self.presentation_data.presentation_filenames)

    def create_visual_widgets(self, import_list):
        """
        Creates the visual widgets for the slave's visuals
        """
        for i in range(0, len(import_list)):
            filename = import_list[i].split("/")[-1]
            filename = filename[:100] #[0][:100]
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
        print("to import:", import_list)
        self.presentation_data.presentation_filenames.extend(import_list)
        self.create_visual_widgets(import_list)

    def get_presentation_from_widgets(self):
        self.visuals.sort()
        self.visuals = self.visuals[::-1]
        presentation_content = []
        for i in range(len(self.children)):
            presentation_content.append(self.children[i].visual_name)
        self.presentation_data.set_files(presentation_content[::-1])
        return self.presentation_data

    def sort(self):
        self.children.sort()
        self.get_presentation_from_widgets()

    def visualize_next(self):
        """
        Highlights the next visual, indicating it is the currently active visual
        """
        for visual in self.visuals:
            visual.set_inactive()
        self.visuals[self.presentation_data.index].set_active() if self.presentation_data.index != -1 else None
        return self.presentation_data.index

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

    def change_draggability(self, draggable):
        self.get_presentation_from_widgets()
        for visual in self.visuals:
            visual.toggle_dragging(draggable)


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

    def toggle_dragging(self, draggable):
        if draggable:
            self.drag_distance = 0
        else:
            self.drag_distance = 6666666666666666

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
        Compares the object's x coordinate with another object's and for some reason returns if the object's x is
        greater than rather than less than; it just works this way
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
        self.parent.sort()

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
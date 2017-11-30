import unittest
from GUI.SlaveGUI.PresentationLayout import PresentationLayout
from Domain.PresentationElement import PresentationElement
from Domain.ContentType import ContentType
from kivy.app import App
import os
from Domain.PathConstants import PathConstants

class TestPresentationLayout(unittest.TestCase):
    def setUp(self):
        self.layout = PresentationLayout()
        self.image_source = "source.jpg"
        self.text_source = os.path.join(PathConstants.ABSOLUTE_TEST_MEDIA_FOLDER, "test_text.txt")
        self.video_source = "video_source.mp4"
        self.image_element = PresentationElement(ContentType.Image, self.image_source)
        self.video_element = PresentationElement(ContentType.Video, self.video_source)
        self.text_element = PresentationElement(ContentType.Text, self.text_source)

    def test_on_enter(self):
        self.layout.on_enter()
        self.assertEqual(self.layout.slave, App.get_running_app().servicemode)
        self.assertEqual(self.layout.image_source, self.layout.start_screen.get_content())
        self.assertEqual(self.layout.ids.text_field.opacity, 0)
        self.assertEqual(self.layout.ids.video.opacity, 0)
        self.assertEqual(self.layout.ids.picture.opacity, 1)
        self.assertEqual(self.layout.slave.source, '')
        self.assertEqual(self.layout.slave.presentation.index, -1)

    def test_on_pre_enter(self):
        self.layout.on_pre_enter()
        self.assertEqual(self.layout.ids.text_field.opacity, 0)
        self.assertEqual(self.layout.ids.video.opacity, 0)
        self.assertEqual(self.layout.ids.picture.opacity, 0)

    def test_set_visible_widget_image(s):
        s.layout.set_visible_widget(s.image_element)
        s.assertEqual(s.layout.image_source, s.image_source)
        s.assertEqual(s.layout.ids.picture.opacity, 1)

    def test_set_visible_widget_video(s):
        s.assertNotEqual(s.layout.ids.video.state, 'play')
        s.layout.set_visible_widget(s.video_element)
        s.assertEqual(s.layout.video_source, s.video_source)
        s.assertEqual(s.layout.ids.video.opacity, 1)
        s.assertEqual(s.layout.ids.video.state, 'play')

    def test_set_visible_widget_text(s):
        s.layout.set_visible_widget(s.text_element)
        s.assertEqual(s.layout.text_element, s.text_element.get_content())
        s.assertEqual(s.layout.ids.text_field.opacity, 1)
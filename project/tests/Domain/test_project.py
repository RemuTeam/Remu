import unittest
from Domain.Presentation import Presentation
from Domain.Project import Project


class TestProjectMethods(unittest.TestCase):

    def setUp(self):
        self.project = Project()
        self.create_test_presentation(self.project)


    def test_to_json(self):
        test_json_data = r'[["kek", ["a.jpg", "b.jpg"]], ["heck", ["b.jpg", "a.jpg"]]]'
        generated_json_data = self.project.dump_json()
        self.assertEqual(sorted(generated_json_data), sorted(test_json_data))

    def test_load_json(self):
        test_json_data = r'[["mad", ["c.jpg", "d.jpg"]], ["sad", ["d.png", "c.png"]]]'
        proj = Project()
        proj.load_json(test_json_data)

        project_json = proj.dump_json()
        self.assertEqual(sorted(project_json), sorted(test_json_data))

    def create_test_presentation(self, project):
        name1 = "kek"
        presentation1 = Presentation()
        presentation1.set_files(["a.jpg", "b.jpg"])

        name2 = "heck"
        presentation2 = Presentation()
        presentation2.set_files(["b.jpg", "a.jpg"])

        project.presentations.append((name1, presentation1))
        project.presentations.append((name2, presentation2))

    def test_removing_from_presentations(self):
        self.project.remove_from_presentations("kek")
        self.assertEqual(len(self.project.presentations), 1)
        self.assertEqual(self.project.presentations[0][0], "heck")


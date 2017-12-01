import json
from Domain.Presentation import Presentation

class Project:

    def __init__(self):
        self.presentations = [] #Lista tupleja, muodossa [(esityksenNimi, presentation), (toisenEsityksenNimi, toinenPresentation)]

    def save_project(self):
        print(json.dumps(self.presentations))

    def create_test_presentation(self):
        name1 = "bullshit"
        presentation1 = Presentation()
        presentation1.set_files(["a.jpg", "b.jpg"])
        #presentation1.load()

        name2 = "wtf"
        presentation2 = Presentation()
        presentation2.set_files(["b.jpg", "a.jpg"])
        #presentation2.load()

        self.presentations.append((name1, presentation1))
        self.presentations.append((name2, presentation2))
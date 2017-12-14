# Remu [![Build Status](https://travis-ci.org/RemuTeam/Remu.svg#1?branch=master)](https://travis-ci.org/RemuTeam/Remu) [![Coverage Status](https://coveralls.io/repos/github/RemuTeam/Remu/badge.svg#2?branch=master)](https://coveralls.io/github/RemuTeam/Remu?branch=master)
Remu is a tool for controlling visual presentations for music performances. With Remu, you can create visual presentations and share them with other devices via WiFi network, and then show through projectors to accompany musical performances.

The aim of Remu is to make the administration of visuals in a musical performance easy. Remu works with a master/slave architecture, where a single device is configured to be a master that sends commands to slaves. With the master device, you can create the presentations to be shown, and then show multiple presentations simultaneously with several devices. 

Remu is a work in progress, and is licensed under MIT license. All contributing is appreciated!

## Installing

Before installing, make sure that you have python 3.x, pip and [Kivy dependencies](https://kivy.org) installed

1. **In the terminal, run command**

    ```bash
    git clone https://github.com/RemuTeam/Remu.git
    ```

2. **Move into the project directory by running command**
    ```bash
    cd Remu/project
    ```

3. **Install project dependencies with command**
    ```bash
    pip install -r requirements.txt
    ```
## Running the program
In the terminal, navigate into the project directory, and from there run command
   ```bash
   python3 Main.py
   ``` 
   
## Usage
How to begin

1. Start the App with your computer and the computers that will handle to visual show.
2. Select "Master" for the computer that will be the one you will use during the show.
3. Select "Slave" for the other computers

Making a presentation

In master-mode, you can make a new presentation by typing the name into the text field and pressing "New Presentation".
Then you can import files to presentations by going to "import files" and there selecting files and checking the box
corresponding to the presentation you want the files imported to. You can also switch the positions of the files
in the master view, by double clicking a file and dragging it to it's new position in the presentation line.

Now it is time to connect the slave machines to your master computer and show your presentation!

By starting this Remu with other machines, and choosing the Slave mode, they automatically signal your master computer
of their existence. Now that you have some presentations done, you can connect a slave and its presentations.
Click the name of the presentations on your master computer. This opens up a list of all the possible slaves. Check
the wanted one and press confirm. Now the presentation is sent to the slave machine.

So you have made a presentation and sent it to its corresponding slave. All that is left is showing the presentation!

If all the steps have been done correctly, the start presentation button on master should be available now. When you
press it, the presentation will begin. You will see in green, which one of the files is being shown and you can proceed
with the presentation by clicking the show next button.

When the last file is shown the presentation will end. Congratulations, now you have used the RemuApp:)

## Definition of done

1. Features are tested reasonably and pass the tests
2. Tests are run in Travis and pass
3. Code is easily understandable and well commented
4. At least 2 RemuTeam members have validated the code.

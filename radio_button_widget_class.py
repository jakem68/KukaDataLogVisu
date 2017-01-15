from PyQt4.QtGui import *

class RadioButtonWidget(QWidget):
    # this class creates a group of radio buttons from a given list of labels

    #constructor
    def __init__(self, label, instruction, button_list):
        super().__init__() #call the super class constructor

        #create widgets
        self.title_label = QLabel(label)
        self.radio_group_box = QGroupBox(instruction)
        self.radio_button_group = QButtonGroup()
        self.radio_button_group.setExclusive(False)


        #create the radio buttons
        self.radio_button_list = []
        for each in button_list:
            self.radio_button_list.append(QRadioButton(each))

        #set the default checked item
        # self.radio_button_list[0].setChecked(True)

        #create layout for radio buttons
        self.radio_button_layout = QHBoxLayout()

        #add buttons to the layout and button group
        counter = 1
        for each in self.radio_button_list:
            self.radio_button_layout.addWidget(each)
            self.radio_button_group.addButton(each)
            self.radio_button_group.setId(each, counter)
            counter += 1

        #add radio buttons tot the group box
        self.radio_group_box.setLayout(self.radio_button_layout)
        # self.radio_group_box.show()
        self.radio_group_box.setStyleSheet("QGroupBox { background-color: rgb(255, 255, 255); border:1px solid rgb(150,150,150);   border-radius: 5px; padding-top: 12px;} \n QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top left; /* position at the top center */ padding: 0 6px;}")


        #create a layout for whole widget
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.radio_group_box)

        #set the layout for this widget
        self.setLayout(self.main_layout)

    #method to find out the selected button
    def selected_button(self):
        # todo iterate through radio buttons and return list of all!!! checked buttons
        self.checked_buttons = []
        self.checked = []
        for self.index, self.radio_button in enumerate(self.radio_button_list):
            if self.radio_button.isChecked():
                self.checked.append(self.index)
        return self.checked
    



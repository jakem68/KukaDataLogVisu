import sys
from PyQt4.Qt import *
from radio_button_widget_class import *
from file_selector_class import *
from graph_class import *

global data_lists

class DataSelect(QMainWindow):
    """This class creates the main start window to select files and data"""

    #constructor
    def __init__(self):
        super().__init__() #call super class constructor

        self.setWindowTitle("Graph Kukalog") #set window title
        self.create_initial_kukalog_layout()

        # this holds the various layouts needed for the app
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.main_window_widget)

        # set the central widget to display the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

        self.gw = None

        self.nr_plots = 0

    # initial layout to select data
    def create_initial_kukalog_layout(self):

        # create main widget and main layout and set widget layout
        self.main_window_widget = QWidget()
        self.main_window_layout = QVBoxLayout()
        self.main_window_widget.setLayout(self.main_window_layout)

        # create select_files button, add to main window layout, connect function when 'clicked'
        self.select_files_button = QPushButton("Select Files")
        # self.select_files_button.setDefault(True)
        self.select_files_button.setDefault(True)
        self.select_files_button.setAutoDefault(True)
        self.main_window_layout.addWidget(self.select_files_button)
        self.select_files_button.clicked.connect(self.select_files)

    def create_show_graph_button(self):
        self.show_graph_button = QPushButton("Show Graph")
        self.main_window_layout.addWidget((self.show_graph_button))
        self.show_graph_button.clicked.connect(self.graph)

# button connections
    def select_files(self):
        self.file_list = FileSelector.select()

        # check whether at least one file was selected
        if len(self.file_list)>0:

            # looping through file list
            self.file_list_data = []
            self.cl_titles = []
            self.radio_button_list = []
            self.data_radio_groups = []
            for self.file_index, self.each_file in enumerate(self.file_list):
                self.data_fields = []
                with open(self.each_file) as self.myfile:

                    # read each line:
                    self.data_lines = self.myfile.readlines()

                    # cut first 3 characters from line 1; is % sign
                    self.data_lines[0] = self.data_lines[0][3:]

                    # split text lines in individual fields
                    for self.line in self.data_lines:
                        self.data_fields.append(self.line.split())

                    # do something with first line fields
                    self.cl_titles.append(self.data_fields[0])
                    self.radio_button_list = self.cl_titles[self.file_index][2:]
                    print("in file {} the column titles are {}".format(self.file_index+1, self.cl_titles[self.file_index]))

                    # cut first line from line fields
                    self.data_fields = self.data_fields[1:]

                    # transform column 1 and 2 to full time --> subtract first value from each value == time
                    for line_index in range(len(self.data_fields)):
                        this_time = float(self.data_fields[line_index][0])*1000000000+float(self.data_fields[line_index][1])
                        if line_index == 0:
                            start_time = this_time
                        self.data_fields[line_index][1] = (this_time - start_time)/1000000
                    # transpose remainder data fields to create eight lines of data
                    self.data_fields_transposed = list(zip(*self.data_fields))

                #append data to data from other files
                self.file_list_data.append(self.data_fields_transposed)

                #create radio buttons and add to main layout
                self.data_radio_buttons = RadioButtonWidget("select data from file", "{}: {}".format(self.file_index + 1, self.each_file, ), self.radio_button_list) #file_list[file_index],data_list[data_index])
                self.main_window_layout.addWidget(self.data_radio_buttons)
                self.data_radio_groups.append(self.data_radio_buttons)

            print("file_list_data[0][1][0:5] = {}".format(self.file_list_data[0][1][0:5])) # are 8 columns of file 1
            # create graph button
            self.create_show_graph_button()

    def graph(self): # function to transform all data to graph data and call graph_class

        # detect and list checked radio buttons
        self.button_groups_buttons_checked = []
        for self.radio_group_index, self.each_radio_group in enumerate(self.data_radio_groups):
            print("radio group {} has checked {}".format(self.radio_group_index, self.each_radio_group.selected_button()))
            self.button_groups_buttons_checked.append(self.each_radio_group.selected_button())

        # map checked radio buttons with page and column in file_list_data
        # iterate through above build list of checked radio buttons and build new list with corresponding data
        self.data_lists = []
        self.cl_titles_checked = []
        for self.buttons_group_index, self.each_button_group in enumerate(self.button_groups_buttons_checked):
            self.data_lists_row = []
            self.cl_titles_checked_row = []
            if self.each_button_group:
                for self.radio_button_index, self.radio_button in enumerate(self.button_groups_buttons_checked[self.buttons_group_index]):
                    # turn value from string into float
                    self.str_value = self.file_list_data[self.buttons_group_index][self.radio_button + 2]
                    # print(self.str_value)
                    try:
                        self.float_value = [float(self.i_str_value) for self.i_str_value in self.str_value]
                    except self.e as error:
                        print("this doesn't look like a float: {}. It was in data_list column {x} on row {y}". format(self.radio_button_index, self.buttons_group_index))
                    self.data_lists_row.append(self.float_value)
                    self.cl_titles_checked_row.append(self.cl_titles[self.buttons_group_index][self.radio_button + 2])
                    self.nr_plots += 1
            self.data_lists.append(self.data_lists_row)
            self.cl_titles_checked.append(self.cl_titles_checked_row)
        print(self.cl_titles_checked)

        # # turn strings into floats
        # try:
        #     self.data_lists = [[float(self.y) for self.y in self.x] for self.x in self.data_lists]
        # except self.e as error:
        #     print("this doesn't look like a float: {}. It was in data_list column {x} on row {y}". format(self.data_lists[self.x][self.y], self.x, self.y))

        # built time-axis values
        self.duration_axis = self.file_list_data[0][1]

        # turn tuple into list
        self.duration_axis = list(self.duration_axis)

        # set Graphwindow class variables
        Graphwindow.data_list = self.data_lists
        Graphwindow.x_axis = self.duration_axis
        Graphwindow.cl_titles_checked = self.cl_titles_checked
        Graphwindow.nr_plots = self.nr_plots

        # instantiate graph element
        self.gw = Graphwindow()
        self.gw.setWindowTitle("Graph Window")
        self.gw.showMaximized()

class Start(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.start_window = DataSelect()
        self.connect(self, SIGNAL("lastWindowClosed()"), self.end)
        self.start_window.show()

    def end(self):
        self.exit(0)

def main(args):
    global program
    program = Start(args)
    program.exec_() # monitor application for events

if __name__ == '__main__':
    main(sys.argv)

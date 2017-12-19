import sys
from Structure import Structure
from PySide import QtGui, QtCore


class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.data = Structure()
        self.itemList = QtGui.QTreeWidget()
        self.initUI()
    '''
    initUI: Method to define the user interface
    '''
    def initUI(self):
        # Call createMenu() method for create Menu Bar
        self.createMenu()
        # Set the Menu Bar
        self.setMenuBar(self.menuBar)
        self.createTreeLayout()
        # Create Status Bar where show clicked info
        self.statusBar()
        self.statusText = QtGui.QLabel("Ready")
        self.statusBar().addWidget(self.statusText, 1)
        # Set Window Size
        self.setGeometry(500, 300, 350, 450)
        self.setWindowTitle('Python Dictionary Explorer')
        self.show()

    '''
    createMenu: Method to generate and add all user interface
                elements to our user interface
    '''
    def createMenu(self):
        # Define actions for Menu Bar
        # Option 1: Load default
        defaultTree = QtGui.QAction('Set Default Tree', self)
        defaultTree.setStatusTip('Create a default tree')
        defaultTree.triggered.connect(self.createDefaultTree)
        # Option 2: Load path to explore
        loadAction = QtGui.QAction('Load Path...', self)
        loadAction.setStatusTip('Load path as python dictionary')
        loadAction.triggered.connect(self.createTreeFromPath)
        # Option 3: Exit option
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        # Create Menu Bar
        self.menuBar = QtGui.QMenuBar()
        # Create File Menu
        self.fileMenu = QtGui.QMenu("&File", self)
        # Add actions to File Menu
        self.fileMenu.addAction(defaultTree)
        self.fileMenu.addAction(loadAction)
        self.fileMenu.addAction(exitAction)
        # Add File Menu to Menu Bar
        self.menuBar.addMenu(self.fileMenu)

    '''
    createTree: Method to generate the QTreeWidget with
                all elements and hierarchy
    '''
    def createTreeLayout(self):
        # Define QTreeWidget and set parameters
        self.itemList.setItemsExpandable(True)
        self.itemList.setAnimated(True)
        self.itemList.setItemsExpandable(True)
        self.itemList.setColumnCount(1)
        self.itemList.setHeaderLabels([''])
        self.itemList.header().hide()
        # Create signal to item clicked Action, when any item is
        # clicked, itemClickedAction is called
        self.connect(self.itemList,
                     QtCore.SIGNAL("itemClicked (QTreeWidgetItem *, int)"),
                     self.itemClickedAction)
        # Generate the Layout for the browser
        self.gridLayout = QtGui.QGridLayout()
        self.widget = QtGui.QWidget()
        self.widget.setLayout(self.gridLayout)
        self.setCentralWidget(self.widget)
        self.gridLayout.addWidget(self.itemList)

    '''
    createTreeFromPath: Method to remove current tree and add
                        the new tree
    '''
    def createTreeFromPath(self):
        self.dictionary = self.data.createDataFromPath()
        self.itemList.clear()
        self.addElementToTree(self.dictionary)

    '''
    createTreeFromPath: Method to remove current tree and add
                        the new tree
    '''
    def createDefaultTree(self):
        self.dictionary = self.data.createDefaultData()
        self.itemList.clear()
        self.addElementToTree(self.dictionary)

    '''
    itemClickedAction:  Method called when user make click on any
                        list element. This method call showMessage()
                        to show in the status bar the item clicked info
    '''
    def itemClickedAction(self):
        # Get current item selected
        item = self.itemList.currentItem()
        # Get item selected text
        selected = item.text(0)
        # setNumElements call to set the number of files and
        # directory that the item selected have
        self.data.setNumElements(self.dictionary, 0, selected)
        # Create the info message
        info = (""
                + selected
                + " contains "
                + str(self.data.getNumFiles())
                + " files and "
                + str(self.data.getNumFolders())
                + " folders."
                )
        # Show the info message
        self.statusBar().showMessage(info)

    '''
    addElementToTree: Method that received an element to add to the tree
                      and insert it in the correct hierarchy.
        - src:        path to analyze
        - dpth:       Depth of the current item
        - key:        Key that identifies the current item
        - father:     Element that identifies the father of the current item
    '''
    def addElementToTree(self, src, dpth=0, key='', father=''):
        # Check if the current item is in dictionary
        if isinstance(src, dict):
            # Check key and value to insert the item
            for key, value in src.iteritems():
                if isinstance(father, str):
                    # If has no parent, it is the root
                    if str(father) == '':
                        item = QtGui.QTreeWidgetItem(self.itemList, [str(key)])
                        if value is not None:
                            self.addElementToTree(value, dpth + 1, key, item)
                    else:
                        if value is not None:
                            self.addElementToTree(value, dpth + 1, key, item)
                else:
                    item = QtGui.QTreeWidgetItem(father, [str(key)])
                    if value is not None:
                        self.addElementToTree(value, dpth + 1, key, item)
        else:
            # It is a child item
            item = QtGui.QTreeWidgetItem(father, [str(src)])


def main():
    app = QtGui.QApplication(sys.argv)
    es = mainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

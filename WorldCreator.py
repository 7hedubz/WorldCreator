import sys
from PySide2 import QtGui, QtCore, QtWidgets



class AddCountry(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.countryNameField = QtWidgets.QLineEdit()
        self.countryCreateButton = QtWidgets.QPushButton("Create Country")
        self.countryDeleteButton = QtWidgets.QPushButton("Delete Country")

        #Set the layout var, add the widgets, apply the layout
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("Country Name"))
        self.layout.addWidget(self.countryNameField)
        self.layout.addWidget(self.countryCreateButton)
        self.layout.addWidget(self.countryDeleteButton)
        self.layout.addSpacing(200)
        self.setLayout(self.layout)

class AddFeature(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.featureChoices = QtWidgets.QComboBox()
        self.featureNameField = QtWidgets.QLineEdit()
        self.featureCreateButton = QtWidgets.QPushButton("Create Feature")
        self.featureDeleteButton = QtWidgets.QPushButton("Delete Feature")

        self.featureChoices.addItem("Landscape", "ls")

        self.layout = QtWidgets.QHBoxLayout()
        # self.layout.addWidget(QtWidgets.QLabel("Feature Type"))
        self.layout.addWidget(self.featureChoices)
        self.layout.addWidget(QtWidgets.QLabel("Feature Name"))
        self.layout.addWidget(self.featureNameField)
        self.layout.addWidget(self.featureCreateButton)
        self.layout.addWidget(self.featureDeleteButton)
        self.layout.addSpacing(200)
        self.setLayout(self.layout)

class CountryNotebook(QtWidgets.QWidget):

    def currCountrySelection(self):
        return self.notebook.currentWidget()

    def isUniq(self, text, listToSrch):
        for clas in listToSrch:
            if text == clas.uName:
                return False
        return True

    @QtCore.Slot()
    def treeSelectionChanged(self):
        a = self.currCountrySelection()
        b = a.tree.currentItem()
        print("Tree selection changed to "+str(b))

    @QtCore.Slot()
    def changeCountrySelection(self):
        a = self.currCountrySelection()
        if True:
            print(self.countries)

            for ea in self.countries:
                try:
                    z = ea.tree.currentItem()
                    z.setSelected(False)
                    print("set Selection in class "+str(ea))
                except:
                    print("No items selected in class "+str(ea))

            self.countryDetInfoField.setPlainText(a.countryDetInfo)
            self.connect(a.tree, QtCore.SIGNAL("itemSelectionChanged()"), self.treeSelectionChanged)
            print("Tree signal connected to",a.uName+"'s tree")
        else:
            print("Nothing to select")

    @QtCore.Slot()
    def saveDetInfo(self):
        a = self.currCountrySelection()
        if a == None:
            return
        a.countryDetInfo = self.countryDetInfoField.toPlainText()

    @QtCore.Slot()
    def createTreeWidget(self):
        a = self.featureCreateGroup.featureChoices.currentData()
        text = self.featureCreateGroup.featureNameField.text()
        b = self.currCountrySelection()
        if b == None:
            return
        if text.replace(" ", "") is "":
            return
        if self.isUniq(text, b.landscapes):
            if a == "ls":
                        c = Landscape(text)
                        b.tree.addTopLevelItem(c)
                        b.landscapes.append(c)
                        print("created Landscape ",text)
            elif a == "np":
                        c = Landscape(text)
                        b.tree.addTopLevelItem(c)
                        b.notablePlaces.append(c)
                        print("created Notable Place ",text)
            if a == "t":
                pass
            if a == "dw":
                pass
            if a == "p":
                pass
            if a == "m":
                pass
            if a == "i":
                pass

    def deleteTreeWidget(self):
        print("User wants to delete a TreeWidget!")

    @QtCore.Slot()
    def createTab(self):
        text = self.countryCreateGroup.countryNameField.text()
        isTextUniq = self.isUniq(text, self.countries)
        if text.replace(" ", "") is "":
            return
        if isTextUniq == False:
            return
        a = CountryTab(text)
        self.countries.append(a)
        b = self.currCountrySelection()
        self.notebook.addTab(a, text)

        if b == None:
            self.countryDetInfoField.setReadOnly(False)
            self.currCountrySelection()

    @QtCore.Slot()
    def deleteTab(self):
        a = self.currCountrySelection()
        if a == None:
            return
        b = self.countries.index(a)
        self.notebook.removeTab(b)
        del self.countries[b]
        a = self.currCountrySelection()
        if a == None:
            self.countryDetInfoField.setReadOnly(True)
            self.countryDetInfoField.clear()

    def __init__(self, parent=None):
        super().__init__()

        self.countries = []
        self.notebook = QtWidgets.QTabWidget()
        self.countryDetInfoField = QtWidgets.QPlainTextEdit()
        self.countryCreateGroup = AddCountry()
        self.featureCreateGroup = AddFeature()

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.countryCreateGroup)
        self.layout.addWidget(self.featureCreateGroup)
        self.layout.addWidget(self.notebook)
        self.layout.addWidget(self.countryDetInfoField)
        self.countryDetInfoField.setReadOnly(True)
        self.layout.addWidget(QtWidgets.QLabel("Country Information PlainTextEdit"))

        self.setLayout(self.layout)

        self.connect(self.countryCreateGroup.countryCreateButton, QtCore.SIGNAL("released()"), self.createTab)
        self.connect(self.countryCreateGroup.countryDeleteButton, QtCore.SIGNAL("released()"), self.deleteTab)
        self.connect(self.featureCreateGroup.featureCreateButton, QtCore.SIGNAL("released()"), self.createTreeWidget)
        self.connect(self.featureCreateGroup.featureDeleteButton, QtCore.SIGNAL("released()"), self.deleteTreeWidget)
        self.connect(self.notebook, QtCore.SIGNAL("currentChanged(int)"), self.changeCountrySelection)
        self.connect(self.countryDetInfoField, QtCore.SIGNAL("textChanged()"), self.saveDetInfo)

class CountryTab(QtWidgets.QWidget):

    @QtCore.Slot()
    def treeSelection(self):
        a = self.tree.currentItem()

    def __init__(self, name, parent=None):
        super().__init__()

        self.uName = name
        self.countryDetInfo = ""
        self.landscapes = []


        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Name","Type"])

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)

class treeObject(QtWidgets.QTreeWidgetItem):
    def __init__(self, Parent=None):
        super().__init__()

        self.uName = ""
        self.detInfo = ""
        self.children = []

class Landscape(treeObject):
    def __init__(self, name, Parent=None):
        super().__init__()

        self.possilbeChildren = [["Notable Place", "np"], ["Town", "t"]]
        self.children = []
        self.uName = name
        self.setText(0, name)
        self.setText(1, "Landscape")

class BuildingInfo(treeObject):
    def __init__(self, parent=None):
        super().__init__()

class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.notebook = CountryNotebook()
        self.middleLayout = QtWidgets.QVBoxLayout()
        self.middleLayout.addWidget(self.notebook)

        self.parentGridLayout = QtWidgets.QGridLayout()
        self.parentGridLayout.addLayout(self.middleLayout, 0,0)
        self.setLayout(self.parentGridLayout)



app = QtWidgets.QApplication(sys.argv)

widget = MyWidget()
widget.setGeometry(300, 300, 500, 750)
widget.setMaximumSize(500, 750) #x, y
widget.show()

sys.exit(app.exec_())

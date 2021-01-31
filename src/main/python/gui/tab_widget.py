from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout


class MyTabWidget(QWidget): 

    def __init__(self, parent): 
        super(QWidget, self).__init__(parent) 
        self.layout = QVBoxLayout(self) 
  
        # Initialize tab screen 
        self.tabs = QTabWidget() 
        self.tab1 = QWidget() 
        self.tab2 = QWidget() 
        self.tab3 = QWidget() 
        self.tabs.resize(300, 200) 
  
        # Add tabs 
        self.tabs.addTab(self.tab1, "Geeks") 
        self.tabs.addTab(self.tab2, "For") 
        self.tabs.addTab(self.tab3, "Geeks") 
  
        # Create first tab 
        self.tab1.layout = QVBoxLayout(self) 
        # self.l = QLabel() 
        # self.l.setText("This is the first tab") 
        self.tab1.layout.addWidget(self.l) 
        self.tab1.setLayout(self.tab1.layout) 
  
        # Add tabs to widget 
        self.layout.addWidget(self.tabs) 
        self.setLayout(self.layout) 
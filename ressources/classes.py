
from   ressources import translation

from   PyQt5.QtCore          import *
from   PyQt5.QtWidgets       import *
from   PyQt5.QtGui           import *



# C O N F I G
# C L A S S
class Config:
    def __init__(self):
        self.cfg_path   = 'config.cfg'
        self.lang       = ''
        self.corpus.dir = ''
        self.dicts_dir  = ''
    
    def load(self):
        return
    
    def save(self):
        return
# END: class Config


# E X A M P L E
# C L A S S
class Example(QHBoxLayout):
    def __init__(self, era, ex):
        super(QHBoxLayout, self).__init__()
        self.era = QLabel(era)
        self.ex  = QLabel(ex)
        
        self.era.setWordWrap(True)
        self.ex.setWordWrap(True)
        
        self.era.setObjectName('list_item_era')
        self.ex.setObjectName('list_item_ex')
        
        self.addWidget(self.ex,  3, Qt.AlignRight)
        self.addWidget(self.era, 2, Qt.AlignRight)
    # END: __init__()


# E R A   E N T R Y
# C L A S S
class EraEntry(QWidget):
    def __init__(self, era='', word_def='', examples=[], expression=False):
        super(QWidget, self).__init__()
        layout         = QVBoxLayout()
        self.era       = QLabel(era)
        content        = QHBoxLayout()
        self.examples  = QVBoxLayout()
        
        if not expression:
            self.word_def = QLabel(word_def)
            self.word_def.setWordWrap(True)
            self.word_def.setAlignment(Qt.AlignTop)
            self.word_def.setObjectName('def_content')

        self.era.setObjectName('era_name')        
        
        self.examples.setAlignment(Qt.AlignRight)
        for ex in examples:
            example = QLabel(' - '+ ex)
            example.setWordWrap(True)
            example.setObjectName('example')
            self.examples.addWidget(example)
        
        # if len(examples) > 0:
        #    self.examples.addStretch()
        
        content.addLayout(self.examples, 5)
        if not expression:
            content.addWidget(self.word_def, 4, Qt.AlignTop)
        
        layout.addWidget(self.era, 0, Qt.AlignRight)
        layout.addLayout(content)

        self.setLayout(layout)
        # self.setLayoutDirection(Qt.RightToLeft)
    # END: __init__()
# END: class EraEntry


# E R A E N T R Y E D I T
# C L A S S
class EraEntryEdit(EraEntry):
    def __init__(self, eras_available=[], current_lang='ar'):
        super(EraEntry, self).__init__()
        
        layout              = QVBoxLayout()
        self.era            = QComboBox() # QLabel(era)
        content             = QHBoxLayout()
        def_content         = QVBoxLayout()
        self.word_def       = QTextEdit()# QLabel(word_def)
        self.search_def_btn = QPushButton()
        examples_layout     = QVBoxLayout()
        self.examples       = QVBoxLayout()
        add_example_layout  = QHBoxLayout()
        add_example_btn     = QPushButton(translation.langs['add_example'][current_lang])
        self.search_ex_btn  = QPushButton()
        
        self.era.addItems(eras_available)
        self.era.setView(QListView())
        self.era.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint);
        
        # self.era.setObjectName('era_name')        
        # self.word_def.setAlignment(Qt.AlignTop)
        # self.word_def.setObjectName('def_content')
        add_example_btn.setObjectName('secondary_button')
        self.search_def_btn.setObjectName('search_btn')
        self.search_ex_btn.setObjectName('search_btn')
        
        self.word_def.setLayoutDirection(Qt.RightToLeft)
        self.word_def.setMinimumHeight(100)
        self.word_def.setMaximumHeight(150)
        self.examples.setAlignment(Qt.AlignRight)
        
        add_example_layout.addWidget(self.search_ex_btn, 1)
        add_example_layout.addWidget(add_example_btn, 2)

        examples_layout.addLayout(self.examples)
        # examples_layout.addWidget(add_example_btn)
        examples_layout.addLayout(add_example_layout)
        examples_layout.addStretch()
        
        # self.search_def.setFixedSize(16, 16)
        # self.search_def.setStyleSheet('background-color: red;')
        
        content.addLayout(examples_layout, 5)
        # content.addWidget(self.search_def_btn, 0, Qt.AlignTop)
        # content.addWidget(self.word_def, 4, Qt.AlignTop)
        def_content.addWidget(self.word_def)
        def_content.addWidget(self.search_def_btn)
        def_content.addStretch()
        content.addLayout(def_content, 4)
        
        layout.addWidget(self.era, 0, Qt.AlignRight)
        layout.addLayout(content)
        
        add_example_btn.clicked.connect(lambda:self.add_example())
        # self.search_def_btn.clicked.connect(lambda:self.search_def_fn())
        # self.search_ex_btn.clicked.connect(lambda:self.search_ex_fn())

        self.setLayout(layout)
    # END: __init__()
    
    # ADD AN EXAMPLE
    def add_example(self):
        example = QLineEdit()
        example.setObjectName('example')    #example_edit
        example.setFixedHeight(20)
        self.examples.addWidget(example)
    # END: add_example()
    
     # ADD AN EXAMPLE
    def add_example_content(self, content):
        example = QLineEdit()
        example.setText(content)
        example.setObjectName('example')    #example_edit
        example.setFixedHeight(20)
        self.examples.addWidget(example)
    # END: add_example()
# END: class EraEntryEdit


# P O P U P
# C L A S S
class Popup(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowStaysOnTopHint)
        self.setObjectName('popup_window')
        # Maybe: Qt.Drawer instead of Qt.Dialog
    # END: __init__()

# END: class Popup

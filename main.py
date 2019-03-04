# -*- coding: utf-8 -*-

"""
 N A T U R A L
 L A N G U A G E
 P R O C E S S I N G
 
 PROJECT

"""


from   ressources.classes import *
from   ressources import translation

from   dicts.histdict import *

import controller

import sys
import os
from   PyQt5.QtCore    import *
from   PyQt5.QtWidgets import *
from   PyQt5.QtGui     import *





# M A I N   W I N D O W
# C L A S S
class MainWindow(QMainWindow):
    # current_page = 'search'    # or create an enum
    # page_handles  = {'search': QWidget, ... }
    
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setWindowFlags(Qt.)
        
        # qApp.setLayoutDirection(Qt.RightToLeft)
        self.window_icon      = QIcon('ressources/imgs/dict_flip.gif')
        self.marked_icon      = QIcon('ressources/imgs/marked.png')
        self.not_marked_icon  = QIcon('ressources/imgs/not_marked.png')
        
        # To read from a file: config.cfg
        self.current_lang        = 'ar'
        self.corpus_dir          = 'data/corpus'
        self.dicts_dir           = 'dicts'
        self.dict_path           = self.dicts_dir +'/hist_dict.xml' 
        self.dict_path_not_valid = self.dicts_dir +'/hist_dict_not_valid.xml'
        
        self.eras                = [
                'العصر الإسلامي',
                'العصر الاموي',
                'العصر الأندلسي',
                'العصر الايوبي',
                'العصر الجاهلي', 
                'العصر العباسي', 
                'العصر العثماني',
                'العصر المملوكي',
                'عصر المخضرمون',
                'عبر العصور'
                ]
        # self.dicts_dir    = ''
        # The changes will take effect in the next restart
        
        self.hist_dict = load_dict(self.dict_path)
        self.hist_dict.update(load_dict(self.dict_path_not_valid, is_valid=False))
        
        self.is_online = False
        
        self.init_ui()

    
    def init_ui(self):
        print('init ui...')
        
        self.setWindowTitle(translation.langs['win_title'][self.current_lang])
        self.setWindowIcon(self.window_icon)
        self.resize(900, 600)
        
        window_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        tabs_layout   = QHBoxLayout()
        

        # T A B S
        tabs_widget   = QWidget(self)
        
        search_btn    = QRadioButton(translation.langs['search'][self.current_lang],  tabs_widget)
        explore_btn   = QRadioButton(translation.langs['explore'][self.current_lang], tabs_widget)
        edit_btn      = QRadioButton(translation.langs['edit'][self.current_lang],    tabs_widget)
        search_btn.setObjectName('menu_item')
        explore_btn.setObjectName('menu_item')
        edit_btn.setObjectName('menu_item')
        search_btn.setChecked(True)
        
        search_btn.toggled.connect( lambda:self.change_page(search_btn,  'search'))
        explore_btn.toggled.connect(lambda:self.change_page(explore_btn, 'explore'))
        edit_btn.toggled.connect(   lambda:self.change_page(edit_btn,    'edit'))
        
        tabs_layout.addStretch(1)
        tabs_layout.addWidget(edit_btn)
        tabs_layout.addWidget(explore_btn)
        tabs_layout.addWidget(search_btn)
        tabs_layout.addStretch(1)
        
        tabs_widget.setLayout(tabs_layout)
        
        # ONLINE/OFFLINE - SETTINGS & about
        # """
        on_off_line           = QWidget()
        on_off_line_layout    = QVBoxLayout()
        on_off_line_indicator = QCheckBox()
        on_off_line_label     = QLabel(translation.langs['offline'][self.current_lang])
        on_off_line_indicator.setObjectName('on_off_line_indicator')
        on_off_line_indicator.setLayoutDirection(Qt.RightToLeft)
        on_off_line_label.setObjectName('on_off_line_label')
        on_off_line_layout.addWidget(on_off_line_indicator, 1)
        on_off_line_layout.addWidget(on_off_line_label, 1, Qt.AlignRight)
        on_off_line.setLayout(on_off_line_layout)
        on_off_line_indicator.stateChanged.connect(lambda:self.set_online(on_off_line_indicator, on_off_line_label))
        # """
        
        """
        on_off_line = QCheckBox(translation.langs['online'][self.current_lang])
        on_off_line.setObjectName('on_off_line')
        on_off_line.setLayoutDirection(Qt.RightToLeft)
        """
        
        settings_about_widget = QWidget()
        settings_about_layout = QHBoxLayout()
        settings_btn = QPushButton()
        about_btn     = QPushButton()
        settings_btn.setObjectName('settings_btn')
        about_btn.setObjectName('about_btn')
        settings_btn.setToolTip(translation.langs['settings'][self.current_lang])
        about_btn.setToolTip(translation.langs['about'][self.current_lang])
        
        settings_btn.clicked.connect(lambda:self.show_settings())
        about_btn.clicked.connect(lambda:self.show_about())
        
        settings_about_layout.addWidget(about_btn)
        settings_about_layout.addWidget(settings_btn)
        settings_about_layout.addStretch()
        settings_about_widget.setLayout(settings_about_layout)
        
        
        
        # H E A D E R
        header_layout.addWidget(settings_about_widget,   1)
        header_layout.addWidget(tabs_widget, 2)
        header_layout.addWidget(on_off_line, 1, Qt.AlignRight)
        
        # P A G E S
        page_layout = QVBoxLayout()
        
        search_page  = QWidget()
        explore_page = QWidget()
        edit_page    = QWidget()
        
        self.pages = { 'search': search_page, 'explore': explore_page, 'edit': edit_page }
        # Maybe add a 'loading' page and show the dictionary animation
        self.current_page = 'search'
        
        
        # =====================
        # S E A R C H
        # P A G E
        # =====================
        search_layout  = QVBoxLayout()
        
        # Search Box
        search_box  = QLineEdit(search_page)
        error_label = QLabel(search_page)
        search_box.setObjectName('search_box')
        error_label.setObjectName('error_label')
        search_box.setPlaceholderText('كلمة / عبارة')
        search_box.setAlignment(Qt.AlignCenter)
        error_label.setAlignment(Qt.AlignCenter)
        error_label.hide()
        search_layout.addWidget(search_box, 0, Qt.AlignHCenter)
        search_layout.addWidget(error_label, 0, Qt.AlignHCenter)
        
        # Welcome Screen
        welcome_page   = QWidget()
        welcome_layout = QVBoxLayout()
        welcome_img    = QMovie('ressources/imgs/dict_flip.gif')
        welcome_widget = QLabel()
        welcome_label  = QLabel(translation.langs['welcome_msg'][self.current_lang])
        
        welcome_widget.setObjectName('welcome_img')
        welcome_label.setObjectName('welcome_label')
        welcome_label.setAlignment(Qt.AlignCenter)
        
        welcome_widget.setMovie(welcome_img)
        welcome_img.start()
        
        welcome_layout.addWidget(welcome_widget, 0, Qt.AlignCenter)
        welcome_layout.addWidget(welcome_label,  0, Qt.AlignCenter)
        welcome_page.setLayout(welcome_layout)
        search_layout.addWidget(welcome_page)
        

        # Search Results
        search_res_layout = QVBoxLayout()
        
        # Definition
        word_layout  = QVBoxLayout()
        def_mark    = QLabel(translation.langs['invalid'][self.current_lang])
        def_word    = QLabel()
        
        def_mark.setObjectName('def_mark')
        def_mark.setStyleSheet('background-color: white')
        def_word.setObjectName('def_word')
        
        word_layout .addWidget(def_mark,    0, Qt.AlignRight)
        word_layout .addWidget(def_word,    0, Qt.AlignRight)
       
        
        search_eras_container = QWidget()
        search_eras_scroll    = QScrollArea()
        search_eras_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        search_eras_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        search_eras_scroll.setWidgetResizable(True)
        search_eras_scroll.setLayoutDirection(Qt.RightToLeft)
        search_eras_scroll.setWidget(search_eras_container)
        search_eras_container.setLayoutDirection(Qt.LeftToRight)
        # Examples
        search_eras_layout = QVBoxLayout()
        search_eras_container.setLayout(search_eras_layout)
        search_eras_container.setObjectName('scroll_container')

        search_res_layout.addLayout(word_layout)
        search_res_layout.addWidget(search_eras_scroll)
        search_layout.addLayout(search_res_layout)

        # LOAD THE RESULTS
        search_box.returnPressed.connect(lambda:self.search_def_dict(search_box.text(), def_mark, def_word, search_eras_layout, error_label, welcome_page))

        # =====================
        # E X P L O R E
        # P A G E
        # =====================
        explore_page.setLayoutDirection(Qt.RightToLeft)
        explore_layout = QHBoxLayout()
        
        files_tree     = QTreeView()
        files_tree.setObjectName('files_tree')
        self.fill_files_tree(files_tree, self.corpus_dir)
        
        meta_layout = QGridLayout()
        meta_era    = QLabel('<b>'+translation.langs['era'][self.current_lang]+'</b>')
        meta_cat    = QLabel('<b>'+translation.langs['category'][self.current_lang]+'</b>')
        meta_author = QLabel('<b>'+translation.langs['author'][self.current_lang]+'</b>')
        meta_source = QLabel('<b>'+translation.langs['source'][self.current_lang]+'</b>')
        
        meta_era.setObjectName('meta_label')
        meta_cat.setObjectName('meta_label')
        meta_author.setObjectName('meta_label')
        meta_source.setObjectName('meta_label')
        
        meta_layout.addWidget(meta_era,    0, 0)
        meta_layout.addWidget(meta_cat,    1, 0)
        meta_layout.addWidget(meta_author, 0, 1)
        meta_layout.addWidget(meta_source, 1, 1)

        file_viewer_layout = QVBoxLayout()
        file_viewer        = QTextEdit(translation.langs['select_file'][self.current_lang])
        file_viewer.setReadOnly(True)
        file_viewer.setObjectName('file_viewer')
        file_viewer_layout.addLayout(meta_layout, 1)
        file_viewer_layout.addWidget(file_viewer, 3)

        files_tree.clicked.connect(lambda:self.view_selected_file(files_tree, file_viewer,  meta_era, meta_cat, meta_author, meta_source))
        
        explore_layout.addWidget(files_tree, 1)
        explore_layout.addLayout(file_viewer_layout, 3)
                
        
        
        # =====================
        # E D I T
        # P A G E
        # =====================
        edit_layout = QHBoxLayout()
        words_list  = QListWidget()

        edit_eras_container = QWidget()
        
        words_list.setObjectName('words_list')
        edit_page.setObjectName('edit_page')
                
        ##########################
        self.fill_words_list(words_list)
        
        words_list.setLayoutDirection(Qt.RightToLeft)

        edit_entry_layout     = QVBoxLayout()
        edit_eras_layout      = QVBoxLayout()
        edit_add_entry_layout = QHBoxLayout()
        edit_add_entry_btn    = QPushButton(translation.langs['add_entry'][self.current_lang])
        edit_add_auto_btn     = QPushButton(translation.langs['add_auto'][self.current_lang])
        edit_word_mark        = QLabel(translation.langs['invalid'][self.current_lang])
        edit_word             = QLineEdit()
        edit_valid            = QCheckBox(translation.langs['validate'][self.current_lang])
        edit_add_era_btn      = QPushButton(translation.langs['add_era'][self.current_lang])
        edit_save             = QPushButton(translation.langs['save'][self.current_lang])
        
        edit_word_mark.setObjectName('def_mark')
        edit_word.setAlignment(Qt.AlignCenter)
        edit_word.setObjectName('edit_entry_word')
        edit_add_entry_btn.setObjectName('primary_button')
        edit_add_auto_btn.setObjectName('primary_button')
        edit_add_era_btn.setObjectName('secondary_button')
        edit_save.setObjectName('primary_button')
        edit_save.setMinimumWidth(100)
        
        # edit_eras_layout.addWidget(EraEntryEdit(['era1', 'era2'], self.current_lang))
        
        edit_eras_container.setLayout(edit_eras_layout)
        edit_eras_container.setLayoutDirection(Qt.LeftToRight)
        edit_eras_container.setObjectName('scroll_container')     
        
        edit_eras_scroll = QScrollArea()
        edit_eras_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        edit_eras_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        edit_eras_scroll.setWidgetResizable(True)
        edit_eras_scroll.setLayoutDirection(Qt.RightToLeft)
        edit_eras_scroll.setWidget(edit_eras_container)
            
        edit_add_entry_layout.addWidget(edit_add_auto_btn)
        edit_add_entry_layout.addWidget(edit_add_entry_btn)
        edit_entry_layout.addLayout(edit_add_entry_layout)
        edit_entry_layout.addWidget(edit_word_mark, 0, Qt.AlignRight)
        edit_entry_layout.addWidget(edit_word)
        
        edit_entry_layout.addWidget(edit_eras_scroll)
        # edit_entry_layout.addStretch()
        
        edit_entry_layout.addWidget(edit_add_era_btn)
        # edit_entry_layout.addStretch()
        edit_entry_layout.addItem(QSpacerItem(1, 40))
        edit_save_layout = QHBoxLayout()
        edit_save_layout.addWidget(edit_save)
        edit_save_layout.addWidget(edit_valid)
        edit_save_layout.addStretch()
        edit_entry_layout.addLayout(edit_save_layout)
        
        edit_layout.addLayout(edit_entry_layout, 3)
        edit_layout.addWidget(words_list,  1)

        edit_add_entry_btn.clicked.connect(lambda:self.add_new_entry(edit_word_mark, edit_word, edit_valid, edit_eras_layout, words_list))
        edit_add_auto_btn.clicked.connect(lambda:self.show_auto_entry())
        edit_add_era_btn.clicked.connect(lambda:self.add_era(edit_eras_layout, edit_word.text()))
        words_list.itemSelectionChanged.connect(lambda:self.view_dict_entry(words_list, edit_word_mark, edit_word, edit_eras_layout, edit_valid))
        edit_save.clicked.connect(lambda:self.save_entry(edit_word.text(), edit_eras_layout, edit_valid, words_list))


        # =====================
        # M A I N   P A G E S
        # =====================
        search_page .setLayout(search_layout)        
        explore_page.setLayout(explore_layout)        
        edit_page   .setLayout(edit_layout)
        
        explore_page.hide()
        edit_page.hide()
        
        page_layout.addWidget(search_page)
        page_layout.addWidget(explore_page)
        page_layout.addWidget(edit_page)
        
        
        # M A I N
        # C O N T E N T
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        header_widget.setFixedHeight(90)
        
        window_layout.addWidget(header_widget)
        window_layout.addLayout(page_layout)
        main_content = QWidget(self)
        main_content.setLayout(window_layout)
        
        self.setCentralWidget(main_content)
        

        # SET THE STYLE
        # self.setStyleSheet(open('ressources/stylesheet.qss').read())
        self.show()
    # END: init_ui()


    
    # =====================
    # E D I T I O N
    # M E T H O D S
    # =====================
    
    # CLEAR A LAYOUT
    def clear_layout(self, layout): 
            if layout is not None: 
                while layout.count(): 
                     item   = layout.takeAt(0) 
                     widget = item.widget() 
                     if widget is not None: 
                         widget.deleteLater() 
                     else: 
                         clear_layout(item.layout())
    # END: clear_layout()

    # CHANGE THE PAGE (Search, Explore, Edit)
    def change_page(self, radio_btn, page):
        if radio_btn.isChecked():
            self.pages[page].show()
        else:
            self.pages[page].hide()
    # END: change_page()
    
    
    # LOOK FOR DEFINITION AND DISPLAY THE RESULT
    def search_def_dict(self, text, mark, word, eras_layout, error_label, welcome_page):    # TO IMPLEMENT
        # look for size(1 word -> def, >1 word -> expression, else nothing)
        if len(text) == 0:
            return
        
        if not welcome_page.isHidden():
            welcome_page.hide()

        if text not in self.hist_dict:
            # Or show error
            error_label.setText(translation.langs['not_found'][self.current_lang])
            error_label.show()
            return
        
        if not error_label.isHidden():
            error_label.hide()
        
        res = self.hist_dict[text]
        
        # Set the word label
        word.setText(' '+ text +' ')
        
        # Clear current examples
        self.clear_layout(eras_layout)
        
        if len(text.split()) == 1:
            # Set the valid mark
            if res[0]:
                mark.setStyleSheet('background-color: white')
            else:
                mark.setStyleSheet('background-color: #D38087')
                
            # Adding examples
            for era in res[1]:
                eras_layout.addWidget(EraEntry(' '+era+' ', ' '+res[1][era][0]+' ', res[1][era][1]))
        else:
            # Set the valid mark
            mark.setStyleSheet('background-color: white')
                
            # Adding examples
            for era in res[1]:
                eras_layout.addWidget(EraEntry(' '+era+' ', '', era[1], True))

    # END: search_def()
    
    def set_online(self, indicator, label):
        if indicator.isChecked():
            label.setText(translation.langs['online'][self.current_lang])
            self.is_online = True
        else:
            label.setText(translation.langs['offline'][self.current_lang])
            self.is_online = False
    # END: set_online
    
    def fill_files_tree(self, files_tree, directory):
        model = QFileSystemModel()
        model.setRootPath(directory)
        files_tree.setModel(model)
        files_tree.setRootIndex(model.index(directory))
        # files_tree.header().hide()
        files_tree.setHeaderHidden(True)
        for i in range(1, files_tree.header().count()):
            files_tree.hideColumn(i)
    # END: fill_files_tree
        
    def view_selected_file(self, files_tree, viewer, era_label, cat_label, author_label, source_label):
        
        path = files_tree.model().fileInfo(files_tree.selectedIndexes()[0]).absoluteFilePath()
        
        if os.path.isfile(path):
            # Parse the xml file
            # text = open(path, 'r').read()
            # viewer.setText(text)
            (meta, content) = controller.get_file_content(path)
            era_label.setText('<b>'+ translation.langs['era'][self.current_lang] +'</b>'+ meta['era'])
            cat_label.setText('<b>'+ translation.langs['category'][self.current_lang] +'</b>'+ meta['category'])
            author_label.setText('<b>'+ translation.langs['author'][self.current_lang] +'</b>'+ meta['author'])
            source_label.setText('<b>'+ translation.langs['source'][self.current_lang] +'</b>'+ meta['source'])
            viewer.setText(content)
    # END: view_selected_file()
    
    def fill_words_list(self, words_list):
        for w in sorted(self.hist_dict):
            if self.hist_dict[w][0]:
                words_list.addItem(QListWidgetItem(self.not_marked_icon, w))
            else:
                words_list.addItem(QListWidgetItem(self.marked_icon, w))
    # END: fill_words_list()

    def add_era(self, edit_eras_layout, word):
        era_edit = EraEntryEdit(self.eras, self.current_lang)
        edit_eras_layout.addWidget(era_edit)
        era_edit.search_def_btn.clicked.connect(lambda:self.search_def(era_edit, word))
        era_edit.search_ex_btn.clicked.connect(lambda:self.search_examples(era_edit, word))
        return era_edit
    # END: add_era()
    
    def view_dict_entry(self, words_list, word_mark, word_edit, edit_eras_layout, valid_checkbox):
        if (len(words_list.selectedItems()) > 0):
            # print(words_list.selectedItems()[0].text())
            word = words_list.selectedItems()[0].text()
            self.clear_layout(edit_eras_layout)
            word_edit.setText(word)
            if self.hist_dict[word][0]:
                word_mark.setStyleSheet('background-color: #FFF')
            else:
                word_mark.setStyleSheet('background-color: #D38087')
            valid_checkbox.setEnabled(not self.hist_dict[word][0])
            valid_checkbox.setChecked(self.hist_dict[word][0])
            
            # Add the entries
            for era in self.hist_dict[word][1]:
                era_entry = self.add_era(edit_eras_layout, word)
                combo_index = era_entry.era.findText(era)
                if combo_index >= 0:
                    era_entry.era.setCurrentIndex(combo_index)
                
                era_entry.word_def.setText(self.hist_dict[word][1][era][0])
                for ex in self.hist_dict[word][1][era][1]:
                    era_entry.add_example_content(ex)
            
    # END: view_dict_entry()
    
    def add_new_entry(self, word_mark, word, valid, layout, words_list):
        word.setText('')
        valid.setChecked(False)
        self.clear_layout(layout)
        word_mark.setStyleSheet('background-color: #D38087')
        if (len(words_list.selectedItems()) > 0):
            item = words_list.selectedItems()[0]
            item.setSelected(False)
    # END: add_new_entry()
    
    def show_settings(self):
        self.settings_popup = Popup()
        self.settings_popup.setWindowTitle(translation.langs['settings'][self.current_lang])
        self.settings_popup.setWindowIcon(self.window_icon)
        self.settings_popup.resize(400, 250)
        self.settings_popup.setObjectName('settings_popup')
        
        layout = QVBoxLayout()
        text   = QLabel('This feature is not available yet.')
        text.setAlignment(Qt.AlignCenter)
        text.setObjectName('popup_text')
        layout.addWidget(text)
        self.settings_popup.setLayout(layout)
        
        self.settings_popup.show()
        
    # END: show_settings
    
    def show_about(self):
        self.about_popup= Popup()
        self.about_popup.setWindowTitle(translation.langs['about'][self.current_lang])
        self.about_popup.setWindowIcon(self.window_icon)
        self.about_popup.resize(400, 300)
        self.about_popup.setObjectName('about_popup')
        
        layout = QVBoxLayout()
        text   = QLabel(translation.langs['about_content'][self.current_lang])
        text.setAlignment(Qt.AlignCenter)
        text.setObjectName('popup_text')
        layout.addWidget(text)
        self.about_popup.setLayout(layout)
        
        self.about_popup.show()
    # END: show_about
    
    def show_auto_entry(self):
        self.auto_add_popup = Popup()
        self.auto_add_popup.setWindowTitle(translation.langs['add_auto'][self.current_lang])
        self.auto_add_popup.setWindowIcon(self.window_icon)
        self.auto_add_popup.resize(400, 200)
        self.auto_add_popup.setObjectName('auto_entry_popup')
        
        layout = QVBoxLayout()
        nb_entries = QLineEdit()
        add_btn    = QPushButton(translation.langs['add_auto'][self.current_lang])
        nb_entries.setPlaceholderText(translation.langs['nb_entries'][self.current_lang])
        nb_entries.setAlignment(Qt.AlignCenter)
        
        add_btn.setObjectName('primary_button')
        layout.addWidget(QLabel(translation.langs['nb_entries'][self.current_lang]))
        layout.addWidget(nb_entries)
        layout.addStretch()
        layout.addWidget(add_btn)
        
        self.auto_add_popup.setLayout(layout)
        
        add_btn.clicked.connect(lambda:self.add_auto_entries(int(nb_entries.text())))
        
        self.auto_add_popup.show()
        nb_entries.clearFocus()
    # END: show_auto_entry()
    
    def save_entry(self, word, edit_eras_layout, valid_checkbox, words_list):
        if len(word) == 0:
            return
        
        eras = {}
        for i in range(edit_eras_layout.count()):
            entry    = edit_eras_layout.itemAt(i).widget()
            entry.__class__ = EraEntryEdit
            era_name = entry.era.currentText()
            word_def = entry.word_def.toPlainText()
            examples = []
            for j in range(entry.examples.count()):
                examples.append(entry.examples.itemAt(j).widget().text())
            eras[era_name] = (word_def, examples)

        self.hist_dict[word] = (valid_checkbox.isChecked(), eras)
        
        # Update the list
        words_list.clear()
        self.fill_words_list(words_list)
        
        print('saving...')
        if valid_checkbox.isChecked():
            save_dict(self.hist_dict, self.dict_path)
        else:
            save_dict(self.hist_dict, self.dict_path_not_valid, False)

    # END: save_entry
    
    
    def add_auto_entries(self, nb_entries):
        print('nb entries:'+ str(nb_entries))
        added_words = controller.generate_entries(nb_entries, self.hist_dict, self.eras, self.is_online)
        print('Added words: ')
        print(added_words)
    # END: add_auto_entries()
    
    
    def search_def(self, era_edit, word):
        if len(word) == 0:
            return
        # call a function to get the definitions of 'word'
        # word_defs = ['def1'+word, 'def2'+word, 'def3'+word]
        
        word_defs = controller.get_definition(word, self.is_online);        
        
        self.select_def_popup = Popup()
        self.select_def_popup.setWindowTitle(translation.langs['select_def'][self.current_lang])
        self.select_def_popup.setWindowIcon(self.window_icon)
        self.select_def_popup.resize(400, 600)
        self.select_def_popup.setObjectName('select_popup')
        
        layout     = QVBoxLayout()
        defs_list  = QListWidget()
        select_btn = QPushButton(translation.langs['select'][self.current_lang])
        select_btn.setObjectName('primary_button')
        
        for d in word_defs:
            defs_list.addItem(QListWidgetItem(d))

        layout     = QVBoxLayout()
        layout.addWidget(QLabel(translation.langs['select_def'][self.current_lang]))
        layout.addWidget(defs_list)
        layout.addStretch()
        layout.addWidget(select_btn)
        
        self.select_def_popup.setLayout(layout)
        
        def select_def():
            if (len(defs_list.selectedItems()) > 0):
                word_def = defs_list.selectedItems()[0].text()
                era_edit.word_def.setText(word_def)
                self.select_def_popup.close()

        select_btn.clicked.connect(lambda:select_def())

        self.select_def_popup.show()
    # END: search_def()
    
    def search_examples(self, era_edit, word):
        if len(word) == 0:
            return
        # call a function to get the examples of 'word'
        # word_examples = ['ex1 '+word, 'ex2 '+word, 'ex3 '+word]
        era = era_edit.era.currentText()
        word_examples = controller.get_examples(word, era);
        print('len(word_examples) = '+ str(len(word_examples)))
        if len(word_examples):
            print('word_examples[0]   = '+ str(word_examples[0]))
        
        self.select_ex_popup = Popup()
        self.select_ex_popup.setWindowTitle(translation.langs['select_ex'][self.current_lang])
        self.select_ex_popup.setWindowIcon(self.window_icon)
        self.select_ex_popup.resize(400, 600)
        self.select_ex_popup.setObjectName('select_popup')
        
        layout     = QVBoxLayout()
        ex_list    = QListWidget()
        select_btn = QPushButton(translation.langs['select'][self.current_lang])
        select_btn.setObjectName('primary_button')
        
        for ex in word_examples:
            ex_list.addItem(QListWidgetItem(ex))

        layout     = QVBoxLayout()
        layout.addWidget(QLabel(translation.langs['select_ex'][self.current_lang]))
        layout.addWidget(ex_list)
        layout.addStretch()
        layout.addWidget(select_btn)
        
        self.select_ex_popup.setLayout(layout)
        
        def select_ex():
            if (len(ex_list.selectedItems()) > 0):
                word_ex = ex_list.selectedItems()[0].text()
                era_edit.add_example_content(word_ex)
                self.select_ex_popup.close()

        select_btn.clicked.connect(lambda:select_ex())

        self.select_ex_popup.show()
    # END: search_examples()

# =====================
# APPLLICATION
# ENTRY POINT
# =====================
def main(args):
    print(' == APPLICATION START ==')
    
    app         = None      # I don't know if that really gets rid of the kernel restart
    app         = QApplication(args)
    main_window = MainWindow()
    
    # ADD THE FONTS
    QFontDatabase.addApplicationFont('ressources/fonts/Cairo_SemiBold.ttf')
    QFontDatabase.addApplicationFont('ressources/fonts/Dubai.ttf')
    
    app.setStyleSheet(open('ressources/stylesheet.qss').read())
    
    app.setQuitOnLastWindowClosed(True)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
    

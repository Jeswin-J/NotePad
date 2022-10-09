from distutils.fancy_getopt import wrap_text
from importlib.resources import path
import sys, os, Icons
from turtle import clear
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QPlainTextEdit, QStatusBar, QToolBar, \
    QVBoxLayout, QAction, QFileDialog, QMessageBox, QTextEdit, QDockWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence
from PyQt5.QtPrintSupport import QPrintDialog

class Notepad(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setWindowTitle('NotePad360')
        self.setWindowIcon(QIcon('./Icons/notepad.ico'))
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 2, self.screen_height * 2)

        self.filterTypes = 'Text Document (*.txt);; Python (*.py);; Markdown (*,md)'

        self.path = None

        fixedFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedFont.setPointSize(14)

        mainLayout = QVBoxLayout()

        #Editor
        self.editor = QPlainTextEdit()          
        self.editor.setFont(fixedFont)
        mainLayout.addWidget(self.editor)

        #Container
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        #Status Bar
        self.statusBar = self.statusBar()

        #File Tool Bar
        #---------X----------X----------X----------
        toolbar = QToolBar('File')
        toolbar.setIconSize(QSize(60, 60))
        self.addToolBar(Qt.RightToolBarArea, toolbar)
        #---------X----------X----------X----------

        
        #File Menu 
        #---------X----------X----------X----------
        menu = self.menuBar().addMenu('&File')

        #Open
        open_file_action = QAction(QIcon('./Icons/file_open.ico'), 'Open File...', self)
        open_file_action.setStatusTip('Open File')
        open_file_action.setShortcut(QKeySequence.Open)
        open_file_action.triggered.connect(self.file_open)

        #Save
        save_file_action = self.create_action(self,'./Icons/save.ico', 'Save File', 'Save File', self.file_save)
        save_file_action.setShortcut(QKeySequence.Save)

        #Save As
        save_fileAs_action = self.create_action(self,'./Icons/save.ico', 'Save File As', 'Save File As...', self.file_saveAs)
        save_fileAs_action.setShortcut(QKeySequence('Ctrl+Shift+S'))


        menu.addActions([open_file_action, save_file_action, save_fileAs_action])
        toolbar.addActions([open_file_action, save_file_action, save_fileAs_action])
        

        #Print Document
        print_action = self.create_action(self,'./Icons/print.ico', 'Print File', 'Print File', self.print_file)
        print_action.setShortcut(QKeySequence.Print)
        menu.addAction(print_action)
        toolbar.addAction(print_action)
        #---------X----------X----------X----------


        #Edit Tool Bar 
        #---------X----------X----------X----------
        edit_toolbar = QToolBar('Edit')
        edit_toolbar.setIconSize(QSize(60,60))
        self.addToolBar(Qt.RightToolBarArea, edit_toolbar)
        #---------X----------X----------X----------


        #Edit Menu 
        #---------X----------X----------X----------
        edit_menu = self.menuBar().addMenu('&Edit')

        #Undo, Redo
        undo_action = self.create_action(self, './Icons/undo.ico', 'Undo', 'Click to Undo', self.editor.undo)
        undo_action.setShortcut(QKeySequence.Undo)

        redo_action = self.create_action(self, './Icons/redo.ico', 'Redo', 'Click to Redo', self.editor.redo)
        redo_action.setShortcut(QKeySequence.Redo)

        edit_menu.addActions({undo_action, redo_action})
        edit_toolbar.addActions([undo_action, redo_action])

        #Clear
        clear_action = self.create_action(self, './Icons/clear.ico', 'Clear', 'Click to Clear', self.editor.clear)
        edit_menu.addAction(clear_action)
        edit_toolbar.addAction(clear_action)

        edit_menu.addSeparator()
        edit_toolbar.addSeparator()

        #Cut, Copy, Paste, Select all 
        cut_action = self.create_action(self, './Icons/cut.ico', 'Cut', 'Cut Text', self.editor.cut)
        copy_action = self.create_action(self, './Icons/copy.ico', 'Copy', 'Copy Text', self.editor.copy)
        paste_action = self.create_action(self, './Icons/paste.ico', 'Paste', 'Paste Here', self.editor.paste)
        selectall_action = self.create_action(self, './Icons/select_all.ico', 'Select All', 'Select All', self.editor.selectAll)
        
        cut_action.setShortcut(QKeySequence.Cut)
        copy_action.setShortcut(QKeySequence.Copy)
        paste_action.setShortcut(QKeySequence.Paste)
        selectall_action.setShortcut(QKeySequence.SelectAll)

        edit_menu.addActions([cut_action, copy_action, paste_action, selectall_action])
        edit_toolbar.addActions([cut_action, copy_action, paste_action, selectall_action])

        edit_menu.addSeparator()
        edit_toolbar.addSeparator()

        #Wrap Text
        wrap_action = self.create_action(self, './Icons/wrap.ico', 'Wrap Text', 'Wrap Text', self.wrap_txt)
        wrap_action.setShortcut('Ctrl+Shift+W')
        edit_menu.addAction(wrap_action)
        edit_toolbar.addAction(wrap_action)
        #---------X----------X----------X---------- 



        self.update_title()

    def wrap_txt(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode())

    def clear(self):
        self.editor.setPlainText('')


    def print_file(self):
        printDialog = QPrintDialog()
        if  printDialog.exec_():
            self.editor.print_(printDialog.printer())


    def file_save(self):
        if self.path is None:
            self.file_saveAs()
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.path, 'w') as f:
                    f.write(text)
                    f.close()

            except Exception as e:
                self.dialog_message(str(e))

    def file_saveAs(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save file as...',
            '',
            self.filterTypes
        )

        text = self.editor.toPlainText()

        if not path:
            return
        else:
            try:
                with open(path, 'w') as f:
                    f.write(text)
                    f.close()
            except Exception as e: 
                self.dialog_message(str(e))
            else:
                self.path = path
                self.update_title()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            directory='',
            filter=self.filterTypes
        )

        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()


    def update_title(self):
        self.setWindowTitle('{0} - Notepad360'.format(os.path.basename(self.path) if self.path else 'Untitled*'))

    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.critical)
        dlg.show()

        

    def create_action(self, parent, icon_path, action_name, set_status_tip, triggered_method):
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action




app = QApplication(sys.argv)
Notepad = Notepad()
Notepad.show()
sys.exit(app.exec_())
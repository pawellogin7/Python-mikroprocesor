from PyQt5 import QtCore, QtGui, QtWidgets
import mp_window
from mp_window import *


class Ui_Program(object):
    def __init__(self, parent):
        self.parent = parent
        self.program = []
        self.program_description = []
        self.load_temp()

    def close(self):
        self.save_temp()
        self.parent.destroy_program_window()

    def send_program(self):
        if len(self.program) > 0:
            self.parent.update_program(self.program)

    def add_command(self):
        dst = self.combo_dst.currentIndex()
        cmd = self.combo_act.currentIndex()
        src = self.combo_src.currentIndex()
        if cmd < 3:
            if src < 8 or src > 11:
                if src != dst:
                    dst += 1000
                    if src == 12:
                        try:
                            src = int(self.edit_src.text())
                        except ValueError:
                            src = 0
                        if -500 < src < 500:
                            self.program.append([dst, cmd, src])
                            self.update_program_text_box()
                    else:
                        src += 1000
                        self.program.append([dst, cmd, src])
                        self.update_program_text_box()
        elif 3 <= cmd < 5:
            if 8 <= src <= 11:
                src += 1000
                self.program.append([-1, cmd, src])
                self.update_program_text_box()
        else:
            self.program.append([-1, cmd, -1])
            self.update_program_text_box()

    def del_command(self):
        if len(self.program) > 0:
            self.program.pop()
            self.update_program_text_box()

    def del_program(self):
        if len(self.program) > 0:
            self.program = []
            self.update_program_text_box()
            self.text_description.setText('')

    def save_file(self):
        if len(self.program) > 0:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName()
            if filename:
                f = open(filename, 'w+')
                f.write('J.C. i P.L. program na mk\n')
                for line in self.program:
                    dst, cmd, src = line
                    if cmd < 3:
                        f.write(str(dst) + ' ' + str(cmd) + ' ' + str(src) + '\n')
                    elif 3 <= cmd < 5:
                        f.write('-1' + ' ' + str(cmd) + ' ' + str(src) + '\n')
                    else:
                        f.write('-1' + ' ' + str(cmd) + ' ' + '-1' + '\n')
                f.write('===$$$===\n')
                program_description = self.text_description.toPlainText()
                f.write(program_description)
                f.close()

    def load_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filename:
            with open(filename, 'r') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    if lines[0].strip() == 'J.C. i P.L. program na mk':
                        self.program = []
                        self.program_description = []
                        lines.pop(0)
                        program_end = False
                        for line in lines:
                            program_line = []
                            if line.strip() == '===$$$===':
                                program_end = True
                                continue
                            if program_end is False:
                                for val in line.split():
                                    program_line.append(int(val))
                                self.program.append(program_line)
                            else:
                                self.program_description.append(line.rstrip('\n'))
                f.close()
                if program_end is False:
                    self.program = []
                    self.program_description = []
                else:
                    self.update_program_text_box()
                    self.update_description_text_box()

    def save_temp(self):
        filename = 'mk_programy/temp.txt'
        if len(self.program) > 0:
            f = open(filename, 'w+')
            f.write('J.C. i P.L. program na mk\n')
            for line in self.program:
                dst, cmd, src = line
                if cmd < 3:
                    f.write(str(dst) + ' ' + str(cmd) + ' ' + str(src) + '\n')
                elif 3 <= cmd < 5:
                    f.write('-1' + ' ' + str(cmd) + ' ' + str(src) + '\n')
                else:
                    f.write('-1' + ' ' + str(cmd) + ' ' + '-1' + '\n')
            f.write('===$$$===\n')
            program_description = self.text_description.toPlainText()
            f.write(program_description)
            f.close()

    def load_temp(self):
        filename = 'mk_programy/temp.txt'
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            if len(lines) > 0:
                if lines[0].strip() == 'J.C. i P.L. program na mk':
                    self.program = []
                    self.program_description = []
                    lines.pop(0)
                    program_end = False
                    for line in lines:
                        program_line = []
                        if line.strip() == '===$$$===':
                            program_end = True
                            continue
                        if program_end is False:
                            for val in line.split():
                                program_line.append(int(val))
                            self.program.append(program_line)
                        else:
                            self.program_description.append(line.rstrip('\n'))
            f.close()
            if program_end is False:
                self.program = []
                self.program_description = []
        except IOError:
            pass

    def addres_id_to_text(self, id):
        if id == 1000:
            addr_txt = 'AH'
        elif id == 1001:
            addr_txt = 'AL'
        elif id == 1002:
            addr_txt = 'BH'
        elif id == 1003:
            addr_txt = 'BL'
        elif id == 1004:
            addr_txt = 'CH'
        elif id == 1005:
            addr_txt = 'CL'
        elif id == 1006:
            addr_txt = 'DH'
        elif id == 1007:
            addr_txt = 'DL'
        elif id == 1008:
            addr_txt = 'AX'
        elif id == 1009:
            addr_txt = 'BX'
        elif id == 1010:
            addr_txt = 'CX'
        elif id == 1011:
            addr_txt = 'DX'
        else:
            addr_txt = '#{}'.format(str(id))
        return addr_txt

    def command_id_to_txt(self, id):
        if id == 0:
            cmd_txt = 'MOV'
        elif id == 1:
            cmd_txt = 'ADD'
        elif id == 2:
            cmd_txt = 'SUB'
        elif id == 3:
            cmd_txt = 'PUSH'
        elif id == 4:
            cmd_txt = 'POP'
        elif id == 5:
            cmd_txt = 'INT 10h'
        elif id == 6:
            cmd_txt = 'INT 15h'
        elif id == 7:
            cmd_txt = 'INT 16h'
        elif id == 8:
            cmd_txt = 'INT 21h'
        elif id == 9:
            cmd_txt = 'INT 1Ah'
        else:
            cmd_txt = ''
        return cmd_txt

    def update_program_text_box(self):
        self.text_program.setText('')
        for line_id in range(len(self.program)):
            dst, cmd, src = self.program[line_id]
            dst_text = self.addres_id_to_text(dst)
            cmd_text = self.command_id_to_txt(cmd)
            src_text = self.addres_id_to_text(src)
            if cmd < 3:
                self.text_program.append(str(line_id + 1) + '.   ' + cmd_text + '   ' + dst_text + ', ' + src_text)
            elif 3 <= cmd < 5:
                self.text_program.append(str(line_id + 1) + '.   ' + cmd_text + '   ' + src_text)
            else:
                self.text_program.append(str(line_id + 1) + '.   ' + cmd_text)

    def update_description_text_box(self):
        self.text_description.setText('')
        for line in self.program_description:
            self.text_description.append(line)

    def setupUi(self, Program):
        Program.setObjectName("Program")
        Program.resize(730, 388)
        self.btn_close = QtWidgets.QPushButton(Program)
        self.btn_close.setGeometry(QtCore.QRect(30, 30, 111, 41))
        self.btn_close.setObjectName("btn_close")
        self.combo_dst = QtWidgets.QComboBox(Program)
        self.combo_dst.setGeometry(QtCore.QRect(30, 110, 71, 41))
        self.combo_dst.setObjectName("combo_dst")
        self.combo_dst.addItem("")
        self.combo_dst.addItem("")
        self.combo_dst.addItem("")
        self.combo_dst.addItem("")
        self.combo_dst.addItem("")
        self.combo_dst.addItem("")
        self.combo_dst.addItem("")
        self.combo_dst.addItem("")
        self.combo_act = QtWidgets.QComboBox(Program)
        self.combo_act.setGeometry(QtCore.QRect(110, 110, 71, 41))
        self.combo_act.setObjectName("combo_act")
        self.combo_act.addItem("")
        self.combo_act.addItem("")
        self.combo_act.addItem("")
        self.combo_act.addItem("")
        self.combo_act.addItem("")
        self.combo_act.addItem("")
        self.combo_act.addItem("")
        self.combo_act.addItem("")
        self.combo_act.addItem("")
        self.combo_act.addItem("")
        self.combo_src = QtWidgets.QComboBox(Program)
        self.combo_src.setGeometry(QtCore.QRect(190, 110, 81, 41))
        self.combo_src.setObjectName("combo_src")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.combo_src.addItem("")
        self.btn_load = QtWidgets.QPushButton(Program)
        self.btn_load.setGeometry(QtCore.QRect(160, 30, 111, 41))
        self.btn_load.setObjectName("btn_load")
        self.edit_src = QtWidgets.QLineEdit(Program)
        self.edit_src.setGeometry(QtCore.QRect(190, 160, 81, 31))
        self.edit_src.setObjectName("edit_src")
        self.btn_add_line = QtWidgets.QPushButton(Program)
        self.btn_add_line.setGeometry(QtCore.QRect(30, 210, 71, 41))
        self.btn_add_line.setObjectName("btn_add_line")
        self.btn_remove_line = QtWidgets.QPushButton(Program)
        self.btn_remove_line.setGeometry(QtCore.QRect(110, 210, 71, 41))
        self.btn_remove_line.setObjectName("btn_remove_line")
        self.line = QtWidgets.QFrame(Program)
        self.line.setGeometry(QtCore.QRect(20, 80, 261, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Program)
        self.line_2.setGeometry(QtCore.QRect(20, 260, 261, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.btn_save_file = QtWidgets.QPushButton(Program)
        self.btn_save_file.setGeometry(QtCore.QRect(30, 290, 111, 41))
        self.btn_save_file.setObjectName("btn_save_file")
        self.btn_load_file = QtWidgets.QPushButton(Program)
        self.btn_load_file.setGeometry(QtCore.QRect(160, 290, 111, 41))
        self.btn_load_file.setObjectName("btn_load_file")
        self.groupBox = QtWidgets.QGroupBox(Program)
        self.groupBox.setGeometry(QtCore.QRect(300, 20, 181, 351))
        self.groupBox.setObjectName("groupBox")
        self.text_program = QtWidgets.QTextBrowser(self.groupBox)
        self.text_program.setGeometry(QtCore.QRect(10, 20, 161, 321))
        self.text_program.setObjectName("text_program")
        self.btn_remove_program = QtWidgets.QPushButton(Program)
        self.btn_remove_program.setGeometry(QtCore.QRect(190, 210, 81, 41))
        self.btn_remove_program.setObjectName("btn_remove_program")
        self.groupBox_2 = QtWidgets.QGroupBox(Program)
        self.groupBox_2.setGeometry(QtCore.QRect(490, 30, 231, 351))
        self.groupBox_2.setObjectName("groupBox_2")
        self.text_description = QtWidgets.QTextEdit(self.groupBox_2)
        self.text_description.setGeometry(QtCore.QRect(10, 20, 211, 321))
        self.text_description.setObjectName("text_description")

        self.retranslateUi(Program)
        QtCore.QMetaObject.connectSlotsByName(Program)


        # Handling button clicks
        self.btn_close.clicked.connect(self.close)
        self.btn_load.clicked.connect(self.send_program)
        self.btn_add_line.clicked.connect(self.add_command)
        self.btn_remove_line.clicked.connect(self.del_command)
        self.btn_remove_program.clicked.connect(self.del_program)
        self.btn_save_file.clicked.connect(self.save_file)
        self.btn_load_file.clicked.connect(self.load_file)
        # Int only validator
        self.only_int_val = QtGui.QIntValidator()
        self.edit_src.setValidator(self.only_int_val)
        self.update_program_text_box()
        self.update_description_text_box()


    def retranslateUi(self, Program):
        _translate = QtCore.QCoreApplication.translate
        Program.setWindowTitle(_translate("Program", "Program"))
        self.btn_close.setText(_translate("Program", "Zamknij okno"))
        self.combo_dst.setItemText(0, _translate("Program", "AH"))
        self.combo_dst.setItemText(1, _translate("Program", "AL"))
        self.combo_dst.setItemText(2, _translate("Program", "BH"))
        self.combo_dst.setItemText(3, _translate("Program", "BL"))
        self.combo_dst.setItemText(4, _translate("Program", "CH"))
        self.combo_dst.setItemText(5, _translate("Program", "CL"))
        self.combo_dst.setItemText(6, _translate("Program", "DH"))
        self.combo_dst.setItemText(7, _translate("Program", "DL"))
        self.combo_act.setItemText(0, _translate("Program", "MOV"))
        self.combo_act.setItemText(1, _translate("Program", "ADD"))
        self.combo_act.setItemText(2, _translate("Program", "SUB"))
        self.combo_act.setItemText(3, _translate("Program", "PUSH"))
        self.combo_act.setItemText(4, _translate("Program", "POP"))
        self.combo_act.setItemText(5, _translate("Program", "INT 10"))
        self.combo_act.setItemText(6, _translate("Program", "INT 15"))
        self.combo_act.setItemText(7, _translate("Program", "INT 16"))
        self.combo_act.setItemText(8, _translate("Program", "INT 21"))
        self.combo_act.setItemText(9, _translate("Program", "INT 1A"))
        self.combo_src.setItemText(0, _translate("Program", "AH"))
        self.combo_src.setItemText(1, _translate("Program", "AL"))
        self.combo_src.setItemText(2, _translate("Program", "BH"))
        self.combo_src.setItemText(3, _translate("Program", "BL"))
        self.combo_src.setItemText(4, _translate("Program", "CH"))
        self.combo_src.setItemText(5, _translate("Program", "CL"))
        self.combo_src.setItemText(6, _translate("Program", "DH"))
        self.combo_src.setItemText(7, _translate("Program", "DL"))
        self.combo_src.setItemText(8, _translate("Program", "AX"))
        self.combo_src.setItemText(9, _translate("Program", "BX"))
        self.combo_src.setItemText(10, _translate("Program", "CX"))
        self.combo_src.setItemText(11, _translate("Program", "DX"))
        self.combo_src.setItemText(12, _translate("Program", "Wart. nat."))
        self.btn_load.setText(_translate("Program", "Wczytaj program"))
        self.edit_src.setText(_translate("Program", "0"))
        self.edit_src.setPlaceholderText(_translate("Program", "0"))
        self.btn_add_line.setText(_translate("Program", "Dodaj rozkaz"))
        self.btn_remove_line.setText(_translate("Program", "Usuń rozkaz"))
        self.btn_save_file.setText(_translate("Program", "Zapisz do pliku"))
        self.btn_load_file.setText(_translate("Program", "Wczytaj z pliku"))
        self.groupBox.setTitle(_translate("Program", "Program"))
        self.btn_remove_program.setText(_translate("Program", "Usuń program"))
        self.groupBox_2.setTitle(_translate("Program", "Opis programu"))

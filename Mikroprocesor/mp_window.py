from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from pynput import keyboard
import datetime
import time
import shutil
import pyautogui
from threading import Thread
from program_window import *


class Ui_Mikroprocesor(object):
    def __init__(self):
        self.child_window = None
        self.program = []
        self.current_line = -1
        self.register_values = np.zeros(8, dtype=np.int16)
        self.stack_register = 255
        self.timer = QtCore.QTimer()
        self.program_is_running = False
        self.register_stack = []
        self.key_buffer = ''
        self.key_listener_function = 0
        self.special_key_id = -1
        listener = keyboard.Listener(
            on_press=self.on_press)
        listener.start()

    def on_press(self, key):
        try:
            key_char = key.char
            self.key_buffer = key_char
        except AttributeError:
            pass
        if key == keyboard.Key.right:
            self.special_key_id = 0
        elif key == keyboard.Key.left:
            self.special_key_id = 1
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.special_key_id = 2
        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            self.special_key_id = 3
        elif key == keyboard.Key.scroll_lock:
            self.special_key_id = 4
        elif key == keyboard.Key.num_lock:
            self.special_key_id = 5
        elif key == keyboard.Key.caps_lock:
            self.special_key_id = 6
        elif key == keyboard.Key.insert:
            self.special_key_id = 7

    def open_program_window(self):
        if self.child_window is None:
            self.child_window = QtWidgets.QDialog()
            self.child_ui = Ui_Program(self)
            self.child_ui.setupUi(self.child_window)
            self.child_window.show()

    def destroy_program_window(self):
        if self.child_window is not None:
            self.child_window.close()
            self.child_window = None

    def update_program(self, program):
        self.program = program
        self.update_program_text_box()
        if self.current_line >= 0:
            self.text_curr_line.setText('Wczytano nowy program.')
            self.reset_program()

    def run_program(self):
        self.program_is_running = True
        self.run()

    def stop_program(self):
        if self.program_is_running is True and self.current_line >= 0:
            self.program_is_running = False
            self.run()

    def run(self):
        if self.program_is_running is False:
            self.text_curr_line.setText('Program został zatrzymany.')
            self.reset_program()
        else:
            error = -1
            if self.key_listener_function == 1:
                error = 0
                if self.key_buffer != '':
                    self.key_listener_function = 0
                    self.register_values[1] = ord(self.key_buffer)
                    self.update_register_text()
                    self.key_buffer = ''
            elif self.key_listener_function == 2:
                error = 0
                if self.special_key_id != -1:
                    self.key_listener_function = 0
                    self.register_values[1] = self.special_key_id
                    self.update_register_text()
            elif self.current_line < len(self.program) - 1:
                self.current_line += 1
                if self.current_line > -1:
                    self.update_line_text_box(self.current_line)
                    curr_command = self.program[self.current_line]
                    error = self.exec_command(curr_command)
                    if error == 0:
                        self.update_register_text()
                        self.update_line_text_box(self.current_line)
                    elif error == 1:
                        self.text_curr_line.setText('Błąd linia {}: wartość rejestru przekracza 127'.format(self.current_line + 1))
                        self.reset_program()
                    elif error == 2:
                        self.text_curr_line.setText('Błąd linia {}: wartość rejestru mniejsza od -128'.format(self.current_line + 1))
                        self.reset_program()
                    elif error == 3:
                        self.text_curr_line.setText('Błąd linia {}: Rejestr stosu jest pusty'.format(self.current_line + 1))
                        self.reset_program()
                    elif error == 4:
                        self.text_curr_line.setText('Błąd linia {}: Rejestr AH zawiera nieprawidłową funkcję dla tego przerwania'.format(self.current_line + 1))
                        self.reset_program()
                    elif error == 5:
                        self.text_curr_line.setText('Błąd linia {}: Nieprawidłowa wartość pozycji kursora(wartość poza ekranem)'.format(self.current_line + 1))
                        self.reset_program()
                else:
                    self.text_curr_line.setText('')
            else:
                error = -1
                if self.current_line > 0:
                    self.program_is_running = False
                    self.text_curr_line.setText('Program został wykonany.')
                    self.reset_program()
            if self.combo_run_mode.currentIndex() == 0 and error == 0:
                self.timer.singleShot(400, self.run)

    def reset_program(self):
        self.current_line = -2
        self.register_values = np.zeros(8, dtype=np.int16)
        self.update_register_text()

    def exec_command(self, params):
        dst, cmd, src = params
        dst_reg = dst - 1000
        error_id = 0
        if 1000 <= src < 1008:
            src_val = self.register_values[src - 1000]
        else:
            src_val = src
        if cmd == 0:  # MOV
            if src_val > 127:
                error_id = 1
            elif src_val < -128:
                error_id = 2
            else:
                self.register_values[dst_reg] = src_val
        elif cmd == 1:  # ADD
            val = self.register_values[dst_reg] + src_val
            if val > 127:
                error_id = 1
            elif val < -128:
                error_id = 2
            else:
                self.register_values[dst_reg] += src_val
        elif cmd == 2:  # SUB
            val = self.register_values[dst_reg] - src_val
            if val > 127:
                error_id = 1
            elif val < -128:
                error_id = 2
            else:
                self.register_values[dst_reg] -= src_val
        elif cmd == 3:  # PUSH
            reg_id = src - 1008
            self.register_stack.append([self.register_values[2*reg_id], self.register_values[2*reg_id + 1]])
            self.stack_register -= 1
        elif cmd == 4:  # POP
            if len(self.register_stack) > 0:
                val_l, val_h = self.register_stack[len(self.register_stack) - 1]
                reg_id = src - 1008
                self.register_values[2*reg_id] = val_l
                self.register_values[2*reg_id + 1] = val_h
                self.register_stack.pop()
                self.stack_register += 1
            else:
                error_id = 3
        elif cmd == 5:  # INT 10h
            if self.register_values[0] == 2:
                x = self.register_values[4] * 100 + self.register_values[5]
                y = self.register_values[6] * 100 + self.register_values[7]
                width, height = pyautogui.size()
                if 0 <= x <= width and 0 <= y <= height:
                    pyautogui.moveTo(x, y)
                else:
                    error_id = 5
            elif self.register_values[0] == 3:
                x, y = pyautogui.position()
                self.register_values[4] = int(np.floor(x / 100))
                self.register_values[5] = int(x - 100*np.floor(x / 100))
                self.register_values[6] = int(np.floor(y / 100))
                self.register_values[7] = int(y - 100*np.floor(y / 100))
            elif self.register_values[0] == 14:
                x = self.register_values[4] * 100 + self.register_values[5]
                y = self.register_values[6] * 100 + self.register_values[7]
                width, height = pyautogui.size()
                if 0 <= x <= width and 0 <= y <= height:
                    r, g, b = pyautogui.pixel(int(x), int(y))
                    self.register_values[1] = r
                    self.register_values[2] = g
                    self.register_values[3] = b
                else:
                    error_id = 5
            else:
                error_id = 4
        elif cmd == 6:  # INT 15h
            if self.register_values[0] == 86:
                tys = self.register_values[4]
                set = self.register_values[5]
                dzies = self.register_values[6]
                jed = self.register_values[7]
                if tys >= 0 and set >= 0 and dzies >= 0 and jed >= 0:
                    time.sleep((tys*1000 + set*100 + dzies*10 + jed) * 0.001)
            else:
                error_id = 4
        elif cmd == 7:  # INT 16h
            if self.register_values[0] == 0:
                if self.key_buffer == '':
                    self.key_listener_function = 1
                else:
                    self.register_values[1] = ord(self.key_buffer)
                    self.key_buffer = ''
            elif self.register_values[0] == 1:
                if self.key_buffer == '':
                    self.register_values[1] = 0
                else:
                    self.register_values[1] = ord(self.key_buffer)
            elif self.register_values[0] == 2:
                self.key_listener_function = 2
                self.special_key_id = -1
            else:
                error_id = 4
        elif cmd == 8:  # INT 21h
            if self.register_values[0] == 36:
                total, used, free = shutil.disk_usage("/")
                free_gb = int(np.floor(free / 1024 / 1024 / 1024))
                self.register_values[2] = int(np.floor(free_gb / 100))
                self.register_values[3] = int(free_gb - 100*np.floor(free_gb / 100))
            else:
                error_id = 4
        elif cmd == 9:  # INT 1Ah
            if self.register_values[0] == 2:
                now = datetime.datetime.now()
                self.register_values[4] = now.hour
                self.register_values[5] = now.minute
                self.register_values[6] = now.second
            elif self.register_values[0] == 4:
                now = datetime.datetime.now()
                century = int(np.floor(now.year / 100) + 1)
                year = now.year % 100
                self.register_values[4] = century
                self.register_values[5] = year
                self.register_values[6] = now.month
                self.register_values[7] = now.day
            else:
                error_id = 4
        return error_id

    def update_register_text(self):
        font = QtGui.QFont()
        font.setPointSize(18)
        self.text_HA.setText(np.binary_repr(self.register_values[0], width=8))
        self.text_HA.setFont(font)
        self.text_HA.setAlignment(QtCore.Qt.AlignCenter)
        self.text_LA.setText(np.binary_repr(self.register_values[1], width=8))
        self.text_LA.setFont(font)
        self.text_LA.setAlignment(QtCore.Qt.AlignCenter)
        self.text_HB.setText(np.binary_repr(self.register_values[2], width=8))
        self.text_HB.setFont(font)
        self.text_HB.setAlignment(QtCore.Qt.AlignCenter)
        self.text_LB.setText(np.binary_repr(self.register_values[3], width=8))
        self.text_LB.setFont(font)
        self.text_LB.setAlignment(QtCore.Qt.AlignCenter)
        self.text_HC.setText(np.binary_repr(self.register_values[4], width=8))
        self.text_HC.setFont(font)
        self.text_HC.setAlignment(QtCore.Qt.AlignCenter)
        self.text_LC.setText(np.binary_repr(self.register_values[5], width=8))
        self.text_LC.setFont(font)
        self.text_LC.setAlignment(QtCore.Qt.AlignCenter)
        self.text_HD.setText(np.binary_repr(self.register_values[6], width=8))
        self.text_HD.setFont(font)
        self.text_HD.setAlignment(QtCore.Qt.AlignCenter)
        self.text_LD.setText(np.binary_repr(self.register_values[7], width=8))
        self.text_LD.setFont(font)
        self.text_LD.setAlignment(QtCore.Qt.AlignCenter)
        self.text_SP.setText(np.binary_repr(self.stack_register, width=8))
        self.text_SP.setFont(font)
        self.text_SP.setAlignment(QtCore.Qt.AlignCenter)

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

    def update_line_text_box(self, line_id):
        if line_id == -1:
            self.text_curr_line.setText('')
        else:
            dst, cmd, src = self.program[line_id]
            dst_text = self.addres_id_to_text(dst)
            cmd_text = self.command_id_to_txt(cmd)
            src_text = self.addres_id_to_text(src)
            if cmd < 3:
                self.text_curr_line.setText(str(line_id + 1) + '.   ' + cmd_text + '   ' + dst_text + ', ' + src_text)
            elif 3 <= cmd < 5:
                self.text_curr_line.setText(str(line_id + 1) + '.   ' + cmd_text + '   ' + src_text)
            else:
                self.text_curr_line.setText(str(line_id + 1) + '.   ' + cmd_text)

    def setupUi(self, Mikroprocesor):
        Mikroprocesor.setObjectName("Mikroprocesor")
        Mikroprocesor.resize(628, 608)
        self.btn_load_program = QtWidgets.QPushButton(Mikroprocesor)
        self.btn_load_program.setGeometry(QtCore.QRect(20, 20, 211, 31))
        self.btn_load_program.setObjectName("btn_load_program")
        self.box_A = QtWidgets.QGroupBox(Mikroprocesor)
        self.box_A.setGeometry(QtCore.QRect(260, 20, 351, 101))
        self.box_A.setObjectName("box_A")
        self.box_LA = QtWidgets.QGroupBox(self.box_A)
        self.box_LA.setGeometry(QtCore.QRect(180, 20, 161, 71))
        self.box_LA.setObjectName("box_LA")
        self.text_LA = QtWidgets.QTextBrowser(self.box_LA)
        self.text_LA.setGeometry(QtCore.QRect(10, 20, 141, 41))
        self.text_LA.setObjectName("text_LA")
        self.box_HA = QtWidgets.QGroupBox(self.box_A)
        self.box_HA.setGeometry(QtCore.QRect(10, 20, 161, 71))
        self.box_HA.setObjectName("box_HA")
        self.text_HA = QtWidgets.QTextBrowser(self.box_HA)
        self.text_HA.setGeometry(QtCore.QRect(10, 20, 141, 41))
        self.text_HA.setObjectName("text_HA")
        self.box_B = QtWidgets.QGroupBox(Mikroprocesor)
        self.box_B.setGeometry(QtCore.QRect(260, 140, 351, 101))
        self.box_B.setObjectName("box_B")
        self.box_LB = QtWidgets.QGroupBox(self.box_B)
        self.box_LB.setGeometry(QtCore.QRect(180, 20, 161, 71))
        self.box_LB.setObjectName("box_LB")
        self.text_LB = QtWidgets.QTextBrowser(self.box_LB)
        self.text_LB.setGeometry(QtCore.QRect(10, 20, 141, 41))
        self.text_LB.setObjectName("text_LB")
        self.box_HB = QtWidgets.QGroupBox(self.box_B)
        self.box_HB.setGeometry(QtCore.QRect(10, 20, 161, 71))
        self.box_HB.setObjectName("box_HB")
        self.text_HB = QtWidgets.QTextBrowser(self.box_HB)
        self.text_HB.setGeometry(QtCore.QRect(10, 20, 141, 41))
        self.text_HB.setObjectName("text_HB")
        self.box_C = QtWidgets.QGroupBox(Mikroprocesor)
        self.box_C.setGeometry(QtCore.QRect(260, 260, 351, 101))
        self.box_C.setObjectName("box_C")
        self.box_LC = QtWidgets.QGroupBox(self.box_C)
        self.box_LC.setGeometry(QtCore.QRect(170, 20, 161, 71))
        self.box_LC.setObjectName("box_LC")
        self.text_LC = QtWidgets.QTextBrowser(self.box_LC)
        self.text_LC.setGeometry(QtCore.QRect(10, 20, 141, 41))
        self.text_LC.setObjectName("text_LC")
        self.box_HC = QtWidgets.QGroupBox(self.box_C)
        self.box_HC.setGeometry(QtCore.QRect(10, 20, 161, 71))
        self.box_HC.setObjectName("box_HC")
        self.text_HC = QtWidgets.QTextBrowser(self.box_HC)
        self.text_HC.setGeometry(QtCore.QRect(10, 20, 141, 41))
        self.text_HC.setObjectName("text_HC")
        self.box_D = QtWidgets.QGroupBox(Mikroprocesor)
        self.box_D.setGeometry(QtCore.QRect(260, 380, 351, 101))
        self.box_D.setObjectName("box_D")
        self.box_LD = QtWidgets.QGroupBox(self.box_D)
        self.box_LD.setGeometry(QtCore.QRect(180, 20, 161, 71))
        self.box_LD.setObjectName("box_LD")
        self.text_LD = QtWidgets.QTextBrowser(self.box_LD)
        self.text_LD.setGeometry(QtCore.QRect(10, 20, 141, 41))
        self.text_LD.setObjectName("text_LD")
        self.box_HD = QtWidgets.QGroupBox(self.box_D)
        self.box_HD.setGeometry(QtCore.QRect(10, 20, 161, 71))
        self.box_HD.setObjectName("box_HD")
        self.text_HD = QtWidgets.QTextBrowser(self.box_HD)
        self.text_HD.setGeometry(QtCore.QRect(10, 20, 141, 41))
        self.text_HD.setObjectName("text_HD")
        self.btn_run = QtWidgets.QPushButton(Mikroprocesor)
        self.btn_run.setGeometry(QtCore.QRect(200, 60, 31, 31))
        self.btn_run.setText("")
        self.btn_run.setObjectName("btn_run")
        self.combo_run_mode = QtWidgets.QComboBox(Mikroprocesor)
        self.combo_run_mode.setGeometry(QtCore.QRect(20, 60, 131, 31))
        self.combo_run_mode.setObjectName("combo_run_mode")
        self.combo_run_mode.addItem("")
        self.combo_run_mode.addItem("")
        self.groupBox = QtWidgets.QGroupBox(Mikroprocesor)
        self.groupBox.setGeometry(QtCore.QRect(20, 99, 211, 61))
        self.groupBox.setObjectName("groupBox")
        self.text_curr_line = QtWidgets.QTextBrowser(self.groupBox)
        self.text_curr_line.setGeometry(QtCore.QRect(10, 20, 191, 31))
        self.text_curr_line.setObjectName("text_curr_line")
        self.groupBox_2 = QtWidgets.QGroupBox(Mikroprocesor)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 170, 211, 421))
        self.groupBox_2.setObjectName("groupBox_2")
        self.text_program = QtWidgets.QTextBrowser(self.groupBox_2)
        self.text_program.setGeometry(QtCore.QRect(10, 20, 191, 391))
        self.text_program.setObjectName("text_program")
        self.btn_stop = QtWidgets.QPushButton(Mikroprocesor)
        self.btn_stop.setGeometry(QtCore.QRect(160, 60, 31, 31))
        self.btn_stop.setStyleSheet("")
        self.btn_stop.setText("")
        self.btn_stop.setObjectName("btn_stop")
        self.groupBox_3 = QtWidgets.QGroupBox(Mikroprocesor)
        self.groupBox_3.setGeometry(QtCore.QRect(260, 510, 181, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.text_SP = QtWidgets.QTextBrowser(self.groupBox_3)
        self.text_SP.setGeometry(QtCore.QRect(10, 20, 161, 51))
        self.text_SP.setObjectName("text_SP")

        self.retranslateUi(Mikroprocesor)
        QtCore.QMetaObject.connectSlotsByName(Mikroprocesor)

        self.update_register_text()
        self.btn_load_program.clicked.connect(self.open_program_window)
        self.btn_run.setStyleSheet("QPushButton{ background-image: url(img/run.png); }")
        self.btn_run.clicked.connect(self.run_program)
        self.btn_stop.setStyleSheet("QPushButton{ background-image: url(img/stop.png); }")
        self.btn_stop.clicked.connect(self.stop_program)

    def retranslateUi(self, Mikroprocesor):
        _translate = QtCore.QCoreApplication.translate
        Mikroprocesor.setWindowTitle(_translate("Mikroprocesor", "Mikroprocesor"))
        self.btn_load_program.setText(_translate("Mikroprocesor", "Wczytaj/Pisz program"))
        self.box_A.setTitle(_translate("Mikroprocesor", "Rejestr A"))
        self.box_LA.setTitle(_translate("Mikroprocesor", "AL"))
        self.text_LA.setHtml(_translate("Mikroprocesor",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_HA.setTitle(_translate("Mikroprocesor", "AH"))
        self.text_HA.setHtml(_translate("Mikroprocesor",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_B.setTitle(_translate("Mikroprocesor", "Rejestr B"))
        self.box_LB.setTitle(_translate("Mikroprocesor", "BL"))
        self.text_LB.setHtml(_translate("Mikroprocesor",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_HB.setTitle(_translate("Mikroprocesor", "BH"))
        self.text_HB.setHtml(_translate("Mikroprocesor",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_C.setTitle(_translate("Mikroprocesor", "Rejestr C"))
        self.box_LC.setTitle(_translate("Mikroprocesor", "CL"))
        self.text_LC.setHtml(_translate("Mikroprocesor",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_HC.setTitle(_translate("Mikroprocesor", "CH"))
        self.text_HC.setHtml(_translate("Mikroprocesor",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_D.setTitle(_translate("Mikroprocesor", "Rejestr D"))
        self.box_LD.setTitle(_translate("Mikroprocesor", "DL"))
        self.text_LD.setHtml(_translate("Mikroprocesor",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_HD.setTitle(_translate("Mikroprocesor", "DH"))
        self.text_HD.setHtml(_translate("Mikroprocesor",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.combo_run_mode.setItemText(0, _translate("Mikroprocesor", "Wykonaj cały"))
        self.combo_run_mode.setItemText(1, _translate("Mikroprocesor", "Wykonaj krokowo"))
        self.groupBox.setTitle(_translate("Mikroprocesor", "Obecna linia"))
        self.groupBox_2.setTitle(_translate("Mikroprocesor", "Program"))
        self.groupBox_3.setTitle(_translate("Mikroprocesor", "Rejestr SP"))
        self.text_SP.setHtml(_translate("Mikroprocesor",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Mikroprocesor = QtWidgets.QDialog()
    ui = Ui_Mikroprocesor()
    ui.setupUi(Mikroprocesor)
    Mikroprocesor.show()
    sys.exit(app.exec_())

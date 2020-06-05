# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Mikroprocesor(object):
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

    def retranslateUi(self, Mikroprocesor):
        _translate = QtCore.QCoreApplication.translate
        Mikroprocesor.setWindowTitle(_translate("Mikroprocesor", "Mikroprocesor"))
        self.btn_load_program.setText(_translate("Mikroprocesor", "Wczytaj/Pisz program"))
        self.box_A.setTitle(_translate("Mikroprocesor", "Rejestr A"))
        self.box_LA.setTitle(_translate("Mikroprocesor", "AL"))
        self.text_LA.setHtml(_translate("Mikroprocesor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_HA.setTitle(_translate("Mikroprocesor", "AH"))
        self.text_HA.setHtml(_translate("Mikroprocesor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_B.setTitle(_translate("Mikroprocesor", "Rejestr B"))
        self.box_LB.setTitle(_translate("Mikroprocesor", "BL"))
        self.text_LB.setHtml(_translate("Mikroprocesor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_HB.setTitle(_translate("Mikroprocesor", "BH"))
        self.text_HB.setHtml(_translate("Mikroprocesor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_C.setTitle(_translate("Mikroprocesor", "Rejestr C"))
        self.box_LC.setTitle(_translate("Mikroprocesor", "CL"))
        self.text_LC.setHtml(_translate("Mikroprocesor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_HC.setTitle(_translate("Mikroprocesor", "CH"))
        self.text_HC.setHtml(_translate("Mikroprocesor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_D.setTitle(_translate("Mikroprocesor", "Rejestr D"))
        self.box_LD.setTitle(_translate("Mikroprocesor", "DL"))
        self.text_LD.setHtml(_translate("Mikroprocesor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.box_HD.setTitle(_translate("Mikroprocesor", "DH"))
        self.text_HD.setHtml(_translate("Mikroprocesor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))
        self.combo_run_mode.setItemText(0, _translate("Mikroprocesor", "Wykonaj cały"))
        self.combo_run_mode.setItemText(1, _translate("Mikroprocesor", "Wykonaj krokowo"))
        self.groupBox.setTitle(_translate("Mikroprocesor", "Obecna linia"))
        self.groupBox_2.setTitle(_translate("Mikroprocesor", "Program"))
        self.groupBox_3.setTitle(_translate("Mikroprocesor", "Rejestr SP"))
        self.text_SP.setHtml(_translate("Mikroprocesor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">00000000</span></p></body></html>"))

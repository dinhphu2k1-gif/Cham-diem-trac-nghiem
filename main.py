from PyQt5 import QtCore, QtWidgets, QtGui
import gui, os, obj_detective

class myApp(gui.Ui_MainWindow, QtWidgets.QMainWindow):
    
    

    def __init__(self):
        super(myApp, self).__init__()
        self.setupUi(self)
        self.btn_capNhat.clicked.connect(self.setUpTable)
        self.btn_browse.clicked.connect(self.loadImg)
        self.btn_chamDiem.clicked.connect(self.score)
        self.btn_chamLai.clicked.connect(self.reScore)
    
    def setUpTable(self):
        soCauHoi = self.inp_soCauHoi.value()
        # for i in range(soCauHoi):
        #     self.tb_nhapDA.insertColumn(self.tb_nhapDA.columnCount())
        
    
    def loadImg(self, filename=None):
        if not filename:
            filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Photo', QtCore.QDir.currentPath(), 'Images (*.png *.jpg)')
            self.imgPath = filename
            # print(filename)
            self.tenAnh.setText(os.path.basename(filename))
            if not filename:
                return
            
    
    def score(self):
        soCauHoi = self.inp_soCauHoi.value()
        ans_predict = obj_detective.objDect(path=self.imgPath, number_ans=soCauHoi)
        string_ans = self.tb_nhapDA.toPlainText()
        ans = []
        for c in string_ans.split(','):
            ans.append(c)
        # print(self.DAout)
        # print(self.imgPath)
        # print(ans)
        # for i in range(soCauHoi):
        #     self.tb_DAout.insertColumn(self.tb_nhapDA.columnCount())
        #     self.tb_DAout.setItem(self.tb_nhapDA.columnCount(), i, self.DAout[i])
        score = 0
        string_predict = ""
        for i in range(0, soCauHoi):
            # cellDAinp = self.tb_nhapDA.item(0, i).text()
            # cellDAout = self.tb_DAout.item(0,i).text()
            # if cellDAinp == cellDAout:
            #     score += 1
            string_predict += ans_predict[i] + " ,"
            if ans[i] == ans_predict[i]:
                score += 1 
                
        print(string_predict)
        self.tb_DAout.setText(string_predict)   
        
        score = str(10*score/self.inp_soCauHoi.value())
        self.Diem.setText("<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">"+score+"</span></p></body></html>")

    def reScore(self):
        score = 0
        for i in range(self.inp_soCauHoi.value()):
            cellDAinp = self.tb_nhapDA.item(0, i).text()
            cellDAout = self.tb_DAout.item(0,i).text()
            if cellDAinp == cellDAout:
                score += 1
        score = str(10*score/self.inp_soCauHoi.value())
        self.Diem.setText("<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">"+score+"</span></p></body></html>")
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    nhom17 = myApp()
    nhom17.show()
    app.exec_()
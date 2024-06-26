from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QListView, QHBoxLayout, QVBoxLayout, QTextBrowser, QFrame
from qfluentwidgets import PushButton
from PyQt5.QtGui import QIcon, QPalette
from UI.QueryTable import *
from service.service import *
from UI.thread import WorkThread
from images.resources import *

class zjuerQuery(QMainWindow):
    def __init__(self,user):
        super().__init__()
        self.resize(1280, 800)
        self.user = user
        self._init_Ui()
        self.addfunction()
    
    def _init_Ui(self):
        self.setWindowTitle('zjuer自动成绩查询')
        self.centerwidget = QWidget(self)
        palette = QPalette()
        self.setPalette(palette)
        self.setCentralWidget(self.centerwidget)

        self.listView = QListView(self.centerwidget)
        self.listView.setGeometry(QtCore.QRect(-5, 1, 1281, 771))
        self.listView.setStyleSheet("border-image: url(:/images/background.png); opacity:0.6;")
        self.listView.setObjectName("listView")

        # 分析区和结果区建立垂直布局放在左边,爬虫工作区放右边
        self.frame = QFrame(self.centerwidget)
        self.frame.setGeometry(-5,1,1281,771)
        self.frame.setStyleSheet("background-color: rgba(216, 213, 214, 164);")
        self.HZoneLayout = QHBoxLayout(self.frame)
        self.VZoneLayout = QVBoxLayout()
        self.HZoneLayout.addLayout(self.VZoneLayout)

        # 结果分析区
        self.VAnalyseZone = QVBoxLayout()
        self.ButtonLayout = QHBoxLayout()
        self.AnalyseButton = PushButton()
        self.AnalyseButton.setText('结果分析')
        self.ButtonLayout.addWidget(self.AnalyseButton)
        self.ButtonLayout.addStretch()
        self.AnalyseRes = QTextBrowser()
        self.VAnalyseZone.addLayout(self.ButtonLayout)
        self.VAnalyseZone.addWidget(self.AnalyseRes)
        self.VZoneLayout.addLayout(self.VAnalyseZone)

        # 结果查询区
        self.ResZone = QFrame()
        self.ResZone.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ResZone.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Result = MyQueryTable(self.user)
        self.VZoneLayout.addWidget(self.Result)

        # 爬虫工作区
        self.VCrawlerLayout = QVBoxLayout()
        self.HButtonLayout = QHBoxLayout()
        self.WorkButton = PushButton()
        self.WorkButton.setText('开始爬取')
        self.HButtonLayout.addWidget(self.WorkButton)
        self.FinishButton = PushButton()
        self.FinishButton.setText('停止爬取')
        self.HButtonLayout.addWidget(self.FinishButton)
        self.WorkText = QTextBrowser()
        self.VCrawlerLayout.addLayout(self.HButtonLayout)
        self.VCrawlerLayout.addWidget(self.WorkText)
        self.HZoneLayout.addLayout(self.VCrawlerLayout)

    def addfunction(self):
        self.WorkButton.clicked.connect(self.crawler)
        self.FinishButton.clicked.connect(self.FinishCrawler)
        self.AnalyseButton.clicked.connect(self.resanalyse)

    def resanalyse(self):
        try:
            yearallres = self.user.YearAllQuery()[0]
            yearmajorres = self.user.YearMajorQuery()[0]
            semesterallres = self.user.SemesterAllQuery()[0]
            semestermajorres = self.user.SemesterMajorQuery()[0]
            data = semesterallres + semestermajorres + yearallres + yearmajorres
            year = self.user.year[12:-1]
            semester = self.user.semester[16:-1]
            html_str = '<!DOCTYPE HTML><html><head><meta name="qrichtext" content="1"><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;"><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:15pt; font-weight:600; color:#000000;">当前学期(semester)：</span></p><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:10pt; font-weight:600; color:#000000;">总学分:</span><span>data[0]，</span><span style=" font-size:10pt; font-weight:600; color:#000000;">总绩点：</span><span>data[1]</span><br /><span style=" font-size:10pt; font-weight:600; color:#000000;">平均绩点:</span><span>data[2]，</span><span style=" font-size:10pt; font-weight:600; color:#000000;">百分制平均分:</span><span>data[3]</span><br /></p><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:10pt; font-weight:600; color:#000000;">主修总学分:</span><span>data[4]，</span><span style=" font-size:10pt; font-weight:600; color:#000000;">主修总绩点：</span><span>data[5]</span><br /><span style=" font-size:10pt; font-weight:600; color:#000000;">主修平均绩点:</span><span>data[6]，</span><span style=" font-size:10pt; font-weight:600; color:#000000;">主修百分制平均分:</span><span>data[7]</span><br /></p><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:15pt; font-weight:600; color:#000000;">当前学年(year)：</span></p><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:10pt; font-weight:600; color:#000000;">总学分:</span><span>data[8]，</span><span style=" font-size:10pt; font-weight:600; color:#000000;">总绩点：</span><span>data[9]</span><br /><span style=" font-size:10pt; font-weight:600; color:#000000;">平均绩点:</span><span>data[10]，</span><span style=" font-size:10pt; font-weight:600; color:#000000;">百分制平均分:</span><span>data[11]</span><br /></p><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:10pt; font-weight:600; color:#000000;">主修总学分:</span><span>data[12]，</span><span style=" font-size:10pt; font-weight:600; color:#000000;">主修总绩点：</span><span>data[13]</span><br /><span style=" font-size:10pt; font-weight:600; color:#000000;">主修平均绩点:</span><span>data[14]，</span><span style=" font-size:10pt; font-weight:600; color:#000000;">主修百分制平均分:</span><span>data[15]</span><br /></p><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:10pt; font-weight:600; color:#ff1b1b;">(备注:如果没有选择年份和学期,则对应区域显示的是目前为止所有课的学分绩点等)</span></p><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"></p></body></html>'
            for i in range(16):
                if type(data[i]) == float:
                    html_str = html_str.replace(f"data[{i}]", f"{data[i] : .2f}")
                else:
                    html_str = html_str.replace(f"data[{i}]", f"{data[i]}")
            html_str = html_str.replace('year', year if year != '' else '所有课程')
            html_str = html_str.replace('semester', semester if semester != '' else '所有课程')
        except:
            html_str = '<div style="font-size:15pt; color:red;">该对应学期或学年无课程数据</div>'
        self.AnalyseRes.setHtml(html_str)

    # 爬虫子线程函数
    def crawler(self):
         # 设置按钮不可用
        self.WorkButton.setChecked(True)
        self.WorkButton.setDisabled(True)
        self.th = WorkThread()
        self.th.querySignal.connect(self.crawlText)
        self.th.start()

    # 更新爬虫区
    def crawlText(self, text):
        self.WorkText.append(text)

    # 停止爬虫
    def FinishCrawler(self):
        self.WorkButton.setChecked(False)
        self.WorkButton.setDisabled(False)
        try:
            self.th.IsCrawl = False
        except:
            pass


if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    ui = zjuerQuery(User())
    ui.show()
    sys.exit(app.exec_())
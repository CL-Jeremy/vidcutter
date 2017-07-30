#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################################################################
#
# VidCutter - media cutter & joiner
#
# copyright © 2017 Pete Alexandrou
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import sys

from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtWidgets import (qApp, QButtonGroup, QCheckBox, QDialog, QDialogButtonBox, QFrame, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QListView, QListWidget, QListWidgetItem, QMessageBox, QRadioButton,
                             QStackedWidget, QVBoxLayout, QWidget)


class ThemePage(QWidget):
    def __init__(self, parent=None):
        super(ThemePage, self).__init__(parent)
        self.parent = parent
        self.setObjectName('settingsthemepage')
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)
        if sys.platform != 'darwin':
            self.lightRadio = QRadioButton(self)
            self.lightRadio.setIcon(QIcon(':/images/%s/theme-light.png' % self.parent.theme))
            self.lightRadio.setToolTip('<img src=":/images/theme-light-large.jpg" />')
            self.lightRadio.setIconSize(QSize(165, 121))
            self.lightRadio.setCursor(Qt.PointingHandCursor)
            self.lightRadio.clicked.connect(self.switchTheme)
            self.lightRadio.setChecked(self.parent.theme == 'light')
            self.darkRadio = QRadioButton(self)
            self.darkRadio.setIcon(QIcon(':/images/%s/theme-dark.png' % self.parent.theme))
            self.darkRadio.setToolTip('<img src=":/images/theme-dark-large.jpg" />')
            self.darkRadio.setIconSize(QSize(165, 121))
            self.darkRadio.setCursor(Qt.PointingHandCursor)
            self.darkRadio.clicked.connect(self.switchTheme)
            self.darkRadio.setChecked(self.parent.theme == 'dark')
            themeLayout = QGridLayout()
            themeLayout.setColumnStretch(0, 1)
            themeLayout.addWidget(self.lightRadio, 0, 1)
            themeLayout.addWidget(self.darkRadio, 0, 3)
            themeLayout.addWidget(QLabel('Light', self), 1, 1, Qt.AlignHCenter)
            themeLayout.setColumnStretch(2, 1)
            themeLayout.addWidget(QLabel('Dark', self), 1, 3, Qt.AlignHCenter)
            themeLayout.setColumnStretch(4, 1)
            themeGroup = QGroupBox('Theme selection')
            themeGroup.setLayout(themeLayout)
            mainLayout.addWidget(themeGroup)
        toolbar_labels = self.parent.settings.value('toolbarLabels', 'beside', type=str)
        toolbar_iconsRadio = QRadioButton('Icons only', self)
        toolbar_iconsRadio.setToolTip('Icons only')
        toolbar_iconsRadio.setCursor(Qt.PointingHandCursor)
        toolbar_iconsRadio.setChecked(toolbar_labels == 'none')
        toolbar_underRadio = QRadioButton('Text under icons', self)
        toolbar_underRadio.setToolTip('Text under icons')
        toolbar_underRadio.setCursor(Qt.PointingHandCursor)
        toolbar_underRadio.setChecked(toolbar_labels == 'under')
        toolbar_besideRadio = QRadioButton('Text beside icons', self)
        toolbar_besideRadio.setToolTip('Text beside icons')
        toolbar_besideRadio.setCursor(Qt.PointingHandCursor)
        toolbar_besideRadio.setChecked(toolbar_labels == 'beside')
        toolbar_buttonGroup = QButtonGroup(self)
        toolbar_buttonGroup.addButton(toolbar_iconsRadio, 1)
        toolbar_buttonGroup.addButton(toolbar_underRadio, 2)
        toolbar_buttonGroup.addButton(toolbar_besideRadio, 3)
        # noinspection PyUnresolvedReferences
        toolbar_buttonGroup.buttonClicked[int].connect(self.parent.parent.toolbar.setLabels)
        toolbarLayout = QGridLayout()
        toolbarLayout.addWidget(toolbar_besideRadio, 0, 0)
        toolbarLayout.addWidget(toolbar_underRadio, 0, 1)
        toolbarLayout.addWidget(toolbar_iconsRadio, 1, 0)
        toolbarGroup = QGroupBox('Toolbar labels')
        toolbarGroup.setLayout(toolbarLayout)
        mainLayout.addWidget(toolbarGroup)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    @pyqtSlot(bool)
    def switchTheme(self) -> None:
        if self.darkRadio.isChecked():
            newtheme = 'dark'
        else:
            newtheme = 'light'
        if newtheme != self.parent.theme:
            # noinspection PyArgumentList
            mbox = QMessageBox(icon=QMessageBox.NoIcon, windowTitle='Restart required', minimumWidth=500,
                               textFormat=Qt.RichText, objectName='genericdialog')
            mbox.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
            mbox.setText('''
                <style>
                    h1 {
                        color: %s;
                        font-family: "Futura-Light", sans-serif;
                        font-weight: 400;
                    }
                    p { font-size: 15px; }
                </style>
                <h1>Warning</h1>
                <p>The application needs to be restarted in order to switch themes. Ensure you have saved
                your project or finished any cut ror join tasks in progress.</p>
                <p>Would you like to restart and switch themes now?</p>'''
                         % ('#C681D5' if self.parent.theme == 'dark' else '#642C68'))
            mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            mbox.setDefaultButton(QMessageBox.Yes)
            response = mbox.exec_()
            if response == QMessageBox.Yes:
                self.parent.parent.theme = newtheme
                self.parent.parent.parent.reboot()
            else:
                self.darkRadio.setChecked(True) if newtheme == 'light' else self.lightRadio.setChecked(True)


class VideoPage(QWidget):
    def __init__(self, parent=None):
        super(VideoPage, self).__init__(parent)
        self.parent = parent
        self.setObjectName('settingsvideopage')
        decodingCheckbox = QCheckBox('Hardware decoding', self)
        decodingCheckbox.setToolTip('Enable hardware based video decoding')
        decodingCheckbox.setCursor(Qt.PointingHandCursor)
        decodingCheckbox.setChecked(self.parent.parent.hardwareDecoding)
        decodingCheckbox.stateChanged.connect(self.switchDecoding)
        decodingLabel = QLabel('''<p>
            <b>on:</b> attempt to use best hardware decoder, fall back to software decoding on error
            <br/>
            <b>off:</b> always use software decoding
        </p>''', self)
        decodingLabel.setObjectName('decodinglabel')
        decodingLabel.setWordWrap(True)
        ratioCheckbox = QCheckBox('Keep aspect ratio', self)
        ratioCheckbox.setToolTip('Keep source video aspect ratio')
        ratioCheckbox.setCursor(Qt.PointingHandCursor)
        ratioCheckbox.setChecked(self.parent.parent.keepRatio)
        ratioCheckbox.stateChanged.connect(self.keepAspectRatio)
        ratioLabel = QLabel('''<p>
            <b>on:</b> lock video to its defined video aspect, black bars added to compensate 
            <br/>
            <b>off:</b> will always stretch video to window size (ignored in fullscreen mode)
        </p>''', self)
        ratioLabel.setObjectName('ratiolabel')
        ratioLabel.setWordWrap(True)
        videoLayout = QVBoxLayout()
        videoLayout.addWidget(decodingCheckbox)
        videoLayout.addWidget(decodingLabel)
        videoLayout.addWidget(SettingsDialog.lineSeparator())
        videoLayout.addWidget(ratioCheckbox)
        videoLayout.addWidget(ratioLabel)
        videoGroup = QGroupBox('Video playback')
        videoGroup.setLayout(videoLayout)
        zoomLevel = self.parent.settings.value('videoZoom', 0, type=int)
        zoom_qtrRadio = QRadioButton('Quarter [1:4]', self)
        zoom_qtrRadio.setToolTip('1/4 Zoom')
        zoom_qtrRadio.setCursor(Qt.PointingHandCursor)
        zoom_qtrRadio.setChecked(zoomLevel == -2)
        zoom_halfRadio = QRadioButton('Half [1:2]', self)
        zoom_halfRadio.setToolTip('1/2 Half')
        zoom_halfRadio.setCursor(Qt.PointingHandCursor)
        zoom_halfRadio.setChecked(zoomLevel == -1)
        zoom_originalRadio = QRadioButton('No zoom [1:1]', self)
        zoom_originalRadio.setToolTip('1/1 No zoom')
        zoom_originalRadio.setCursor(Qt.PointingHandCursor)
        zoom_originalRadio.setChecked(zoomLevel == 0)
        zoom_doubleRadio = QRadioButton('Double [2:1]', self)
        zoom_doubleRadio.setToolTip('2/1 Double')
        zoom_doubleRadio.setCursor(Qt.PointingHandCursor)
        zoom_doubleRadio.setChecked(zoomLevel == 1)
        zoom_buttonGroup = QButtonGroup(self)
        zoom_buttonGroup.addButton(zoom_qtrRadio, 1)
        zoom_buttonGroup.addButton(zoom_halfRadio, 2)
        zoom_buttonGroup.addButton(zoom_originalRadio, 3)
        zoom_buttonGroup.addButton(zoom_doubleRadio, 4)
        # noinspection PyUnresolvedReferences
        zoom_buttonGroup.buttonClicked[int].connect(self.setZoom)
        zoomLayout = QGridLayout()
        zoomLayout.addWidget(zoom_qtrRadio, 0, 0)
        zoomLayout.addWidget(zoom_halfRadio, 0, 1)
        zoomLayout.addWidget(zoom_originalRadio, 1, 0)
        zoomLayout.addWidget(zoom_doubleRadio, 1, 1)
        zoomGroup = QGroupBox('Video zoom level')
        zoomGroup.setLayout(zoomLayout)
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)
        mainLayout.addWidget(videoGroup)
        mainLayout.addWidget(zoomGroup)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    @pyqtSlot(int)
    def switchDecoding(self, state: int) -> None:
        self.parent.parent.mpvWidget.mpv.set_property('hwdec', 'auto' if state == Qt.Checked else 'no')
        self.parent.parent.saveSetting('hwdec', state == Qt.Checked)
        self.parent.parent.hardwareDecoding = (state == Qt.Checked)

    @pyqtSlot(int)
    def keepAspectRatio(self, state: int) -> None:
        self.parent.parent.mpvWidget.mpv.set_option('keepaspect', state == Qt.Checked)
        self.parent.settings.setValue('aspectRatio', 'keep' if state == Qt.Checked else 'stretch')
        self.parent.parent.keepRatio = (state == Qt.Checked)
        
    @pyqtSlot(int)
    def setZoom(self, button_id: int) -> None:
        if button_id == 1:
            level = -2
        elif button_id == 2:
            level = -1
        elif button_id == 4:
            level = 1
        else:
            level = 0
        self.parent.parent.mpvWidget.mpv.set_property('video-zoom', level)
        self.parent.settings.setValue('videoZoom', level)


class GeneralPage(QWidget):
    def __init__(self, parent=None):
        super(GeneralPage, self).__init__(parent)
        self.parent = parent
        self.setObjectName('settingsgeneralpage')
        keepClipsCheckbox = QCheckBox('Keep clip segments', self)
        keepClipsCheckbox.setToolTip('Keep joined clip segments')
        keepClipsCheckbox.setCursor(Qt.PointingHandCursor)
        keepClipsCheckbox.setChecked(self.parent.parent.keepClips)
        keepClipsCheckbox.stateChanged.connect(self.keepClips)
        keepClipsLabel = QLabel('''<p>
            <b>on:</b> keep the clip segments set in your clip index after they have been joined 
            <br/>
            <b>off:</b> clip segments are automatically deleted once joined to produce your new file
        </p>''', self)
        keepClipsLabel.setObjectName('keepclipslabel')
        keepClipsLabel.setWordWrap(True)
        nativeDialogsCheckbox = QCheckBox('Use native dialogs', self)
        nativeDialogsCheckbox.setToolTip('Use native file dialogs')
        nativeDialogsCheckbox.setCursor(Qt.PointingHandCursor)
        nativeDialogsCheckbox.setChecked(self.parent.parent.nativeDialogs)
        nativeDialogsCheckbox.stateChanged.connect(self.setNativeDialogs)
        nativeDialogsLabel = QLabel('''<p>
            <b>on:</b> use native dialog widgets as provided by your operating system
            <br/>
            <b>off:</b> use a generic file open & save dialog widget provided by the Qt toolkit
            <br/><br/>
            (turn off only if native dialogs are not working for you)
        </p>''', self)
        nativeDialogsLabel.setObjectName('nativedialogslabel')
        nativeDialogsLabel.setWordWrap(True)
        generalLayout = QVBoxLayout()
        generalLayout.addWidget(keepClipsCheckbox)
        generalLayout.addWidget(keepClipsLabel)
        generalLayout.addWidget(SettingsDialog.lineSeparator())
        generalLayout.addWidget(nativeDialogsCheckbox)
        generalLayout.addWidget(nativeDialogsLabel)
        generalGroup = QGroupBox('General settings')
        generalGroup.setLayout(generalLayout)
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)
        mainLayout.addWidget(generalGroup)
        # mainLayout.addWidget(seekGroup)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    @pyqtSlot(int)
    def keepClips(self, state: int):
        self.parent.parent.saveSetting('keepClips', state == Qt.Checked)
        self.parent.parent.keepClips = (state == Qt.Checked)

    @pyqtSlot(int)
    def setNativeDialogs(self, state: int):
        self.parent.parent.saveSetting('nativeDialogs', state == Qt.Checked)
        self.parent.parent.nativeDialogs = (state == Qt.Checked)


class SettingsDialog(QDialog):
    def __init__(self, parent=None, flags=Qt.WindowCloseButtonHint):
        super(SettingsDialog, self).__init__(parent, flags)
        self.parent = parent
        self.settings = self.parent.settings
        self.theme = self.parent.theme
        self.setObjectName('settingsdialog')
        self.categories = QListWidget(self)
        self.categories.setStyleSheet('QListView::item { text-decoration: none; }')
        self.categories.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.categories.setObjectName('settingsmenu')
        self.categories.setUniformItemSizes(True)
        self.categories.setMouseTracking(True)
        self.categories.setViewMode(QListView.IconMode)
        self.categories.setIconSize(QSize(90, 50))
        self.categories.setMovement(QListView.Static)
        self.categories.setFixedWidth(105)
        self.pages = QStackedWidget(self)
        self.pages.addWidget(ThemePage(self))
        self.pages.addWidget(GeneralPage(self))
        self.pages.addWidget(VideoPage(self))
        self.initCategories()
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.categories)
        horizontalLayout.addWidget(self.pages, 1)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok, self)
        buttons.accepted.connect(self.close)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addSpacing(12)
        mainLayout.addWidget(buttons)
        self.setLayout(mainLayout)
        self.setWindowTitle('Settings - {0}'.format(qApp.applicationName()))
        self.setFixedSize(620, 385)

    def initCategories(self):
        themeButton = QListWidgetItem(self.categories)
        themeButton.setIcon(QIcon(':/images/{0}/settings-theme.png'.format(self.theme)))
        themeButton.setText('Theme')
        themeButton.setToolTip('Theme settings')
        themeButton.setTextAlignment(Qt.AlignHCenter)
        themeButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        generalButton = QListWidgetItem(self.categories)
        generalButton.setIcon(QIcon(':/images/{0}/settings-general.png'.format(self.theme)))
        generalButton.setText('General')
        generalButton.setToolTip('General settings')
        generalButton.setTextAlignment(Qt.AlignHCenter)
        generalButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        videoButton = QListWidgetItem(self.categories)
        videoButton.setIcon(QIcon(':/images/{0}/settings-video.png'.format(self.theme)))
        videoButton.setText('Video')
        videoButton.setToolTip('Video settings')
        videoButton.setTextAlignment(Qt.AlignHCenter)
        videoButton.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.categories.currentItemChanged.connect(self.changePage)
        self.categories.setCurrentRow(0)
        self.categories.adjustSize()

    @staticmethod
    def lineSeparator() -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def changePage(self, current: QListWidgetItem, previous: QListWidgetItem):
        if not current:
            current = previous
        index = self.categories.row(current)
        self.pages.setCurrentIndex(index)

    @pyqtSlot()
    def closeEvent(self, event: QCloseEvent):
        self.deleteLater()
        super(SettingsDialog, self).closeEvent(event)
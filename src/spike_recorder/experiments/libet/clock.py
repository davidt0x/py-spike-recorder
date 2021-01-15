#!/usr/bin/env python3
"""
An implementation of the Libet clock as a QtWidget. This is a heavily
modified version of the Qt5 example forked from:

# forked from https://github.com/baoboa/pyqt5/blob/master/examples/widgets/analogclock.py

The original license is copied below

"""

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

import math
import numpy as np

from PyQt5.QtCore import QPoint, Qt, QDateTime, QTime, QTimer, QSettings, QRect, QRectF
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QColor, QPainter, QPolygon, QIcon, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class LibetClock(QWidget):
    minuteHand = QPolygon([
        QPoint(-2, 0),
        QPoint(-2, 0),
        QPoint(-2, -80),
        QPoint(-2, -80)
    ])

    handColor = QColor(0, 0, 0)
    minuteColor = QColor(57, 57, 57)
    whiteShadowColor = QColor(128, 128, 128)
    darkShadowColor = QColor(20, 20, 20)
    highlightColor = QColor(255, 0, 0)
    smokeBackgroundColor = QColor(255, 255, 255)
    rubyColor = QColor(255, 255, 255)
    textColor = QColor(0, 0, 0)
    textPanelColor = QColor(255, 255, 255)

    def setShowFrame(self, showFrame):
        self.showFrame = showFrame
        flags = self.windowFlags()
        if not showFrame:
            flags |= Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint
        else:
            flags &= ~int(Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

    def checkUpdate(self):
        self.update()

    def rotatedPoint(self, x, y, degr):
        theta = degr * math.pi / 180
        s = math.sin(theta)
        c = math.cos(theta)
        return int(x * c - y * s), int(x * s + y * c)

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)
        self.settings.sync()
        super(LibetClock, self).closeEvent(event)

    def __init__(self, parent=None, showFrame=False, windowSize=None, rotation_per_minute = 6.0):
        super(LibetClock, self).__init__(parent)

        self.rotation_per_minute = 8.0

        self._clock_cursor_pos = None

        self._start_time = None
        self._stop_time = None
        self.clock_stopped = True

        self.setMouseTracking(True)

        timer = QTimer(self)
        timer.timeout.connect(self.checkUpdate)
        timer.start(5)

        appIcon = QIcon.fromTheme("applications-accessories")
        self.setWindowIcon(appIcon)

        #self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setStyleSheet("background-color:black;")

        self.settings = QSettings('ToshihiroKamiya', 'Analog Clock')
        if windowSize is None:
            geometry = self.settings.value('geometry', None)
            if geometry is not None:
                self.restoreGeometry(geometry)
            else:
                windowSize = 100
                self.resize(windowSize, windowSize)
        else:
            if windowSize < 100:
                windowSize = 100
            self.resize(windowSize, windowSize)

        self.setShowFrame(not not showFrame)

        self.setWindowTitle("Analog Clock")

        font = QFont()
        font.setStyleHint(QFont.SansSerif)
        font.setFamily('monospace')
        font.setPointSize(12)
        self.font = font

        font = QFont(font)
        font.setPointSize(13)
        self.rubyFont = font

    def reset_clock(self):
        """
        Reset the clock. This moves the hand to the 12 position and stops the clock.

        Returns:
            None
        """
        self._start_time = None
        self._stop_time = None
        self.clock_stopped = True

    def start_clock(self):
        """
        Start running the clock. This starts movement of the hand.

        Returns:
            None
        """
        self.clock_stopped = False

    def stop_clock(self):
        """
        Stop the clock in its current position.

        Returns:
            None
        """
        self.clock_stopped = True
        self._stop_time = QDateTime.currentDateTime().time()

    def msecs_elapsed(self) -> int:
        """
        Get the amount of time elapsed since the clock was first started. If the clock has been stopped
        calculate the time between start and stop time.

        Returns:
            The elapsed number of milliseconds. Returns 0 when the clock has not been started.
        """
        if self._start_time is None:
            return 0
        elif self._stop_time is None:
            return self._start_time.msecsTo(QDateTime.currentDateTime().time())
        else:
            return self._start_time.msecsTo(self._stop_time)

    def paintEvent(self, event):
        """
        Render the clock. Invoked periodicaly by a QTimer setup in the constructor.

        Args:
            event: The event signal.

        Returns:
            None
        """

        side = min(self.width(), self.height())

        if self._start_time is None and not self.clock_stopped:
            self._start_time = QDateTime.currentDateTime().time()

        # Compute the hand rotation based on the elapsed milliseconds
        rotation = math.fmod(self.rotation_per_minute * 360.0 * (self.msecs_elapsed() / 60000.0), 360.0)

        # Start all the drawing.
        handColor = self.handColor
        whiteShadowPen = QPen(self.whiteShadowColor)
        whiteShadowPen.setJoinStyle(Qt.MiterJoin)
        whiteShadowPen.setWidthF(0.9)

        hlPen = QPen(self.highlightColor)
        hlPen.setJoinStyle(Qt.MiterJoin)
        hlPen.setWidthF(0.9)

        darkShadowPen = QPen(self.darkShadowColor)
        darkShadowPen.setJoinStyle(Qt.MiterJoin)
        darkShadowPen.setWidthF(0.9)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.smokeBackgroundColor))
        painter.drawEllipse(QPoint(0, 0), 99, 99)

        # Draw the 5 minute tick marks
        painter.setPen(whiteShadowPen)
        painter.setFont(self.rubyFont)
        painter.setBrush(QBrush(handColor))
        for i in range(0, 12):
            angle = i * 360/12
            x, y = self.rotatedPoint(0, -92, angle)
            painter.drawEllipse(x - 3, y - 3, 6, 6)

        # Draw the 1 minute tick marks
        painter.setPen(self.rubyColor)
        painter.setBrush(QBrush(self.minuteColor))
        for j in range(0, 60):
            if j % 5 != 0:
                angle = j * 360/60
                x, y = self.rotatedPoint(0, -92, angle)
                painter.drawEllipse(x - 1, y - 1, 2, 2)
        painter.setClipping(False)

        # Draw hour numbers
        painter.setPen(darkShadowPen)
        hour_nums = [12] + list(range(1, 12))
        for i in range(0, 12):
            x, y = self.rotatedPoint(0, -76, i * 360 / 12)
            painter.drawText(QRect(x - 10, y - 10, 20, 20), Qt.AlignCenter, "%d" % (hour_nums[i]))

        # Draw the mouse curosor highlight
        if self._clock_cursor_pos is not None:
            painter.setPen(hlPen)
            painter.drawEllipse(int(self._clock_cursor_pos[0] - 1), int(self._clock_cursor_pos[1] - 1), 2, 2)

        # draw hand
        painter.setPen(darkShadowPen)
        painter.setBrush(QBrush(self.minuteColor))
        painter.save()
        painter.rotate(rotation)
        painter.drawConvexPolygon(self.minuteHand)
        painter.restore()

        painter.end()

    def mouseMoveEvent(self, event):

        side = min(self.width(), self.height())
        scale = (200.0 / side)

        # Unscale the radius of the clock. The painter coordinate system is scaled
        # and translated in paintEvent
        radius = (1/scale) * 92

        # Find the closest point on the clock dial surface from the mouse location
        p = np.array([event.x(), event.y()])
        c = np.array([self.width() / 2, self.height() / 2])
        v = p - c

        # Get the nearest point on the clock surface
        self._clock_cursor_pos = (c + radius * (v / np.linalg.norm(v)))

        # We need to scale and transform the clock cursor position because of how the painter
        # coordinate system is setup in paintEvent. Maybe this should be done in paint event
        # I guess.
        self._clock_cursor_pos = (self._clock_cursor_pos - c) * scale

        # If the mouse isn't close enough to the surface, don't display it.
        if np.linalg.norm(self._clock_cursor_pos - (v * scale)) > 8.0:
            self._clock_cursor_pos = None


if __name__ == "__main__":
    import sys

    __doc__ = """Show wall clock.

Usage: {argv0} [Options]

Options:
  -f        Show window frame.
  -s SIZE   Set window size.
""".format(argv0=sys.argv[0])

    optionShowFrame = True
    optionWindowSize = None
    argv = sys.argv[1:]
    while argv:
        if argv[0] == '-f':
            optionShowFrame = True
        elif argv[0].startswith('-s'):
            if len(argv[0]) > 2:
                s = int(argv[0][2:])
            else:
                s = int(argv[1])
                del argv[0]
            optionWindowSize = s
        elif argv[0] == '-h':
            print(__doc__)
            sys.exit(0)
        else:
            sys.exit("error: too many arguments / unknown option: %s" % argv[0])
        del argv[0]

    argv.insert(0, sys.argv[0])
    app = QApplication(argv)
    clock = LibetClock(showFrame=optionShowFrame, windowSize=optionWindowSize)
    clock.show()
    sys.exit(app.exec_())


"""
Class OWTextableMessage
Copyright 2012-2019 LangTech Sarl (info@langtech.ch)
-----------------------------------------------------------------------------
This file is part of the Orange3-Textable package.

Orange3-Textable is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Orange3-Textable is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Orange3-Textable. If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = '0.01.4'


import json
from LTTL.Segmentation import Segmentation
from _textable.widgets.TextableUtils import (
    OWTextableBaseWidget, VersionedSettingsHandler,
    JSONMessage, SendButton, InfoBox, pluralize
)

from Orange.widgets import gui, settings
from _textable.i18n_config import *
def __(key):
    return i18n.t("textable.owtextablemessage." + key)


class OWTextableMessage(OWTextableBaseWidget):
    """Orange widget for parsing JSON data in segmentation"""

    name = __(u'name')
    description = __(u'desc')
    icon = "icons/Message.png"
    priority = 10002

    inputs = [("Segmentation", Segmentation, "inputData")]
    outputs = [("Message", JSONMessage)]

    settingsHandler = VersionedSettingsHandler(
        version=__version__.rsplit(".", 1)[0]
    )
    want_main_area = False

    def __init__(self, *args, **kwargs):
        """Initialize a Message widget"""
        super().__init__(*args, **kwargs)

        # Other attributes...
        self.segmentation = None
        self.infoBox = InfoBox(widget=self.controlArea,
                               stringNoDataSent=__(u'no_data_sent_to_output_yet'),
                                stringSettingsChanged=__(u'settings_were_changed'),
                                stringInputChanged=__(u'input_has_changed'),
                                stringSeeWidgetState=__(u'see_widget_state_below'),
                                stringClickSend=__(u'please_click_send_when_ready'))
        gui.separator(self.controlArea, height=3)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute='infoBox',
            buttonLabel=__(u'send'),
            checkboxLabel=__(u'send_automatically'),
        )

        # GUI
        gui.rubber(self.controlArea)

        # Send button...
        self.sendButton.draw()

        # Info box...
        self.infoBox.draw()

        self.setMinimumWidth(150)

        self.sendButton.sendIf()
        self.adjustSizeWithTimer()

    def inputData(self, newInput):
        """Process incoming data"""
        self.segmentation = newInput
        self.infoBox.inputChanged()
        self.sendButton.sendIf()

    def sendData(self):
        """Parse JSON data and send message"""
        if not self.segmentation:
            self.infoBox.setText(u'Widget needs input.', 'warning')
            self.send('Message', None, self)
            return
        if len(self.segmentation) > 1:
            self.infoBox.setText(
                u'Please make sure that input contains only one segment.',
                'error',
            )
            self.send('Message', None, self)
            return
        self.infoBox.inputChanged()
        try:
            content = self.segmentation[0].get_content()
            jsonList = json.loads(content)
            jsonMessage = JSONMessage(content)
            message = u'%i item@p sent to output.' % len(jsonList)
            message = pluralize(message, len(jsonList))
            self.infoBox.setText(message)
            self.send('Message', jsonMessage, self)
        except ValueError:
            self.infoBox.setText(
                u"Please make sure that input contains valid JSON data.",
                'error'
            )
            self.send('Message', None, self)
            return
        self.sendButton.resetSettingsChangedFlag()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    appl = QApplication(sys.argv)
    ow = OWTextableMessage()
    ow.show()
    appl.exec_()

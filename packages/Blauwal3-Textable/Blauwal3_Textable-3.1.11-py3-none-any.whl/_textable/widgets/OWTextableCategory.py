"""
Class OWTextableCategory
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

__version__ = '0.12.5'

from LTTL.Table import Table
from LTTL.Segmentation import Segmentation
import LTTL.Processor as Processor

from _textable.widgets.TextableUtils import (
    OWTextableBaseWidget, ProgressBar,
    InfoBox, SendButton, updateMultipleInputs, SegmentationListContextHandler,
    SegmentationsInputList
)
import Orange.data
from Orange.widgets import widget, gui, settings
from  _textable.i18n_config import *
def __(key):
    return i18n.t("textable.owtextablecategory." + key)


class OWTextableCategory(OWTextableBaseWidget):
    """Orange widget for extracting content or annotation information"""

    name = __("name")
    description = __("desc")
    icon = "icons/Category.png"
    priority = 8006

    inputs = [('Segmentation', Segmentation, "inputData", widget.Multiple)]
    outputs = [('Textable table', Table, widget.Default),
               ('Orange table', Orange.data.Table)]

    settingsHandler = SegmentationListContextHandler(
        version=__version__.rsplit(".", 1)[0]
    )
    segmentations = SegmentationsInputList()  # type: list

    intraSeqDelim = settings.Setting(u'#')
    sortOrder = settings.Setting(u'Frequency')
    sortReverse = settings.Setting(True)
    keepOnlyFirst = settings.Setting(True)
    valueDelimiter = settings.Setting(u'|')

    units = settings.ContextSetting(-1)
    _contexts = settings.ContextSetting(-1)
    unitAnnotationKey = settings.ContextSetting(u'(none)')
    contextAnnotationKey = settings.ContextSetting(u'(none)')
    sequenceLength = settings.ContextSetting(1)

    want_main_area = False

    def __init__(self):

        """Initialize a Category widget"""

        super().__init__()

        self.infoBox = InfoBox(
            widget=self.controlArea,
            stringDataSent=__(u'data_correctly_sent_to_output'),
            stringNoDataSent=__(u'no_data_sent_to_output_yet'),
            stringSettingsChanged=__(u'settings_were_changed'),
            stringInputChanged=__(u'input_has_changed'),
            stringSeeWidgetState=__(u'see_widget_state_below'),
            stringClickSend=__(u'please_click_send_when_ready')
        )
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute='infoBox',
            buttonLabel=__(u'send'),
            checkboxLabel=__(u'msg.sendcheck'),
            sendIfPreCallback=self.updateGUI,
        )

        # GUI...

        # Units box
        self.unitsBox = gui.widgetBox(
            widget=self.controlArea,
            box=__(u'units'),
            orientation='vertical',
            addSpace=True,
        )
        self.unitSegmentationCombo = gui.comboBox(
            widget=self.unitsBox,
            master=self,
            value='units',
            orientation='horizontal',
            label=__(u'segmentation'),
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=__(u'msg.segment_info'),
        )
        self.unitSegmentationCombo.setMinimumWidth(120)
        gui.separator(widget=self.unitsBox, height=3)
        self.unitAnnotationCombo = gui.comboBox(
            widget=self.unitsBox,
            master=self,
            value='unitAnnotationKey',
            sendSelectedValue=True,
            emptyString=u'(none)',
            orientation='horizontal',
            label=__(u'annotation_key'),
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=__(u'msg.annotation_info'),
        )

        gui.separator(widget=self.unitsBox, height=3)
        self.sequenceLengthSpin = gui.spin(
            widget=self.unitsBox,
            master=self,
            value='sequenceLength',
            minv=1,
            maxv=1,
            step=1,
            orientation='horizontal',
            label=__(u'sequence_length'),
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            keyboardTracking=False,
            tooltip=__(u'msg.sequence_info'),
        )
        gui.separator(widget=self.unitsBox, height=3)
        self.intraSeqDelimLineEdit = gui.lineEdit(
            widget=self.unitsBox,
            master=self,
            value='intraSeqDelim',
            orientation='horizontal',
            label=__(u'intra_seq_delimiter'),
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=__(u'msg.intra_seq_delimiter_info'),
        )
        gui.separator(widget=self.unitsBox, height=3)

        # Multiple Values box
        self.multipleValuesBox = gui.widgetBox(
            widget=self.controlArea,
            box=__(u'multiple_values'),
            orientation='vertical',
            addSpace=True,
        )
        self.sortOrderCombo = gui.comboBox(
            widget=self.multipleValuesBox,
            master=self,
            value='sortOrder',
            items=[u'Frequency', u'ASCII'],
            sendSelectedValue=True,
            orientation='horizontal',
            label=__(u'sort_by'),
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=__(u'msg.sort_by_info'),
        )
        self.sortOrderCombo.setMinimumWidth(120)
        gui.separator(widget=self.multipleValuesBox, height=3)
        self.sortReverseCheckBox = gui.checkBox(
            widget=self.multipleValuesBox,
            master=self,
            value='sortReverse',
            label=__(u'sort_in_reverse_order'),
            callback=self.sendButton.settingsChanged,
            tooltip=__(u'sort_in_reverse_order_info'),
        )
        gui.separator(widget=self.multipleValuesBox, height=3)
        gui.checkBox(
            widget=self.multipleValuesBox,
            master=self,
            value='keepOnlyFirst',
            label=__(u'keep_only_first_value'),
            callback=self.sendButton.settingsChanged,
            tooltip=__(u'msg.keep_only_first_value_info'),
        )
        gui.separator(widget=self.multipleValuesBox, height=3)
        self.multipleValuesDelimLineEdit = gui.lineEdit(
            widget=self.multipleValuesBox,
            master=self,
            value='valueDelimiter',
            orientation='horizontal',
            label=__(u'value_delimiter'),
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=__(u'msg.value_delimiter_info'),
        )
        gui.separator(widget=self.multipleValuesBox, height=3)

        # Contexts box...
        self.contextsBox = gui.widgetBox(
            widget=self.controlArea,
            box=__(u'contexts'),
            orientation='vertical',
            addSpace=True,
        )
        self.contextSegmentationCombo = gui.comboBox(
            widget=self.contextsBox,
            master=self,
            value='_contexts',
            orientation='horizontal',
            label=__(u'segmentation'),
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=__(u'msg.segment_info'),
        )
        gui.separator(widget=self.contextsBox, height=3)
        self.contextAnnotationCombo = gui.comboBox(
            widget=self.contextsBox,
            master=self,
            value='contextAnnotationKey',
            sendSelectedValue=True,
            emptyString=u'(none)',
            orientation='horizontal',
            label=__(u'annotation_key'),
            labelWidth=180,
            callback=self.sendButton.settingsChanged,
            tooltip=__(u'msg.context_info'),
        )
        gui.separator(widget=self.contextsBox, height=3)

        gui.rubber(self.controlArea)

        # Send button...
        self.sendButton.draw()

        # Info box...
        self.infoBox.draw()

        self.sendButton.sendIf()
        self.adjustSizeWithTimer()

    def inputData(self, newItem, newId=None):
        """Process incoming data."""
        self.closeContext()
        updateMultipleInputs(
            self.segmentations,
            newItem,
            newId,
            self.onInputRemoval
        )
        self.infoBox.inputChanged()
        self.updateGUI()

    def onInputRemoval(self, index):
        """Handle removal of input with given index"""
        if index < self.units:
            self.units -= 1
        elif index == self.units and self.units == len(self.segmentations) - 1:
            self.units -= 1
        if index == self._contexts:
            self.mode = u'No context'
            self._contexts = -1
        elif index < self._contexts:
            self._contexts -= 1
            if self._contexts < 0:
                self.mode = u'No context'
                self._contexts = -1

    def sendData(self):

        """Check input, build table, then send it"""

        # Check that there's something on input...
        if len(self.segmentations) == 0:
            self.infoBox.setText(__(u'msg.widget_needs_input'), 'warning')
            self.send('Textable table', None)
            self.send('Orange table', None)
            return

        # Units parameter...
        units = {
            'segmentation': self.segmentations[self.units][1],
            'annotation_key': self.unitAnnotationKey or None,
            'seq_length': self.sequenceLength,
            'intra_seq_delimiter': self.intraSeqDelim,
        }
        if units['annotation_key'] == u'(none)':
            units['annotation_key'] = None

        # Multiple values parameter...
        multipleValues = {
            'sort_order': self.sortOrder,
            'reverse': self.sortReverse,
            'keep_only_first': self.keepOnlyFirst,
            'value_delimiter': self.valueDelimiter,
        }

        # Contexts parameter...
        assert self._contexts >= 0
        contexts = {
            'segmentation': self.segmentations[self._contexts][1],
            'annotation_key': self.contextAnnotationKey or None,
        }
        if contexts['annotation_key'] == u'(none)':
            contexts['annotation_key'] = None

        # Count...
        self.controlArea.setDisabled(True)
        self.infoBox.setText(__(u'msg.processing_please_wait'), "warning")
        progressBar = ProgressBar(
            self,
            iterations=len(contexts['segmentation'])
        )
        table = Processor.annotate_contexts(
            units,
            multipleValues,
            contexts,
            progress_callback=progressBar.advance,
        )
        progressBar.finish()
        self.controlArea.setDisabled(False)

        if not len(table.row_ids):
            self.infoBox.setText(__(u'msg.resulting_table_is_empty'), 'warning')
            self.send('Textable table', None)
            self.send('Orange table', None)
        else:
            self.infoBox.setText(__(u'msg.table_sent_to_output'))
            self.send('Textable table', table)
            self.send('Orange table', table.to_orange_table())

        self.sendButton.resetSettingsChangedFlag()

    def updateGUI(self):

        """Update GUI state"""

        self.unitSegmentationCombo.clear()
        self.unitAnnotationCombo.clear()
        self.unitAnnotationCombo.addItem(u'(none)')

        if len(self.segmentations) == 0:
            self.units = -1
            self.unitAnnotationKey = u''
            self.unitsBox.setDisabled(True)
            self.contextsBox.setDisabled(True)
            return
        else:
            if len(self.segmentations) == 1:
                self.units = 0
            for segmentation in self.segmentations:
                self.unitSegmentationCombo.addItem(segmentation[1].label)
            self.units = self.units
            unitAnnotationKeys \
                = self.segmentations[self.units][1].get_annotation_keys()
            for k in unitAnnotationKeys:
                self.unitAnnotationCombo.addItem(k)
            if self.unitAnnotationKey not in unitAnnotationKeys:
                self.unitAnnotationKey = u'(none)'
            self.unitAnnotationKey = self.unitAnnotationKey
            self.unitsBox.setDisabled(False)
            self.sequenceLengthSpin.setRange(
                1,
                len(self.segmentations[self.units][1])
            )
            self.sequenceLength = self.sequenceLength or 1
            self.contextsBox.setDisabled(False)
            self.contextSegmentationCombo.clear()
            for index in range(len(self.segmentations)):
                self.contextSegmentationCombo.addItem(
                    self.segmentations[index][1].label
                )
            self._contexts = max(self._contexts, 0)
            segmentation = self.segmentations[self._contexts]
            self.contextAnnotationCombo.clear()
            self.contextAnnotationCombo.addItem(u'(none)')
            contextAnnotationKeys = segmentation[1].get_annotation_keys()
            for key in contextAnnotationKeys:
                self.contextAnnotationCombo.addItem(key)
            if self.contextAnnotationKey not in contextAnnotationKeys:
                self.contextAnnotationKey = u'(none)'
            self.contextAnnotationKey = self.contextAnnotationKey

    def handleNewSignals(self):
        """Overridden: called after multiple signals have been added"""
        self.openContext(self.uuid, self.segmentations)
        self.updateGUI()
        self.sendButton.sendIf()


if __name__ == '__main__':
    import sys
    import re
    from PyQt5.QtWidgets import QApplication
    from LTTL.Input import Input
    from LTTL import Segmenter as segmenter

    appl = QApplication(sys.argv)
    ow = OWTextableCategory()
    seg1 = Input(u'aaabc', 'text1')
    seg2 = Input(u'abbc', 'text2')
    # segmenter = Segmenter()
    seg3 = segmenter.concatenate(
        [seg1, seg2],
        import_labels_as='string',
        label='corpus'
    )
    seg4 = segmenter.tokenize(
        seg3,
        regexes=[(re.compile(r'\w+'), u'tokenize',)],
    )
    seg5 = segmenter.tokenize(
        seg4,
        regexes=[(re.compile(r'[ai]'), u'tokenize',)],
        label='V'
    )
    seg6 = segmenter.tokenize(
        seg4,
        regexes=[(re.compile(r'[bc]'), u'tokenize',)],
        label='C'
    )
    seg7 = segmenter.concatenate(
        [seg5, seg6],
        import_labels_as='category',
        label='letters',
        sort=True,
        merge_duplicates=True,
    )
    ow.inputData(seg7, 1)
    ow.inputData(seg4, 2)
    ow.show()
    appl.exec_()
    ow.saveSettings()

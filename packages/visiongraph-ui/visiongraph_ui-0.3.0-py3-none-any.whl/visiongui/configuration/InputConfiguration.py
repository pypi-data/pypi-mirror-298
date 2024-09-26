from typing import Dict, Any

import duit.ui as dui
from duit.annotation.AnnotationList import AnnotationList
from duit.arguments.Argument import Argument
from duit.model.DataField import DataField
from visiongraph.input import InputProviders


class InputConfiguration:
    def __init__(self):
        self.input = DataField(self._first_entry(InputProviders)) | AnnotationList(
            dui.Options("Input Device", list(InputProviders.keys())),
            Argument()
        )

        self.source = DataField("0") | AnnotationList(
            dui.Text("Input Source"),
            Argument()
        )

    @staticmethod
    def _first_entry(data: Dict[str, Any]) -> str:
        return list(data.items())[0][0]

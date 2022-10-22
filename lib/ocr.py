#!/usr/bin/python
# -*- coding: utf-8 -*-

import ddddocr
import onnxruntime

onnxruntime.set_default_logger_severity(3)


class OCR(object):

    def __init__(self, engine_choice='dddd'):
        self.engine_choice = engine_choice
        self.__init_ocr_engine(engine_choice)

    def __init_ocr_engine(self, engine):
        if engine == 'dddd':
            self.engine = ddddocr.DdddOcr(show_ad=False)

    def ocr(self, content):
        result = None
        if self.engine_choice == 'dddd':
            result = self.engine.classification(content)
        return result

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
from flask_restful.reqparse import Argument, RequestParser


class ArgumentField(dict):
    pass


class ParserModel(object):

    def __new__(cls):
        parser = RequestParser()
        for k, v in cls.__dict__.items():
            if "__" not in k and isinstance(v, dict):
                _args_dict = {**dict(name=k), **v}
                parser.add_argument(
                    Argument(**_args_dict)
                )
        return parser

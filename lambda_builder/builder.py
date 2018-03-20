#!/usr/bin/env python


import os 

class LambdaBuilder(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def run(self):
        print(self.dest)

    def _python27(self):
        pass
    def _python36(self):
        pass
    def _go(self):
        pass
    def _dotnet(self):
        pass
    def _java(self):
        pass

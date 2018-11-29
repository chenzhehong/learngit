# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 23:26:35 2018

@author: TomRayn
"""

import config_default

class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            if not k in kw:
                self[k] = v
                
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute %s" % key)
            
    def __setattr__(self, key, value):
        self[key] = value
        
def merge(default, override):
    r = {}
    for k, v in default.items():
        if k in override:
            r[k] = merge(v, override[k]) if isinstance(v, dict) else override[k]
        else:
            r[k] = v
    return r
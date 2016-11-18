from bottle import *
import os
import imp
import sys
import json, base64
from modulefinder import ModuleFinder

@get('/health')
def health():
  return dict(ok=True, message="Search, kiss and destroy!")

def __load_handlers():
  handlers_dir = os.getcwd() + '/handlers'
  ls = os.listdir(handlers_dir)
  modules = ['handlers.%s' % f.replace('.py', '') for f in ls if f != '__init__.py' and f.endswith('.py')]
  print [__import(module) for module in modules]

def __import(module):
  print 'Import module: %s' % module
  return __import__(module, globals(), locals(), [], -1) 


def __main__():
  __load_handlers()
  run(debug=True, reloader=True)

if __name__ == '__main__':
  __main__()


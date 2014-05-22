# -*- coding: utf-8 -*-
'''
Created on 2014/05/12

@author: samuraitaiga
'''

import os
import sys
import re
import shutil
import subprocess
import ConfigParser
import zipfile
import bson
import logging
import json
import fnmatch
import urllib
from doit.action import CmdAction
from doit import get_var

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    level=logging.INFO)
BUILD_DIR = 'build'
MQL_URL = 'http://files.metaquotes.net/metaquotes.software.corp/mt5/mql.exe'
DOIT_CONFIG = {'default_tasks': ['create_product'],}

experts = []
compiled_experts = []
for root, dirnames, filenames in os.walk('Experts'):
  for filename in fnmatch.filter(filenames, '*.mq4'):
      subbed_filename = re.sub('.mq4$','',filename)
      experts.append(os.path.join('Experts', subbed_filename))
      compiled_experts.append(os.path.join('Experts', subbed_filename + '.ex4'))

libs = []
compiled_libs = []
for root, dirnames, filenames in os.walk('Libraries'):
  for filename in fnmatch.filter(filenames, '*.mq4'):
      subbed_filename = re.sub('.mq4$','',filename)
      libs.append(os.path.join('Libraries', subbed_filename))
      compiled_libs.append(os.path.join('Libraries', subbed_filename + '.ex4'))

def archive_folder(targets):
    zip_file = zipfile.ZipFile(targets[0], 'w', zipfile.ZIP_DEFLATED)
    for mql_file in compiled_experts:
        msg = 'adding ' + mql_file + ' into zip archive'
        logging.info(msg)
        zip_file.write(mql_file)

    for mql_file in compiled_libs:
        msg = 'adding ' + mql_file + ' into zip archive'
        logging.info(msg)
        zip_file.write(mql_file)
    zip_file.close()


def clean_installer_dir():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)

def task_create_product():
    "archive eas and libs for mt4"
    abs_build_dir = os.path.abspath(BUILD_DIR)
    product = os.path.join(BUILD_DIR, 'eas.zip')
    if not os.path.exists(abs_build_dir):
        os.mkdir(abs_build_dir)

    return {'actions': [archive_folder],
            'targets': [product],
            'task_dep': ['build_installer'], 
            'task_dep': ['build_mql', 
                         'build_lib'],
            'clean': True,
            'clean': [clean_installer_dir],
            'verbosity':2}


def download_mt4_compiler_if_not_exists(compiler):
    if not os.path.exists(compiler):
        logging.info('start download compiler')
        try:
            urllib.urlretrieve(MQL_URL, 'mql.exe')
        except:
            logging.exception('download mt4 compiler error')
        logging.info('download compiler finish')
    else:
        logging.info('local mt4 compiler found')

def compile_mql(module):
    mt4_compiler = get_var('mt4_compiler', None)
    if mt4_compiler:
        if os.path.exists(mt4_compiler):
            logging.info('mt4 compile with %s' % mt4_compiler)
        else:
            download_mt4_compiler_if_not_exists('mql.exe')
            mt4_compiler = 'mql.exe'
    else:
        download_mt4_compiler_if_not_exists('mql.exe')
        mt4_compiler = 'mql.exe'
    p = subprocess.Popen([mt4_compiler, module+'.mq4'])
    p.wait()
    if p.returncode is 0:
        logging.info('%s compile success' % module)
    else:
        logging.error('%s compile error' % module)

def task_build_mql():
    "build ea"
    for module in experts:
        dependencies = ['%s.mq4' % module]
        yield {'name': module,
               'actions': [(compile_mql, [module])],
               'targets': ["%s.ex4" % module],
               'file_dep': dependencies,
               'clean': True
               }

def task_build_lib():
    "build mt4 lib"
    for module in libs:
        dependencies = ['%s.mq4' % module]
        yield {'name': module,
               'actions': [(compile_mql, [module])],
               'targets': ["%s.ex4" % module],
               'file_dep': dependencies,
               'clean': True
               }


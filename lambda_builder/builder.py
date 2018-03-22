#!/usr/bin/env python


import logging
import os 
import shutil
import subprocess


logger = logging.getLogger('common')

class LambdaBuilder(object):
    def __init__(self, src, dest, lambda_runtime=None):
        self.src = src
        self.dest = dest
        self.runtime = self._get_type(lambda_runtime)

    def run(self):
        if 'python' in self.runtime: 
            if '2.7' in self.runtime:
                logger.info("Runtime detected: Python 2.7")
                self._python('2.7')
            elif '3.6' in self.runtime:
                logger.info("Runtime detected: Python 3.6")
                self._python('3.6')
        elif 'go' in self.runtime: 
            logger.info("Runtime detected: Go")
            self._go()
        elif 'node' in self.runtime: 
            logger.info("Runtime detected: Node")
            self._node()
        elif 'java' in self.runtime: 
            logger.info("Runtime detected: Java")
            self._java()
        elif 'c#' in self.runtime: 
            logger.info("Runtime detected: C#")
            self._dotnet()

    def _get_type(self, lambda_runtime):
        if not lambda_runtime:
            default = self._check_default()
            logger.debug("Default file check returned: {}".format(default))
            if not default:
                return False
            return default
        return lambda_runtime
        
    def _check_default(self):
        default_file = "{}/lambda_build".format(self.src)
        logger.debug("Starting to check the default file: {}".format(default_file))
        if os.path.exists(default_file):
            logger.debug("Default file exists: {}".format(default_file))
            with open(default_file,'r') as f:
                return f.readline()
        return None
            
    def _create_temp_dir(self):
        temp_dir = self.src + "_temp"
        copied = shutil.copytree(self.src,temp_dir)
        return temp_dir

    def _python(self,version='3.6'):
        temp_dir = self._create_temp_dir()
        req_file = '/'.join([self.src,'requirements.txt'])
        if os.path.exists(req_file):
            logger.debug('Requirements exists, installing')
            command = "pip-{} install -t {} -r {}".format(version,temp_dir,req_file)
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, env=os.environ)
            output, error = process.communicate()
        shutil.make_archive(self.src.split('/')[-1], 'zip', temp_dir)
        shutil.rmtree(temp_dir) 

    def _go(self):
        temp_dir = self._create_temp_dir()
        zip_temp = "/".join([temp_dir,"_zip_temp"])
        pkg_name = self.src.split('/')[-1]
        os.environ['GOOS'] = 'linux'
        os.environ['GOARCH'] = 'amd64'
        commands = ["go get", "go build -o {}".format(pkg_name)]
        for command in commands:
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, env=os.environ, cwd=temp_dir)
            output, error = process.communicate()
        os.makedirs(zip_temp)
        shutil.move("/".join([temp_dir,pkg_name]),"/".join([zip_temp,pkg_name]))
        shutil.make_archive(pkg_name, 'zip', zip_temp)
        shutil.rmtree(temp_dir) 
        
    def _dotnet(self):
        pass
    def _java(self):
        pass
    def _node(self):
        pass

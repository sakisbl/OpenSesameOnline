""" This handles uploaded OS-script files and
    translated JS files """
from django.contrib.auth.models import User
from django.conf import settings
from os_online.translator.translator import main as translate
import os, tarfile, shutil, glob

def make_random_path():
    """ this functions creates a random path for storing
        JS file """
    return "%s" % (User.objects.make_random_password(20))

def try_translation(infile, resultname):
    """ this function tries to translate an OS-script """
    translate(infile, resultname)
    os.remove(infile)

def handle_uploaded_file(u_file, dest):
    """ this function handles uploaded OS-script file """
    destfolder = _get_path([dest])
    destfile = _get_path([dest,dest])
    pool = _get_path([dest,'pool'])
    if not os.path.isdir(destfolder):
        os.mkdir(destfolder)
    with open(destfile, 'w+') as destination:
        for chunk in u_file.chunks():
            destination.write(chunk)
    if tarfile.is_tarfile(destfile):
        _check_tar(destfolder, destfile)
        tar = tarfile.open(destfile)
        tar.extractall(destfolder)
        tar.close()
        allfiles = os.listdir(destfolder)
        for filename in allfiles:
            if filename.endswith('.opensesame'):
                old_name = _get_path([dest,filename])
                new_name = destfile + '.opensesame'
                os.rename(old_name, new_name)
    else:
        os.rename(destfile, destfile + '.opensesame')

def _check_tar(target_dir, tar):
    tar = tarfile.open(tar)
    for t_file in tar.getmembers():
        name = t_file.name
        if not os.path.abspath(os.path.join(target_dir, name)).startswith(\
                target_dir):
            raise UnsafeTarFile
                    
def _get_path(path_list):
    path = os.path.join(settings.MEDIA_ROOT, reduce(os.path.join,path_list))
    return path

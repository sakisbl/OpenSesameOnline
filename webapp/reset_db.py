#! /usr/bin/env python
"""Module that runs pylint on all python scripts found in a directory tree.
"""

import os
import re
import sys
import pexpect
import time

if __name__ == "__main__":
    print 'Cleaning up the database and media files...'
    
    # Delete the old files
    pout = os.popen('rm -f os_online/database/db.sqlite3', 'r')
    pout = os.popen('rm -rf os_online/media/*', 'r')
    time.sleep(1)

    # Create the db again, and set up a superuser
    ps = pexpect.spawn('python manage.py syncdb')
    ps.expect(r"Would you like to create one now?.*")
    ps.sendline('yes')
    ps.expect(r"Username.*")
    ps.sendline('admin')
    ps.expect(r'Email address.*')
    ps.sendline('admin@admin.com')
    ps.expect(r'Password.*')
    ps.sendline('admin')
    ps.expect(r'Password.*')
    ps.sendline('admin')
    ps.terminate()

    # Add testtest user to the database
    ps = pexpect.spawn('python manage.py shell')
    ps.expect('>>>\s*')
    ps.sendline('from django.contrib.auth.models import User')
    ps.expect('>>>\s*')
    ps.sendline("user = User.objects.create_user('testtest', '', 'testtest')")
    ps.expect('>>>\s*')
    ps.sendline("user = User.objects.create_user('testtest2', '', 'testtest2')")
    ps.expect('>>>\s*')
    ps.sendline('exit()')
    ps.terminate()

    print 'Cleanup done. New database has login/password of admin/admin'
    print 'OS Experimenters are: testtest/testtest and testtest2/testtest2'

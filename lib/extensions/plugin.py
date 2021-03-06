# coding: utf-8
import sublime
import os
import re

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
    from JoomlaPack.lib.extensions.base import Base
    from JoomlaPack.lib.inflector import *
else:
    from lib import *
    from lib.extensions.base import Base
    from lib.inflector import *


class Plugin(Base):

    '''
    Implements the Joomla's Plugin extension.
    '''

    def __init__(self, content=None, inflector=English):
        Base.__init__(self, inflector)

        self.prefix = 'plg_'
        self.template_path = 'plugin'

        if content is not None:
            self.group, self.name = self.inflector.humanize(content,
                                                            prefix='plg_') \
                .split(' ')
            self.fullname = self.inflector.underscore(
                self.inflector.variablize(self.prefix +
                                          self.group + ' ' + self.name))
        else:
            self.fullname = self.inflector.underscore(
                Project().get_project_name())
            self.group, self.name = self.inflector.humanize(self.fullname,
                                                            prefix='plg_') \
                .split(' ')

    def rename(self):
        for root, dirs, files in os.walk(self.path):
            for filename in files:
                newname = re.sub('{{name}}', self.name,
                                 re.sub('{{group}}', self.group,
                                        re.sub('{{locale}}',
                                               Helper().language(), filename)))

                if newname != filename:
                    os.rename(os.path.join(root, filename),
                              os.path.join(root, newname))

        for root, dirs, files in os.walk(self.path):
            for folder in dirs:
                newname = folder.replace(
                    '{{locale}}', Helper().language())

                if newname != folder:
                    os.rename(os.path.join(root, folder),
                              os.path.join(root, newname))

    def __str__(self):
        return "JoomlaPack: Joomla Plugin"

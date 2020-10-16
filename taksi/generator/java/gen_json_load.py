# Copyright (C) 2018-present ichenq@outlook.com. All rights reserved.
# Distributed under the terms and conditions of the Apache License.
# See accompanying files LICENSE.

import os
import taksi.predef as predef
import taksi.strutil as strutil
import taksi.generator.genutil as genutil
import taksi.version as version
from taksi.generator.java.gen_struct import JavaStructGenerator


#
class JavaJsonLoadGenerator(JavaStructGenerator):
    TAB_SPACE = '    '

    def __init__(self):
        pass

    @staticmethod
    def name():
        return "java-json"

    def run(self, descriptors, params):
        basedir = params.get(predef.OptionOutSourceFile, '.')
        print(basedir)
        if 'pkg' in params:
            package = params['pkg']
            names = [basedir] + package.split('.')
            basedir = '/'.join(names)
            try:
                print('make dir', basedir)
                os.makedirs(basedir)
            except Exception as e:
                # print(e)
                pass

        for struct in descriptors:
            genutil.setup_comment(struct)
            genutil.setup_key_value_mode(struct)

        class_dict = {}

        for struct in descriptors:
            content = '// This file is auto-generated by TAKSi v%s, DO NOT EDIT!\n\n' % version.VER_STRING
            filename = '%s.java' % struct['camel_case_name']
            # print(filename)
            if 'pkg' in params:
                filename = '%s/%s' % (basedir, filename)
                content += 'package %s;\n\n' % params['pkg']
            content += 'import java.util.*;\n'
            content += '\n'
            content += self.gen_java_class(struct)
            content += '}\n\n'
            class_dict[filename] = content

        for filename in class_dict:
            content = class_dict[filename]
            filename = os.path.abspath(filename)
            strutil.save_content_if_not_same(filename, content, 'utf-8')
            print('wrote source file to', filename)

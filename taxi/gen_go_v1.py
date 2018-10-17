# Copyright (C) 2018-present ichenq@outlook.com. All rights reserved.
# Distributed under the terms and conditions of the Apache License.
# See accompanying files LICENSE.

import os
import codecs
import basegen
import descriptor
import predef
import util

# Go code generator
class GoV1Generator(basegen.CodeGeneratorBase):

    def __init__(self):
        pass

    @staticmethod
    def name():
        return "gov1"


    def get_const_key_name(self, name):
        return 'Key%sName' % name


    def gen_const_names(self, descriptors):
        content = 'const (\n'
        for struct in descriptors:
            content += '\t%s = "%s"\n' % (self.get_const_key_name(struct['name']), struct['name'].lower())
        content += ')\n\n'
        return content


    # 生成赋值方法
    def gen_field_assgin_stmt(self, name, typename, valuetext, tips):
        content = ''
        if typename == 'string':
            return '%s = %s\n' % (name, valuetext)
        content += 'var value = MustParseTextValue("%s", %s, %s)\n' % (typename, valuetext, tips)
        content += '%s = value.(%s)\n' % (name, typename)
        return content


    # 生成array赋值
    def gen_field_array_assign_stmt(self, prefix, typename, name, row_name, delimeters):
        if delimeters == '':
            delimeters = '|'

        content = ''
        elem_type = descriptor.array_element_type(typename)
        elem_type = map_go_type(elem_type)

        content += '  for _, item := range strings.Split(%s, "%s") {\n' % (row_name, delimeters)
        content += '    var value = MustParseTextValue("%s", item, %s)\n' % (elem_type, row_name)
        content += '    %s%s = append(p.%s, value.(%s))\n' % (prefix, name, name, elem_type)
        content += '  }\n'
        return content


    # 生成map赋值
    def gen_field_map_assign_stmt(self, prefix, typename, name, row_name, delimeters):
        delim1 = '|'
        delim2 = '='
        if delimeters != '':
            delist = [x.strip() for x in delimeters.split(',')]
            assert len(delist) == 2, delimeters
            delim1 = delist[0]
            delim2 = delist[1]

        k, v = descriptor.map_key_value_types(typename)
        key_type = map_go_type(k)
        val_type = map_go_type(v)

        content = ''
        content += '  %s%s = map[%s]%s{}\n' % (prefix, name, key_type, val_type)
        content += '  for _, text := range strings.Split(%s, "%s") {\n' % (row_name, delim1)
        content += '     if text == "" {\n\t\tcontinue\n}\n'
        content += '     var item = strings.Split(text, "%s")\n' % delim2
        content += '     var value = MustParseTextValue("%s", item[0], %s)\n' % (key_type, row_name)
        content += '     var key = value.(%s)\n' % key_type
        content += '     value = MustParseTextValue("%s", item[1], %s)\n' % (val_type, row_name)
        content += '     var val = value.(%s)\n' % val_type
        content += '     %s%s[key] = val\n' % (prefix, name)
        content += '\t}\n'
        return content


    #生成struct定义
    def gen_go_struct(self, struct):
        fields = struct['fields']
        if struct['options'][predef.PredefParseKVMode]:
            fields = self.get_struct_kv_fields(struct)

        vec_done = False
        vec_names, vec_name = self.get_field_range(struct)

        content = '// %s\n' % struct['comment']
        content += 'type %s struct\n{\n' % struct['camel_case_name']
        for field in fields:
            typename = map_go_type(field['original_type_name'])
            assert typename != "", field['original_type_name']

            if field['name'] not in vec_names:
                content += '    %s %s // %s\n' % (field['camel_case_name'], typename, field['comment'])
            elif not vec_done:
                vec_done = True
                content += '    %s [%d]%s // %s\n' % (vec_name, len(vec_names), typename, field['comment'])

        return content


    # KV模式的ParseFromRow方法
    def gen_kv_parse_method(self, struct):
        content = ''
        rows = struct['data-rows']
        keycol = struct['options'][predef.PredefKeyColumn]
        valcol = struct['options'][predef.PredefValueColumn]
        typcol = int(struct['options'][predef.PredefValueTypeColumn])
        assert keycol > 0 and valcol > 0 and typcol > 0

        keyidx, keyfield = self.get_field_by_column_index(struct, keycol)
        validx, valfield = self.get_field_by_column_index(struct, valcol)
        typeidx, typefield = self.get_field_by_column_index(struct, typcol)

        delimeters = ''
        if predef.OptionDelimeters in struct['options']:
            delimeters = struct['options'][predef.OptionDelimeters]

        content += 'func (p *%s) ParseFromRows(rows [][]string) error {\n' % struct['camel_case_name']
        content += '\tif len(rows) < %d {\n' % len(rows)
        content += '\t\tlog.Panicf("%s:row length out of index, %%d < %d", len(rows))\n' % (struct['name'], len(rows))
        content += '\t}\n'

        idx = 0
        for row in rows:
            content += '\tif rows[%d][%d] != "" {\n' % (idx, validx)
            name = rows[idx][keyidx].strip()
            name = util.camel_case(name)
            origin_typename = rows[idx][typeidx].strip()
            typename = map_go_type(origin_typename)
            valuetext = 'rows[%d][%d]' % (idx, validx)
            # print('kv', name, origin_typename, valuetext)
            if origin_typename.startswith('array'):
                content += self.gen_field_array_assign_stmt('p.', origin_typename, name, valuetext, delimeters)
            elif origin_typename.startswith('map'):
                content += self.gen_field_map_assign_stmt('p.', origin_typename, name, valuetext, delimeters)
            else:
                content += 'var value = MustParseTextValue("%s", %s, rows[%d])\n' % (typename, valuetext, idx)
                content += 'p.%s = value.(%s)\n' % (name, typename)
            content += '}\n'
            idx += 1
        content += '    return nil\n'
        content += '}\n\n'
        return content


    #生成ParseFromRow方法
    def gen_parse_method(self, struct):
        if struct['options'][predef.PredefParseKVMode]:
            return self.gen_kv_parse_method(struct)

        delimeters = ''
        if predef.DefaultDelim1 in struct['options']:
            delimeters = struct['options'][predef.DefaultDelim1]

        vec_idx = 0
        vec_names, vec_name = self.get_field_range(struct)

        content = ''
        content += 'func (p *%s) ParseFromRow(row []string) error {\n' % struct['camel_case_name']
        content += '\tif len(row) < %d {\n' % len(struct['fields'])
        content += '\t\tlog.Panicf("%s: row length out of index %%d", len(row))\n' % struct['name']
        content += '\t}\n'

        idx = 0
        for field in struct['fields']:
            content += '\tif row[%d] != "" {\n' % idx
            origin_type_name = field['original_type_name']
            typename = map_go_type(origin_type_name)
            field_name = field['camel_case_name']
            valuetext = 'row[%d]' % idx
            if origin_type_name.startswith('array'):
                content += self.gen_field_array_assign_stmt('p.', field['original_type_name'], field['name'], valuetext, delimeters)
            elif origin_type_name.startswith('map'):
                content += self.gen_field_map_assign_stmt('p.', field['original_type_name'], field['name'], valuetext, delimeters)
            else:
                if field_name in vec_names:
                    name = '%s[%d]' % (vec_name, vec_idx)
                    content += self.gen_field_assgin_stmt('p.'+name, typename, valuetext, 'row')
                    vec_idx += 1
                else:
                    content += self.gen_field_assgin_stmt('p.'+field_name, typename, valuetext, 'row')
            content += '}\n'
            idx += 1
        content += 'return nil\n'
        content += '}\n\n'
        return content


    # KV模式下的Load方法
    def gen_load_method_kv(self, struct):
        content = ''
        content += 'func Load%s(loader DataSourceLoader) (*%s, error) {\n' % (struct['name'], struct['name'])
        content += '\tbuf, err := loader.LoadDataByKey(%s)\n' % self.get_const_key_name(struct['name'])
        content += '\tif err != nil {\n'
        content += '\treturn nil, err\n'
        content += '\t}\n'
        content += '\tr := csv.NewReader(buf)\n'
        content += '\trows, err := r.ReadAll()\n'
        content += '\tif err != nil {\n'
        content += '\t    log.Errorf("%s: csv read all, %%v", err)\n' % struct['name']
        content += '\t    return nil, err\n'
        content += '\t}\n'
        content += '\tvar item %s\n' % struct['name']
        content += '\tif err := item.ParseFromRows(rows); err != nil {\n'
        content += '\t    log.Errorf("%s: parse row %%d, %%v", len(rows), err)\n' % struct['name']
        content += '\t    return nil, err\n'
        content += '\t}\n'
        content += 'return &item, nil\n'
        content += '}\n\n'
        return content


    # 生成Load方法
    def gen_load_method(self, struct):
        content = ''
        if struct['options']['parse-kv-mode']:
            return self.gen_load_method_kv(struct)

        content += 'func Load%sList(loader DataSourceLoader) ([]*%s, error) {\n' % (struct['name'], struct['name'])
        content += '\tbuf, err := loader.LoadDataByKey(%s)\n' % self.get_const_key_name(struct['name'])
        content += '\tif err != nil {\n'
        content += '\t    return nil, err\n'
        content += '\t}\n'
        content += '\tvar list []*%s\n' % struct['name']
        content += '\tvar r = csv.NewReader(buf)\n'
        content += '\tfor i := 0; ; i++ {\n'
        content += '\t row, err := r.Read()\n'
        content += '    if err == io.EOF {\n'
        content += '        break\n'
        content += '    }\n'
        content += '    if err != nil {\n'
        content += '        log.Errorf("%s: read csv %%v", err)\n' % struct['name']
        content += '        return nil, err\n'
        content += '    }\n'
        content += '    var item %s\n' % struct['name']
        content += '    if err := item.ParseFromRow(row); err != nil {\n'
        content += '\t     log.Errorf("%s: parse row %%d, %%s, %%v", i+1, row, err)\n' % struct['name']
        content += '    return nil, err\n'
        content += '}\n'
        content += '\tlist = append(list, &item)\n'
        content += '}\n'
        content += 'return list, nil\n'
        content += '}\n\n'
        return content


    def generate(self, struct):
        content = ''
        content += self.gen_go_struct(struct)
        content += '}\n\n'
        content += self.gen_parse_method(struct)
        content += self.gen_load_method(struct)
        return content


    def run(self, descriptors, args):
        params = util.parse_args(args)
        content = '// This file is auto-generated by taxi v%s, DO NOT EDIT!\n\n' % util.version_string
        content += 'package %s\n' % params['pkg']
        content += 'import (\n'
        content += '"encoding/csv"\n'
        content += '"io"\n'
        content += ')\n'
        content += self.gen_const_names(descriptors)

        data_only = params.get(predef.OptionDataOnly, False)
        no_data = params.get(predef.OptionNoData, False)

        for struct in descriptors:
            self.setup_comment(struct)
            self.setup_key_value_mode(struct)
            if not no_data:
                self.write_data_rows(struct, params)
            if not data_only:
                content += self.generate(struct)

        if data_only:
            return

        outdir = params.get(predef.OptionOutDataDir, '.')
        filename = outdir + '/stub.go'
        f = codecs.open(filename, 'w', 'utf-8')
        f.writelines(content)
        f.close()
        print('wrote to %s' % filename)

        gopath = os.getenv('GOPATH')
        if gopath is not None:
            cmd = gopath + '/bin/goimports -w ' + filename
            print(cmd)
            os.system(cmd)


def map_go_type(typ):
    type_mapping = {
        'bool':     'bool',
        'int8':     'int8',
        'uint8':    'uint8',
        'int16':    'int16',
        'uint16':   'uint16',
        'int':      'int',
        'int32':    'int32',
        'uint32':   'uint32',
        'int64':    'int64',
        'uint64':   'uint64',
        'float':    'float32',
        'float32':  'float32',
        'float64':  'float64',
        'enum':     'int',
        'string':   'string',
    }
    abs_type = descriptor.is_abstract_type(typ)
    if abs_type is None:
        return type_mapping[typ]

    if abs_type == 'array':
        t = descriptor.array_element_type(typ)
        elem_type = type_mapping[t]
        return '[]%s' % elem_type
    elif abs_type == 'map':
        k, v = descriptor.map_key_value_types(typ)
        key_type = type_mapping[k]
        value_type = type_mapping[v]
        return 'map[%s]%s' % (key_type, value_type)
    assert False, typ

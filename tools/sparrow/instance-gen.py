#!/usr/bin/python
#
# Copyright (c) 2016, SICS, Swedish ICT
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Institute nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# Author: Joakim Eriksson, joakime@sics.se
#         Niclas Finne, nfi@sics.se
#
# Sparrow Instance Code Generator for instance variables
#
# This tool requires PyYAML.
#
# Python:
#   pip install pyyaml
# Linux:
#   sudo apt-get install python-yaml
# OSX Port:
#   sudo port install libyaml
#   sudo pip install pyyaml
# OSX Homebrew:
#   brew install libyaml
#   sudo python -m easly_install pyyaml
#

import yaml, sys, os.path, time

#
# Some globals for Code generation
#
opstr = {}
opstr['r'] = 'SPARROW_OAM_WRITABILITY_RO'
opstr['w'] = 'SPARROW_OAM_WRITABILITY_WO'
opstr['rw'] = 'SPARROW_OAM_WRITABILITY_RW'

formstr = {}
formstr['int'] = 'SPARROW_OAM_FORMAT_INTEGER'
formstr['array'] = 'SPARROW_OAM_FORMAT_ARRAY'
formstr['string'] = 'SPARROW_OAM_FORMAT_STRING'
formstr['enum'] = 'SPARROW_OAM_FORMAT_ENUM'
formstr['blob'] = 'SPARROW_OAM_FORMAT_BLOB'
formstr['time'] = 'SPARROW_OAM_FORMAT_TIME'

flags = {}
flags['no-check'] = 'SPARROW_OAM_VECTOR_DEPTH_DONT_CHECK'

def get_flags(var):
    if 'flag' in var:
        return flags[var['flag']]
    return '0'

def get_varname(varname):
    return "VARIABLE_" + varname.upper().replace(' ', '_')

def usage():
    print "Usage: instance-gen.py <instance-file>"
    exit()

if len(sys.argv) != 2 or sys.argv[1] == "-h":
    usage()

if not os.path.isfile(sys.argv[1]):
    print "Can not read this file:",sys.argv[1]
    usage()

with open(sys.argv[1], 'r') as yaml_file:
    instance = yaml.load(yaml_file)

vars = instance['variables']
iname = str(instance['name']).replace(' ', '_')
uname = iname.upper()
dname = "INSTANCE_" + uname + "_VAR_H_"
print """
/*--------------------------------------------------------------------*/
/* Sparrow OAM Instance - DO NOT EDIT - automatically generated file. */
/* Generated by instance-gen.py on """ + time.strftime("%Y-%m-%d %H:%M:%S") + """.               */
/*--------------------------------------------------------------------*/

/*
 * Copyright (c) 2016, SICS, Swedish ICT.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *   1. Redistributions of source code must retain the above copyright
 *      notice, this list of conditions and the following disclaimer.
 *   2. Redistributions in binary form must reproduce the above copyright
 *      notice, this list of conditions and the following disclaimer in the
 *      documentation and/or other materials provided with the distribution.
 *   3. Neither the name of the copyright holders nor the
 *      names of its contributors may be used to endorse or promote products
 *      derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
 * USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 */

/*--------------------------------------------------------------------*/
/* Sparrow OAM Instance - DO NOT EDIT - automatically generated file. */
/*--------------------------------------------------------------------*/

"""
print "#ifndef " + dname
print "#define " + dname
print
print "#include \"sparrow-oam.h\""
print
print "#define INSTANCE_" + uname + "_OBJECT_TYPE      0x%016XULL"%instance['id']
print "#define INSTANCE_" + uname + '_LABEL            "' + instance['label'] + '"'
print

if 'def-enum' in instance:
    print "/* Enum types for instance", instance['name'], "*/"
    print
    for enums in instance['def-enum']:
        ename = enums['name'].replace(' ', '_')
        tname = ename.upper()
        print "typedef enum {"
        enumlist = sorted(enums['values'].items(), key=lambda x:x[1])
        for enum in enumlist:
            print '  %-*s %s'%(37,tname + "_" + enum[0].upper()," = "+str(enum[1])) + ","
        print "} " + ename + "_t;"
        print

print "/* Variables for instance", instance['name'], "*/"
for var in vars:
    print '#define %-*s %s' % (32, get_varname(var['name']),hex(var['id']))
print
print "static const sparrow_oam_variable_t instance_" + iname + "_variables[] = {"
for var in vars:
    print '{ 0x%03x, %2d, %s, %-28s %s },'%(var['id'],var['size'],opstr[var['op']], formstr[var['type']] + ",",get_flags(var))
print "};"
print
print "#endif /* " + dname + " */"

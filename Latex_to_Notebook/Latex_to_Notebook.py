#!/usr/bin/env python3

from subprocess import check_output as bash

import sys
import re
import numpy as np




# Obtenemos el nombre del archivo del primer algumento de la llamada
file_name = sys.argv[1:][0]
print("===========================")
print("Input File  = ", file_name)

out_file = file_name[:-4]+'.ipynb'



with open(file_name, 'r') as f:
    
    f_data = []
    i = 0
    i_part            = []
    i_chapter         = []
    i_section         = []

    for line in f:
        line = line.lstrip()
        
        f_data.append(line)

        if line != "" and line[0] != "%":
        
            if "\\section{" in line or "\\section*{" in line:
                i_section.append(i)
            
            elif "\\chapter{" in line or "\\chapter*{" in line:
                i_chapter.append(i)

            elif "\\part{" in line or "\\part*{" in line:
                i_part.append(i)
            
            elif "\\begin{document}" in line:
                i_begin_doc = i

            elif "\\end{document}" in line:
                i_end_doc = i

            elif "% == Bibliograf" in line: 
                i_bib = i
        i +=1 
'''
k_sec  = 0
k_part = 0

for k_chap in range(len(i_chapter)):
    if k_part < len(i_part):
        if i_chapter[k_chap] < i_part[k_part]:
            print(i_chapter[k_chap], {f_data[i_chapter[k_chap]]})
            while i_section[k_sec] < i_chapter[k_chap +1]:
                print(i_section[k_sec], {f_data[i_section[k_sec]]})
                k_sec +=1

        else:
            print(i_part[k_part], {f_data[i_part[k_part]]}) 
            k_part +=1
            print(i_chapter[k_chap], {f_data[i_chapter[k_chap]]})
            while i_section[k_sec] < i_chapter[k_chap +1]:
                print(i_section[k_sec], {f_data[i_section[k_sec]]})
                k_sec +=1
    else:
        print(i_chapter[k_chap], {f_data[i_chapter[k_chap]]})
        if k_chap < len(i_chapter) - 1 :
            while i_section[k_sec] < i_chapter[k_chap +1]:
                print(i_section[k_sec], {f_data[i_section[k_sec]]})
                k_sec +=1
        else:
            while i_section[k_sec] < i_section[len(i_section)-1]:
                print(i_section[k_sec], {f_data[i_section[k_sec]]})
                k_sec +=1
            print(i_section[k_sec], {f_data[i_section[k_sec]]})


k_sec  = 0
k_part = 0

i_chap_in_parts   = []
i_sec_in_chap = []

i_chap_in_parts_aux   = []

def make_i_sec_in_chap_aux(i_section, i_chapter, k_sec, k_chap):
    i_sec_in_chap_aux = []
    while i_section[k_sec] < i_chapter[k_chap +1]:
        i_sec_in_chap_aux.append(k_sec)
        k_sec +=1
    return i_sec_in_chap_aux, k_sec


for k_chap in range(len(i_chapter)):
    if k_part < len(i_part):
        if i_chapter[k_chap] < i_part[k_part]:
            i_chap_in_parts_aux.append(k_chap)

            i_sec_in_chap_aux, k_sec = make_i_sec_in_chap_aux(i_section, i_chapter, k_sec, k_chap)
            i_sec_in_chap.append(i_sec_in_chap_aux)
            

        else:
            i_chap_in_parts.append(i_chap_in_parts_aux)
            i_chap_in_parts_aux   = [] 

            k_part +=1
            i_chap_in_parts_aux.append(k_chap)

            i_sec_in_chap_aux, k_sec = make_i_sec_in_chap_aux(i_section, i_chapter, k_sec, k_chap)
            i_sec_in_chap.append(i_sec_in_chap_aux)
    else:
        i_chap_in_parts_aux.append(k_chap)

        if k_chap < len(i_chapter) - 1 :
            i_sec_in_chap_aux, k_sec = make_i_sec_in_chap_aux(i_section, i_chapter, k_sec, k_chap)
            i_sec_in_chap.append(i_sec_in_chap_aux)
        else:
            i_sec_in_chap_aux, k_sec = make_i_sec_in_chap_aux(i_section, i_section, k_sec, len(i_section)-2)
            i_sec_in_chap_aux.append(k_sec)
            i_sec_in_chap.append(i_sec_in_chap_aux)
            i_chap_in_parts.append(i_chap_in_parts_aux)

for i in i_chap_in_parts:
    print(i)

for i in i_sec_in_chap:
    print(i)
print("")

i_part, i_section


i_chap_in_parts = []
aux = []

if i_part[0] > i_chapter[0]:
    chapters_before_part_1 = True

if chapters_before_part_1 == True:
    k_chap = 0
    while i_chapter[k_chap] < i_part[0]:
        aux.append(k_chap)
        k_chap +=1
    i_chap_in_parts.append(aux)
    aux = []
else:
    k_chap = 0

for k_part in range(len(i_part) - 1):
    while i_chapter[k_chap] < i_part[k_part +1 ]:
        aux.append(k_chap)
        k_chap +=1
    i_chap_in_parts.append(aux)
    aux = []

while i_chapter[k_chap] < i_chapter[len(i_chapter) -1]:
    aux.append(k_chap)
    k_chap +=1
aux.append(k_chap)
i_chap_in_parts.append(aux)
'''

def build_i_a_in_b(i_a, i_b):

    i_a_in_b = []
    aux = []

    if i_b[0] > i_a[0]:
        a_before_firt_b = True
    else:
        a_before_firt_b = False

    if a_before_firt_b == True:
        k_a = 0
        while i_a[k_a] < i_b[0]:
            aux.append(k_a)
            k_a +=1
        i_a_in_b.append(aux)
        aux = []
    else:
        k_a = 0

    for k_b in range(len(i_b) - 1):
        while i_a[k_a] < i_b[k_b +1 ]:
            aux.append(k_a)
            k_a +=1
        i_a_in_b.append(aux)
        aux = []

    while i_a[k_a] < i_a[len(i_a) -1]:
        aux.append(k_a)
        k_a +=1
    aux.append(k_a)
    i_a_in_b.append(aux)

    return i_a_in_b

i_chap_in_parts = build_i_a_in_b(i_chapter, i_part)
i_sec_in_chap = build_i_a_in_b(i_section, i_chapter)

for i in i_chap_in_parts:
    print(i)

for i in i_sec_in_chap:
    print(i)

exit()
with open(out_file, 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])

    
print("Output file = ", out_file)
print("===========================")
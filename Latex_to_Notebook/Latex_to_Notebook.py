#!/usr/bin/env python3

from subprocess import check_output as bash

import sys
import re
import numpy as np
import os
from shutil import rmtree

Notebook_folder_path = "../Notebooks"
Notebook_old_folder_path = "../Notebooks_old"
Plantilla_section_path = "Plantilla_seccion.ipynb"


if os.path.exists(Notebook_folder_path):
    if os.path.exists(Notebook_old_folder_path):
        rmtree(Notebook_old_folder_path)
    os.rename(Notebook_folder_path,Notebook_old_folder_path)

os.mkdir(Notebook_folder_path)



# Obtenemos el nombre del archivo del primer algumento de la llamada
file_name = sys.argv[1:][0]
print("===========================")
print("Input File  = ", file_name)

out_file = file_name[:-4]+'.ipynb'


with open(Plantilla_section_path, 'r') as f:
    header_plantilla = []
    tail_plantilla = []

    tail = False
    count_source = 0
    for line in f:
        if tail == False:
            if '\"source\"' in line:
                count_source +=1
                if count_source > 1:
                    tail = True
                    continue
            header_plantilla.append(line)
        
        else:
            tail_plantilla.append(line)        

            print(line)


with open(file_name, 'r') as f:
    
    f_data = []
    i = 0
    i_part            = []
    i_chapter         = []
    i_section         = []

    last_line = None
    for line in f:
        line = line.lstrip()
        
        if line == "":
            line = "\n"
        
        if line == "\n" and last_line == "\n":
            pass
        else:
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
        last_line = line

def build_i_a_in_b(i_a, i_b):

    i_a_in_b = []
    aux = []

    if i_b[0] > i_a[0]:
        a_before_first_b = True
    else:
        a_before_first_b = False

    if a_before_first_b == True:
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

    return i_a_in_b, a_before_first_b

i_chap_in_parts, chapters_before_first_part = build_i_a_in_b(i_chapter, i_part)
i_sec_in_chap, _ = build_i_a_in_b(i_section, i_chapter)

print("")


chapters_before_first_part_aux = chapters_before_first_part
k_part = 0
k_part_sum = 0
k_chap_sum = 0
for k_chap_in_one_part in i_chap_in_parts:
    if chapters_before_first_part_aux == False:
        print(f"Part_"+str(k_part_sum+1).zfill(2), {f_data[i_part[k_part]]})
        part_folder_path = str(Notebook_folder_path) + "/" + f"Part_"+str(k_part_sum+1).zfill(2)
        os.mkdir(part_folder_path)
        k_part +=1
        k_part_sum +=1
    else:
        print(f"Part_"+str(k_part_sum+1).zfill(2))
        part_folder_path = str(Notebook_folder_path) + "/" + f"Part_"+str(k_part_sum+1).zfill(2)
        os.mkdir(part_folder_path)
        k_part_sum +=1

    for k_chap in k_chap_in_one_part:
        print("  ",f"Chapter_"+str(k_chap_sum +1).zfill(3), {f_data[i_chapter[k_chap]]})
        k_sec_sum = 0
        chapter_folder_path = part_folder_path + "/Chapter_"+str(k_chap_sum +1).zfill(3)
        if len(i_sec_in_chap[k_chap]) >= 1:
            os.mkdir(chapter_folder_path)
        for k_sec in i_sec_in_chap[k_chap]:
            print("    ", f"Section_"+ str(k_sec_sum+1).zfill(3) ,i_section[k_sec], {f_data[i_section[k_sec]]})
            sec_file_path = str(chapter_folder_path) + "/" + f"Section_"+ str(k_sec_sum+1).zfill(3) + ".ipynb"
            if k_sec_sum < len(i_sec_in_chap[k_chap]) -1 :
                with open(sec_file_path, 'w') as f_out:
                    for line in header_plantilla:
                        f_out.write(line)

                    f_out.write('   \"source\": [\n')
                    for k in range(i_section[k_sec], i_section[k_sec + 1] - 1):
                        f_out.write('    \"' +f_data[k][:-1].replace("\\","\\\\") + '\\n",\n')
                    f_out.write('    \"' +f_data[k+1][:-1].replace("\\","\\\\") + '\\n\"\n')
                    f_out.write('   ]\n')

                    for line in tail_plantilla:
                        f_out.write(line)
                pass
            
            k_sec_sum += 1
        
        k_chap_sum +=1
    chapters_before_first_part_aux = False

for i in range(7642, 7642+10):
    print({f_data[i]})

exit()
with open(out_file, 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])

    
print("Output file = ", out_file)
print("===========================")
#!/usr/bin/env python3

from subprocess import check_output as bash

import sys
import re
import numpy as np
import os
import shutil 

Notebook_folder_path = "../Notebooks"
Notebook_old_folder_path = "../Notebooks_old"
Plantilla_section_path = "Plantilla_seccion.ipynb"
Name_Figuras_folder = "Figuras"


if os.path.exists(Notebook_folder_path):
    if os.path.exists(Notebook_old_folder_path):
        shutil.rmtree(Notebook_old_folder_path)
    os.rename(Notebook_folder_path,Notebook_old_folder_path)

os.mkdir(Notebook_folder_path)
shutil.copytree(Name_Figuras_folder,Notebook_folder_path +"/"+ Name_Figuras_folder)



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

# =============================================================================
## Las dos siguientes funciones son para reemplazar las \label por <a id='..
def reemplazo_label_aux(match):
    titulo = match.group(1)
    return f"<a id='{titulo}'></a>"

def reemplazo_label(line):
    patron_lab = r"\\\\label\{(.+?)\}"
    return re.sub(patron_lab, reemplazo_label_aux, line)


# =============================================================================
## Las dos siguientes funciones son para reemplazar \section por #
## Se reemplazan también la label 
def reemplazo_sec(line, nonumber):
    
    def reemplazo_sec_aux(match):
        titulo = match.group(1)
        return f"# {titulo}"
    
    if nonumber == True:
        #patron_sec = r"\\\\section\*\{(.+?)\}"
        patron_sec = r"\\\\section\*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    else:
        #patron_sec = r"\\\\section\{(.+?)\}"
        patron_sec = r"\\\\section\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return reemplazo_label(re.sub(patron_sec, reemplazo_sec_aux, line))

# =============================================================================
## Las dos siguientes funciones son para reemplazar \subsection por ##
## Se reemplazan también la label 
def reemplazo_subsec(line, nonumber):

    def reemplazo_subsec_aux(match):
        titulo = match.group(1)
        return f"## {titulo}"
    
    if nonumber == True:
        #patron_subsec = r"\\\\subsection\*\{(.+?)\}"
        patron_subsec = r"\\\\subsection\*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    else:
        #patron_subsec = r"\\\\subsection\{(.+?)\}"
        #patron_subsec = r"\\\\subsection\{([^{}]+)\}"
        patron_subsec = r"\\\\subsection\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return reemplazo_label(re.sub(patron_subsec, reemplazo_subsec_aux, line))


# =============================================================================
## Las dos siguientes funciones son para reemplazar \SubsubiIt por ###
## Se reemplazan también la label 
def reemplazo_SubsubIt(line):

    def reemplazo_SubsubIt_aux(match):
        titulo = match.group(1)
        return f"### {titulo}"

    #patron_SubsubIt = r"\\\\SubsubiIt\{(.+?)\}"
    patron_SubsubIt = r"\\\\SubsubiIt\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return reemplazo_label(re.sub(patron_SubsubIt, reemplazo_SubsubIt_aux, line))

# =============================================================================
## Las dos siguientes funciones son para reemplazar \caption por <center> <center>
def reemplazo_caption(line):

    def reemplazo_caption_aux(match):
        titulo = match.group(1)
        return f"<center>{titulo}</center>"

    patron_caption = r"\\\\caption\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return reemplazo_label(re.sub(patron_caption, reemplazo_caption_aux, line))


# =============================================================================
## Funcion para sustituir la llamada a la figura
def reemplazo_includegraphics(line):
    patron_includegraphics = r"\\\\includegraphics\[width=(\d+(\.\d+)?)\\\\linewidth\]\{([^}]+)\}"
    print(line)
    # Definir la función de reemplazo
    def reemplazo_includegraphics_aux(match):
        width = float(match.group(1))
        nombre_archivo = match.group(3)
        nueva_width = int(width * 1000)
        return f"<img src=\\\"{nombre_archivo}\\\" alt=\\\"\\\" align=center width='{nueva_width}px'/>"

    # Realizar el reemplazo
    return re.sub(patron_includegraphics, reemplazo_includegraphics_aux, line)


# =============================================================================
i_begin_doc = 0
i_end_doc = 0
find_mybox_gray2 = False
find_proof = False
find_mybox_blue = False
find_itemize = False
find_itemize_2 = False
find_figure = False

with open(file_name, 'r') as f:
    
    f_data = []
    i = 0
    i_part            = []
    i_chapter         = []
    i_section         = []

    last_line = None
    for line in f:
        # Eliminamos los espacios en blanco a izquierda y derecha
        # Sustituimos "\" por "\\"
        line = line.lstrip().rstrip().replace("\\","\\\\").replace("``","\\\"").replace("''","\\\"")

        # Eliminamos los tabuladores \t, teniendo cuidado de no eliminar los \\t
        line = re.sub(r'(?<!\\)\t','',line)

        if line == "":
            line = "\\n"
        
        if line == "\\n":
            if last_line == "\\n":
                pass
            elif find_mybox_gray2 == True or find_mybox_blue == True or \
                find_proof == True or find_itemize == True or find_figure == True:

                line = "<br>"
                f_data.append(line)
                i +=1 
                last_line = line
            else:
                f_data.append(line)
                i +=1 
                last_line = line
        else:
            
            if line[0] != "%":

                if "\\section{" in line:
                    i_section.append(i)
                    line = reemplazo_sec(line, nonumber = False)

                elif "\\section*{" in line:
                    i_section.append(i)
                    line = reemplazo_sec(line, nonumber = True)
                
                elif "\\subsection{" in line:
                    line = reemplazo_subsec(line, nonumber = False)
                
                elif "\\subsection*{" in line:
                    line = reemplazo_sec(line, nonumber = True)
                
                elif "\\chapter{" in line or "\\chapter*{" in line:
                    i_chapter.append(i)

                elif "\\part{" in line or "\\part*{" in line:
                    i_part.append(i)

                elif "\\SubsubiIt{" in line:
                    line = reemplazo_SubsubIt(line)
                
                elif "\\begin{document}" in line:
                    i_begin_doc = i
                    print(line)

                elif "\\end{document}" in line:
                    i_end_doc = i

                elif "\\begin{mybox_gray2}" in line and i_begin_doc > 0:
                    find_mybox_gray2 = True
                    line = '<div class=\\"alert alert-block alert-info\\">\\n",\n' + \
                            '    "<p style=\\"color: navy;\\">'
                    
                elif "\\end{mybox_gray2}" in line and i_begin_doc > 0:
                    find_mybox_gray2 = False
                    line = '</p></div>'

                elif "\\begin{mybox_blue}" in line and i_begin_doc > 0:
                    find_mybox_blue = True
                    line = '<div class=\\"alert alert-block alert-danger\\">\\n",\n' + \
                            '    "<p style=\\"color: DarkRed;\\">\\n",\n' + \
                            '    "<b>Nota</b>:\\n",\n' + \
                            '    "<br>'
                    
                elif "\\end{mybox_blue}" in line and i_begin_doc > 0:
                    find_mybox_blue = False
                    line = '</p></div>'

                elif "\\begin{itemize}" in line and i_begin_doc > 0:
                    if find_itemize == True:
                        find_itemize_2 = True
                    else:
                        find_itemize = True
                    line = '\\n'
                    
                elif "\\end{itemize}" in line and i_begin_doc > 0:
                    if find_itemize_2 == True:
                        find_itemize_2 = False
                    else:
                        find_itemize = False
                    line = '\\n'
                
                ########################## Figuras #############################
                elif "\\begin{figure}" in line and i_begin_doc > 0:
                    find_figure = True
                    line = '<figure><center>'

                elif "\\end{figure}" in line and i_begin_doc > 0:
                    find_figure = False
                    line = '</center></figure>\\n'
                
                elif "\\centering" in line and find_figure == True:
                    line = '<br>'
                
                elif "\\caption{" in line and find_figure == True:
                    line = reemplazo_caption(line)

                elif "\\includegraphics[" in line and find_figure == True and not "\\subfigure" in line:
                    line = reemplazo_includegraphics(line)
                    print(line)
                
                elif "\\label{" in line and find_figure == True:
                    line = reemplazo_label(line)

                ########################## Itemice #############################
                elif find_itemize == True and "\\\\item " in line:
                    if find_itemize_2 == True:
                        line = line.replace('\\\\item', '    -')
                    else:
                        line = line.replace('\\\\item', '-')

                elif "\\begin{proof}" in line and i_begin_doc > 0:
                    find_proof = True
                    line = '<details><summary><p style=\\"color:blue\\" > >> <i>Demostración</i> </p></summary>'
                    
                elif "\\end{proof}" in line and i_begin_doc > 0:
                    find_proof = False
                    line = '</details>'



                f_data.append(line)
                i +=1 
                last_line = line

            if "% == Bibliograf" in line: 
                i_bib = i
                f_data.append(line)
                
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

def write_notebook(f_data, i_start_write, i_end_write, sec_file_path, header_plantilla, tail_plantilla):

    with open(sec_file_path, 'w') as f_out:
        for line in header_plantilla:
            f_out.write(line)

        f_out.write('   \"source\": [\n')
        for k in range(i_start_write, i_end_write - 1):
            if f_data[k] == '\\n':
                f_out.write('   ]\n')
                f_out.write('  },\n')
                f_out.write('  {\n')
                f_out.write('   "cell_type": "markdown",\n')
                f_out.write('   "id": "080fe82e",\n')
                f_out.write('   "metadata": {},\n')
                f_out.write('   "source": [\n')
            #print({'    \"' +f_data[k].replace("\\","\\\\") + '\\n",\n'})
            elif f_data[k+1] == '\\n':
                f_out.write('    \"' +f_data[k]+ '\\n"\n')
            else:
                f_out.write('    \"' +f_data[k]+ '\\n",\n')
        if f_data[k+1] != '\\n':
            f_out.write('    \"' +f_data[k+1]+ '\\n\"\n')
        f_out.write('   ]\n')

        for line in tail_plantilla:
            f_out.write(line)




chapters_before_first_part_aux = chapters_before_first_part
k_part = 0
k_part_sum = 0
k_chap_sum = 0
for k_chap_in_one_part in i_chap_in_parts:
    if chapters_before_first_part_aux == False:
        print(f"Part_"+str(k_part_sum+1).zfill(2), {f_data[i_part[k_part]]})
        part_folder_path = str(Notebook_folder_path) + "/" + f"Part_"+str(k_part_sum+1).zfill(2)
        os.mkdir(part_folder_path)
        shutil.copytree(Name_Figuras_folder, part_folder_path + "/" + Name_Figuras_folder)
        k_part +=1
        k_part_sum +=1
    else:
        print(f"Part_"+str(k_part_sum+1).zfill(2))
        part_folder_path = str(Notebook_folder_path) + "/" + f"Part_"+str(k_part_sum+1).zfill(2)
        os.mkdir(part_folder_path)
        shutil.copytree(Name_Figuras_folder, part_folder_path + "/" + Name_Figuras_folder)
        k_part_sum +=1

    k_chap_sum_part = 0
    for k_chap in k_chap_in_one_part:
        print("  ",f"Chapter_"+str(k_chap_sum +1).zfill(3), {f_data[i_chapter[k_chap]]})
        k_sec_sum = 0
        chapter_folder_path = part_folder_path + "/Chapter_"+str(k_chap_sum +1).zfill(3)

        '''
        NOTA (to do): Crear Jupyter con la intro de lo capitulos
        '''

        if len(i_sec_in_chap[k_chap]) >= 1:
            os.mkdir(chapter_folder_path)
            shutil.copytree(Name_Figuras_folder, chapter_folder_path + "/" + Name_Figuras_folder)
        for k_sec in i_sec_in_chap[k_chap]:
            print("    ", f"Section_"+ str(k_sec_sum+1).zfill(3) ,i_section[k_sec], {f_data[i_section[k_sec]]})
            sec_file_path = str(chapter_folder_path) + "/" + f"Section_"+ str(k_sec_sum+1).zfill(3) + ".ipynb"
            i_start_write = i_section[k_sec]

            if k_sec_sum < len(i_sec_in_chap[k_chap]) -1 :
                i_end_write   = i_section[k_sec + 1]

                write_notebook(f_data, i_start_write, i_end_write, sec_file_path, header_plantilla, tail_plantilla)
               
            else:
                if k_chap_sum_part < len(k_chap_in_one_part) - 1:
                    i_end_write   = i_chapter[k_chap + 1]
                    write_notebook(f_data, i_start_write, i_end_write, sec_file_path, header_plantilla, tail_plantilla)

                else:
                    if k_part == k_part_sum:
                        k_part_aux = k_part + 1
                            
                    else:
                        k_part_aux = k_part 

                    if k_part_aux < len(i_part):
                        i_end_write = i_part[k_part_aux]
                        write_notebook(f_data, i_start_write, i_end_write, sec_file_path, header_plantilla, tail_plantilla)
                    else:
                        i_end_write = i_bib
                        write_notebook(f_data, i_start_write, i_end_write, sec_file_path, header_plantilla, tail_plantilla)
                    


            k_sec_sum += 1
        
        k_chap_sum +=1
        k_chap_sum_part += 1
    chapters_before_first_part_aux = False

#for i in range(7642, 7642+10):
#    print({f_data[i]})


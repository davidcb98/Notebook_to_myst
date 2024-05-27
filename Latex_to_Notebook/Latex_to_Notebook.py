#!/usr/bin/env python3

from subprocess import check_output as bash

import sys
import re
import numpy as np
import os
import shutil 
import unicodedata

from LtN_replaces_and_others import reemplazo_label
from LtN_replaces_and_others import reemplazo_sec
from LtN_replaces_and_others import reemplazo_subsec
from LtN_replaces_and_others import reemplazo_chapter
from LtN_replaces_and_others import reemplazo_SubsubIt
from LtN_replaces_and_others import reemplazo_caption
from LtN_replaces_and_others import reemplazo_includegraphics
from LtN_replaces_and_others import find_title_subtitle_BeginBox
from LtN_replaces_and_others import reemplazo_textbf
from LtN_replaces_and_others import reemplazo_textit
from LtN_replaces_and_others import delete_vspace
from LtN_replaces_and_others import delete_comments
from LtN_replaces_and_others import build_i_a_in_b
from LtN_replaces_and_others import replace_start_newtheorem
from LtN_replaces_and_others import replace_end_newtheorem

from LtN_replaces_and_others import ErrorGenerico

Notebook_folder_path = "../Notebooks"
Notebook_old_folder_path = "../Notebooks_old"
Plantilla_section_path = "Plantilla_seccion.ipynb"
Name_Figuras_folder = "Figuras"


def remove_capital_accents(string):
    # Normalizar y eliminar acentos
    normalized_string = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))

    # Convertir a minúsculas
    final_string = normalized_string.lower()

    return final_string



if os.path.exists(Notebook_folder_path):
    if os.path.exists(Notebook_old_folder_path):
        shutil.rmtree(Notebook_old_folder_path)
    os.rename(Notebook_folder_path,Notebook_old_folder_path)

os.mkdir(Notebook_folder_path)
#shutil.copytree(Name_Figuras_folder,Notebook_folder_path +"/"+ Name_Figuras_folder)



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





#i_begin_doc = 0
#i_end_doc = 0
begin_doc_bool = False
end_doc_bool   = False

find_mybox_gray2 = False
find_proof = False
find_mybox_blue = False
find_itemize = False
find_itemize_2 = False
find_figure = False
find_Teorema = False
find_Lemma = False
find_Corolario = False
find_Definicion = False
find_Proposicion = False
find_Ejercicio = False
find_mybox_green = False


num_line_text_file = -1

omitir_seccion = False



with open(file_name, 'r') as f:


    f_data = []
    i = 0
    i_part            = []
    i_chapter         = []
    i_section         = []

    last_line = None
    for line in f:
        num_line_text_file += 1
        finds = [
                 find_mybox_gray2,
                 find_proof,
                 find_mybox_blue,
                 find_itemize,
                 find_itemize_2,
                 find_figure,
                 find_Teorema,
                 find_Lemma,
                 find_Corolario,
                 find_Definicion,
                 find_Proposicion,
                 find_Ejercicio,
                 find_mybox_green
                 ]


        ## Cogemos solo lo que hay entre el \\begin{document} y el \\end{document}
        if begin_doc_bool == False:
            if "\\begin{document}" in line:
                begin_doc_bool = True
            else:
                continue
        if end_doc_bool == True:
            continue

        # Eliminamos los espacios en blanco a izquierda y derecha
        # Sustituimos "\" por "\\"
        line = line.lstrip().rstrip().replace("\\","\\\\").replace("``","\\\"").replace("''","\\\"")
        line = line.replace("\\section*{", "\\section{")
        line = line.replace("\\subsection*{", "\\subsection{")
        line = line.replace("\\chapter*{", "\\chapter{")
        line = line.replace("\\part*{", "\\part{")
        line = line.replace("\\\\newpage","")

        # Eliminamos los tabuladores \t, teniendo cuidado de no eliminar los \\t
        line = re.sub(r'(?<!\\)\t','',line)

        if "\\\\vspace{" in line:
            line = delete_vspace(line)



        if line == "":
            line = "\\n"
        
        if line == "\\n":
            if last_line == "\\n":
                continue
            elif True in finds:
                line = "<br><br>"

                if last_line == "<br>" or last_line == "<br><br>" or last_line[-4:] == "<br>":
                    continue
                else:
                    f_data.append(line)
                    i +=1 
                    last_line = line
                    continue
            else:
                f_data.append(line)
                i +=1 
                last_line = line
                continue

        if "% == Bibliograf" in line:
            i_bib = i
            f_data.append(line)

            i +=1
            last_line = line
            continue

        if line[0] == "%":
            continue


        line = delete_comments(line) # Eliminamos lo de despues de "%"

        ##### If's sueltos
        if "\\\\textbf{" in line:
            line = reemplazo_textbf(line)

        if "\\\\textit{" in line:
            line = reemplazo_textit(line)



        if "\\\\section{" in line:
            if "%%Omitir_seccion" in line:
                omitir_seccion = True
                print(line)
            else:
                omitir_seccion = False
                i_section.append(i)
                line = reemplazo_sec(line, nonumber = False)


        if omitir_seccion == True:
            continue

        ###############################################################################################################
        ##### Cadena principal de elif's
        ###############################################################################################################


        #################### part/chapter/section/subsec #######################
        if "\\\\subsection{" in line:
            line = reemplazo_subsec(line, nonumber = False)

        elif "\\\\chapter{" in line:
            line = reemplazo_chapter(line, nonumber = False)
            i_chapter.append(i)

        elif "\\\\part{" in line: # or "\\part*{" in line:
            i_part.append(i)

        elif "\\\\SubsubiIt{" in line:
            line = reemplazo_SubsubIt(line)

        #################### mybox_gray / Nota sin titulo #######################

        elif "\\\\begin{mybox_gray2}" in line :
            find_mybox_gray2 = True
            line = '<div class=\\"alert alert-block alert-info\\">\\n",\n' + \
                    '    "<p style=\\"color: navy;\\">\\n",\n'+ \
                    '    "<b></b>'

        elif "\\\\end{mybox_gray2}" in line:
            find_mybox_gray2 = False
            line = '</p></div>'


        #################### mybox_blue / Nota y Resumen #######################
        elif "\\\\begin{mybox_blue}" in line:
            find_mybox_blue = True

            title, subtitle = find_title_subtitle_BeginBox(line)

            if subtitle == None:
                line = '<div class=\\"alert alert-block alert-danger\\">\\n",\n' + \
                        '    "<p style=\\"color: DarkRed;\\">\\n",\n' + \
                        '    "<b>'+title+'</b>:\\n",\n' + \
                        '    "<br>'
            else:
                line = '<div class=\\"alert alert-block alert-danger\\">\\n",\n' + \
                        '    "<p style=\\"color: DarkRed;\\">\\n",\n' + \
                        '    "<b>'+title+'</b>: <i>('+subtitle+')</i>\\n",\n' + \
                        '    "<br>'

        elif "\\\\end{mybox_blue}" in line:
            find_mybox_blue = False
            line = '</p></div>'

        #################### mybox_greeb / Ejemplos #######################

        elif "\\\\begin{mybox_green}" in line:
            find_mybox_green = True
            title, subtitle = find_title_subtitle_BeginBox(line)

            if subtitle == None:
                line = '<div class=\\"alert alert-block alert-success\\">\\n",\n' + \
                        '    "<p style=\\"color: DarkGreen;\\">\\n",\n' + \
                        '    "<b>'+title+'</b>:\\n",\n' + \
                        '    "<br>'
            else:
                line = '<div class=\\"alert alert-block alert-success\\">\\n",\n' + \
                        '    "<p style=\\"color: DarkGreen;\\">\\n",\n' + \
                        '    "<b>'+title+'</b>: <i>('+subtitle+')</i>\\n",\n' + \
                        '    "<br>'

        elif "\\\\end{mybox_green}" in line:
            find_mybox_green = False
            line = '</p></div>'


        ########################### Teoremas  #############################
        elif "\\\\Teorema{" in line:
            find_Teorema = True

            i_start_teorema_in_tex   = num_line_text_file
            num_start_braket_teorema = len(re.findall(r'(?<!\\)\{', line))
            num_end_braket_teorema   = len(re.findall(r'(?<!\\)\}', line))

            line = replace_start_newtheorem(f_data, line, "Teorema", "Teorema")

            '''
            if "\\\\label{" in line:
                line = reemplazo_label(line)

                pre_label = line.split("<a id='")[0]
                label     = "<a id='" + line.split("<a id='")[1]

                line = label + '\\n",\n' + \
                        pre_label

                new_line = '    "<div class=\\"alert alert-block alert-info\\">\\n",\n' + \
                            '    "<p style=\\"color: navy;\\">\\n",\n' + \
                            '    "<b>Teorema</b>:'
                line = line.replace("\\\\Teorema{", new_line)

            else:

                new_line = '<div class=\\"alert alert-block alert-info\\">\\n",\n' + \
                            '    "<p style=\\"color: navy;\\">\\n",\n' + \
                            '    "<b>Teorema</b>:'
                line = line.replace("\\\\Teorema{", new_line)
            '''

        elif find_Teorema == True:
            num_start_braket_teorema = len(re.findall(r'(?<!\\)\{', line)) + num_start_braket_teorema
            num_end_braket_teorema   = len(re.findall(r'(?<!\\)\}', line)) + num_end_braket_teorema

            line, find_Teorema = \
                replace_end_newtheorem(f_data, line, find_Teorema, i_start_teorema_in_tex, num_start_braket_teorema, num_end_braket_teorema, "Teorema")

            '''
            if line == "}":
                find_Teorema = False

                if num_start_braket_teorema != num_end_braket_teorema:

                    message = "El numero de \"{{\" y \"}}\" diferentes."
                    raise ErrorGenerico(f_data, line, i_start_teorema_in_tex, message)

                line = '</p></div>'


            elif num_start_braket_teorema == num_end_braket_teorema:

                message = "El numero de \"{\" y \"}\" iguales, pero no se ha encontrado el final del teorema (linea con solo un \"}\")"
                raise ErrorGenerico(f_data, line, i_start_teorema_in_tex, message)
            '''

        ########################### Definicion  #############################
        elif "\\\\Definicion{" in line:

            find_Definicion = True

            i_start_definicion_in_tex   = num_line_text_file
            num_start_braket_definicion = len(re.findall(r'(?<!\\)\{', line))
            num_end_braket_definicion   = len(re.findall(r'(?<!\\)\}', line))

            line = replace_start_newtheorem(f_data, line, "Definicion", "Definicion")


        elif find_Definicion == True:
            num_start_braket_definicion = len(re.findall(r'(?<!\\)\{', line)) + num_start_braket_definicion
            num_end_braket_definicion   = len(re.findall(r'(?<!\\)\}', line)) + num_end_braket_definicion

            line, find_Definicion = \
                replace_end_newtheorem(f_data, line, find_Definicion, i_start_definicion_in_tex, num_start_braket_definicion, num_end_braket_definicion, "Definicion")


        ########################### Lemma  #############################
        elif "\\\\Lemma{" in line:

            find_Lemma = True

            i_start_lemma_in_tex   = num_line_text_file
            num_start_braket_lemma = len(re.findall(r'(?<!\\)\{', line))
            num_end_braket_lemma   = len(re.findall(r'(?<!\\)\}', line))

            line = replace_start_newtheorem(f_data, line, "Lemma", "Lema")


        elif find_Lemma == True:
            num_start_braket_lemma = len(re.findall(r'(?<!\\)\{', line)) + num_start_braket_lemma
            num_end_braket_lemma   = len(re.findall(r'(?<!\\)\}', line)) + num_end_braket_lemma

            line, find_Lemma = \
                replace_end_newtheorem(f_data, line, find_Lemma, i_start_lemma_in_tex, num_start_braket_lemma, num_end_braket_lemma, "Lemma")


        ##################### end document #######################
        elif "\\\\end{document}" in line:
            end_doc_bool = True


        ###############################################################################################################
        ##### Otros if
        ###############################################################################################################

        ############################ Itemice ##############################
        if ("\\\\begin{itemize}" in line or "\\\\begin{enumerate}" in line):
            if find_itemize == True:
                find_itemize_2 = True
            else:
                find_itemize = True
            line = '<br>'

        elif ("\\\\end{itemize}" in line or "\\\\end{enumerate}" in line):
            if find_itemize_2 == True:
                find_itemize_2 = False
            else:
                find_itemize = False
            line = '<br>'

        elif find_itemize == True and "\\\\item " in line:
            if find_itemize_2 == True:
                line = line.replace('\\\\item', '    *')
            else:
                line = line.replace('\\\\item', '-')

            line = line + '\\n",\n' + \
                    '    "<br>'

        ######################## proof / dropdown #########################
        if "\\\\begin{proof}" in line :
            find_proof = True
            line = '<details><summary><p style=\\"color:blue\\" > >> <i>Demostración</i> </p></summary>'

        elif "\\\\end{proof}" in line :
            find_proof = False
            line = '</details>'

                ############################ Figuras ##############################
        elif "\\\\begin{figure}" in line :
            find_figure = True
            line = '<figure><center>'

        elif "\\\\end{figure}" in line :
            find_figure = False
            line = '</center></figure>\\n'

        elif "\\\\centering" in line and find_figure == True:
            line = '<br>'

        elif "\\\\caption{" in line and find_figure == True:
            line = reemplazo_caption(line)

        elif "\\\\includegraphics[" in line and find_figure == True and not "\\subfigure" in line:
            line = reemplazo_includegraphics(line)

        elif "\\\\label{" in line and find_figure == True:
            line = reemplazo_label(line)






        f_data.append(line)
        i +=1
        last_line = line




i_chap_in_parts, chapters_before_first_part = build_i_a_in_b(i_chapter, i_part)
i_sec_in_chap, _ = build_i_a_in_b(i_section, i_chapter)

print("")

def test_write_start_end(i_end_write_old, i_start_write, write_path):
    if i_end_write_old > i_start_write:
        print(f"\033[91m======\033[0m") 
        print(f"\033[91mLa anterior escritura termino después del inicio de la actual\033[0m")
        print(f"\033[91mEs decir, i_end_write_old > i_start_write: {i_end_write_old} > {i_start_write} \033[0m")
        print(f"\033[91mPath al ultimo archivo escrito: \033[0m")
        print("   ",write_path)
        print(f"\033[91m======\033[0m") 
        raise 

def write_notebook(f_data, i_start_write, i_end_write, write_path, header_plantilla, tail_plantilla):

    print(f"[INFO]: Writing {write_path}")

    with open(write_path, 'w') as f_out:
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
    
    ##################
    ### Test
    global i_end_write_old

    test_write_start_end(i_end_write_old, i_start_write, write_path)

    i_end_write_old = i_end_write
    




chapters_before_first_part_aux = chapters_before_first_part
k_part = 0
k_part_sum = 0
k_chap_sum = 0
i_end_write_old = -1

for k_chap_in_one_part in i_chap_in_parts:
    if chapters_before_first_part_aux == False:
        print(f"\nPart_"+str(k_part_sum+1).zfill(2), {f_data[i_part[k_part]]})
        part_folder_path = str(Notebook_folder_path) + "/" + f"Part_"+str(k_part_sum+1).zfill(2)
        os.mkdir(part_folder_path)
        shutil.copytree(Name_Figuras_folder, part_folder_path + "/" + Name_Figuras_folder)
        k_part +=1
        k_part_sum +=1
    else:
        print(f"\nPart_"+str(k_part_sum+1).zfill(2))
        part_folder_path = str(Notebook_folder_path) + "/" + f"Part_"+str(k_part_sum+1).zfill(2)
        os.mkdir(part_folder_path)
        shutil.copytree(Name_Figuras_folder, part_folder_path + "/" + Name_Figuras_folder)
        k_part_sum +=1

    k_chap_sum_part = 0
    
    for k_chap in k_chap_in_one_part:

        #print("  ",f"Chapter_"+str(k_chap_sum +1).zfill(3), {f_data[i_chapter[k_chap]]})
        k_sec_sum = 0

        i_start_write = i_chapter[k_chap]

        title_lowecase = remove_capital_accents(f_data[i_start_write].replace("#","").lstrip().replace(" ","_")  \
                        .replace(":","").replace(".","").replace(">","").replace("<","").replace("\"","")        \
                        .replace("/","").replace("\\","").replace("|","").replace("?","").replace("¿","").split("_a_id=")[0])


        chapter_intro_file_path = part_folder_path + "/Chapter_"+str(k_chap_sum +1).zfill(3)+"_01_" + title_lowecase + ".ipynb"
        chapter_folder_path     = part_folder_path + "/Chapter_"+str(k_chap_sum +1).zfill(3)+"_02"



        if len(i_sec_in_chap[k_chap]) >= 1:
            ## Escribimos lo que hay antes de la primera seccion del capitulo en un archivo Chapter_.._01
            write_path = chapter_intro_file_path
            i_end_write = i_section[i_sec_in_chap[k_chap][0]]

            write_notebook(f_data, i_start_write, i_end_write, write_path, header_plantilla, tail_plantilla)

            ## Carpeta para las secciones
            os.mkdir(chapter_folder_path)
            shutil.copytree(Name_Figuras_folder, chapter_folder_path + "/" + Name_Figuras_folder)

            ## Escribirmos las secciones
            for k_sec in i_sec_in_chap[k_chap]:
                #print("    ", f"Section_"+ str(k_sec_sum+1).zfill(3) ,i_section[k_sec], {f_data[i_section[k_sec]]})
                i_start_write = i_section[k_sec]

                title_lowecase = remove_capital_accents(f_data[i_start_write].replace("#","").lstrip().replace(" ","_")  \
                                .replace(":","").replace(".","").replace(">","").replace("<","").replace("\"","")        \
                                .replace("/","").replace("\\","").replace("|","").replace("?","").replace("¿","").split("_a_id=")[0])

                sec_file_path = str(chapter_folder_path) + "/" + f"Section_"+ str(k_sec_sum+1).zfill(3)+"_"+ title_lowecase + ".ipynb"
                write_path = sec_file_path

                if k_sec_sum < len(i_sec_in_chap[k_chap]) -1 :
                    i_end_write   = i_section[k_sec + 1]
                    
                    
                else:
                    if k_chap_sum_part < len(k_chap_in_one_part) - 1:
                        i_end_write   = i_chapter[k_chap + 1]

                    else:
                        if k_part == k_part_sum:
                            k_part_aux = k_part + 1
                        else:
                            k_part_aux = k_part 

                        if k_part_aux < len(i_part):
                            i_end_write = i_part[k_part_aux]
                        else:
                            i_end_write = i_bib
                    
                write_notebook(f_data, i_start_write, i_end_write, write_path, header_plantilla, tail_plantilla)
                k_sec_sum += 1
        else:
            ## Escribimos lo que hay antes de la primera seccion del capitulo en un archivo Chapter_.._01
            write_path = chapter_intro_file_path
            if k_chap_sum_part < len(k_chap_in_one_part) - 1:
                i_end_write   = i_chapter[k_chap + 1]

            else:
                if k_part == k_part_sum:
                    k_part_aux = k_part + 1
                else:
                    k_part_aux = k_part 

                if k_part_aux < len(i_part):
                    i_end_write = i_part[k_part_aux]
                else:
                    i_end_write = i_bib

            write_notebook(f_data, i_start_write, i_end_write, write_path, header_plantilla, tail_plantilla)


            
        

        k_chap_sum +=1
        k_chap_sum_part += 1
    chapters_before_first_part_aux = False

#for i in range(7642, 7642+10):
#    print({f_data[i]})


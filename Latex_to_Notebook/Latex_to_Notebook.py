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
        #patron = r"\\\\section\*\{(.+?)\}"
        patron = r"\\\\section\*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    else:
        #patron = r"\\\\section\{(.+?)\}"
        patron = r"\\\\section\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return reemplazo_label(re.sub(patron, reemplazo_sec_aux, line))

# =============================================================================
## Las dos siguientes funciones son para reemplazar \subsection por ##
## Se reemplazan también la label 
def reemplazo_subsec(line, nonumber):

    def reemplazo_subsec_aux(match):
        titulo = match.group(1)
        return f"## {titulo}"
    
    if nonumber == True:
        #patron = r"\\\\subsection\*\{(.+?)\}"
        patron = r"\\\\subsection\*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    else:
        #patron = r"\\\\subsection\{(.+?)\}"
        #patron = r"\\\\subsection\{([^{}]+)\}"
        patron = r"\\\\subsection\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return reemplazo_label(re.sub(patron, reemplazo_subsec_aux, line))

# =============================================================================
## Las dos siguientes funciones son para reemplazar \chapter por #
## Se reemplazan también la label 
def reemplazo_chapter(line, nonumber):
    
    def reemplazo_chapter_aux(match):
        titulo = match.group(1)
        return f"# {titulo}"
    
    if nonumber == True:
        #patron = r"\\\\section\*\{(.+?)\}"
        patron = r"\\\\chapter\*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    else:
        #patron = r"\\\\section\{(.+?)\}"
        patron = r"\\\\chapter\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return reemplazo_label(re.sub(patron, reemplazo_chapter_aux, line))


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
    # Definir la función de reemplazo
    def reemplazo_includegraphics_aux(match):
        width = float(match.group(1))
        nombre_archivo = match.group(3)
        nueva_width = int(width * 1000)
        return f"<img src=\\\"{nombre_archivo}\\\" alt=\\\"\\\" align=center width='{nueva_width}px'/>"

    # Realizar el reemplazo
    return re.sub(patron_includegraphics, reemplazo_includegraphics_aux, line)

# =============================================================================
## Para buscar un titulo y subtitulo en \begin{..}{Titulo: subtitulo}

def find_title_subtitle_BeginBox(line):
    #patron = r"\{([^:{}]+)(?:: ([^}]+))?\}"
    patron_segundo_conjunto = r"\\begin{[^{}]+}\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    contenido_segundo_conjunto = re.search(patron_segundo_conjunto, line).group(1)


    patron_division = r"([^:]+):\s*(.+)"
    match_division = re.match(patron_division, contenido_segundo_conjunto)

    if match_division:
        Titulo = match_division.group(1).strip()
        Subtitulo = match_division.group(2).strip()

    else:
        Titulo = contenido_segundo_conjunto.strip()
        Subtitulo = None
    # print(Titulo, "------", Subtitulo)
    return Titulo, Subtitulo


# =============================================================================
## Reemplazar \\textbf{texto} por <b>texto</b>
def reemplazo_textbf(line):

    def reemplazo_textbf_aux(match):
        texto = match.group(1)
        return f"<b>{texto}</b>"

    patron_textbf = r"\\\\textbf\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return re.sub(patron_textbf, reemplazo_textbf_aux, line)

# =============================================================================
## Reemplazar \\textit{texto} por <b>texto</b>
def reemplazo_textit(line):

    def reemplazo_textit_aux(match):
        texto = match.group(1)
        return f"<i>{texto}</i>"

    patron_textit = r"\\\\textit\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return re.sub(patron_textit, reemplazo_textit_aux, line)

# =============================================================================
## Eliminar los \vspace{...}
def delete_vspace(line):
    patron_vspace = r"\\\\vspace\{[^{}]*\}"
    return re.sub(patron_vspace, '', line)

# =============================================================================
## Eliminar lo que hay despues de "%" (sin contar "\%")
def delete_comments(line):
    patron_comments = r"(?<!\\)%.*"
    return re.sub(patron_comments, '', line)

# ===========================================================================


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

num_start_braket_teorema = 0
num_end_braket_teorema = 0




omitir_seccion = False

#conteo_corch_abrir = 0
#conteo_corch_cerrar = 0

'''
# Contar llaves que no están escapadas
conteo_abrir = len(re.findall(r'(?<!\\){', cadena))
conteo_cerrar = len(re.findall(r'(?<!\\)}', cadena))
'''


with open(file_name, 'r') as f:
    
    f_data = []
    i = 0
    i_part            = []
    i_chapter         = []
    i_section         = []

    last_line = None
    for line in f:
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
                pass
            elif True in finds:
                line = "<br><br>"
                if last_line == "<br>" or last_line == "<br><br>":
                    continue
                else:
                    f_data.append(line)
                    i +=1 
                    last_line = line
            else:
                f_data.append(line)
                i +=1 
                last_line = line
        else:
            
            if line[0] != "%":

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


                ###############################################################
                ##### Cadena de elif's
                ###############################################################


                if omitir_seccion == True:
                    pass

                #################### part/chapter/section/subsec #######################
                elif "\\\\subsection{" in line:
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
                    new_line = '<div class=\\"alert alert-block alert-info\\">\\n",\n' + \
                               '    "<p style=\\"color: navy;\\">\\n",\n' + \
                               '    "<b>Teorema</b>:\\n",\n' + \
                               '    "<br>'
                    line = line.replace("\\\\Teorema{", new_line)
                elif line == "}" and find_Teorema == True:
                    find_Teorema = False
                    line = '</p></div>'


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

                ############################ Itemice ##############################
                elif ("\\\\begin{itemize}" in line or "\\\\begin{enumerate}" in line):
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
                        line = line.replace('\\\\item', '    -')
                    else:
                        line = line.replace('\\\\item', '-')
                    
                    line = line + '\\n",\n' + \
                           '    "<br>'

                ######################## proof / dropdown #########################
                elif "\\\\begin{proof}" in line :
                    find_proof = True
                    line = '<details><summary><p style=\\"color:blue\\" > >> <i>Demostración</i> </p></summary>'
                    
                elif "\\\\end{proof}" in line :
                    find_proof = False
                    line = '</details>'

                ##################### end document #######################

                elif "\\\\end{document}" in line:
                    end_doc_bool = True





                if omitir_seccion == True:
                    pass
                else:
                    f_data.append(line)
                    i +=1 
                    last_line = line

            if "% == Bibliograf" in line: 
                i_bib = i
                f_data.append(line)
                
                i +=1 
                last_line = line

def build_i_a_in_b(i_a, i_b):
    '''
    Funcion para construir:
        - i_chap_in_parts y chapters_before_first_part
    a partir de
        - i_chapter, i_part

    Es decir, a la función se le pasan
        - los indices de las lineas de los capítulos
        - los indices de las lineas de las partes
    y te devuelve:
        - Una lista de listas donde en cada lista están los indices
          de los capitulos de cada parte (i_chap_in_parts)
        - Un booleano que nos dice si hay capitulos antes de la primera
          parte (chapters_before_first_part)
    '''

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
        chapter_intro_file_path = part_folder_path + "/Chapter_"+str(k_chap_sum +1).zfill(3)+"_01.ipynb"
        chapter_folder_path     = part_folder_path + "/Chapter_"+str(k_chap_sum +1).zfill(3)+"_02"

        if len(i_sec_in_chap[k_chap]) >= 1:
            ## Escribimos lo que hay antes de la primera seccion del capitulo en un archivo Chapter_.._01
            i_start_write = i_chapter[k_chap]
            i_end_write = i_section[i_sec_in_chap[k_chap][0]]

            write_path = chapter_intro_file_path
            write_notebook(f_data, i_start_write, i_end_write, write_path, header_plantilla, tail_plantilla)

            ## Carpeta para las secciones
            os.mkdir(chapter_folder_path)
            shutil.copytree(Name_Figuras_folder, chapter_folder_path + "/" + Name_Figuras_folder)

            ## Escribirmos las secciones
            for k_sec in i_sec_in_chap[k_chap]:
                #print("    ", f"Section_"+ str(k_sec_sum+1).zfill(3) ,i_section[k_sec], {f_data[i_section[k_sec]]})
                sec_file_path = str(chapter_folder_path) + "/" + f"Section_"+ str(k_sec_sum+1).zfill(3) + ".ipynb"
                write_path = sec_file_path
                i_start_write = i_section[k_sec]


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
            i_start_write = i_chapter[k_chap]
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


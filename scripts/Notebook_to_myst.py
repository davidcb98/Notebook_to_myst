#!/usr/bin/env python3
#from pprint import pprint

from subprocess import check_output as bash
import unicodedata

import sys
import re

def grep_file_index(grep_command):
    
    out_grep_command = bash(grep_command, shell=True).decode("utf-8")

    index_Lines = []
    for line in out_grep_command.splitlines():
        index_Lines.append(int(line)-1)
    
    return index_Lines

def remove_capital_accents(string):
    # Normalizar y eliminar acentos
    normalized_string = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))

    # Convertir a minúsculas
    final_string = normalized_string.lower()

    return final_string

def find_boxes(f_data, i_Lines_start):
    i_line_end_list           = [] 
    i_line_start_list         = []
    i_line_start_p_list       = []
    i_line_end_p_list         = []
    i_line_start_details_list = []
    i_line_end_details_list   = []
    i_line_title_list         = []
    title_details_list        = []
    title_list                = []
    title_lowercase_list      = []
    subtitle_list             = []


    i_line_end_last_iteration = 0
    for i_line_start in i_Lines_start:

        assert i_line_end_last_iteration < i_line_start, f"{i_line_end_last_iteration} < {i_line_start} The previous box ends after the begining of the next one"

        i_line_end           = i_line_start 
        i_line_start_p       = 0
        i_line_end_p         = 0
        i_line_start_details = 0
        i_line_end_details   = 0
        i_line_title         = 0
        
        title_details   = None
        subtitle        = None
        title           = None
        title_lowercase = None
        subtitle        = None
                
        found = False
        while not found:

            if "<details><summary>" in f_data[i_line_end]:
                i_line_start_details = i_line_end
            elif "</details>"       in f_data[i_line_end]:
                i_line_end_details   = i_line_end
            elif "<p"               in f_data[i_line_end]:
                i_line_start_p       = i_line_end
            elif "</p></div>"       in f_data[i_line_end]:
                i_line_end_p         = i_line_end
                found = True
            elif "</p>"             in f_data[i_line_end]:
                i_line_end_p         = i_line_end
            elif "<b>"              in f_data[i_line_end] and i_line_title == 0:
                i_line_title         = i_line_end
            elif "</div>"           in f_data[i_line_end]:
                found = True
            
            i_line_end += 1
        i_line_end -= 1       

        i_line_end_last_iteration = i_line_end
        ########################
        ######## TITLE 

        line_title   = f_data[i_line_title]
        
        # Esta expresión es para borrar los espacios       
        # title_no_clean_aux = e.sub(r'"(.*?)"', 
        #                     lambda x: x.group(0).replace(' ', ''), line_title)

        title_no_clean = re.search(r'"([^"]*)"', line_title).group(1)
        title = re.sub(r'<.*?>', '', title_no_clean.split(':')[0]).strip()   #  +'\\n",\n'
        #print(f_data[i_line_title])
        #print(i_line_title)
        #title = re.search(r'<b>(.*?)</b>', f_data[i_line_title]).group(1)
        title_lowercase = remove_capital_accents(title).strip()
        
        ########################
        ######## SUB-TITLE 

        if "<i>" in f_data[i_line_title]:
            subtitle = re.search(r'<i>(.*?)</i>', f_data[i_line_title]).group(1)
          

        
        ########################
        ######## #prints y asserts

        #assert i_line_start_p       <= i_line_end_p, f"Problems findins <p>, {i_line_start_p} and </p> {i_line_end_p}"
        #assert i_line_start_details <= i_line_end_details, f"Problems findins <details>, {i_line_start_p} and </details> {i_line_end_p}"
        
        #print(i_line_start,             {f_data[i_line_start]})

        if i_line_start_p > 0:
            assert i_line_start <= i_line_start_p < i_line_end, f"{i_line_start} <= {i_line_start_p} < {i_line_end}"
            #if i_line_start < i_line_start_p:
                #print(i_line_start_p,   {f_data[i_line_start_p]})
        
        #print(i_line_title,  title, title_lowercase, subtitle)
        
        if i_line_start_details > 0:
            assert i_line_start < i_line_start_details <= i_line_end, f"{i_line_start} < {i_line_start_details} <= {i_line_end}"

            ###### Title details:
            title_details = re.search(r'<i>(.*?)</i>', f_data[i_line_start_details]).group(1)

            #print(i_line_start_details, {f_data[i_line_start_details]})
            #print("")
            #print(i_line_start_details, {f_data[i_line_start_details]} , title_details)

        if i_line_end_details > 0:
            
            assert i_line_start < i_line_start_details < i_line_end_details <= i_line_end, f"{i_line_start} < {i_line_start_details} < {i_line_end_details} <= {i_line_end}"
            
            #print(i_line_end_details,   {f_data[i_line_end_details]})
        
        if i_line_end_p > 0:
            
            assert i_line_start <= i_line_start_p < i_line_end_p <= i_line_end, f"{i_line_start} <= {i_line_start_p} < {i_line_end_p} <= {i_line_end}"
            
            #if i_line_end > i_line_end_p:
                #print(i_line_end_p,   {f_data[i_line_end_p]})

        #print("")
        #print(i_line_end,               {f_data[i_line_end]})
        #print("===============================================================")
        
        if not title == None:

            i_line_end_list.append(i_line_end) 
            i_line_start_list.append(i_line_start) 
            i_line_start_p_list.append(i_line_start_p) 
            i_line_end_p_list.append(i_line_end_p) 
            i_line_start_details_list.append(i_line_start_details) 
            i_line_end_details_list.append(i_line_end_details) 
            i_line_title_list.append(i_line_title) 
            title_details_list.append(title_details) 
            title_list.append(title) 
            title_lowercase_list.append(title_lowercase) 
            subtitle_list.append(subtitle)
    
    index_list_list = [i_line_start_list, 
                       i_line_end_list,
                       i_line_start_p_list, 
                       i_line_end_p_list, 
                       i_line_start_details_list, 
                       i_line_end_details_list, 
                       i_line_title_list]

    titles_list_list = [title_details_list, title_list, title_lowercase_list, subtitle_list]
        
    return index_list_list, titles_list_list


def find_figures(f_data, i_Lines_start):
    i_line_end_list      = [] 
    i_line_start_list    = []
    i_line_label_a_list  = []
    i_line_img_list      = []
    i_line_caption_list  = []

    path_fig_list    = []
    align_fig_list   = []
    width_fig_list   = []
    caption_fig_list = []
    label_fig_list   = []
    


    i_line_end_last_iteration = 0
    for i_line_start in i_Lines_start:

        assert i_line_end_last_iteration < i_line_start, f"{i_line_end_last_iteration} < {i_line_start} The previous figure ends after the begining of the next one"

        i_line_end     = i_line_start 
        i_line_label_a = 0
        i_line_img     = 0
        i_line_caption = 0
        
        path_fig    = None
        align_fig   = None
        width_fig   = None
        caption_fig = None
        label_fig   = None
                
        found = False
        while not found:

            if "<a id"           in f_data[i_line_end]:
                i_line_label_a   = i_line_end
                label_fig = f_data[i_line_label_a].split('>')[0].split('=')[1].replace("\'",'')

            elif "<img"        in f_data[i_line_end]:
                i_line_img     = i_line_end
            
            elif "<center>"    in f_data[i_line_end] and  "</center>"    in f_data[i_line_end]:
                i_line_caption = i_line_end
                caption_fig = re.search(r'<center>(.*?)</center>', f_data[i_line_caption]).group(1)
            
            elif "</figure>"   in f_data[i_line_end]:
                found = True
            
            i_line_end += 1
        i_line_end -= 1       

        i_line_end_last_iteration = i_line_end

        ########################
        ######## Path, align, scale

        line_img   = f_data[i_line_img]
        
        line_img_split = line_img.split(' ')

        for i in range(len(line_img_split)):
            if 'src='      in line_img_split[i]:
                path_fig   = line_img_split[i].split('=')[1].replace('\\"','').replace("\\'",'').replace('/>','').replace('\\n",\n','').replace(',\n','')
            elif 'align='  in line_img_split[i]:
                align_fig  = line_img_split[i].split('=')[1].replace('\\"','').replace("\\'",'').replace('/>','').replace('\\n",\n','').replace(',\n','')
            elif 'width='  in line_img_split[i]:
                width_fig  = line_img_split[i].split('=')[1].replace('\\"','').replace("\'",'').replace('/>','').replace('\\n",\n','').replace(',\n','')
        
      
        ########################
        ######## #prints y asserts
    
        if i_line_label_a > 0:
            assert i_line_start <= i_line_label_a < i_line_end, f"{i_line_start} <= {i_line_label_a} < {i_line_end}"

        if i_line_caption > 0:
            assert i_line_start < i_line_caption <= i_line_end, f"{i_line_start} < {i_line_caption} <= {i_line_end}"

        if not path_fig == None and not align_fig == None and not width_fig == None:

            i_line_end_list.append(i_line_end) 
            i_line_start_list.append(i_line_start) 
            i_line_label_a_list.append(i_line_label_a)
            i_line_img_list.append(i_line_img)
            i_line_caption_list.append(i_line_caption)

            path_fig_list.append(path_fig)
            align_fig_list.append(align_fig)
            width_fig_list.append(width_fig)
            caption_fig_list.append(caption_fig)
            label_fig_list.append(label_fig)
    
    index_list_list = [i_line_start_list, 
                       i_line_end_list,
                       i_line_label_a_list, 
                       i_line_img_list, 
                       i_line_caption_list]

    datos_list_list = [path_fig_list, align_fig_list, width_fig_list, caption_fig_list, label_fig_list]
        
    return index_list_list, datos_list_list


def my_replace(f_data, i_line, new_text):

    #print("------> ", new_text)

    # Encontrar la posición de la primera comilla doble
    index_firts_quote = f_data[i_line].find('"')

    # Realizar la sustitución
    f_data[i_line]= f_data[i_line][:index_firts_quote + 1] +new_text 
        #f_data[i_line_start_p][f_data[i_line_start_p].find('\n', indice_primera_comilla + 1):] 



def build_admonition_box(i, f_data, index_list_list, titles_list_list, Class):

    i_line_start         = index_list_list[0][i]  
    i_line_end           = index_list_list[1][i]  
    i_line_start_p       = index_list_list[2][i]  
    i_line_end_p         = index_list_list[3][i]
    i_line_start_details = index_list_list[4][i]
    i_line_end_details   = index_list_list[5][i]
    i_line_title         = index_list_list[6][i]
       
    title_details   = titles_list_list[0][i]
    title           = titles_list_list[1][i]
    #title_lowercase = titles_list_list[2][i]
    subtitle        = titles_list_list[3][i]
    
    #for i in range(i_line_end-i_line_start+1):
    #    print({f_data[i_line_start+i]})
    #print("")

    ############################################################################
    ###### Empezamos a sustituir por el final

    ### </div>    
    if f_data[i_line_end + 1] == "   ]\n":
        my_replace(f_data, i_line_end, '::::'+'\\n"\n' )
    else:
        my_replace(f_data, i_line_end, '::::'+'\\n",\n' )

    ### </p>
    if i_line_end_p > 0:
        if i_line_end > i_line_end_p:
            my_replace(f_data, i_line_end_p, ''+'\\n",\n' )

    ### </details>
    if i_line_end_details > 0:
        if i_line_end > i_line_end_details:
            my_replace(f_data, i_line_end_details, ':::'+'\\n",\n')

    ### <detail>
    if i_line_start_details > 0:
        my_replace(f_data, i_line_start_details, ':::{dropdown} '+ title_details+'\\n",\n')

    #### TITLE 
    my_replace(f_data, i_line_title,''+'\\n",\n')
    
    ### <p style=...>
    if i_line_start_p > 0:
        if i_line_start < i_line_start_p:
            my_replace(f_data, i_line_start_p, ''+'\\n",\n')

    #### <div class...> o <div class...><p style...>
    if subtitle == None:
        my_replace(f_data, i_line_start, '::::{admonition} '+ title+'\\n",\n' + '    ":class: '+Class+'\\n",\n')
    else:
        my_replace(f_data, i_line_start, '::::{admonition} '+ title + ' (' + subtitle + ') '+'\\n",\n' + '    ":class: '+Class+'\\n",\n')

    #print("")
    #for i in range(i_line_end-i_line_start+1):
    #    print({f_data[i_line_start+i]})
    #print("")


def build_card_box(i, f_data, index_list_list, titles_list_list):
    i_line_start         = index_list_list[0][i]  
    i_line_end           = index_list_list[1][i]  
    i_line_start_p       = index_list_list[2][i]  
    i_line_end_p         = index_list_list[3][i]
    i_line_start_details = index_list_list[4][i]
    i_line_end_details   = index_list_list[5][i]
    i_line_title         = index_list_list[6][i]
       
    title_details   = titles_list_list[0][i]
    title           = titles_list_list[1][i]
    #title_lowercase = titles_list_list[2][i]
    subtitle        = titles_list_list[3][i]
    
    #for i in range(i_line_end-i_line_start+1):
    #    print({f_data[i_line_start+i]})
    #print("")

    ############################################################################
    ###### Empezamos a sustituir por el final

    ##################################
    ######## </div> o </p></div>

    ### </div>    
    if f_data[i_line_end + 1] == "   ]\n":
        my_replace(f_data, i_line_end, '::::'+'\\n"\n' )
    else:
        my_replace(f_data, i_line_end, '::::'+'\\n",\n' )


    if i_line_end_p > 0:
        ##############################
        ######## </p>
        if i_line_end > i_line_end_p:
            my_replace(f_data, i_line_end_p, ''+'\\n",\n' )


    if i_line_end_details > 0:
        ##############################
        ######## </details>
        if i_line_end > i_line_end_details:
            my_replace(f_data, i_line_end_details, ':::'+'\\n",\n')

    if i_line_start_details > 0:
        ##############################
        ######## <detail>
        my_replace(f_data, i_line_start_details, ':::{dropdown} '+ title_details+'\\n",\n')

    my_replace(f_data, i_line_title, '^^^\\n",\n')
    
    if i_line_start_p > 0:
        ##############################
        ######## <p style=...>

        if i_line_start < i_line_start_p:
            my_replace(f_data, i_line_start_p, ''+'\\n",\n')

    ##############################
    ######## TITLE and <div class...> o <div class...><p style...>
    
    if subtitle == None:
        my_replace(f_data, i_line_start, '::::{card} \\n",\n'+'    "**'+title+'**: '+' \\n",\n')
    else:
        my_replace(f_data, i_line_start, '::::{card} \\n",\n'+'    "**'+title+'**: *'+ subtitle + '* '+'\\n",\n')

    #print("")
    #for i in range(i_line_end-i_line_start+1):
    #    print({f_data[i_line_start+i]})
    #print("")

def build_figure(i, f_data, index_fig_list_list, datos_list_list):

    i_line_start   = index_fig_list_list[0][i]
    i_line_end     = index_fig_list_list[1][i]
    i_line_label_a = index_fig_list_list[2][i]
    i_line_img     = index_fig_list_list[3][i]
    i_line_caption = index_fig_list_list[4][i]

    path_fig    = datos_list_list[0][i]
    align_fig   = datos_list_list[1][i]
    width_fig   = datos_list_list[2][i]
    caption_fig = datos_list_list[3][i]
    label_fig   = datos_list_list[4][i]
        
    ############################################################################
    ###### Empezamos a sustituir por el final


    if f_data[i_line_end + 1] == "   ]\n":
        my_replace(f_data, i_line_end, '::::'+'\\n"\n' )
    else:
        my_replace(f_data, i_line_end, '::::'+'\\n",\n' )
    

    if i_line_caption != 0 and caption_fig != None:
        my_replace(f_data, i_line_caption, caption_fig +'\\n",\n')
    
    my_replace(f_data, i_line_img, 
               ':width: ' + width_fig + '\\n",\n' + 
               '    ":align: ' + align_fig + '\\n",\n')
        
    if i_line_label_a != 0 and label_fig != None:
        my_replace(f_data, i_line_label_a, ':name: ' + label_fig +'\\n",\n')

    my_replace(f_data, i_line_start, '::::{figure} '+ path_fig +'\\n",\n' )


################################################################################
# Obtenemos el nombre del archivo del primer algumento de la llamada
file_name = sys.argv[1:][0]
print("===========================")
print("Input File  = ", file_name)



#command_i_LINES_start_alert_info   = 'grep -n "<div class=" '+file_name+'| grep "alert alert-block alert-info" |  cut -d":" -f1'
#command_i_LINES_start_alert_danger = 'grep -n "<div class=" '+file_name+'| grep "alert alert-block alert-danger" |  cut -d":" -f1'
#command_i_LINES_start_alert_success = 'grep -n "<div class=" '+file_name+'| grep "alert-block alert-success" |  cut -d":" -f1'

################################################################################
# Sacamalos el numero de linea del inicio de todos los cuadros con "<div class=.... alert alert-block alert...>"
command_i_Lines_start_alert   = 'grep -n "<div class=" '+file_name+' | grep "alert alert-block alert" |  cut -d":" -f1'
i_Lines_start_alert = grep_file_index(command_i_Lines_start_alert)

################################################################################
# Sacamalos el numero de linea del inicio de las <figure>
command_i_Lines_start_figure = 'grep -n "<figure>" ' + file_name + ' |  cut -d":" -f1'
i_Lines_start_figure = grep_file_index(command_i_Lines_start_figure)

################################################################################
# Leemos el archivo linea a linea y modificamos los cuadros
with open(file_name, 'r') as f:
    #f_data = f.read()
    ##print(f_data[20])

    f_data=[]
    for line in f:
        ##print(line)
        f_data.append(line)

    ############################################################################
    # Usando el número de linea donde empiezan los cuadros, sacamos todas las lineas
    # importantes de los cuadros
    index_list_list, titles_list_list = find_boxes(f_data, i_Lines_start_alert)

    ############################################################################
    # Comenzamos a sustituir los cuadros (empezando por el final)
    for i in reversed(range(len(index_list_list[0]))):
        title_lowercase = titles_list_list[2][i]        

        if 'definicion' in title_lowercase:
            build_card_box(i, f_data, index_list_list, titles_list_list)

        elif 'teorema' in title_lowercase:
            build_card_box(i, f_data, index_list_list, titles_list_list)

        elif 'lema' in title_lowercase:
            build_card_box(i, f_data, index_list_list, titles_list_list)

        elif 'nota' in title_lowercase:
            build_admonition_box(i, f_data, index_list_list, titles_list_list, Class = "note")

        elif 'ejercicio' in title_lowercase:
            build_admonition_box(i, f_data, index_list_list, titles_list_list, Class = "tip")

        elif 'ejemplo' in title_lowercase:
            build_admonition_box(i, f_data, index_list_list, titles_list_list, Class = "tip")


    ############################################################################
    # Usando el número de linea donde empiezan las figuras, sacamos todas las lineas importantes          
    index_fig_list_list, datos_list_list = find_figures(f_data, i_Lines_start_figure)

    ############################################################################
    # Comenzamos a sustituir las figuras (empezando por el final)
    for i in reversed(range(len(index_fig_list_list[0]))):
        build_figure(i, f_data, index_fig_list_list, datos_list_list)


################################################################################
###### Guardamos los cambios en un nuevo fichero

out_file = file_name[:-6]+'_lab.ipynb'

with open(out_file, 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])


################################################################################
###### Eliminamos los </br>

clean_br_command = "sed -i 's/<br>//g' " + out_file
bash(clean_br_command, shell=True).decode("utf-8")

################################################################################
### Creamos un nuevo fichero {out_file}_clean con las tres celdas de título

number_line_head = str(int(bash('grep -n "^  }," Firts_cells.ipynb |  cut -d":" -f1 | head -n 3 | tail -n 1' , 
                                shell=True).decode("utf-8")))

bash('head -n ' +number_line_head+' Firts_cells.ipynb ' +' > ' + out_file + '_clean' , 
     shell=True).decode("utf-8")

################################################################################
### Sacamos la linea de titulo en el archivo {out_file} y sustituimos el título 
### en el archivo {out_file}_clean
### Recordemos que hasta aquí {out_file}_clean solo tiene las tres celdas de título

Title_jupyter = str(bash('grep -n "# " '+ file_name +' |  cut -d":" -f2 | head -n 1 ', 
                     shell=True).decode("utf-8")).split('"')[1]

i_Title_jupyter_new_file = int(bash('grep -n "# " '+ out_file + '_clean' + ' |  cut -d":" -f1 | head -n 1', 
                                shell=True).decode("utf-8"))-1

# Leemos el archivo nuevo
with open(out_file + '_clean', 'r') as f:
    #f_data = f.read()
    ##print(f_data[20])

    f_data=[]
    for line in f:
        ##print(line)
        f_data.append(line)
    
    # Reemplazamos el título
    my_replace(f_data, i_Title_jupyter_new_file , Title_jupyter +'\\n"\n')

# Pisamos el archivo _clean con la nueva versión con el titulo 
with open(out_file + '_clean', 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])

################################################################################
### Concatenamos al archivo _clean el texto completo con los cuadros nuevos sin 
### las dos primeras celdas primera celda
number = str(int(bash('grep -n "^  }," ' + out_file + ' |  cut -d":" -f1 | head -n 2 | tail -n 1', shell= True).decode("utf-8")) + 1)
bash('tail -n +' + number + ' ' + out_file  +' >> ' + out_file + '_clean', shell=True).decode("utf-8")

### Renombramos para quitar el _clean
bash('mv ' +  out_file + '_clean ' + out_file, shell=True).decode("utf-8")








################################################################################
### Atacamos los <deatail> sueltos (los que no estaban en un cuadro)
# Tenemos que hacerlo despues de haber reemplazado los cuadros, por eso lo 
# hacemos sobre el archivo de salida

command_i_Lines_start_details   = 'grep -n "<details><summary>" '+out_file + ' |  cut -d":" -f1'
command_i_Lines_end_details   = 'grep -n "</details>" '+ out_file + ' |  cut -d":" -f1'

i_Lines_start_details = grep_file_index(command_i_Lines_start_details)
i_Lines_end_details = grep_file_index(command_i_Lines_end_details)


################################################################################
# Leemos el archivo linea a linea y modificamos los cuadros
with open(out_file, 'r') as f:
    #f_data = f.read()
    ##print(f_data[20])

    f_data=[]
    for line in f:
        ##print(line)
        f_data.append(line)
    

    for i in i_Lines_start_details:
        title_details = re.search(r'<i>(.*?)</i>', f_data[i]).group(1)
        my_replace(f_data, i, ':::{dropdown} '+title_details+'\\n",\n')
    
    
    
    for i in i_Lines_end_details:
        
        if f_data[i+1] == "   ]\n":
            my_replace(f_data, i, ':::'+'\\n"\n')
        else:
            my_replace(f_data, i, ':::'+'\\n",\n')
    

with open(out_file, 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])

    
print("Output file = ", out_file)
print("===========================")
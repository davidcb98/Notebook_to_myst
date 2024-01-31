#!/usr/bin/env python3

from subprocess import check_output as bash

import sys
import re

from find_functions import find_div_boxes
from find_functions import find_figures
from find_functions import find_cell

from build_functions import my_replace
from build_functions import build_admonition_box
from build_functions import build_card_box
from build_functions import build_figure

def grep_file_index(grep_command):
    
    out_grep_command = bash(grep_command, shell=True).decode("utf-8")

    index_list = []
    for line in out_grep_command.splitlines():
        index_list.append(int(line)-1)
    
    return index_list



# Obtenemos el nombre del archivo del primer algumento de la llamada
file_name = sys.argv[1:][0]
print("===========================")
print("Input File  = ", file_name)


# Sacamalos el numero de linea del inicio de todos los cuadros con "<div class=.... alert alert-block alert...>"
command_i_start_alert_list   = 'grep -n "<div class=" '+file_name+' | grep "alert alert-block alert" |  cut -d":" -f1'
i_start_alert_list = grep_file_index(command_i_start_alert_list)


# Sacamalos el numero de linea del inicio de las <figure>
command_i_start_figure_list = 'grep -n "<figure>" ' + file_name + ' |  cut -d":" -f1'
i_start_figure_list = grep_file_index(command_i_start_figure_list)


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
index_list_list, titles_list_list = find_div_boxes(f_data, i_start_alert_list)

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
index_fig_list_list, datos_list_list = find_figures(f_data, i_start_figure_list)

############################################################################
# Comenzamos a sustituir las figuras (empezando por el final)
for i in reversed(range(len(index_fig_list_list[0]))):
    build_figure(i, f_data, index_fig_list_list, datos_list_list)


# Añadimos el tiempo de lectura en la primera linea:
command_i_first_line = 'grep -n "\\"source\\": \\[" ' + file_name + ' |  cut -d":" -f1 | head -n 1'
i_first_line = grep_file_index(command_i_first_line)
my_replace(f_data, i_first_line[0], 'source": [\n'+
                                         '    "> {sub-ref}`today` | {sub-ref}`wordcount-words` words | {sub-ref}`wordcount-minutes` min read\\n",\n'
                                         '    "\\n",\n'    )


################################################################################
## Indice

command_i_ToC_pattern = 'grep -n "## Índice" '+ file_name + ' |  cut -d":" -f1 | head -n 1'
i_ToC_pattern = grep_file_index(command_i_ToC_pattern)

if len(i_ToC_pattern) == 1:
    i_start_ToC_cell, i_ToC_start, i_ToC_end = find_cell(f_data, i_ToC_pattern[0])

    my_replace(f_data, i_ToC_start, ':::{contents}\\n",\n'+
                                        '    ":local:\\n",\n'
                                        '    ":depth: 1\\n",\n'
                                        '    ":::\\n",\n')
    for i in range(i_ToC_start+1, i_ToC_end):
        my_replace(f_data, i, '",\n')
    my_replace(f_data, i_ToC_end, '"\n')


################################################################################
## Inicio de todas las celdas

command_i_start_all_cells = 'grep -n "   \\"cell_type\\":" '+ file_name + ' |  cut -d":" -f1 '
i_start_all_cells = grep_file_index(command_i_start_all_cells)

################################################################################
## Buscamos las celdas de código con el tag
pattern_code = '_code_cell\'\'\''
command_i_pattern_code = 'grep -n "'+pattern_code+'" '+ file_name + ' |  cut -d":" -f1 '
i_pattern_code_list = grep_file_index(command_i_pattern_code)

num_cells_pattern_code = []
num_cell = 0

for i_pattern_code in i_pattern_code_list:
    found = False
    while not found:
        if i_pattern_code > i_start_all_cells[-1]:
            num_cells_pattern_code.append(len(i_start_all_cells)-1)
            found = True
        elif i_pattern_code < i_start_all_cells[num_cell]:
            num_cells_pattern_code.append(num_cell-1)
            found = True
        num_cell +=1
    num_cell -=1

print(num_cells_pattern_code)

################################################################################
###### Guardamos los cambios en un nuevo fichero

out_file = file_name[:-6]+'_lab.ipynb'

with open(out_file, 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])


'''
################################################################################
###### Eliminamos los </br>

clean_br_command = "sed -i 's/<br>//g' " + out_file
bash(clean_br_command, shell=True).decode("utf-8")

################################################################################
### Creamos un nuevo fichero {out_file}_clean con las tres celdas de título

number_head = str(int(bash('grep -n "^  }," Firts_cells.ipynb |  cut -d":" -f1 | head -n 3 | tail -n 1' , 
                                shell=True).decode("utf-8")))

bash('head -n ' +number_head+' Firts_cells.ipynb ' +' > ' + out_file + '_clean' , 
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

'''






################################################################################
### Atacamos los <deatail> sueltos (los que no estaban en un cuadro)
# Tenemos que hacerlo despues de haber reemplazado los cuadros, por eso lo 
# hacemos sobre el archivo de salida

command_i_start_details_list = 'grep -n "<details><summary>" '+out_file + ' |  cut -d":" -f1'
command_i_end_details_list   = 'grep -n "</details>" '+ out_file + ' |  cut -d":" -f1'

i_start_details_list = grep_file_index(command_i_start_details_list)
i_end_details_list = grep_file_index(command_i_end_details_list)


################################################################################
# Leemos el archivo linea a linea y modificamos los cuadros
with open(out_file, 'r') as f:
    #f_data = f.read()
    ##print(f_data[20])

    f_data=[]
    for line in f:
        ##print(line)
        f_data.append(line)
    

    for i in i_start_details_list:
        title_details = re.search(r'<i>(.*?)</i>', f_data[i]).group(1)
        my_replace(f_data, i, ':::{dropdown} '+title_details+'\\n",\n')
    
    
    
    for i in i_end_details_list:
        
        if f_data[i+1] == "   ]\n":
            my_replace(f_data, i, ':::'+'\\n"\n')
        else:
            my_replace(f_data, i, ':::'+'\\n",\n')
    

with open(out_file, 'w') as f_out:
    for k in range(len(f_data)):
        f_out.write(f_data[k])

    
print("Output file = ", out_file)
print("===========================")
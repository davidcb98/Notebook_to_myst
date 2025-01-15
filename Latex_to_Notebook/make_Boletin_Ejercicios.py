from LtN_replaces_and_others import replace_end_newtheorem, ErrorGenerico
import sys
import re

def help_message():
    ayuda = """
=======================================================================================
Help Message:

 Este script hacer un .tex a partir de otro .tex que incluya solo los Ejercicio. Estos
 deben de estar en la forma:

    \Ejercicio{
    Texto del Ejercicio
    }

 Parametros:

    - Primer argumento: ruta archivo .tex
    - Segundo argumento (opcional): ruta al archivo .bib


 Ejemplos de ejecucion:

    python Latex_to_Notebook.py my_archivo_latex.tex
    python Latex_to_Notebook.py my_archivo_latex.tex my_bibliografia.bib
=======================================================================================
    """
    print(ayuda)
    exit(0)


#####################
## Archivo tex

try:
    file_name  = sys.argv[1:][0] # Obtenemos el nombre del archivo del primer argumento de la llamada
except:
    print("\033[91m[ERROR]: No se ha pasado ningún argumento\033[0m")
    help_message()

#####################
## Archivo .bib

try:
    bib_file  = sys.argv[1:][1] # Obtenemos el nombre del archivo bib del cercer algumento de la llamada
    find_bib_file = True
except:
    find_bib_file = False

######################

find_Ejercicio = False
begin_doc_bool = False
end_doc_bool   = False


num_line_text_file = 0

Pre_begin_doc_list=[]
Ejercicios_list = []

with open(file_name, 'r') as f:
    f_data = []
    i = 0

    for line in f:
        num_line_text_file += 1

        ###############################################################################################################
        ## Cogemos solo lo que hay entre el \\begin{document} y el \\end{document}
        ###############################################################################################################
        if begin_doc_bool == False:

            Pre_begin_doc_list.append(line)

            if "\\begin{document}" in line:
                begin_doc_bool = True
            else:
                continue
        if end_doc_bool == True:
            continue



        line = line.lstrip().rstrip().replace("\\","\\\\")

        if line == "":
            line = "\n"

        if line[0] == "%":
            continue

        ########################### Ejercicio  #############################
        if "\\\\Ejercicio{" in line:

            find_Ejercicio = True

            i_start_ejercicio_in_tex   = num_line_text_file
            num_start_braket_ejercicio = len(re.findall(r'(?<!\\)\{', line))
            num_end_braket_ejercicio   = len(re.findall(r'(?<!\\)\}', line))

            Ejercicios_list.append(line.replace("\\\\","\\")+"\n")



        elif find_Ejercicio == True:
            num_start_braket_ejercicio = len(re.findall(r'(?<!\\)\{', line)) + num_start_braket_ejercicio
            num_end_braket_ejercicio   = len(re.findall(r'(?<!\\)\}', line)) + num_end_braket_ejercicio

            Ejercicios_list.append(line.replace("\\\\","\\")+"\n")


            if line == "}":
                find_Ejercicio = False

                if num_start_braket_ejercicio != num_end_braket_ejercicio:

                    message = "El numero de \"{\" y \"}\" diferentes."
                    raise ErrorGenerico(f_data, line, i_start_ejercicio_in_tex, message)
                Ejercicios_list.append("\n")

            elif num_start_braket_ejercicio == num_end_braket_ejercicio:

                message = f"El numero de \"{{\" y \"}}\" iguales, pero no se ha encontrado el final de el/la {theorem_type_in} (linea con solo un \"}}\")"
                raise ErrorGenerico(f_data, line, i_start_ejercicio_in_tex, message)

        ##################### end document #######################
        elif "\\\\end{document}" in line:
            end_doc_bool = True



out_file = file_name.replace(".tex","_ejercicios.tex")
write_path = out_file

assert file_name != out_file
assert file_name != write_path

with open(write_path, 'w') as f_out:
    for line in Pre_begin_doc_list:
        f_out.write(line)

    for line in Ejercicios_list:
        f_out.write(line)

    if find_bib_file==True:
        f_out.write("% ========================================================\n")
        f_out.write("% == Bibliografía\n")
        f_out.write("%\\nocite{*}\n")
        f_out.write("\\bibliographystyle{ieeetr}\n")
        f_out.write("\\bibliography{" + bib_file +"}\n")

    f_out.write("\\end{document}")











import re
import unicodedata

# ===========================================================================

def remove_capital_accents(string):
    # Normalizar y eliminar acentos
    normalized_string = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))

    # Convertir a minúsculas
    final_string = normalized_string.lower()

    return final_string

# ===========================================================================

class ErrorGenerico(Exception):

    def __init__(self, f_data, line, num_line_text_file, message):

        final_message = "\n" + \
                        "\033[91m=============================\033[0m\n" + \
                        "\033[91m " + message + "\033[0m\n" + \
                        "\n" + \
                        f"\033[91m Linea del .tex: {num_line_text_file}.\033[0m\n"

        if len(f_data) > 4:
            final_message = final_message + \
                      f"\033[91m    {f_data[-4]}\033[0m\n" + \
                      f"\033[91m    {f_data[-3]}\033[0m\n" + \
                      f"\033[91m    {f_data[-2]}\033[0m\n" + \
                      f"\033[91m    {f_data[-1]}\033[0m\n" + \
                      f"\033[91m    {line}\033[0m\n"

        final_message = final_message + f"\033[91m=============================\033[0m"

        self.message = final_message

        super().__init__(self.message)

# ===========================================================================

class ErrorUnrecognizedBox(Exception):

    def __init__(self, box_type):

        final_message = "\n" + \
                        "\033[91m======\033[0m\n" + \
                       f"\033[91m {box_type}: Tipo de alert-block no reconocido\033[0m\n" +\
                        "\n" +\
                        "\033[91m Este es un error en los parámetros de la funcion, no es culpa del .tex\033[0m\n" +\
                        "\033[91m======\033[0m\n"


        self.message = final_message

        super().__init__(self.message)



# =============================================================================
## Las dos siguientes funciones son para reemplazar las \label por <a id='..


def reemplazo_label(line):
    patron_lab = r"\\\\label\{(.+?)\}"

    def reemplazo_label_aux(match):
        titulo = match.group(1)
        return f"<a id='{titulo}'></a>"

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
## Para buscar un los titulos y las labels de las partes

def find_title_part(line):

    # Expresiones regulares para extraer el contenido de part y label
    part_pattern = r'\\part\{([^}]*)\}'
    label_pattern = r'\\label\{([^}]*)\}'

    # Buscar las coincidencias
    part_match = re.search(part_pattern, line)
    label_match = re.search(label_pattern, line)

    part_title = part_match.group(1)

    # Extraer los contenidos si las coincidencias se encontraron
    if label_match:
        label_content = label_match.group(1)
    else:
        label_content = ""

    return part_title, label_content



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
## Reemplazar \\begin{figure}[...] por <figure><center>
def reemplazo_begin_figure(line):

    patron_beg_fig = re.compile(r'\\\\begin{figure}(\[.*?\])?')

    # Función para reemplazar el patrón encontrado
    def reemplazo_begin_figure_aux(match):
        if match.group(1):  # Si hay opciones entre corchetes
            return '<figure><center>'
        else:  # Si no hay opciones entre corchetes
            return '<figure><center>'

    # Aplicar la sustitución
    return patron_beg_fig.sub(reemplazo_begin_figure_aux, line)



# =============================================================================
## Reemplazar \item por - y \item[1.] por 1.
def reemplazo_item(line, out_spaces):

    patron = re.compile(r'\\\\item(\[(.*?)\])?')

    # Función para reemplazar el patrón encontrado
    def reemplazar_item_aux(match):
        if match.group(1):  # Si hay una opción entre corchetes
            return out_spaces + match.group(2)
        else:  # Si no hay opciones entre corchetes
            return out_spaces + "-"

    # Aplicar la sustitución
    return patron.sub(reemplazar_item_aux, line)






# =============================================================================
## Los \cite{
# Separamos los \cite{bib_..., bib_..., ...} en \cite{bib_...},\cite{bib_...}, ...

def split_cites(line):
    # Expresión regular para encontrar y reemplazar el formato
    patron = re.compile(r'\\cite{([^}]+)}')

    def reemplazar_citas(match):
        citas = match.group(1).split(',')
        citas = [cita.strip() for cita in citas]  # Eliminar espacios alrededor de las citas
        return ','.join(f'\\cite{{{cita}}}' for cita in citas)

    return patron.sub(reemplazar_citas, line)


def reemplazo_cite(line, cites_dic, path_bib_ipynb):

    def reemplazo_cite_aux(match):
        texto = match.group(1)

        return f"[[{cites_dic[texto]}]]({path_bib_ipynb}#{texto})"

    patron_textit = r"\\\\cite\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})+)\}"
    return re.sub(patron_textit, reemplazo_cite_aux, line)

def reemplazo_cite_full(f_data, i_start_write, i_end_write, cites_dic, path_bib_ipynb):

    for i in range(i_start_write, i_end_write):
    #for i in range(len(f_data)):
        line = f_data[i]
        if "\\\\cite{" in line:

            line = split_cites(line)
            line = reemplazo_cite(line, cites_dic, path_bib_ipynb)

            f_data[i] = line

# =============================================================================
## Eliminar los \vspace{...}
def delete_vspace(line):
    patron_vspace = r"\\\\vspace\{[^{}]*\}"
    return re.sub(patron_vspace, '', line)

# =============================================================================
## Eliminar los \hspace{...}
def delete_hspace(line):
    patron_hspace = r"\\\\hspace\{[^{}]*\}"
    return re.sub(patron_hspace, '', line)

# =============================================================================
## Eliminar lo que hay despues de "%" (sin contar "\%")
def delete_comments(line):
    patron_comments = r"(?<!\\)%.*"
    return re.sub(patron_comments, '', line)



# =============================================================================

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


# =============================================================================

def replace_start_newtheorem(f_data, line, theorem_type_in, theorem_type_out, box_type):

    if box_type == "info":
        color_text = "navy"
    elif box_type == "success":
        color_text = "DarkGreen"
    elif box_type == "danger":
        color_text = "DarkRed"
    elif box_type == "warning":
        color_text = "#4B5320"
    else:
        raise ErrorUnrecognizedBox(box_type)



    if "\\\\label{" in line:
        line = reemplazo_label(line)

        pre_label = line.split("<a id='")[0]
        label     = "<a id='" + line.split("<a id='")[1]

        line = label + '\\n",\n' + \
                pre_label

        new_line = '    "<div class=\\"alert alert-block alert-' + box_type + '\\">\\n",\n' + \
                   '    "<p style=\\"color: '+ color_text +';\\">\\n",\n' + \
                  f'    "<b>{theorem_type_out}</b>:'



    else:
        new_line = '<div class=\\"alert alert-block alert-' + box_type + '\\">\\n",\n' + \
                   '    "<p style=\\"color: '+ color_text +';\\">\\n",\n' + \
                  f'    "<b>{theorem_type_out}</b>:'

    text_to_replace = "\\\\" + theorem_type_in + "{"
    line = line.replace(text_to_replace, new_line)

    return line


def replace_end_newtheorem(f_data, line, find_bool, i_start_in_tex, num_start_braket, num_end_braket, theorem_type_in):

    if line == "}":
        find_bool = False

        if num_start_braket != num_end_braket:

            message = "El numero de \"{\" y \"}\" diferentes."
            raise ErrorGenerico(f_data, line, i_start_in_tex, message)

        line = '</p></div>\\n",\n' + \
               '    "\\n'


    elif num_start_braket == num_end_braket:

        message = f"El numero de \"{{\" y \"}}\" iguales, pero no se ha encontrado el final de el/la {theorem_type_in} (linea con solo un \"}}\")"
        raise ErrorGenerico(f_data, line, i_start_in_tex, message)

    return line, find_bool





























#!/usr/bin/env python3

from subprocess import check_output as bash
import unicodedata

import sys
import re



def remove_capital_accents(string):
    # Normalizar y eliminar acentos
    normalized_string = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))

    # Convertir a minúsculas
    final_string = normalized_string.lower()

    return final_string









def find_div_boxes(f_data, i_Lines_start):
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
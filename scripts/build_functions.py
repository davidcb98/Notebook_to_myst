#!/usr/bin/env python3

def my_replace(f_data, i_line, new_text):

    #print("------> ", new_text)

    # Encontrar la posición de la primera comilla doble
    index_firts_quote = f_data[i_line].find('"')

    # Realizar la sustitución
    f_data[i_line]= f_data[i_line][:index_firts_quote + 1] +new_text 
        #f_data[i_start_p][f_data[i_start_p].find('\n', indice_primera_comilla + 1):] 



def build_admonition_box(i, f_data, index_list_list, titles_list_list, Class):

    i_start         = index_list_list[0][i]  
    i_end           = index_list_list[1][i]  
    i_start_p       = index_list_list[2][i]  
    i_end_p         = index_list_list[3][i]
    i_start_details = index_list_list[4][i]
    i_end_details   = index_list_list[5][i]
    i_title         = index_list_list[6][i]
       
    title_details   = titles_list_list[0][i]
    title           = titles_list_list[1][i]
    #title_lowercase = titles_list_list[2][i]
    subtitle        = titles_list_list[3][i]
    
    #for i in range(i_end-i_start+1):
    #    print({f_data[i_start+i]})
    #print("")

    ############################################################################
    ###### Empezamos a sustituir por el final

    ### </div>    
    if f_data[i_end + 1] == "   ]\n":
        my_replace(f_data, i_end, '::::'+'\\n"\n' )
    else:
        my_replace(f_data, i_end, '::::'+'\\n",\n' )

    ### </p>
    if i_end_p > 0:
        if i_end > i_end_p:
            my_replace(f_data, i_end_p, ''+'\\n",\n' )

    ### </details>
    if i_end_details > 0:
        if i_end > i_end_details:
            my_replace(f_data, i_end_details, ':::'+'\\n",\n')

    ### <detail>
    if i_start_details > 0:
        my_replace(f_data, i_start_details, ':::{dropdown} '+ title_details+'\\n",\n')

    #### TITLE 
    my_replace(f_data, i_title,''+'\\n",\n')
    
    ### <p style=...>
    if i_start_p > 0:
        if i_start < i_start_p:
            my_replace(f_data, i_start_p, ''+'\\n",\n')

    #### <div class...> o <div class...><p style...>
    if subtitle == None:
        my_replace(f_data, i_start, '::::{admonition} '+ title+'\\n",\n' + '    ":class: '+Class+'\\n",\n')
    else:
        my_replace(f_data, i_start, '::::{admonition} '+ title + ' (' + subtitle + ') '+'\\n",\n' + '    ":class: '+Class+'\\n",\n')

    #print("")
    #for i in range(i_end-i_start+1):
    #    print({f_data[i_start+i]})
    #print("")


def build_card_box(i, f_data, index_list_list, titles_list_list):
    i_start         = index_list_list[0][i]  
    i_end           = index_list_list[1][i]  
    i_start_p       = index_list_list[2][i]  
    i_end_p         = index_list_list[3][i]
    i_start_details = index_list_list[4][i]
    i_end_details   = index_list_list[5][i]
    i_title         = index_list_list[6][i]
       
    title_details   = titles_list_list[0][i]
    title           = titles_list_list[1][i]
    #title_lowercase = titles_list_list[2][i]
    subtitle        = titles_list_list[3][i]
    
    #for i in range(i_end-i_start+1):
    #    print({f_data[i_start+i]})
    #print("")

    ############################################################################
    ###### Empezamos a sustituir por el final

    ##################################
    ######## </div> o </p></div>

    ### </div>    
    if f_data[i_end + 1] == "   ]\n":
        my_replace(f_data, i_end, '::::'+'\\n"\n' )
    else:
        my_replace(f_data, i_end, '::::'+'\\n",\n' )


    if i_end_p > 0:
        ##############################
        ######## </p>
        if i_end > i_end_p:
            my_replace(f_data, i_end_p, ''+'\\n",\n' )


    if i_end_details > 0:
        ##############################
        ######## </details>
        if i_end > i_end_details:
            my_replace(f_data, i_end_details, ':::'+'\\n",\n')

    if i_start_details > 0:
        ##############################
        ######## <detail>
        my_replace(f_data, i_start_details, ':::{dropdown} '+ title_details+'\\n",\n')

    my_replace(f_data, i_title, '^^^\\n",\n')
    
    if i_start_p > 0:
        ##############################
        ######## <p style=...>

        if i_start < i_start_p:
            my_replace(f_data, i_start_p, ''+'\\n",\n')

    ##############################
    ######## TITLE and <div class...> o <div class...><p style...>
    
    if subtitle == None:
        my_replace(f_data, i_start, '::::{card} \\n",\n'+'    "**'+title+'**: '+' \\n",\n')
    else:
        my_replace(f_data, i_start, '::::{card} \\n",\n'+'    "**'+title+'**: *'+ subtitle + '* '+'\\n",\n')

    #print("")
    #for i in range(i_end-i_start+1):
    #    print({f_data[i_start+i]})
    #print("")

def build_figure(i, f_data, index_fig_list_list, datos_list_list):

    i_start   = index_fig_list_list[0][i]
    i_end     = index_fig_list_list[1][i]
    i_label_a = index_fig_list_list[2][i]
    i_img     = index_fig_list_list[3][i]
    i_caption = index_fig_list_list[4][i]

    path_fig    = datos_list_list[0][i]
    align_fig   = datos_list_list[1][i]
    width_fig   = datos_list_list[2][i]
    caption_fig = datos_list_list[3][i]
    label_fig   = datos_list_list[4][i]
        
    ############################################################################
    ###### Empezamos a sustituir por el final


    if f_data[i_end + 1] == "   ]\n":
        my_replace(f_data, i_end, '::::'+'\\n"\n' )
    else:
        my_replace(f_data, i_end, '::::'+'\\n",\n' )
    

    if i_caption != 0 and caption_fig != None:
        my_replace(f_data, i_caption, caption_fig +'\\n",\n')
    
    my_replace(f_data, i_img, 
               ':width: ' + width_fig + '\\n",\n' + 
               '    ":align: ' + align_fig + '\\n",\n')
        
    if i_label_a != 0 and label_fig != None:
        my_replace(f_data, i_label_a, ':name: ' + label_fig +'\\n",\n')

    my_replace(f_data, i_start, '::::{figure} '+ path_fig +'\\n",\n' )



def build_tabset(f_data, i_start_next_cell, name_code_list ,content_list):

    def build_tab_item(f_data, i_start_next_cell, name_code, content):
        f_data[i_start_next_cell] = \
            '    ":::\\n",\n' + \
            '    "::::\\n",\n' + \
            f_data[i_start_next_cell]
        
        for line in reversed(content):
            f_data[i_start_next_cell] = line + f_data[i_start_next_cell]
        
        f_data[i_start_next_cell] = \
            '    "::::{tab-item}'+name_code+'\\n",\n' + \
            '    ":::python\\n",\n' + \
            f_data[i_start_next_cell]
    

    f_data[i_start_next_cell] = '    ":::::\\n"\n' + '   ]\n' + '  },\n' + f_data[i_start_next_cell] 

    for i in reversed(range(len(name_code_list))):
        content   = content_list[i]
        name_code = name_code_list[i]
        
        content[-1] = content[-1][:-1]+',\n'

        build_tab_item(f_data, i_start_next_cell, name_code, content)
    
    f_data[i_start_next_cell] = \
        '  {\n' + \
        '   "cell_type": "markdown",\n' + \
        '   "metadata": {},\n' + \
        '   "source": [\n' + \
        '    ":::::{tab-set}\\n",\n' + f_data[i_start_next_cell]
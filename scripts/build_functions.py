#!/usr/bin/env python3

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



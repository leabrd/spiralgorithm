# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 12:04:46 2022

@author: leabr
"""

def set_size(width, aspect = 1):
    
    '''
    This function sets aesthetic figure dimensions to avoid scaling in latex.
    
    :param width: width of the figure in pt
    :type width: float
    :param fraction: fraction of the width for the figure to occupy, defaults to 1
    :type fraction: float, optional
    :param aspect: aspect ratio, defaults to 1
    :type aspect: float, optional
    :return: fig_dim,dimensions of the figure in inches
    :rtype: tuple
    '''
    
    fraction = 1
    # Width of figure
    fig_width_pt = width * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27
    # Golden ratio to set aesthetic figure height
    golden_ratio = (5**.5 + 1) / 2
    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio
    fig_dim = (fig_width_in, fig_height_in * aspect)
    
    return fig_dim


def relative_stacked_bar_plot_CA_subsystem (recipe, master_output):
    
    
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from brightway2 import methods
    from colours import graph_colours
    
    abbreviation_list = []
    
    # don't try to plot if False in the recipe
    if not recipe['analyses']['CA_subsystems']['relative_stacked_bar_plot']:
        return abbreviation_list
    
    nomenclature_dict = {}
    database_list = recipe['CA_subsystems']['relative_stacked_bar_plot']['databases']
    for database in database_list:
        
        if database != 'S1' or database != 'S2' or database != 'S3':
            nomenclature_dict[database] = database[:5].replace('db_','').capitalize()
            
        if 'transport' in database: 
            name = str(database[:13].replace('db_','').replace('_','').capitalize() + ' ' + database[:16].replace('db_','').replace('transport_',''))
            nomenclature_dict[database] = name
            
        if 'infrastructures' in database:
            nomenclature_dict[database] = database[:18].replace('db_','').capitalize()
        
        if 'operation' in database:
            nomenclature_dict[database] = database[:12].replace('db_','').capitalize()
        
    raw_data = {}

    for database in database_list:
        subsystem = nomenclature_dict[database]
        raw_data[subsystem] = {}
                
        for method in master_output.keys():
            
            lca_score = master_output[method][database]['total_lca_score']
            raw_data[subsystem][method[2]] = lca_score
              
                
    # find the methods unit
    unit_list = []
        
    for method in recipe['CA_subsystems']['relative_stacked_bar_plot']['lcia_methods']:
        unit = methods[method]['unit']
        unit_list.append(unit) 

    fig = plt.figure(figsize = set_size(500,0.5))
    ax = fig.add_subplot(111)
    
    method_list = [method[2] for method in master_output.keys()]

    nomenclature_table = ['S1', 'S2', 'S3', 'Infr.', 'Op.', 'Tr.S12', 'Tr.S23']

    df = pd.DataFrame(raw_data, columns = nomenclature_dict.values(), index = method_list)
    print(df.columns)
    
    df_latex = df.copy()
    df_latex.columns = nomenclature_table
    
    
    df['total'] = df.sum(axis=1)
    # add a column with the unit of the impact category
    df.insert(0,'unit', unit_list)
    
    # THIS IS BAD CODE BUT IT WILL WORK
    df_latex['total'] = df_latex.sum(axis=1)
    # add a column with the unit of the impact category
    df_latex.insert(0,'unit', unit_list)
    
    period_number = database[-1:]
        

    
    df_latex.to_excel(str(recipe['rdir'] + "/CA_subsystem/LCA-scores-CA-subsystems-period%s.xlsx"%period_number))
    
    caption = ('Contribution of each subsystem to the overall impacts of the biorefinery for the period %s.' %period_number)
    label = 'tab:lca_score_subsystems'
    df_latex.to_latex(recipe['rdir'] + '/CA_subsystem/LCA-scores-CA-subsystems-period%s.tex'%period_number,
            caption = caption,
            label = label,
            float_format="%.3f",
            longtable = True)
     
    # plot
    ind = np.arange(len(list(master_output.keys())))*1.5
    bar_width = 0.85
    name_list = []
         
    # create a name list (x labels) by selecting only the method abbreviation
    for i in range(len(list(master_output.keys()))):
        name = list(master_output.keys())[i][2]
        name_list.append(name)
        
    y_minus_1 = np.array([0]*len(ind))
        
    for i in range(len(list(nomenclature_dict.values()))): 
    
        # subsystem
        subsystem = list(nomenclature_dict.values())[i]
    
        # LCA score in % contribution
        y = [j / k * 100 for j,k in zip(df[subsystem], df['total'])]
    
        # if it is the first subsystem,just plot it 
        if i == 0:
    
            ax.bar(x=ind, 
                   height=[i for i in y], 
                   width=bar_width, 
                   bottom = 0,
                   align = 'center',
                   label = subsystem,
                   #color = activity_colours[i],
                   color = graph_colours(list(nomenclature_dict.values()))[i],
                   edgecolor=None)
            
        # if it isn't plot it on top of the previous one
        else:
            ax.bar(x=ind,
                   height=[i for i in y], 
                   width=bar_width, 
                   bottom= y_minus_1,
                   #label = [i[1] for i in y][0], 
                   label = subsystem,
                   #color = activity_colours[i],
                   color = graph_colours(list(nomenclature_dict.values()))[i],
                   edgecolor=None)
            
        y_minus_1 = y_minus_1 + np.array([i for i in y])   
    
    # Create a description to put under figure title in Latex    
    for i in range(len(list(master_output.keys()))):
        name = list(master_output.keys())[i][1]
        abbreviation = list(master_output.keys())[i][2]
        abbreviation_list.append(name.strip() + ': ' + abbreviation.strip())
        
    abbreviation_list = str(abbreviation_list).replace("'",'')
    abbreviation_list = str(abbreviation_list).replace(',','\n')
                   
    # # set the ticks position
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
        
    # # hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
        
    ax.set_ylabel('Contribution to the overall impact of the biorefinery (%)')
    ax.set_xlabel('Impact categories')
    ax.set_xticks(ind,name_list, rotation=45)
        
    plt.legend (loc='lower center', 
                #bbox_to_anchor=(0.5,1), 
                bbox_to_anchor=(0.5,1), 
                ncol=4,
                frameon=False)
    fig.tight_layout()
    
    #plt.text(x = 0.99, y = 0, s = str(abbreviation_list).strip('[]').strip("'"), transform = ax.transAxes, va = 'bottom', ha = 'left')
    plt.savefig(str(recipe['rdir'] + "/CA_subsystem/CA-subsystem-relative-stacked-bar-chart-period%s.pdf"%period_number))
                
    plt.show()
        

    return abbreviation_list

def diff_LCA_scores_CA_subsystem(recipe):
    
    
    import pandas as pd
    import numpy as np
    try:
    	table1 = pd.read_excel(str(recipe['rdir'] + "/CA_subsystem/LCA-scores-CA-subsystems-period1.xlsx"))
    	table2 = pd.read_excel(str(recipe['rdir'] + "/CA_subsystem/LCA-scores-CA-subsystems-period2.xlsx"))   
    except:
    	print('Could not load Table 1 and/or 2 - raising exception')
    	return recipe
    
    # selectedMethod = 'GWP100'


    
    # del table1['Unnamed: 0']
    # del table2['Unnamed: 0']
    
    del table1['unit']
    del table2['unit']
    
    del table1['total']
    del table2['total']

    # table1 = table1[table1['Method'] == selectedMethod]
    # table2 = table2[table2['Method'] == selectedMethod]
    
    # del table1['Method']
    # del table2['Method']
    
    
    table1.reset_index(inplace = True)
    
    table2.reset_index(inplace = True)
    
    
    newtable = pd.DataFrame([])

    df_diff = (table2.set_index('Unnamed: 0') - table1.set_index('Unnamed: 0')) 
    
    
    totaldf = pd.DataFrame([])
    for subsystem in df_diff.columns:
        totaldf[subsystem] = [np.nansum(df_diff[subsystem])]
        
    totaldf.index = ['Total']   

    df_diff = pd.concat([df_diff,totaldf],ignore_index=False)
  
    del df_diff['index']
    
    df_diff['Total'] = [np.sum(df_diff.T[i]) for i in df_diff.index]
    
    # pm = lambda x: '+'+str(round(x,3)) if x>0 else '-'
    for index, row in df_diff.iterrows():
        for subsystem in df_diff.columns:
            
            value =  df_diff.at[index,subsystem]
            if  not np.isfinite(value):
                df_diff.at[index,subsystem] = '-'
            elif value<0:
                df_diff.at[index,subsystem] = '\cellcolor{green!10}$\downarrow$ %.1e ' % value
            elif value>0:
                 df_diff.at[index,subsystem] = '\cellcolor{red!10} $\\uparrow$ %.1e ' % value

    label = 'table:LCA_scores_per_exchange_diff_d'
    caption = 'Difference of contribution of the subsystems to the overall environmental impacts of the biorefinery between periods 1 and 2. ' 
    
    df_diff.to_latex(str(recipe['rdir'] + '/CA_subsystem/LCA_scores_per_subsystem_diff.tex') ,
                         label = label,
                         caption = caption,
                         column_format= 'l' + 'c'* (len(df_diff.columns)-1)+'|c',
                         na_rep = '-',
                          escape = False,
                         # float_format="{:0.1e}".format,
                         
                         longtable = False, index = True)
    
    df_diff.to_excel(str(recipe['rdir'] + '/CA_subsystem/LCA_scores_per_subsystem_diff.xlsx'))
    
    
    return recipe
    
    
    
def bar_chart_CA_subsystems_specific_IC (recipe, master_output):
    
    '''
    Plot a bar chart showing the contribution of each subsystem to a specific
    impact category. Not realative and showing the "real" values (e.g. kg CO2-eq)
    :param LCA_scores_per_subsystem_dict: DESCRIPTION
    :type LCA_scores_per_subsystem_dict: TYPE
    :param recipe: DESCRIPTION
    :type recipe: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    '''
    
    # don't try to plot if False in the recipe
    if not recipe['analyses']['CA_subsystems']['bar_chart_one_ic']:
        return recipe

    import matplotlib.pyplot as plt
    import numpy as np
    from colours import graph_colours
    from brightway2 import methods
    
    # plt.rcParams.update({'font.size': 7})
    # create a pie chart for each impact category listed in the YAML file
    for method in recipe['CA_subsystems']['bar_chart_one_ic']['lcia_methods']: 
        
        height = []
        subsystem_lst = []
        
        residual = {}
        
        residual['tech_1'] = 0
        
        residual['tech_2'] = 0
        
        
        residual_db = ['operation','transport']
        # calculate the contribution of each subsystems (1 subsystem = 1 database)        
        for database in recipe['CA_subsystems']['bar_chart_one_ic']['databases']:
            
            
            
            lca_score = master_output[method][database]['total_lca_score']
            
            if any([i in database for i in residual_db]):
                for key in residual.keys():
                    if key in database:
                        residual[key]+=lca_score
            else:
                height.append(lca_score)
                subsystem_lst.append(recipe['nomenclature'][database])
        
        
        height+=[residual['tech_1']] 
        height+=[residual['tech_2']] 
        
        subsystem_lst+=['Res_1']
        subsystem_lst+=['Res_2']
        height_abs = [abs(i) for i in height]
        
        colours = graph_colours(subsystem_lst)
        x_pos = np.arange(len(height_abs))
        
        
        ss = [i.split('_')[0] for i in subsystem_lst]
        
        color_ss = dict(zip(list(set(ss)),colours))
        
        colours = [color_ss[s] for s in ss]
        
        # make figure and assign axis objects
        fig = plt.figure(figsize = set_size(500,0.5))
        ax = fig.add_subplot(111)

        ax.bar(x = x_pos,
               height = height_abs, 
               color = colours,
               edgecolor=None)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels([i.replace('_',' ') for i in subsystem_lst])
  
        # # hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # ylabel = str(method) + '[' + str(methods[method]['unit']) + ']'
        # ylabel = str(method[1:]) + ' [' + str(methods[method]['unit']) + ']'
        
        ylabel =  str(methods[method]['unit'])
        ax.set_ylabel(ylabel.replace("'","").replace('(','').replace(')',''))
        
        
        if max(height_abs)<1e-1:
            ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        for i, v in list(zip(x_pos,height_abs)):
            if max(height_abs)<1e-1:
                ax.text(i, v,'%.1e' % v, color='black',ha = 'center',va ='bottom')
            else:
                ax.text(i, v,'%.1f' % v, color='black',ha = 'center',va ='bottom')
        
        title = str(method[1:]).replace("'","").replace(')','').replace('(','')
        title = title.split(',')[0] + ' (' + title.split(',')[1].strip() + ')' 
        title  = title[0].capitalize() + title[1:]
        ax.set_title(title)
        fig.tight_layout()
        
        plt.savefig(str(recipe['rdir'] + "/CA_subsystem/bar_chart_" + method[2] + ".pdf"))
                     
        # show plot
        fig.show()
           
    return recipe
    

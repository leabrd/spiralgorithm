# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 20:58:38 2022

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


    
def stacked_bar_plot_comparison (recipe, LCA_scores_dict_processes):
    
    
    abbreviation_list = []
    
    # don't try to plot if False in the recipe
    if not recipe['analyses']['CA_processes']['stacked_bar_plot_comparison']:
        return abbreviation_list
    
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from brightway2 import methods
    from colours import graph_colours
    
    # create a chart for each impact category listed in the YAML file
    for method in recipe['CA_processes']['stacked_bar_plot_comparison']['lcia_methods']: 
                
        unit = methods[method]['unit']
        print('LCIA impact category: %s (%s)' % (method[1], method[2]))
        
        # Get the LCA scores from the results dictionary
        database = recipe['CA_processes']['stacked_bar_plot_comparison']['databases'][0]
        activity_list = recipe['all_databases'][database]['CA_activities']
        raw_data = {}
        
        for activity in activity_list:
            
            print('\nActivity: %s' %activity)
            
            result_list = []
            
            for database in recipe['CA_processes']['stacked_bar_plot_comparison']['databases']:
                                
                score = LCA_scores_dict_processes[method][database][activity]['individual_LCA_score']
                print('LCA score %s: %.4f %s' %(database, score, unit))
                result_list.append(score)
                
            raw_data[activity] = result_list

                
            print(raw_data)
                
            df = pd.DataFrame(raw_data, columns = recipe['all_databases'][database]['CA_activities'], index = recipe['CA_processes']['stacked_bar_plot_comparison']['databases']).abs()
            df['total'] = df.sum(axis=1)
            df.insert(0,'unit',unit)
            df.to_excel(str(recipe['rdir'] + "/CA_activity/LCA_scores_.xlsx"))
            df.to_latex(str(recipe['rdir'] + "/CA_activity/LCA_scores_.tex"))

        # plot
        
        fig = plt.figure(str(method),figsize = set_size(500,0.5))
        #
        
        ax = fig.add_subplot(111, aspect = 'auto')
        
        ind = np.arange(len(recipe['CA_processes']['stacked_bar_plot_comparison']['databases']))
        print('indice plotting: %s' %ind)
        ind2 = ind*0.3
        print('indice plotting reduced: %s' %ind2)        
        
        bar_width = 0.15
        name_list = []
                
        name_list = list(recipe['CA_processes']['stacked_bar_plot_comparison']['databases'])
        name_list_short = []
        for i in name_list:
            name_list_short.append(recipe['nomenclature'][i])
        print(name_list)
        print(name_list_short)
        # use the nomenclature to shorten the names

#         # create a name list (x labels) by selecting only the method abbreviation
#         for i in range(len(recipe['all_databases'].keys())):
#             name = list(recipe['all_databases'].keys())[i][2]
#             name_list.append(name)
            
       #-------------------------------------------------------------------------    
        # STACK THE BARS PER ACTIVITY
    
        y_minus_1 = np.array([0]*len(ind))
        
        print(y_minus_1)
        
        for i in range(len(recipe['all_databases'][database]['CA_activities'])): 
            
            print(i)
    
            # activity
            activity = recipe['all_databases'][database]['CA_activities'][i]
            
            print(activity)
    
            # LCA score for current activity in format  [ [database,activity,lca score] , ... ] 
            #y = [j / k * 100 for j,k in zip(df[activity], df['total'])]
            print(df[activity])
            y = [i for i in df[activity]]
    
            # if it is the first activity,just plot it 
            print(y)
            
            if len(ind)==0:
                continue
            
            if i == 0:
    
                ax.bar(x=ind2, 
                       height=y, 
                       width=bar_width, 
                       bottom = [0]*len(ind),
                       align = 'center',
                       label = activity.capitalize(),
                       #color = activity_colours[i],
                       color = graph_colours(recipe['all_databases'][database]['CA_activities'])[i],
                       edgecolor=None)
            
            # if it isn't plot it on top of the previous one
            else:
                ax.bar(x=ind2,
                       height=y, 
                        width=bar_width, 
                        bottom= y_minus_1,
                        #label = [i[1] for i in y][0], 
                        label = activity.capitalize(),
                        #color = activity_colours[i],
                        color = graph_colours(recipe['all_databases'][database]['CA_activities'])[i],
                        edgecolor=None)
            
            y_minus_1 = y_minus_1 + np.array([i for i in y])   
            
        # Create a description to put under figure title in Latex
        abbreviation_list = []
        
        for i in range(len(list(LCA_scores_dict_processes.keys()))):
            
            name = list(LCA_scores_dict_processes.keys())[i][1]
            abbreviation = list(LCA_scores_dict_processes.keys())[i][2]
            abbreviation_list.append(name.strip() + ': ' + abbreviation.strip())
            
        abbreviation_list = str(abbreviation_list).replace("'",'')
        abbreviation_list = str(abbreviation_list).replace(',','\n')
    
        # # set the ticks position
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        
        # # hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        ax.set_ylabel('LCA score (%s per FU)' %unit)
        ax.set_xlabel('Database scenario')
        ax.set_xticks(ind2,name_list_short, rotation=0)
        ax.set_xlim(min(ind2)-bar_width,max(ind2)+bar_width)

        
        ax.legend (loc='lower center', 
                    bbox_to_anchor=(0.5,1), 
                    #ncol=len(recipe['all_databases'][database]['CA_activities'])//2,
                    ncol=3,
                    frameon=False)
        
        fig.tight_layout()
        #plt.text(x = 0.99, y = 0, s = str(abbreviation_list).strip('[]').strip("'"), transform = ax.transAxes, va = 'bottom', ha = 'left')
        
        plt.savefig(str(recipe['rdir'] + "/CA_activity/stacked_bar_chart_" + database + '_' + method[2] + ".pdf"))
                
        plt.show()


    return abbreviation_list        


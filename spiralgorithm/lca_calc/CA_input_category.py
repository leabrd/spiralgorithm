#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 10:10:36 2023

@author: leabraud
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


    
def stacked_bar_plot_input_category (recipe, LCA_scores_dict):
    

    
    # don't try to plot if False in the recipe
    if not recipe['analyses']['CA_input_category']['stacked_bar_plot']:
        return []
    
    
        
    abbreviation_list = []
    
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from brightway2 import methods
    from colours import graph_colours
    
    # create a chart for each impact category listed in the YAML file
    
    # Get a lable for each database ... e.g. db_s1tecth_1 => S1
    
    db_label = list(set(i.replace('db_','')[:-1] for i in recipe['CA_input_category']['stacked_bar_plot']['databases']))

    shortenNames = {'chemicals':'Chem.', 'energy':'Ener.', 
                    'equipment':'Equip.', 'construction':'Con.',
                    'nutrient':'Nutr.', 'packaging':'Pack.', 
                    'transport':'Trans.', 'waste':'Waste', 'water':'Water'}
   
    for db_l in db_label:
        database = [i for i in recipe['CA_input_category']['stacked_bar_plot']['databases'] if db_l[:-1] in i]
        raw_data = {}
        for db in database:
            raw_data[db] = {}
            for method in recipe['CA_input_category']['stacked_bar_plot']['lcia_methods']:
           
            
                raw_data[db][method] = {} 
             
                        
                unit =   methods[method]['unit']
              
                #input_categories = [i for i in plot_dict if i != 'database identification']
                
                print('LCIA impact category: %s (%s)' % (method[1], method[2]))
                
                # Get the list of input categories
                # for database in LCA_scores_dict.keys(): 
                    
                input_list = [i for i in LCA_scores_dict[db][method].keys() if i != 'database identification']
    
            
            
                for input_cat in input_list:
                    
                    print('\nInput category: %s' %input_cat)
                    
                    # result_list = []
                    
                    
                                        
                    score = LCA_scores_dict[db][method][input_cat]
                    print('LCA score %s: %.4f %s' %(db, score, unit))
                    # result_list.append(score)
                        
                    raw_data[db][method][input_cat] = score
                    raw_data[db][method][input_cat+'_unit'] = unit
                    # raw_data[db][method][input_cat]['unit'] = unit
        
                # print(raw_data)
                 
    
        df_series = []
        row = 0
        
        methodExplainations = {}
        
        for method in raw_data.keys():
       
            df_method = pd.DataFrame.from_records(raw_data[method])
            
   
            for s in df_method.columns: 
                # df_method = pd.DataFrame([])
              

                
                
                series  = df_method[s].T
                
                units  = [series[i]  for i in series.index if 'unit' in i]
                unit  = list(set(units))
                
                slabel = str(s[2]).replace('_','-')
                
                
                if slabel not in methodExplainations:
                    methodExplainations[slabel] = s[1]
          
                if len(unit)>1:
                    print('Inconsitent units, contact Sean')
                    exit()
                unit = unit[0].replace('square meter' ,'m$^{2}$').replace('m3' ,'m$^{3}$')
                    
                for idx in series.index:
                    if 'unit' in idx:
                        del series[idx]
                    
                    
                newSeries = pd.DataFrame({'Impact Catagory': slabel,
                                          'Unit': unit,
                                          'S':method} | dict(series) |
                                         {'Total':sum(dict(series).values()) },index = [0])
                
                df_series.append(newSeries)
                
                row+=1
                
                      
        df = pd.concat(df_series,ignore_index=True)
        
        
        #  Rename scenarios
        renameS = {}
        
        for i in list(set(df['S'])):
            newName = i.split('_')[-1]#
            renameS[i]=newName
            
        df.replace(renameS,inplace = True)
        
        df.sort_values(by =['Impact Catagory','S'],inplace = True)
        
        df.reset_index(inplace = True)
        for i in df.index:
            if i % 2 != 0:
                df.at[i,'Impact Catagory'] = ''
                df.at[i,'Unit'] = ''
        
        df.rename(columns = {'Impact Catagory':' '},inplace = True)
        
        df.replace({0:'-'},inplace = True)
        
        
        df.rename(columns = shortenNames,inplace = True)
        
       
        
        del df['index']
        

         #  df = pd.DataFrame(raw_data, columns = input_list, index = recipe['CA_input_category']['stacked_bar_plot']['databases']).abs()
          # df['total'] = df.sum(axis=1)
         # df.insert(0,'unit',unit)
         # db_name = recipe['CA_input_category']['stacked_bar_plot']['databases'][0][:5]
        # df.to_excel(str(recipe['rdir'] + '/CA_input_category/LCA_scores_' + db_name + '.xlsx'))
        # df.to_csv(str(recipe['rdir'] + '/CA_input_category/LCA_scores_' + db_name + '.csv'),float_format = '%.1e')
        
            
        label = 'table:LCA_scores_per_input_cat_%s' % db_l 
        caption = 'LCA scores per input category for %s. \\textbf{Abbreviations}: ' % db_l
        
        for k, v in shortenNames.items():
            
            caption+= '%s = %s, ' % (v,k[0].title() + k[1:])
        caption = caption[:-2] + '.'
        
        caption+=' \\textbf{Impact categories}: '
        
        for k, v in methodExplainations.items():
            
            caption+= '%s: %s, ' % (k,v[0].title() + v[1:])
            
        caption = caption[:-2] + '.'
        
        df.to_latex(str(recipe['rdir'] + '/CA_input_category/LCA_scores_per_input_category_%s.tex' % db_l[:-1]) ,
                             label = label,
                             caption = caption,
                             escape  = False,
                             float_format="{:0.1e}".format,
                             column_format=  'c'* (len(df.columns)-1)+'|c',
                           
                             longtable = True, 
                             index = False)
        
        df.to_excel(recipe['rdir'] + '/CA_input_category/LCA_scores_per_input_category_%s.xlsx' % db_l[:-1])

        # stop
     # plot
     
    #  fig = plt.figure(str(method),figsize = set_size(500,0.5))
    #  #
     
    #  ax = fig.add_subplot(111, aspect = 'auto')
     
    #  ind = np.arange(len(recipe['CA_input_category']['stacked_bar_plot']['databases']))
    #  print('indice plotting: %s' %ind)
    #  ind2 = ind*0.3
    #  print('indice plotting reduced: %s' %ind2)        
     
    #  bar_width = 0.15
    #  name_list = []
             
    #  name_list = list(recipe['CA_input_category']['stacked_bar_plot']['databases'])
    #  name_list_short = []
    #  for i in name_list:
    #      name_list_short.append(recipe['nomenclature'][i])
    #  print(name_list)
    #  print(name_list_short)

    # #-------------------------------------------------------------------------    
    #  # STACK THE BARS PER ACTIVITY
 
    #  y_minus_1 = np.array([0]*len(ind))
     
    #  print(y_minus_1)
     
    #  for i in range(len(input_list)): 
         
    #      print(i)
 
    #      # input category
    #      input_category = input_list[i]
         
    #      print(input_category)
 
    #      # LCA score for current activity in format  [ [database,activity,lca score] , ... ] 
    #      #y = [j / k * 100 for j,k in zip(df[activity], df['total'])]
    #      print(df[input_category])
    #      y = [i for i in df[input_category]]
 
    #      # if it is the first activity,just plot it 
    #      print(y)
         
    #      if len(ind)==0:
    #          continue
         
    #      if i == 0:
 
    #          ax.bar(x = ind2, 
    #                 height = y, 
    #                 width = bar_width, 
    #                 bottom = [0]*len(ind),
    #                 align = 'center',
    #                 label = input_category.capitalize(),
    #                 #color = activity_colours[i],
    #                 color = graph_colours(input_list)[i],
    #                 edgecolor = None)
         
    #      # if it isn't plot it on top of the previous one
    #      else:
    #          ax.bar(x = ind2,
    #                 height = y, 
    #                  width = bar_width, 
    #                  bottom = y_minus_1,
    #                  #label = [i[1] for i in y][0], 
    #                  label = input_category.capitalize(),
    #                  #color = activity_colours[i],
    #                  color = graph_colours(input_list)[i],
    #                  edgecolor = None)
         
    #      y_minus_1 = y_minus_1 + np.array([i for i in y])   
         
    #  # Create a description to put under figure title in Latex
    #  abbreviation_list = []
     
    #  for i in range(len(list(LCA_scores_dict[database].keys()))):
         
    #      name = list(LCA_scores_dict[database].keys())[i][1]
    #      abbreviation = list(LCA_scores_dict[database].keys())[i][2]
    #      abbreviation_list.append(name.strip() + ': ' + abbreviation.strip())
         
    #  abbreviation_list = str(abbreviation_list).replace("'",'')
    #  abbreviation_list = str(abbreviation_list).replace(',','\n')
 
    #  # # set the ticks position
    #  ax.yaxis.set_ticks_position('left')
    #  ax.xaxis.set_ticks_position('bottom')
     
    #  # # hide the right and top spines
    #  ax.spines['right'].set_visible(False)
    #  ax.spines['top'].set_visible(False)
     
    #  ax.set_ylabel('LCA score (%s per FU)' %unit)
    #  ax.set_xlabel('Database scenario')
    #  ax.set_xticks(ind2,name_list_short, rotation=0)
    #  ax.set_xlim(min(ind2)-bar_width,max(ind2)+bar_width)

    #  ax.legend (loc='lower center', 
    #              bbox_to_anchor=(0.5,1), 
    #              ncol=len(input_list)//2,
    #              frameon=False)
     
    #  fig.tight_layout()
    #  #plt.text(x = 0.99, y = 0, s = str(abbreviation_list).strip('[]').strip("'"), transform = ax.transAxes, va = 'bottom', ha = 'left')
     
    #  plt.savefig(str(recipe['rdir'] + "/CA_input_category/stacked_bar_chart_" + name_list[0][:5] + '_' + method[2] + ".pdf"))
             
    #  plt.show()


    return abbreviation_list        


def heatmap_input_category (recipe, LCA_scores_dict):
    
     
    abbreviation_list = []
    
    # don't try to plot if False in the recipe
    if not recipe['analyses']['CA_input_category']['heatmap']:
        return abbreviation_list
    
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from brightway2 import methods
    from colours import graph_colours
    
    # include all the impact categories listed in the YAML file
    for method in recipe['CA_input_category']['heatmap']['lcia_methods']: 
                
        unit = methods[method]['unit']
               
        print('LCIA impact category: %s (%s)' % (method[1], method[2]))
        
        # Get the list of input categories
        for database in LCA_scores_dict.keys(): 
            input_list = [i for i in LCA_scores_dict[database][method].keys() if i != 'database identification']

    lcia_methods = recipe['CA_input_category']['heatmap']['lcia_methods']
    databases_scenarios = recipe['CA_input_category']['heatmap']['databases']
    
    # Create figures
    plotData = {}
    ydata = input_list
    xdata = list(set(lcia_methods))
    
    sorter = np.argsort([i[-1] for i in xdata])
    xdata = list(np.array(xdata)[sorter])
    xdata = [tuple(i) for i in xdata]
    for i in xdata:
        plotData[i]={}
        for j in ydata:
            plotData[i][j] =0
         

        
    for db in LCA_scores_dict.keys():
        for i in xdata:
            for j in ydata:
                plotData[i][j] += recipe['CA_input_category']['heatmap']['scaling'][db]*LCA_scores_dict[db][i][j]
                
    for i in xdata:
        total = sum(plotData[i].values())    
        for j in ydata:
            plotData[i][j] = 100*plotData[i][j]/total

    heatmap = np.zeros([len(xdata),len(ydata)])
    
    for i in range(len(xdata)):
        for j in range(len(ydata)):
            ii = xdata[i]
            jj = ydata[j]
            heatmap[i][j] = round(abs(plotData[ii][jj]))
      
    # Create the heatmap plot
    heatmap[heatmap == 0] = 1e-3
    
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    from mpl_toolkits.axes_grid1 import make_axes_locatable
    from matplotlib import colors, cm
    from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
    
    plt.close('all')
    fig = plt.figure(figsize = (14,12))
    ax1 = fig.add_subplot(111)
    
    plt.rcParams.update({'font.size': 12})


    # This will make the small and big numbers look kinda similar 
    norm = colors.LogNorm(vmin = 0.1,vmax =100)

    # get some colors
    #cmap = cm.get_cmap('RdBu',np.nanmax(heatmap) - np.nanmin(heatmap) + 1)   

    # get some colors
    cmap = cm.get_cmap('RdYlGn_r',101)   


    # plot the heatmap in a log scale
    im = ax1.imshow(heatmap.T, cmap = cmap,norm = norm,alpha=0.75)

    # make a colour bar in a linear scale
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin = im.get_clim()[0],
                                                             vmax = im.get_clim()[1]))
    sm._A = []

    xdataLabel = [i[-1].replace("'",'') for i in xdata]
    ydataLabel = [i.title() for i in ydata]

    # set y and x axis tick labels 
    ax1.set_xticks(np.arange(len(xdataLabel)))
    ax1.set_xticklabels(xdataLabel,rotation = 45)

    ax1.set_yticks(np.arange(len(ydataLabel)))
    ax1.set_yticklabels(ydataLabel)
    
    for i in range(len(xdata)):
        for j in range(len(ydata)):
            ii = xdata[i]
            jj = ydata[j]
            value = '%.1f%%' % abs(plotData[ii][jj])
            
            ax1.text(i,j,value,va = 'center',ha = 'center',fontsize = 7)
            
    ax1.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax1.xaxis.set_minor_locator(MultipleLocator(0.5))
    
    ax1.grid(which='minor', color='grey', linestyle='-',lw = 1.25,alpha = 0.75)
    ax1.grid(which='minor', color='grey', linestyle='-',lw = 1.25,alpha = 0.75)

    ax1.tick_params(which='minor', color='white')
    
    
    fig.tight_layout()
    plt.show()
    
    fig.savefig(str(recipe['rdir'] + '/CA_input_category/heatmap_' + databases_scenarios[0].replace(databases_scenarios[0][:5],'') + '.pdf'))
         
    
    return abbreviation_list








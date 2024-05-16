# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 15:50:02 2022

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


def relative_stacked_bar_plot_CA_process (recipe, LCA_scores_dict):

    abbreviation_list = []

    # don't try to plot if False in the recipe
    if not recipe['analyses']['CA_processes']['relative_stacked_bar_plot']:
        return abbreviation_list

    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from brightway2 import methods
    from colours import graph_colours

    # Get the LCA scores from the results dictionary
    database_list = recipe['CA_processes']['relative_stacked_bar_plot']['databases']
    raw_data = {}

    for database in database_list:


        #print('\n Subsystem: '+database)

        for activity in recipe['all_databases'][database]['CA_activities']:

            #print('\t Process:'+activity)

            result_list = []

            # get the individual scores per activity
            for method in list(LCA_scores_dict.keys()):

                #print('\t \t'+str(method))

                score = LCA_scores_dict[method][database][activity]['individual_LCA_score']
                result_list.append(score)

            raw_data[activity] = result_list

        # find the methods unit
        unit_list = []

        for method in recipe['CA_processes']['relative_stacked_bar_plot']['lcia_methods']:

            unit = methods[method]['unit']
            unit_list.append(unit)

        df = pd.DataFrame(raw_data, columns = recipe['all_databases'][database]['CA_activities'], index = list(LCA_scores_dict.keys())).abs()
        df['total'] = df.sum(axis=1)
        df.insert(0,'unit',unit_list)
        df.to_excel(str(recipe['rdir'] + "/CA_activity/LCA_scores_" + database + ".xlsx"))

        # plot

        fig = plt.figure(database,figsize = set_size(500,0.5))
        ax = fig.add_subplot(111)

        ind = np.arange(len(list(LCA_scores_dict.keys())))
        bar_width = 0.85
        name_list = []


        # create a name list (x labels) by selecting only the method abbreviation
        for i in range(len(list(LCA_scores_dict.keys()))):
            name = list(LCA_scores_dict.keys())[i][2]
            name_list.append(name)


       #-------------------------------------------------------------------------
        # STACK THE BARS PER ACTIVITY

        y_minus_1 = np.array([0]*len(ind))

        for i in range(len(recipe['all_databases'][database]['CA_activities'])):

            # activity
            activity = recipe['all_databases'][database]['CA_activities'][i]

            # LCA score for current activity in format  [ [database,activity,lca score] , ... ]
            y = [j / k * 100 for j,k in zip(df[activity], df['total'])]

            # if it is the first activity,just plot it
            print(ind)
            print(y)

            if len(ind)==0:
                continue
            if i == 0:

                ax.bar(x=ind,
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
                ax.bar(x=ind,
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

        for i in range(len(list(LCA_scores_dict.keys()))):

            name = list(LCA_scores_dict.keys())[i][1]
            abbreviation = list(LCA_scores_dict.keys())[i][2]
            abbreviation_list.append(name.strip() + ': ' + abbreviation.strip())

        abbreviation_list = str(abbreviation_list).replace("'",'')
        abbreviation_list = str(abbreviation_list).replace(',','\n')

        # # set the ticks position
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')

        # # hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.set_ylabel('contribution to overall impact (%)')
        ax.set_xlabel('Impact categories')
        ax.set_xticks(ind,name_list, rotation=45, fontsize=10)

        ax.legend (loc='lower center',
                    bbox_to_anchor=(0.5,1),
                    ncol=3,
                    frameon=False)

        fig.tight_layout()
        #plt.text(x = 0.99, y = 0, s = str(abbreviation_list).strip('[]').strip("'"), transform = ax.transAxes, va = 'bottom', ha = 'left')

        plt.savefig(str(recipe['rdir'] + "/CA_activity/stacked_bar_chart_" + database + ".pdf"))

        #plt.savefig(str(recipe['rdir'] + "/stacked_bar_chart_CA_processes_" + database + ".jpeg"))

        plt.show()


    return abbreviation_list



def pie_chart_stacked_bar_plot(LCA_scores_dict, recipe):
    '''

    :param LCA_scores_dict: DESCRIPTION
    :type LCA_scores_dict: TYPE
    :param recipe: DESCRIPTION
    :type recipe: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    '''

    # don't try to plot if False in the recipe
    if not recipe['analyses']['CA_processes']['pie_chart_stacked_bar_plot']:
        return recipe



    import matplotlib.pyplot as plt
    from matplotlib.patches import ConnectionPatch
    import numpy as np
    from colours import graph_colours
    from matplotlib.gridspec import GridSpec




    colors_ColorBrewer = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c',
                            '#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928',
                              '#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462',
                              '#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f',
                                'dodgerblue', 'g', 'r', 'goldenrod', 'k', '0.5', '0.5',
                                 'slateblue', 'b', 'yellowgreen','crimson', 'salmon',
                                  'chocolate', 'darkred', 'orangered',
                                   'saddlebrown', 'mediumorchid', 'purple', 'midnightblue',
                                    'darkorange', 'cyan']

    #-------------------------------------------------------------------------
    # STACKED BAR PLOT

    # create a pie chart for each impact category studied
    for method in recipe['CA_processes']['pie_chart_stacked_bar_plot']['lcia_methods']:

        '''Create a pie chart using the percentage LCA score of each activity and explode the largest wedge
        i.e. the largest contributor. 2 items are removed from the dictionary.'''

    #-------------------------------------------------------------------------
    # PIE CHART SHOWING THE CONTRIBUTION OF EACH ACTIVITY TO THE IC STUDIED

        for database in recipe['CA_processes']['pie_chart_stacked_bar_plot']['databases']:



            # make figure and assign axis objects
            fig = plt.figure(database,figsize = set_size(500,1))

            gs = GridSpec(4, 3, figure=fig,
                          height_ratios=[0.9,1,1,1],
                          width_ratios=[0.01,1,0.9],
                          wspace = 0.25)
            ax1 = fig.add_subplot(gs[:, 1])
            ax2 = fig.add_subplot(gs[1:3, 2])

            # labels are the activity names
            act_list = list(LCA_scores_dict[method][database].keys())

            act_list.remove('database identification')

            act_list.remove('total_LCA_score')

            wedge_sizes = []

            act_lst_tmp = []

            for act in act_list:

                if LCA_scores_dict[method][database][act]['percentage_LCA_score'] < 1:
                    continue

                act_lst_tmp.append(act)

                wedge_sizes.append(LCA_scores_dict[method][database][act]['percentage_LCA_score'])

            act_list = act_lst_tmp
            wedge_sizes_abs = [abs(i)/10 for i in wedge_sizes]

            #explode the largest wedge only
            explode = np.zeros(len(act_list))
            max_idx = np.argmax(wedge_sizes_abs)
            explode[max_idx] = 0.05

            # rotate so that first wedge is split by the x-axis
            angle = 42*wedge_sizes_abs[0]

            #pie_color_dict = dict(zip(act_list,colors_ColorBrewer))
            colours = graph_colours(act_list)
            pie_color_dict = dict(zip(act_list,colours))

            labels = [i.capitalize() for i in list(pie_color_dict.keys())]

            total =sum(wedge_sizes_abs)

            wedge_sizes_abs/=total
            patches, texts = ax1.pie(wedge_sizes_abs,
                    # explode=tuple(explode),
                    # labels = [i.capitalize() for i in list(pie_color_dict.keys())],
                    # autopct="%d%%",
                    startangle = angle,
                    colors=list(pie_color_dict.values())) #'%1.1f%%' to have one figure after comma
            labels = ['%s - %.1f%%' % (i,j) for i,j in zip(labels, wedge_sizes_abs*100)]
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            # ax1.set_title(' - '.join([i.replace("''",'') for i in method]))

            ax1.legend(patches, labels, loc='lower center',ncols = len(labels)//2,frameon = False)
        #-------------------------------------------------------------------------
        # BAR CHART SHOWING THE CONTRIBUTION OF EACH ACTIVITY OF THE MAIN CONTRIBUTOR

            '''Create a bar chart to show the contribution of each exchange to the LCA score of the activity
            (largest contributor)'''

            xpos = 0
            bottom = 0
            width = 0.2

            # create a dictionary with absolute impacts for each foreground activity
            max_dict = {}
            for k in range(len(LCA_scores_dict[method][database])):
                # ignore 'database identification' and 'total_LCA_score'
                if k<=1:
                    continue
                else:
                    act = list(LCA_scores_dict[method][database].keys())[k]
                    max_dict[act] = abs(LCA_scores_dict[method][database][act]['percentage_LCA_score'])

            # get the foreground activity that contributes the most to the overall impact
            max_key = max(max_dict, key = max_dict.get)
            print('The max key for database %s is %s' % (database,max_key))
            # max_key = 'drying' <- break whn we change from cultivation, need while loop

            # get exchanges of the main contributor activity
            exchange_list = list(LCA_scores_dict[method][database][max_key]['exchange'].keys())

            d = {}

            # for each exchange (label = exchange name)
            for exc_label in exchange_list:

                if exc_label not in act_list:

                    LCA_score_exc = abs(LCA_scores_dict[method][database][max_key]['exchange'][exc_label])
                    d[exc_label] = LCA_score_exc

                # each activity is linked to another one, so exchanges are further searched
                else:
                    additional_labels = list(LCA_scores_dict[method][database][exc_label]['exchange'].keys()) # create a list of additional exchange names
                    tag=' (' + exc_label + ')'
                    new_labels = [x + tag for x in additional_labels]

                    for add in additional_labels:
                        #total_activity = LCA_results_dictionary[method][database][max_key]['exchange'][label]
                        LCA_score_exc = abs(LCA_scores_dict[method][database][exc_label]['exchange'][add])
                        d[add] = LCA_score_exc
                        # add (facility) to the name of the exchanges coming form the activity 'facility'
                        tag = add + ' (' + exc_label + ')'
                        d[tag] = d.pop(add)
            total_impact_max_key = sum(d.values())

            #dict_percentages = {i:100*d[i]/abs(LCA_scores_dict[method][database][max_key]['cumulative_LCA_score']) for i in d}
            dict_percentages = {i:100*d[i]/total_impact_max_key for i in d}

            sizes_bar_chart = list(dict_percentages.values())
            labels_bar_chart = list(dict_percentages.keys())

            # import pprint as pp
            # pp.pprint(dict_percentages)
            # print('\nTotal : %.10f' % np.sum([dict_percentages[i] for i in dict_percentages]))


            '''Make the bar chart to show the contribution of each exchanges to the impact of the largest activity contributor.'''


            colors_dict = dict(zip(labels_bar_chart,colors_ColorBrewer[len(list(pie_color_dict.keys())):][::-1]))
            #colors_dict = dict(zip(labels_bar_chart,colours[len(list(pie_color_dict.keys())):]))

            i=0
            for j in range(len(sizes_bar_chart)):

                exc_name = labels_bar_chart[j]
                height = sizes_bar_chart[j]



                ax2.bar(xpos, height, width, bottom,color=colors_dict[exc_name],
                        label =exc_name.split(',')[0].capitalize() )

                patch_height = ax2.patches[i].get_height()
                ypos = bottom + patch_height
                bottom += height


                if ax2.patches[i].get_height()  > 1:
                    ax2.text(xpos, ypos - ax2.patches[i].get_height()/2,
                             "%d%%" % (ax2.patches[i].get_height()),
                             ha = 'center',
                             va=  'center')
                i+=1
            # ax2.set_title(max_key.upper())
            ax2.legend(bbox_to_anchor=(-0.2, 1),
                       frameon = False,loc='lower center',
                       ncol=2,)

            #,title='Technosphere exchanges (%s):'% max_key.upper()
            ax2.set_xlim(- 2.5 * width, 2.5 * width)
            ax2.axis('off')
            ax1.axis('off')



            fig.tight_layout()

            fig.savefig(str(recipe['rdir'] + "/CA_activity/pie_chart_" + database + "_" + method[2] + ".pdf"))

            plt.show()

    return recipe

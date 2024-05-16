# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 09:55:16 2022

@author: leabr
"""

'''
This file contains a function to calculate LCA scores according to the information
contained in the recipe file (YAML). 

    * databases_scenarios = [SpiralG_base_case,...,...]: list of database names (database to compare)
    * lcia_methods = [('IPCC 2013', 'climate change', 'GWP 100a'),('CML 2001 (obsolete)', 'acidification 
    potential', 'average European'),...]: list of LCIA methods
    * CA_activities = ['facility','cultivation', 'filtration','dewatering','shaping','drying']: list of
    activities to include in the contribution analysis    
    * FU_activity_name = 'drying': name of the FU activity 
'''

def dict_LCA_score_per_process(recipe):
    
    '''
    This function creates a nested dictionary with LCA scores calculated per 
    process (i.e. the supply chain is traversed from the foreground system). 
    The output dictionary groups LCA scores per method analysed, per database, 
    per activity, per exchange.
 
    :param recipe: YAML file containing all the information to conduct the LCA analysis.
    :type recipe: yml
    :return: master_output, recipe
    :rtype: TYPE

    '''
    
    from brightway2 import Database, LCA, methods
    import numpy as np
    
    # main dictionary that will contain the LCA scores
    master_output = {} 
    
    # only do the calculations if asked in the recipe
    if all(np.array(list(recipe['analyses']['CA_processes'].values())) == False):
        
        print('\nWARNING: To perform a contribution analysis per process, set any of the "CA_processes" items to "True" in the recipe (input > analyses > CA_processes).')
        
        return master_output, recipe
    
    ## START THE CONTRIBUTION ANALYSIS        
    print('\n> CONTRIBUTION ANALYSIS PER FOREGROUND PROCESS: \n  ---------------------------------------------')

    ## DEFINE THE GRAPHS TO PLOT ACCORDING TO THE RECIPE
    do_relative_stacked = False
    do_pie_chart = False
    do_stacked_comparison = False
    
    if recipe['analyses']['CA_processes']['relative_stacked_bar_plot'] ==  True:
        do_relative_stacked = True
        
    if recipe['analyses']['CA_processes']['pie_chart_stacked_bar_plot'] ==  True:
        do_pie_chart = True    
        
    if recipe['analyses']['CA_processes']['stacked_bar_plot_comparison'] ==  True:
        do_stacked_comparison = True              
    
    # GET THE LCIA METHOD(S) AND DATABASE NAME(S) FROM THE RECIPE
    if do_pie_chart:
        lcia_methods = recipe['CA_processes']['pie_chart_stacked_bar_plot']['lcia_methods']
        databases_scenarios = recipe['CA_processes']['pie_chart_stacked_bar_plot']['databases']
        
    if do_stacked_comparison:
        lcia_methods = recipe['CA_processes']['stacked_bar_plot_comparison']['lcia_methods']
        databases_scenarios = recipe['CA_processes']['stacked_bar_plot_comparison']['databases'] 

    if do_relative_stacked:
        lcia_methods = recipe['CA_processes']['relative_stacked_bar_plot']['lcia_methods']
        databases_scenarios = recipe['CA_processes']['relative_stacked_bar_plot']['databases']

    ## CHECK THAT THE LCIA METHODS ARE TUPLES (does not work if not tuples)
    lcia_methods = [tuple(i) for i in lcia_methods]
        
    print('\nImpact categories selected (%s):' %len(lcia_methods))
    for method in lcia_methods: 
        print('\t- %s (%s)' %(str(method[1]),str(method[2])))
    
    # CREATE A DICTIONARY WITH THE DATABASES TO ASSESS
    db_dict = {}
    # for each database name, load the database into db_dict
    for db_i in databases_scenarios: 
        # convert the file in a database format (to access all functions)
        db = Database(db_i) 
        # store the database in the dictionary
        db_dict[db_i] = db 
        
    print('\nForeground database retrieved (%s):' %len(list(db_dict.keys())))
    for db in db_dict.keys(): 
        print('\t- %s' %db)
    
    # CREATE A NESTED DICTIONARY PER METHOD
    '''Create the nested dictionary to store all the data after LCA calculations.
    The dictionary is organised per method. For each method, sub-dictionaries contain 
    LCA scores for each process/exchange.'''

    # create the output dictionary (nested dict) with one sub-dict per method
    for method in lcia_methods:
        # create sub-dictionary for each method
        master_output[method] = {} 

        for i in db_dict:
            # create sub-dictionary for each database (per method)
            master_output[method][i] = {}
            # db_dict['SpiralG_base_case']=Brightway2 SQLiteBackend: SpiralG_base_case
            master_output[method][i]['database identification'] = db_dict[i] 
            
    #-------------------------------------------------------------------------    
    # INITIAL LCA CALCULATION
            
    '''For each method, do an initial LCA calculation and redo the LCIA for each 
    process and exchange in the database.'''
    
    for method in master_output:

        '''Do the initial LCA calculation for each database. It gives the aggregated LCA score (per method)'''
        
        print('\n>> LCA calculations - %s' %method[2])
        print('   -------------------------')
        
        # Do the LCA calculations for each database i.e. each subsystem in the bioref
        for db_name in master_output[method]:
            
            print('\nDatabase name/scenario: %s' %db_name)

            #FU_activity_name = recipe['all_databases'][db_name]['FU_activity_name']
            FU_activity_name = str('model_'+db_name)
            print('Functional unit name: %s' %str(FU_activity_name))
            
            #FU_value = recipe['all_databases'][db_name]['FU_value']
            FU_value = 1
            FU_unit = recipe['all_databases'][db_name]['FU_unit']
            print('Functional unit value: %s %s' %(FU_value, FU_unit))
            
            activity_FU_list = [act for act in master_output[method][db_name]['database identification'] if FU_activity_name in act['name']] 
            
            activity_FU = activity_FU_list[0]
            
            # The FU to calculate the overall LCA score is the model
            FU = {activity_FU:FU_value}
            print('FU = %s' %str(FU))
            
            lca_iter = LCA(FU, method)
            lca_iter.lci(factorize=True)
            lca_iter.lcia()    
            
            method_unit = methods.get(method).get('unit')

            # total LCA score for each database for each method
            master_output[method][db_name]['total_LCA_score'] = lca_iter.score 
            print('Total LCA score %s: %s %s' %(db_name, str(lca_iter.score), method_unit))

            # For each activity, recalculate the LCIA for each exchange using the exchange and its amount as FU.            
            for activity in recipe['all_databases'][db_name]['CA_activities']:
                
                print('\nActivity: %s' %str(activity))
                
                FU_activity_value = recipe['all_databases'][db_name]['FU_value']
                FU_activity_unit = recipe['all_databases'][db_name]['FU_unit']
                
                print('Functional unit value: %s %s' %(FU_activity_value, FU_activity_unit))
                
                # create a sub-dictionary for each activity
                master_output[method][db_name][activity] = {} 

                activity_selected_list = [act for act in master_output[method][db_name]['database identification'] if activity in act['name']] 
                activity_selected = activity_selected_list[0]

                # create a sub-dictionary for each exchange in the activity dictionary
                master_output[method][db_name][activity]['exchange'] = {} 


                for exc in activity_selected.exchanges(): # replaced technosphere by exchanges
                
                    if exc['type'] == 'production':
                        pass
                    
                    else: 
                    
                        print('>>> %s' %exc)
    
                        lca_iter.redo_lcia({exc.input: exc['amount']})
    
                        # remove the unit from the exchange name for simplicity
                        exchange_key = str(exc.input).split("' ")[0].replace("'",'') 
    
                        master_output[method][db_name][activity]['exchange'][exchange_key] = lca_iter.score
                        print('LCA score of the exchange: %.4f %s' %(lca_iter.score, method_unit))

                # cumulative LCA score for the activity
                indiv_score = np.sum(list(master_output[method][db_name][activity]['exchange'].values()))
                master_output[method][db_name][activity]['individual_LCA_score'] = indiv_score
                print('\nLCA score of the activity %s: %.4f %s' % (activity, indiv_score, method_unit))
                
                ## check if the individual score is the same as the production exchange
                for exc in activity_selected.exchanges():
                    
                    if exc['type'] == 'production':
                        lca_iter.redo_lcia({exc.input: exc['amount']})
                        exchange_key = str(exc.input).split("' ")[0].replace("'",'')
                        print('LCA score production exchange: %.4f %s' %(lca_iter.score, method_unit))
                
                total_score = master_output[method][db_name]['total_LCA_score']
                master_output[method][db_name][activity]['percentage_LCA_score'] = indiv_score / total_score * 100
                
            # for each method and db cheack that the sum of individual scores == total score
            sum_indiv_scores = 0
            for activity in master_output[method][db_name].keys():
                
                if activity == 'database identification': pass
                elif activity == 'total_LCA_score': pass
                else:
                    print('Activity: %s - LCA score: %.2f' %(activity, master_output[method][db_name][activity]['individual_LCA_score']))
                    sum_indiv_scores += master_output[method][db_name][activity]['individual_LCA_score']
            
            print('\nTotal LCA score %s: %.4f %s' %(db_name,sum_indiv_scores,method_unit))
                    
            if sum_indiv_scores == total_score:
                print('LCA scores verified!')
            else: 
                print('\nDifference between the total score of the database and the sum of individual scores for each activity: %s' %(total_score - sum_indiv_scores))
                
    
    
    #  Make a latex table with the master output as a .tex file
    
    import pandas as pd

    #pd.set_option('display.max_colwidth', -1) ##COMMENTED THIS OUT
    deleteActivites = ['database identification', 'total_LCA_score']
    databases = []
    
    
    for m in master_output.keys():
        databases.append(list(master_output[m].keys()))

    databases = list(set(np.array(databases).ravel()))
    
    for db in databases:
        df = []
        
        #  One table per method
        methods = list(master_output.keys())

        
        for m in methods:
            activities = list(master_output[m][db].keys())
            activities = [i for i in activities if i not in deleteActivites]
            mlabel = str(m[-1])
            
            
            for act in activities:
                # exchange =list(master_output[m][db][act].keys())
                
                actlabel = act[:4]
                if actlabel == 'S2A7':
                    actlabel = act[:5]
                exchangeList = master_output[m][db][act]['exchange'].keys()
                
                for ex in exchangeList:
         
                        
                    exlabel = str(ex)
                    # if len(ex)>10:
                    #     exlabel= ex.replace(',','\\\\',1)
                    entry = { 'Method':str(mlabel),
                             'Exchange':exlabel,
                             actlabel:master_output[m][db][act]['exchange'][ex]} 

                
                    df.append(pd.DataFrame(entry,index = [0]))
                    
                    # mlabel = ' '
           
            df.append(pd.DataFrame({},index = [0]))      
            
        df = pd.concat(df)
        
        #  Remove diagnonal layout
        
        combo = {}
        for i in np.sort(list(set(df['Method'].values))):
            if str(i)=='nan': continue
            combo[i]=[]
            for j in np.sort(list(set(df['Exchange'].values))):
                if str(j)=='nan': continue
                
                
                combo[i].append(j)

        df_new = []
        
        activities = np.sort([i for i in df.columns if i.startswith('S')])
        
        # blankDF = pd.DataFrame([])
        # blankDF['Method'] = ['test']
        for method in combo.keys():
            methodLabel = method
            for exchange in combo[method]:
                df_i = pd.DataFrame([])
                df_i['Method'] =[str(methodLabel)]
                df_i['Exchange'] = [str(exchange)]
                for activity in activities:
                    row = df[(df['Method'].values == method) & (df['Exchange'].values ==exchange) &(np.isfinite(df[activity].values))
                              ]
                    
                    df_i[activity] = row[activity]
                    
                df_new.append(df_i)
                # methodLabel = ' '
                # print(df_i)
            # df_new.append(blankDF )

        
        df_new = pd.concat(df_new,ignore_index=True)
        # print(df_new.head(15))
        df = df_new
        
        # Fix exchange names
        
        
        
        
        for index, row in df.iterrows():
            newExchangename = df.at[index,'Exchange'].split(',')[0]
            checkDuplicates = np.sum([i.split(',')[0] == newExchangename for i in list(set(df['Exchange'].values)) ])
            
            if 'transport' in newExchangename:
                newExchangename = df.at[index,'Exchange'].split(',')
                
                if 'freight' in newExchangename[1] :
                    newExchangename = '%s, %s (%s)' % (newExchangename[0],newExchangename[1],newExchangename[2].strip())
                else:
                    newExchangename = '%s, %s ' % (newExchangename[0],newExchangename[1])
                
                
            # print(df.at[index,'Exchange'],'->',newExchangename)
            df.at[index,'Exchange'] = newExchangename
            
            
        label = 'table:LCA_scores_exchanges_%s' % db.replace('_',' ')
        caption = 'LCA scores for  exchnages in  %s' % db.replace('_',' ')
        
        df.to_latex(str(recipe['rdir'] + '/CA_exchanges/LCA_scores_per_exchange_%s.tex' % db) ,
                             label = label,
                             caption = caption,
                             column_format= '|l|p{5cm}|' + 'c'* (len(df.columns)-2)+'|',
                             na_rep = '-',
                             # escape = False,
                             float_format="{:0.1e}".format,
                             longtable = True, index = False)
        
        df.to_excel(str(recipe['rdir'] + '/CA_exchanges/LCA_scores_per_exchange_%s.xlsx' % db))
        
        
# =============================================================================
#         Make difference table 
# =============================================================================
    
    selectedMethod = 'GWP100'
    for n in [1,2,3]:
        table1 =pd.read_excel(recipe['rdir'] + '/CA_exchanges/LCA_scores_per_exchange_db_S%dtech_1.xlsx'% n)
        table2 = pd.read_excel(recipe['rdir'] + '/CA_exchanges/LCA_scores_per_exchange_db_S%dtech_2.xlsx' % n)
        
        del table1['Unnamed: 0']
        del table2['Unnamed: 0']
    
        table1 = table1[table1['Method'] == selectedMethod]
        table2 = table2[table2['Method'] == selectedMethod]
        
        del table1['Method']
        del table2['Method']
        
        
        table1.reset_index(inplace = True)
        
        table2.reset_index(inplace = True)
        
        
        newtable = pd.DataFrame([])

        df_diff =  (table2.set_index('Exchange') - table1.set_index('Exchange')) 
        
        
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
                     
                # df_diff.at[index,subsystem]  = value

        
        print(df_diff.head(10))
        label = 'table:LCA_scores_per_exchange_diff_S%d' % n
        caption = 'table:LCA scores per exchange diff S%d' % n
        
        df_diff.to_latex(str(recipe['rdir'] + '/CA_exchanges/LCA_scores_per_exchange_diff_S%d.tex' % n) ,
                             label = label,
                             caption = caption,
                              column_format= 'l' + 'c'* (len(df_diff.columns)-1)+'|c',
                             na_rep = '-',
                              escape = False,
                             # float_format="{:0.1e}".format,
                             
                             longtable = False, index = True)
        
        df_diff.to_excel(str(recipe['rdir'] + '/CA_exchanges/LCA_scores_per_exchange_diff_S%d..xlsx' % n))
        
        
        
        
        
    return master_output, recipe

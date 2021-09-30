# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 15:38:58 2021

@author: TurpeauR
"""

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pylab

def trans_toDict(df):
    columns = df.columns
    Dict = {}
    for i in range(len(df)):
        Dict2 = {}
        for j in range(len(columns)-1):
            Dict2[columns[j+1]]=df.iloc[i,j+1]
        Dict[df.iloc[i,0]]=Dict2
    return Dict

Path = "U:\\Service Maintenance\\Original Base Actions Maintenance\\Bdd\\"

df_base = pd.read_csv(Path + "maintenance.csv", sep=";")

df_equipements = pd.read_csv(Path + "equipements.csv", sep=";")

df_litho = pd.read_csv(Path + "litho.csv", sep=";")

Trans_params = [
    {'table':"collabs_trans.csv",
     'encoding':'utf-8',
     'modifs' : [
             {'col_Dict': 'Col2', 'col_df_init': 'ModquiC','col_df_copy': 'ModquiC_det'},
             {'col_Dict': 'Col2', 'col_df_init': 'réalisée par','col_df_copy': 'réalisée par_det'},
             {'col_Dict': 'Col2', 'col_df_init': 'responsable','col_df_copy': 'responsable_det'},
             {'col_Dict': 'Col1', 'col_df_init': 'ModquiC','col_df_copy': 'ModquiC'},
             {'col_Dict': 'Col1', 'col_df_init': 'réalisée par','col_df_copy': 'réalisée par'},
             {'col_Dict': 'Col1', 'col_df_init': 'responsable','col_df_copy': 'responsable'},
             ]},
    {'table':"ateliers_trans.csv",
     'encoding':'utf-8',
     'modifs' : [
             {'col_Dict': 'Col2', 'col_df_init': 'atelier','col_df_copy': 'procédé'},
             {'col_Dict': 'Col1', 'col_df_init': 'atelier','col_df_copy': 'atelier'},
             ]},
    {'table':"equipements_trans.csv",
     'encoding':'utf-8',
     'modifs' : [
             {'col_Dict': 'Col3', 'col_df_init': 'équipement','col_df_copy': 'role'},
             ]},
    {'table':"lignes_trans.csv",
     'encoding':'ISO-8859-1',
     'modifs' : [
             {'col_Dict': 'Col1', 'col_df_init': 'ligne','col_df_copy': 'ligne'},
             ]},]


Dict_lignes=trans_toDict(pd.read_csv( Path + "lignes.csv", sep=";"))

Dict_equipement=trans_toDict(pd.read_csv( Path + "equipements.csv", sep=";"))

#Dict_service=trans_toDict(pd.read_csv( Path + "services.csv", sep=";"))  

Dict_role=trans_toDict(pd.read_csv( Path + "roleCategory.csv", sep=";"))   


def get_data(x,Dict,col, **kwargs):
    default = kwargs.get('default', np.nan)
    if str(x) == 'nan':
        return default
    else:
        try:
            return Dict[x][col]
        except:
            raise Exception (x,Dict,col)

def Update_df(param):
    encoding = param.get('encoding', 'utf-8')
    file = param.get('table')
    sep = param.get('sep',';')
    modifs = param.get('modifs')
    
    Dict=trans_toDict(pd.read_csv( Path + file, sep=sep, encoding = encoding))
    for modif in modifs:
        df_base[modif['col_df_copy']] = df_base[modif['col_df_init']].apply(lambda x :get_data(x,Dict,modif['col_Dict']))
 
def check_ligne(x):
    global results, cnt
    
    #On va d'abord aller chercher la ligne pour comparer vers l'atelier
    ligne = Dict_lignes.get(x['ligne'], "")
    if ligne !="":
        if Dict_lignes[x['ligne']]['Col2']!=x['atelier']:
            x['atelier'] = Dict_lignes[x['ligne']]['Col2']
            return 'ligne ne correspondait pas à atelier'
        else:
            return "Ok"
    else:
        x['ligne'] = np.nan
        return 'ligne non renseignée ou non significative'

def adjust_real(x):
    if x['réalisée par']=='UKN':
        if x['responsable']!='UKN' and x['responsable']!='EXT':
            return x['responsable']
        elif x['ModquiC']!='UKN' and x['ModquiC']!='EXT':
            return x['ModquiC']
        else:
            return 'UKN'
    else:
        return x['réalisée par']

def create_boxplot(df, colonne,title, colonne_date, **kwargs):
    df = df[df.loc[:,colonne].notna()]
    
    fig1, ax = plt.subplots(2,2)
    data = df[colonne]
    ymin = kwargs.get('ymin',data.min())
    ymax = kwargs.get('ymax',data.max())
    ax[0][0].set_title(title, fontsize=8)
    ax[0][0].boxplot(data)
    ax[0][0].set_ylim(ymin,ymax)
    
    
    data = df[colonne][df.loc[:,colonne_date]>datetime.datetime.now()-datetime.timedelta(days=365)]
    ymin = kwargs.get('ymin',data.min())
    ymax = kwargs.get('ymax',data.max())
    ax[0][1].set_title('{}_année'.format(title), fontsize=8)
    ax[0][1].boxplot(data)
    ax[0][1].set_ylim(ymin,ymax)
    
    
    data = df[colonne][df.loc[:,colonne_date]>datetime.datetime.now()-datetime.timedelta(days=30)]
    ymin = kwargs.get('ymin',data.min())
    ymax = kwargs.get('ymax',data.max())
    ax[1][0].set_title('{}_mois'.format(title), fontsize=8)
    ax[1][0].boxplot(data)
    ax[1][0].set_ylim(ymin,ymax)
    
    
    data = df[colonne][df.loc[:,colonne_date]>datetime.datetime.now()-datetime.timedelta(days=15)]
    ymin = kwargs.get('ymin',data.min())
    ymax = kwargs.get('ymax',data.max())
    ax[1][1].set_title('{}_semaine'.format(title), fontsize=8)
    ax[1][1].boxplot(data)
    ax[1][1].set_ylim(ymin,ymax)
    
    fig1.savefig('{}.jpeg'.format(title))
    
def create_pieplot(df, colonne, title, colonne_date, **kwargs):
    data = df[colonne].value_counts()
    fig1, ax = plt.subplots(2,2)
    fig1.figsize=(30,30)
    ax[0][0].set_title(title, fontsize=10)
    _, texts, autopcts = ax[0][0].pie(data, labels = data.index, autopct='%1.1f%%')
    plt.setp(autopcts, **{'color':'white', 'fontsize':6})
    plt.setp(texts, **{ 'fontsize':8})
    if len(texts)>2:
        for i in range(len(texts)-2):
            texts[i+2].set_fontsize(max(8-i,0))
            autopcts[i+2].set_fontsize(max(6-i,0))
    
    data = df[colonne][df.loc[:,colonne_date]>datetime.datetime.now()-datetime.timedelta(days=365)].value_counts()
    ax[0][1].set_title('{}_année'.format(title), fontsize=10)
    _, texts, autopcts = ax[0][1].pie(data, labels = data.index, autopct='%1.1f%%')
    plt.setp(autopcts, **{'color':'white', 'fontsize':6})
    plt.setp(texts, **{ 'fontsize':8})
    if len(texts)>2:
        for i in range(len(texts)-2):
            texts[i+2].set_fontsize(max(8-i,0))
            autopcts[i+2].set_fontsize(max(6-i,0))
    
    data = df[colonne][df.loc[:,colonne_date]>datetime.datetime.now()-datetime.timedelta(days=30)].value_counts()
    ax[1][0].set_title('{}_mois'.format(title), fontsize=10)
    _, texts, autopcts = ax[1][0].pie(data, labels = data.index, autopct='%1.1f%%')
    plt.setp(autopcts, **{'color':'white', 'fontsize':6})
    plt.setp(texts, **{ 'fontsize':8})
    if len(texts)>2:
        for i in range(len(texts)-2):
            texts[i+2].set_fontsize(max(8-i,0))
            autopcts[i+2].set_fontsize(max(6-i,0))

    data = df[colonne][df.loc[:,colonne_date]>datetime.datetime.now()-datetime.timedelta(days=15)].value_counts()
    ax[1][1].set_title('{}_semaine'.format(title), fontsize=10)
    _, texts, autopcts = ax[1][1].pie(data, labels = data.index, autopct='%1.1f%%')
    plt.setp(autopcts, **{'color':'white', 'fontsize':6})
    plt.setp(texts, **{ 'fontsize':8})
    if len(texts)>2:
        for i in range(len(texts)-2):
            texts[i+2].set_fontsize(max(8-i,0))
            autopcts[i+2].set_fontsize(max(6-i,0))
    
    fig1.savefig('{}.jpeg'.format(title))

def create_histo_litho(df,lignes):
    fig1, ax = plt.subplots(2,2)
    df2 = df[df.loc[:,'Equi']==lignes[0]]
    x=df2['date']
    height=df2['eff_Jour']
    ax[0][0].bar(x,height)
    ax[0][0].set_title(lignes[1], fontsize=10)
    
    df2 = df[df.loc[:,'Equi']==lignes[1]]
    x=df2['date']
    height=df2['eff_Jour']
    ax[0][1].bar(x,height)
    ax[0][1].set_title(lignes[1], fontsize=10)
    
    df2 = df[df.loc[:,'Equi']==lignes[2]]
    x=df2['date']
    height=df2['eff_Jour']
    ax[1][0].bar(x,height)
    ax[1][0].set_title(lignes[2], fontsize=10)
    
    df2 = df[df.loc[:,'Equi']==lignes[3]]
    x=df2['date']
    height=df2['eff_Jour']
    ax[1][1].bar(x,height)
    ax[1][1].set_title(lignes[3], fontsize=10)
    fig1.savefig('{}.jpeg'.format('litho'))

def convert_date(x,date_fmt):
    return datetime.datetime.strptime(x, date_fmt)

def detail_date(df,colonne, date_fmt):
    df[colonne]=df.loc[:,colonne].apply(lambda x : datetime.datetime.strptime(x, date_fmt))
    df['{}_Year'.format(colonne)] = df.loc[:,colonne].apply(lambda x : x.year)
    df['{}_YM'.format(colonne)] = df.loc[:,colonne].apply(lambda x :'{}_{}'.format(x.year, x.month))    
    df['{}_YW'.format(colonne)] = df.loc[:,colonne].apply(lambda x :'{}_{}'.format(x.year, x.isocalendar()[1]))
        

def get_eff(x):
    hrs_eff = float(x['hrs_eff_M'].replace(',','.'))+float(x['hrs_eff_AM'].replace(',','.'))+float(x['hrs_eff_S'].replace(',','.'))
    hrs_ouv = float(x['hrs_M'].replace(',','.'))+float(x['hrs_AM'].replace(',','.'))+float(x['hrs_S'].replace(',','.'))
    if hrs_eff > hrs_ouv:
        print(x, hrs_eff, hrs_ouv)
    if hrs_ouv == 0:
        return np.nan
    else:
        return hrs_eff/hrs_ouv

def main():
    global results, cnt
    #On va d'abord modifier la valeur de certaines colonnes en utilisant les tableaux de conversion _trans
    for param in Trans_params:
        Update_df(param)
    
    print('____convertion_date___:')
    detail_date(df_base,"date d'ouverture",'%d/%m/%Y %H:%M')
    detail_date(df_base,"réalisée le",'%d/%m/%Y')
    detail_date(df_base,"délai",'%d/%m/%Y')
    detail_date(df_litho,"date",'%d/%m/%Y')

    print('____check_acteur_action___:')
    df_base['réalisée par'] = df_base.apply(lambda x: adjust_real(x), axis = 1)
    print("nombre d'actions dont acteurs inconnus : {}".format(df_base['réalisée par'].value_counts().get('UKN','erreur')))
    print("nombre d'actions dont acteurs externes : {}".format(df_base['réalisée par'].value_counts().get('EXT','erreur')))
    
    #Ensuite on va faire quelques contrôles de cohérence:
    print('____check_lignes____') 
    df_base['ligne_check'] = df_base.apply(lambda x : check_ligne(x), axis = 1)
    print(df_base['ligne_check'].value_counts())
    
    print('____check_equipements___')
    
    print('____adjust_role___')
    df_base['role']=df_base['role'].apply(lambda x: get_data(x,Dict_role,'Col1'))
    
    print('____check_durée_interventions___')
    create_boxplot(df_base,'durée intervention',"repart durées d'intervention","date d'ouverture")
    create_pieplot(df_base,'atelier',"repart atelier","date d'ouverture")
    create_pieplot(df_base,'role',"repart type équipement","date d'ouverture")
    
    print('__prod__')
    df_prod=df_litho
    df_prod['eff_Jour'] = df_prod.apply(lambda x: get_eff(x), axis = 1)
    create_histo_litho(df_prod,['LV1','LV2','LV3','LV4'])
    
    return df_base, df_prod



df_base, df_prod = main()
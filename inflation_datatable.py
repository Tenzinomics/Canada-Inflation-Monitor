import pandas as pd
from stats_can import StatsCan
sc = StatsCan()
from dash import Dash, dcc, html
import plotly.graph_objects as go

def run_datatable():
    #Inflation data table from statscan
    df = sc.table_to_df("18-10-0004-01")
    canada_inf_raw = df[df["GEO"]=="Canada"]  
    #canada[canada["REF_DATE"]=="2024-11-01"] #change the date to the latest release


    cadinf_main = canada_inf_raw[canada_inf_raw["Products and product groups"].isin(["All-items",	"Food",	"Shelter",	"Household operations, furnishings and equipment",	"Clothing and footwear",	"Transportation",	"Gasoline",	"Health and personal care",	"Recreation, education and reading",	"Alcoholic beverages, tobacco products and recreational cannabis",	"All-items excluding food and energy",	"All-items excluding energy",	"Energy",	"Goods",	"Services"])]

    cadinf_main = cadinf_main[["Products and product groups","VECTOR","REF_DATE","VALUE"]]

    date_arr = canada_inf_raw['REF_DATE'].dt.strftime('%b %Y').unique()

    cadinf_main.sort_values(by='REF_DATE', inplace=True)

    cadinf_main["%Y/Y"] = cadinf_main.groupby('Products and product groups')['VALUE'].pct_change(periods=12)*100 


    df_output_new = cadinf_main[cadinf_main["REF_DATE"]== date_arr[-1]]
    df_output_old_1m = cadinf_main[cadinf_main["REF_DATE"]== date_arr[-2]]
    df_output_old_2m = cadinf_main[cadinf_main["REF_DATE"]== date_arr[-3]]

    df_output = pd.merge(df_output_new, df_output_old_1m, on="Products and product groups", suffixes=("", "_old_1m"))
    df_output = pd.merge(df_output, df_output_old_2m, on="Products and product groups", suffixes=("", "_old_2m"))

    df_output = df_output[["Products and product groups", "VECTOR", "VALUE","%Y/Y", "VALUE_old_1m", "%Y/Y_old_1m", "VALUE_old_2m", "%Y/Y_old_2m"]]

    df_output.set_index("Products and product groups", inplace=True)


    df_output.columns = pd.MultiIndex.from_tuples([
        #("", "Products and product groups"),  
        ("", "VECTOR"),  
        
        # Adding level for "REF_DATE"
        (date_arr[-1], "VALUE"),  
        (date_arr[-1], "%Y/Y"),
        (date_arr[-2], "VALUE_old_1m"), 
        (date_arr[-2], "%Y/Y_old_1m"),
        (date_arr[-3], "VALUE_old_2m"),  
        (date_arr[-3], "%Y/Y_old_2m")
    ])


    category_order = ["All-items",	"Food",	"Shelter",	"Household operations, furnishings and equipment",	"Clothing and footwear",	"Transportation",	"Gasoline",	"Health and personal care",	"Recreation, education and reading",	"Alcoholic beverages, tobacco products and recreational cannabis",	"All-items excluding food and energy",	"All-items excluding energy",	"Energy",	"Goods",	"Services"]
    df_output.index = pd.Categorical(df_output.index, categories=category_order, ordered=True)
    df_output = df_output.sort_index()

    df_output.rename(columns={
        "VECTOR":"Vector",
        "VALUE":"Value",
        "VALUE_old_1m": "Value",
        "%Y/Y_old_1m": "%YoY",
        "VALUE_old_2m": "Value",
        "%Y/Y_old_2m": "%YoY"
    }, inplace=True)

    return df_output.round(2)

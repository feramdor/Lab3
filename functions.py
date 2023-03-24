import pandas as pd
import re

def f_leer_archivo(param_archivo: str, param_lib = False, param_cred = dict()) -> pd.DataFrame:
    def verificar_formato_df(df):
        columnas_requeridas = ['opentime', 'closetime', 'Symbol', 'Type']
        columnas_faltantes = set(columnas_requeridas) - set(df.columns)
        if len(columnas_faltantes) > 0:
            print(f'Error: el DataFrame no contiene las columnas requeridas: {columnas_faltantes}')
            return False
        else:
            return True
        
    if param_lib:
        return None
    else:
        ext = re.split(r'(\.\w+)$',param_archivo)
        ext = ext[-2]
        if ext == ".csv":
            df = pd.read_csv(param_archivo)
        elif ext == ".xls" or ext == ".xlsx":
            df = pd.read_excel(param_archivo)
        else:
            print("Archivo inválido")
            df = None
        # Verificación de que se cumple el formato para proseguir el procesado    
        if verificar_formato_df(df):
            return df
        else:
            print("Favor de corregir el archivo")
            return None

def f_pip_size(param_ins: str) -> int:
    try:
        df = pd.read_csv('files/instruments_pips.csv')
        df['Instrument'] = df['Instrument'].str.lower().str.replace('_', '')
        ins = param_ins.lower().replace('_', '')
        ticksize = df.loc[df['Instrument'] == ins, 'TickSize'].iloc[0]
    except:
        ticksize = 0.01
    return int(1/ticksize)
def f_columnas_tiempos(param_data: pd.DataFrame) -> pd.DataFrame:
    param_data["opentime"] = pd.to_datetime(param_data["opentime"])
    param_data["closetime"] = pd.to_datetime(param_data["closetime"])
    param_data["Tiempo"] = (param_data["closetime"] - param_data["opentime"]).dt.total_seconds()
    return param_data

def f_columnas_pips(param_data: pd.DataFrame) -> pd.DataFrame:
    param_data["pip_size"] = param_data["Symbol"].apply(f_pip_size)
    param_data["pips"] = (param_data["closeprice"] - param_data["openprice"]) * param_data["pip_size"]
    param_data["pips"] = param_data.apply(lambda x: -x['pips'] if x['Type'] == 'sell' else x['pips'], axis=1)
    param_data['pips_acm'] = param_data['pips'].cumsum()
    param_data['profit_acm'] = (param_data['pips'] * param_data['Volume']).cumsum()
    return param_data

def f_estadisticas_ba(param_data: pd.DataFrame) -> pd.DataFrame:
    return None

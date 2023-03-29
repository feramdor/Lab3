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
        # Total de operaciones
    total_ops = len(param_data)
        # Operaciones ganadoras
    ganadoras = len(param_data[param_data['profit'] > 0])
        # Operaciones ganadoras de compra
    ganadoras_c = len(param_data[(param_data['profit'] > 0) & (param_data['Type'] == 'compra')])
        # Operaciones ganadoras de venta
    ganadoras_v = len(param_data[(param_data['profit'] > 0) & (param_data['Type'] == 'venta')])
        # Operaciones perdedoras
    perdedoras = len(param_data[param_data['profit'] < 0])
        # Operaciones perdedoras de compra
    perdedoras_c = len(param_data[(param_data['profit'] < 0) & (param_data['Type'] == 'compra')])
        # Operaciones perdedoras de venta
    perdedoras_v = len(param_data[(param_data['profit'] < 0) & (param_data['Type'] == 'venta')])
        # Mediana de profit
    mediana_profit = param_data['profit'].median()
        # Mediana de pips
    mediana_pips = param_data['pips'].median()
        # Razón de efectividad
    r_efectividad = ganadoras / total_ops
        # Razón de proporción
    r_proporcion = ganadoras / perdedoras
        # Razón de efectividad de compras
    r_efectividad_c = ganadoras_c / total_ops
        # Razón de efectividad de ventas
    r_efectividad_v = ganadoras_v / total_ops
        # Crear un DataFrame para almacenar los df_1_tabla
    df_1_tabla = pd.DataFrame(columns=['medida', 'valor', 'descripcion'])
        # Agregar los df_1_tabla al DataFrame
    df_1_tabla.loc[0] = ['ops totales', total_ops, 'operaciones totales']
    df_1_tabla.loc[1] = ['ganadoras', ganadoras, 'operaciones ganadoras']
    df_1_tabla.loc[2] = ['ganadoras_c', ganadoras_c, 'operaciones ganadoras de compra']
    df_1_tabla.loc[3] = ['ganadoras_v', ganadoras_v, 'operaciones ganadoras de venta']
    df_1_tabla.loc[4] = ['perdedoras', perdedoras, 'operaciones perdedoras']
    df_1_tabla.loc[5] = ['perdedoras_c', perdedoras_c, 'operaciones perdedoras de compra']
    df_1_tabla.loc[6] = ['perdedoras_v', perdedoras_v, 'operaciones perdedoras de venta']
    df_1_tabla.loc[7] = ['mediana (profit)', mediana_profit, 'mediana de profit de operaciones']
    df_1_tabla.loc[8] = ['mediana (pips)', mediana_pips, 'mediana de pips de operaciones']
    df_1_tabla.loc[9] = ['r_efectividad', r_efectividad, 'ganadoras totales/operaciones totales']
    df_1_tabla.loc[10] = ['r_proporcion', r_proporcion, 'ganadoras totales/perdedoras totales']
    df_1_tabla.loc[11] = ['r_efectividad_c', r_efectividad_c, 'ganadoras compras/operaciones totales']
    df_1_tabla.loc[12] = ['r_efectividad_v', r_efectividad_v, 'ganadoras ventas/operaciones totales']
   
    df_2_ranking = param_data.groupby('Symbol').agg({'pips': ['count', lambda x: sum(x > 0)]})  
    df_2_ranking['Porcentaje de operaciones ganadoras'] = df_2_ranking.iloc[:, 1]/df_2_ranking.iloc[:, 0] * 100
    df_2_ranking = df_2_ranking.sort_values(by='Porcentaje de operaciones ganadoras', ascending=False).reset_index()
    df_2_ranking = df_2_ranking.iloc[:, [0, 3]]
    df_2_ranking.columns = ['Symbol', 'Rank']
    ex = {
        "df_1_tabla" : df_1_tabla,
        "df_2_ranking" : df_2_ranking
    }
    return ex
#Prueba
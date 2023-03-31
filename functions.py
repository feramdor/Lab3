"""
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import pandas as pd
import re
import numpy as np

def eliminar_espacios(cadena):
    patron = r'\s+'
    return re.sub(patron, '', cadena)
def splitter(cadena):
    lista = cadena.split()
    return lista[0]

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
def f_benchmark(param_archivo: str) -> pd.DataFrame:
    out = pd.read_csv(param_archivo)
    out.rename(columns={"Price" : "close"}, inplace=True)
    out['close'] = out['close'].apply(lambda x: x.replace(",",""))
    out['close'] = out['close'].astype(float)
    out["timestamp"] = pd.to_datetime(out["Date"]).dt.date
    out.set_index("timestamp", inplace=True)
    return out

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
    param_data['Profit'] = param_data['Profit'].apply(eliminar_espacios).astype(float)
    param_data['Volume'] = param_data['Volume'].apply(splitter).astype(float)
    param_data = param_data.rename(columns={'Price' : 'openprice'})
    param_data = param_data.rename(columns={'State' : 'closeprice'})
    return param_data

def f_columnas_pips(param_data: pd.DataFrame) -> pd.DataFrame:
    param_data["pip_size"] = param_data["Symbol"].apply(f_pip_size)
    param_data["pips"] = (param_data["closeprice"] - param_data["openprice"]) * param_data["pip_size"]
    param_data["pips"] = param_data.apply(lambda x: -x['pips'] if x['Type'] == 'sell' else x['pips'], axis=1)
    param_data['pips_acm'] = param_data['pips'].cumsum()
    param_data["profit"] = (param_data['pips'] * param_data['Volume'])
    param_data['profit_acm'] = param_data["profit"].cumsum()
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

def f_evolucion_capital(df: pd.DataFrame, capital: float = 100000) -> pd.DataFrame:
    # Transformación de timestamp
    df['closetime'] = pd.to_datetime(df['closetime']).dt.date
    # Cálculo del profit
    profit_d = df.groupby('closetime')['profit'].sum()

    # Acumulado diario 
    profit_acm_d = (profit_d.cumsum() + capital)

    # Salida
    ex = pd.DataFrame({
        'timestamp' : profit_d.index,
        'profit_d' : profit_d,
        'profit_acm_d' : profit_acm_d
    })
    ex.set_index('timestamp',inplace=True)
    return ex

def f_estadisticas_mad(mad: pd.DataFrame, benchmark: pd.DataFrame, rf: float = 0.05) -> pd.DataFrame:
    mad['timestamp'] = mad.index
    # Calcular el logaritmo de los rendimientos diarios
    log_rendimientos = np.log(mad['profit_acm_d'] / mad['profit_acm_d'].shift(1))
    # Calcular el promedio y la desviación estándar de los rendimientos diarios
    # Calcular el Sharpe Ratio utilizando la fórmula
    sharpe_ratio = (log_rendimientos.mean() - rf) / log_rendimientos.std()
    benchmark = benchmark.reindex(mad.index)
    log_benchmark = np.log(benchmark['close'] / benchmark['close'].shift(1))
    log_rendimientos_diferencia = log_rendimientos - log_benchmark
    sharpe_actualizado = (log_rendimientos.mean() - log_benchmark.mean()) / log_rendimientos_diferencia.std()
    ##################################### Esbozo del drawup y drawdown
    # Obtenemos el máximo de capital acumulado hasta la fecha
    mad['max_capital'] = mad['profit_acm_d'].cummax()
        # Calculamos el drawdown
    mad['drawdown'] = (mad['max_capital'] - mad['profit_acm_d'])/mad['max_capital']
        # Obtenemos la fecha de inicio y fin del drawdown
    drawdown_start = mad.loc[mad['drawdown'].idxmax(), 'timestamp']
    try:
        drawdown_end = mad.loc[mad['drawdown'].idxmax():, 'timestamp'].loc[mad['drawdown'] == 0].iloc[0]
    except:
        drawdown_end = mad.loc[mad['drawdown'].idxmax():, 'timestamp'].iloc[0]
        # Calculamos el capital perdido en el drawdown
    try:
        drawdown_capital = (mad.loc[mad['drawdown'].idxmax(), 'profit_acm_d'] - mad.loc[mad['drawdown'].idxmax():, 'profit_acm_d'].loc[mad['drawdown'] == 0].iloc[0])
    except:
        drawdown_capital = (mad.loc[mad['drawdown'].idxmax():, 'profit_acm_d'].iloc[0] - mad.loc[mad['drawdown'].idxmax(), 'profit_acm_d'])
    # Obtenemos la fecha de inicio y fin del drawup
    try:
        drawup_start = mad.loc[mad['drawdown'].idxmax():, 'timestamp'].loc[mad['drawdown'] == 0].iloc[0]
    except:
        drawup_start = mad.loc[mad['drawdown'].idxmin(), 'timestamp']
    try:
        drawup_end = mad.loc[mad['drawdown'].idxmax():, 'timestamp'].loc[mad['drawdown'] == 0].iloc[-1]
    except:
        drawup_end = mad.loc[mad['drawdown'].idxmax():, 'timestamp'].iloc[-1]
    # Calculamos el capital ganado en el drawup
    try:
        drawup_capital = (mad.loc[mad['drawdown'].idxmax():, 'profit_acm_d'].iloc[-1] - mad.loc[mad['drawdown'].idxmax(), 'profit_acm_d'])
    except:
        mad.loc[mad['drawdown'].idxmax():, 'profit_acm_d'].values[-1] - mad.loc[mad['drawdown'].idxmax(), 'profit_acm_d']
    mad_statistics = pd.DataFrame(columns=['metrica','unidad','valor','descripcion'])
    mad_statistics.loc[0] = ['sharpe_original','Cantidad',sharpe_ratio,'Sharpe Ratio Fórmula Original']
    mad_statistics.loc[1] = ['sharpe_actualizado','Cantidad',sharpe_actualizado,'Sharpe Ratio Fórmula Ajustada']
    mad_statistics.loc[2] = ['drawdown_capi','Fecha Inicial',drawdown_start,'Fecha inicial del DrawDown de Capital']
    mad_statistics.loc[3] = ['drawdown_capi','Fecha Final',drawdown_end,'Fecha final del DrawDown de Capital']
    mad_statistics.loc[4] = ['drawdown_capi','DrawDown $ (capital)',drawdown_capital,'Máxima pérdida flotante registrada']
    mad_statistics.loc[5] = ['drawup_capi','Fecha Inicial',drawup_start,'Fecha inicial del DrawUp de Capital']
    mad_statistics.loc[6] = ['drawup_capi','Fecha Final',drawup_end,'Fecha final del DrawUp de Capital']
    mad_statistics.loc[7] = ['drawup_capi','DrawDown $ (capital)',drawup_capital,'Máxima ganancia flotante registrada']
    return mad_statistics, mad

def f_behavioural_finance(param_data: pd.DataFrame) -> pd.DataFrame:
    # Agrupar el dataframe por instrumento
    grupos = param_data.groupby('Symbol')
    sesgos = {}
    contador = 1
    
    # Iterar sobre cada grupo
    for simbolo, grupo in grupos:
        # Buscar la ganancia máxima y la pérdida máxima, junto con sus respectivos índices
        idx_ganancia_maxima = grupo['profit'].idxmax()
        idx_perdida_maxima = grupo['profit'].idxmin()
        ganancia_maxima = grupo.loc[idx_ganancia_maxima, 'profit']
        perdida_maxima = grupo.loc[idx_perdida_maxima, 'profit']
        
        # Verificar si después de la ganancia máxima ocurrió una pérdida, o si después de la pérdida máxima ocurrió otra pérdida
        if ((grupo.loc[idx_ganancia_maxima+1:, 'profit'] < 0).any()) or ((grupo.loc[idx_perdida_maxima+1:, 'profit'] < 0).any()):
            # Guardar la información relevante en un diccionario
            sesgo = {}
            sesgo['timestamp'] = (grupo.loc[idx_ganancia_maxima, 'opentime']).strftime('%Y-%m-%d %H:%M:%S')
            sesgo['operaciones'] = {}

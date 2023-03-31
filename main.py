import functions
import visualizations

f = (functions.f_leer_archivo("files/Orders.csv")
     .pipe(functions.f_columnas_tiempos)
     .pipe(functions.f_columnas_pips))
tab_rank = functions.f_estadisticas_ba(f)
tab_rank["df_1_tabla"]
tab_rank["df_2_ranking"]
mad = functions.f_evolucion_capital(f)
benchmark = functions.f_benchmark("files/sp500.csv")
mad_statistics, mad_hist = functions.f_estadisticas_mad(mad,benchmark)
behavioural_finance, DE_oc = functions.f_behavioural_finance(f)
graph1 = visualizations.ranking_vis(tab_rank["df_2_ranking"])
graph2 = visualizations.drawdwn_vis(mad_hist, mad_statistics)
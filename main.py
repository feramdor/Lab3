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
mad_statistics = functions.f_estadisticas_mad(mad,benchmark)
visualizations.ranking_vis(tab_rank["df_2_ranking"])
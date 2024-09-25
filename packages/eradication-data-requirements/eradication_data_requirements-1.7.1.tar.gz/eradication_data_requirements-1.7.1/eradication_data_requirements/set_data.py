def filter_data_by_method(raw_data, method):
    filtered_by_method = raw_data[raw_data.Tecnica == method]
    filtered_by_method.loc[:, ["Acumulado"]] = filtered_by_method.Capturas.cumsum()
    return filtered_by_method

# 将结果格式化为 echarts 可用的数据格式
def format_for_echarts(data):
    columns = data['columns']
    rows = data['data']
    echarts_data = {
        'columns': columns,
        'rows': [list(row) for row in rows]
    }
    return echarts_data

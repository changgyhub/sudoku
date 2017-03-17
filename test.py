import pygal

def main():
    line_chart = pygal.Line(truncate_label=-1)
    line_chart.title = 'NKD'
    line_chart.x_labels = ['PE', 'PM', 'PH']
    line_chart.add('NKDddddddddddddddddddddddddddddddddddddddddddd', [3, 2, 1])
    line_chart.render_to_png('NKD.png')

if __name__ == '__main__':
    main()

from util.MarkovChain import MarkovChain
from client.util.ChartBuilder import ChartBuilder
from client.Reporter import Reporter
from client.util.charts.DataSet import DataSet


def generate_report():
    ticker = 'NYT'
    mc = MarkovChain(ticker)
    mc.build_markov_chain()
    x, y = mc.predict()
    ds = DataSet()
    ds.set_x(y)
    ds.append_y_set({'data': x.tolist(), 'label': ''})

    report = Reporter()
    report.set_title('Markov Chain Report')
    report.set_body(ChartBuilder(title='Markov Chain', chart_type='bar', data_set=ds, y_label=ticker))
    report.compile()
    return report.title


if __name__ == "__main__":
    generate_report()
from app import app
from flask import render_template

import urllib

@app.route('/')
@app.route('/index')

@app.route("/simple.png")
def simple():
    import datetime
    import random
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter


    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    img_data = image_data(fig)
    print  urllib.quote('sdfsfd')
    return render_template("index.html", img_data=img_data)


def image_data(fig):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    import StringIO

    Canvas=FigureCanvas(fig)
    png_output=StringIO.StringIO()
    Canvas.print_png(png_output)
    png_output = png_output.getvalue().encode("base64")
    img_data = urllib.quote(png_output.rstrip('\n'))
    return img_data
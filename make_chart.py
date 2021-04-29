import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from discord import File

async def make_chart(ctx, x_array, y_array, title, reverse): # x Month array,  y Value array
    # Chart Color Block
    fig = plt.figure()
    ax = plt.axes()
    fig.patch.set_facecolor('darkslategrey')
    ax.set_facecolor('darkslategrey')
    ax.spines['bottom'].set_color('silver')
    ax.spines['top'].set_color('silver')
    ax.spines['right'].set_color('silver')
    ax.spines['left'].set_color('silver')
    ax.xaxis.label.set_color('silver')
    ax.yaxis.label.set_color('silver')
    ax.tick_params(colors='silver', which='both')
    plt.rcParams['axes.titlecolor'] = 'silver'

    ######
    data_day_range = (x_array[-1] - x_array[0]).days
    interval_int = (data_day_range // 8) + 1
    date_format = '%b %d'

    if data_day_range > 80:
        date_format = '%b %Y'
    elif data_day_range > 365:
        date_format = '%b %Y'
        interval_int = 90
    elif data_day_range > 730:
        date_format = '%b %Y'
        interval_int = 180

    if reverse == True:
        ax.invert_yaxis()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval_int))
    plt.plot(x_array, y_array, color='silver')
    plt.title(title)
    plt.gcf().autofmt_xdate()
    plt.savefig('my_files/chart.png')
    plt.close()
    await ctx.send(file=File('my_files/chart.png'))

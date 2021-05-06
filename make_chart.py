import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter, MonthLocator
from discord import File

async def make_chart(ctx, x_array, y_array, title, reverse, days): # x Month array,  y Value array
    # Chart Color Block
    fig = plt.figure()
    ax = plt.axes()
    ax.grid(linestyle='-', linewidth=0.3, axis='y')
    fig.patch.set_facecolor('darkslategrey')
    ax.set_facecolor('darkslategrey')
    ax.spines['bottom'].set_color('silver')
    ax.spines['top'].set_color('silver')
    ax.spines['right'].set_color('silver')
    ax.spines['left'].set_color('silver')
    ax.xaxis.label.set_color('silver')
    ax.yaxis.label.set_color('silver')
    plt.rcParams['axes.titlecolor'] = 'silver'
    ax.tick_params(colors='silver', which='both')

    if reverse == True: ax.invert_yaxis()

    dateFmt = DateFormatter('%d %b')
    if x_array[0].year != x_array[-1].year: # if years are changing
        dateFmt = DateFormatter('%b %Y')

    ax.xaxis.set_major_formatter(dateFmt)
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))

    plt.gcf().autofmt_xdate(rotation=45)
    plt.plot(x_array, y_array, color='silver')
    plt.title(title)
    plt.savefig('my_files/chart.png')
    plt.close()
    await ctx.send(file=File('my_files/chart.png'))

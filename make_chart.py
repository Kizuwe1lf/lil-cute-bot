import matplotlib.pyplot as plt
from discord import File

async def make_chart(ctx, x_array, y_array, title, x_label, y_label): # x Month array,  y Value array
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

    plt.plot(x_array, y_array, color='silver', marker='o', markerfacecolor='darkslategrey')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig('my_files/chart.png')
    plt.close()
    await ctx.send(file=File('my_files/chart.png'))

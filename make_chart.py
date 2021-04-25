import matplotlib.pyplot as plt
from discord import File

async def make_chart(ctx, x_array, y_array, title, x_label, y_label): # x Month
    plt.plot(x_array, y_array, color='red', marker='o')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig('my_files/chart.png')
    plt.close()
    await ctx.send(file=File('my_files/chart.png'))

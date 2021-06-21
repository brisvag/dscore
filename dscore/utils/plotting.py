import matplotlib.pyplot as plt


def plot_dscore(df, image_path):
    df.plot(x='resn', y='dscore')
    plt.axhline(y = 0.5, color = 'r', linestyle = 'dashed')
    plt.savefig(image_path)

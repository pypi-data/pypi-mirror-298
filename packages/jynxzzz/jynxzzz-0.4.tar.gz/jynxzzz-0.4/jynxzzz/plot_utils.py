import torch
import matplotlib.pyplot as plt
import numpy as np


def plot_func(f, tx=None, ty=None, min=-2, max=2, title=None, figsize=(6, 4)):
    x = torch.linspace(min, max, 100)
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x, f(x))
    if title is not None:
        ax.set_title(title)
    if tx is not None:
        ax.set_xlabel(tx)
    if ty is not None:
        ax.set_ylabel(ty)


def corr(x, y):
    return np.corrcoef(x, y)[0][1]


def show_corr(df, a, b):
    x, y = df[a], df[b]
    plt.scatter(x, y, alpha=0.5, s=4)
    plt.title(f"{a} vs {b}; r: {corr(x, y):.2f}")

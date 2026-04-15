import pandas as pd
import matplotlib.pyplot as plt
import math

# ===== GLOBAL SETTINGS =====
REFERENCE_COLUMN = 'timestamp'
FILE_NAME = r"Data/TUTORIAL_ROUND_1/prices_round_0_day_-2.csv"

plt.style.use('seaborn-v0_8-whitegrid')

plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "legend.fontsize": 14
})

# ===== HELPER FUNCTIONS =====
def load_data(file_name):
    df = pd.read_csv(file_name, sep=';')

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Normalize product names (prevents bugs)
    df["product"] = df["product"].str.upper()

    df["spread"] = df["ask_price_1"] - df["bid_price_1"]

    return df


def filter_product(df, product):
    if product == 'B':
        return {
            p: df[df["product"] == p]
            for p in df["product"].unique()
        }

    elif product == 'T':
        return {
            p: df[df["product"] == p]
            for p in df["product"].unique()
            if "TOMATOES" in p
        }

    elif product == 'E':
        return {
            p: df[df["product"] == p]
            for p in df["product"].unique()
            if "EMERALDS" in p
        }

    else:
        raise ValueError("product must be 'T', 'E', or 'B'")


def get_color(product_name):
    if "TOMATOES" in product_name:
        return 'red'
    elif "EMERALDS" in product_name:
        return 'green'
    return 'blue'


# ===== GRAPH FUNCTIONS (RETURN DATA, NOT PLOT) =====
def graph_column(file_name, column, product='B'):
    df = load_data(file_name)
    data_dict = filter_product(df, product)

    series = []

    for prod_name, sub_df in data_dict.items():
        series.append((
            sub_df[REFERENCE_COLUMN],
            sub_df[column],
            prod_name,
            get_color(prod_name),
            '-'
        ))

    return {
        "title": f"{column} vs {REFERENCE_COLUMN}",
        "xlabel": REFERENCE_COLUMN,
        "ylabel": column,
        "series": series
    }


def graph_columns(file_name, cols, product='B'):
    df = load_data(file_name)
    data_dict = filter_product(df, product)

    series = []

    for prod_name, sub_df in data_dict.items():
        for i, col in enumerate(cols):
            series.append((
                sub_df[REFERENCE_COLUMN],
                sub_df[col],
                f"{prod_name}-{col}",
                get_color(prod_name),
                '-' if i == 0 else '--'
            ))

    return {
        "title": f"{', '.join(cols)} vs {REFERENCE_COLUMN}",
        "xlabel": REFERENCE_COLUMN,
        "ylabel": "Values",
        "series": series
    }


def col_vs_col(file_name, x_col, y_col, product='B'):
    df = load_data(file_name)
    data_dict = filter_product(df, product)

    series = []

    for prod_name, sub_df in data_dict.items():
        series.append((
            sub_df[x_col],
            sub_df[y_col],
            prod_name,
            get_color(prod_name),
            '-'
        ))

    return {
        "title": f"{y_col} vs {x_col}",
        "xlabel": x_col,
        "ylabel": y_col,
        "series": series
    }


def print_columns(file_name):
    df = load_data(file_name)

    print("Columns in file:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")


# ===== MASTER PLOTTING FUNCTION =====
def plot_grid(*graphs, cols=2):
    n = len(graphs)
    rows = math.ceil(n / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(8 * cols, 5 * rows))

    # Normalize axes
    if rows == 1 and cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, graph in enumerate(graphs):
        ax = axes[i]

        for x, y, label, color, linestyle in graph["series"]:
            ax.plot(x, y, label=label, color=color, linestyle=linestyle)

        ax.set_title(graph["title"])
        ax.set_xlabel(graph["xlabel"])
        ax.set_ylabel(graph["ylabel"])

        ax.legend(frameon=True, facecolor='white', framealpha=1)

    # Remove unused plots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    g1 = graph_column(FILE_NAME, 'spread', 'T')
    g2 = graph_column(FILE_NAME, 'spread', 'E')
    g3 = graph_column(FILE_NAME, 'bid_price_1', 'B')
    g4 = col_vs_col(FILE_NAME, 'bid_price_1', 'ask_price_1', 'B')

    plot_grid(g1, g2, g3, g4, cols=2)
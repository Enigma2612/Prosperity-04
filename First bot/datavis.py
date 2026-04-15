import pandas as pd
import matplotlib.pyplot as plt

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

# ===== HELPER FUNCTION =====
def load_data(file_name):
    df = pd.read_csv(file_name, sep=';')

    # df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    df["spread"] = df["ask_price_1"] - df["bid_price_1"]

    return df


def filter_product(df, product):
    product_map = {
        'T': 'TOMATOES',
        'E': 'EMERALDS'
    }

    if product == 'B':
        return {
            'TOMATOES': df[df["product"] == 'TOMATOES'],
            'EMERALDS': df[df["product"] == 'EMERALDS']
        }
    else:
        prod_name = product_map[product]
        return {prod_name: df[df["product"] == prod_name]}


def get_color(product_name):
    return 'red' if product_name == 'TOMATOES' else 'green'


# ===== 1. SINGLE COLUMN GRAPH =====
def graph_column(file_name, column, product='B'):
    df = load_data(file_name)
    data_dict = filter_product(df, product)

    plt.figure()

    for prod_name, sub_df in data_dict.items():
        plt.plot(
            sub_df[REFERENCE_COLUMN],
            sub_df[column],
            label=prod_name,
            color=get_color(prod_name)
        )

    plt.xlabel(REFERENCE_COLUMN)
    plt.ylabel(column)
    plt.title(f"{column} vs {REFERENCE_COLUMN}")

    plt.legend(frameon=True, facecolor='white', framealpha=1)
    plt.tight_layout()
    plt.show()


# ===== 2. MULTIPLE COLUMNS GRAPH =====
def graph_columns(file_name, cols, product='B'):
    df = load_data(file_name)
    data_dict = filter_product(df, product)

    plt.figure()

    for prod_name, sub_df in data_dict.items():
        for col in cols:
            plt.plot(
                sub_df[REFERENCE_COLUMN],
                sub_df[col],
                label=f"{prod_name} - {col}",
                color=get_color(prod_name),
                linestyle='-' if col == cols[0] else '--'
            )

    plt.xlabel(REFERENCE_COLUMN)
    plt.ylabel("Values")
    plt.title(f"{', '.join(cols)} vs {REFERENCE_COLUMN}")

    plt.legend(frameon=True, facecolor='white', framealpha=1)
    plt.tight_layout()
    plt.show()


# ===== 3. COLUMN VS COLUMN =====
def col_vs_col(file_name, x_col, y_col, product='B'):
    df = load_data(file_name)
    data_dict = filter_product(df, product)

    plt.figure()

    for prod_name, sub_df in data_dict.items():
        plt.plot(
            sub_df[x_col],
            sub_df[y_col],
            label=prod_name,
            color=get_color(prod_name)
        )

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{y_col} vs {x_col}")

    plt.legend(frameon=True, facecolor='white', framealpha=1)
    plt.tight_layout()
    plt.show()


# ===== 4. PRINT COLUMNS =====
def print_columns(file_name):
    df = load_data(file_name)

    print("Columns in file:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")


# ===== EXAMPLE =====
print_columns(FILE_NAME)
graph_column(FILE_NAME, 'mid_price', product='T')
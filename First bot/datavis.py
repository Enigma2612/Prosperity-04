import pandas as pd
import matplotlib.pyplot as plt

# ===== GLOBAL SETTINGS =====
REFERENCE_COLUMN = 'timestamp'  # change this to your default x-axis column
FILE_NAME = r"Data/TUTORIAL_ROUND_1/prices_round_0_day_-2.csv"


plt.style.use('seaborn-v0_8-whitegrid')
# Improve readability globally
plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "legend.fontsize": 14
})


# ===== HELPER FUNCTION =====
def load_data(file_name):
    df = pd.read_csv(file_name, sep=';')

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    df["spread"] = df["ask_price_1"] - df["bid_price_1"]

    # 🔥 Downsample (take every Nth point)
    df = df.iloc[::50]   # try 10, 50, 100

    return df

# ===== 1. SINGLE COLUMN GRAPH =====
def graph_column(file_name, column):
    df = load_data(file_name)

    if REFERENCE_COLUMN not in df.columns:
        raise ValueError(f"Reference column '{REFERENCE_COLUMN}' not found")

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")

    plt.figure()
    plt.plot(df[REFERENCE_COLUMN], df[column])

    plt.xlabel(REFERENCE_COLUMN)
    plt.ylabel(column)
    plt.title(f"{column} vs {REFERENCE_COLUMN}")

    plt.legend([column], frameon=True, facecolor='white', framealpha=1)

    plt.tight_layout()
    plt.show()


# ===== 2. MULTIPLE COLUMNS GRAPH =====
def graph_columns(file_name, cols):
    df = load_data(file_name)

    if REFERENCE_COLUMN not in df.columns:
        raise ValueError(f"Reference column '{REFERENCE_COLUMN}' not found")

    plt.figure()

    for col in cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found")
        plt.plot(df[REFERENCE_COLUMN], df[col], label=col)

    plt.xlabel(REFERENCE_COLUMN)
    plt.ylabel("Values")
    plt.title(f"{', '.join(cols)} vs {REFERENCE_COLUMN}")

    plt.legend(frameon=True, facecolor='white', framealpha=1)

    plt.tight_layout()
    plt.show()


# ===== 3. COLUMN VS COLUMN =====
def col_vs_col(file_name, x_col, y_col):
    df = load_data(file_name)

    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError("One or both columns not found")

    plt.figure()
    plt.plot(df[x_col], df[y_col])

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{y_col} vs {x_col}")

    plt.legend([f"{y_col} vs {x_col}"], frameon=True, facecolor='white', framealpha=1)

    plt.tight_layout()
    plt.show()


def print_columns(file_name):
    df = load_data(file_name)

    print("Columns in file:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")


graph_column(FILE_NAME, 'spread')
# eda_laptop.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure output directory exists
if not os.path.exists("images"):
    os.makedirs("images")

# Load dataset
try:
    df = pd.read_csv("data/data.csv")
    print("SUCCESS: Dataset loaded successfully\n")
except FileNotFoundError:
    print("ERROR: data/data.csv not found.")
    exit()

# Basic Metadata
print("METADATA: Dataset Shape:", df.shape)
print("METADATA: Column Names:", df.columns.tolist())

print("\nSCHEMA: Data Types and Null Values:")
print(df.info())

print("\nCLEANING: Missing Value Count:")
print(df.isnull().sum())

print("\nSTATISTICS: Numerical Summary:")
print(df.describe())

# --- Univariate Analysis ---

# Price Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Price'], kde=True, bins=30)
plt.title("Price Distribution Analysis")
plt.xlabel("Price (INR)")
plt.ylabel("Frequency")
plt.savefig("images/eda_price_distribution.png")
plt.close()

# Brand Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Brand', order=df['Brand'].value_counts().index)
plt.title("Inventory Distribution by Brand")
plt.xticks(rotation=45)
plt.savefig("images/eda_brand_count.png")
plt.close()

# Price vs RAM Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='RAM_GB', y='Price')
plt.title("Price Variance across RAM Configurations")
plt.savefig("images/eda_price_vs_ram.png")
plt.close()

# --- Bivariate Analysis ---

# RAM vs Price Scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='RAM_GB', y='Price', hue='Brand')
plt.title("Price-to-RAM Correlation by Brand")
plt.savefig("images/eda_ram_price_brand.png")
plt.close()

# --- Multivariate Analysis ---

# Correlation Heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Matrix")
plt.savefig("images/eda_correlation_heatmap.png")
plt.close()

# Rating Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['Rating'], kde=True, bins=10, color='orange')
plt.title("User Rating Distribution")
plt.savefig("images/eda_rating_distribution.png")
plt.close()

print("\nPROCESS COMPLETE: All EDA visualizations saved to 'images/' directory.")

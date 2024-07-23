import matplotlib.pyplot as plt

import pandas as pd

# Load the provided Excel file
file_path = 'C:\\Users\\EDY\\Desktop'
data = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
data.head()


# Convert the 日期列 to datetime type
data['日期'] = pd.to_datetime(data['日期'])

# Set 日期 as the index
data.set_index('日期', inplace=True)

# Plot ETH and BTC spot prices
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['ETH现货价格'], label='ETH现货价格', color='blue')
plt.plot(data.index, data['BTC现货价格'], label='BTC现货价格', color='orange')
plt.xlabel('日期')
plt.ylabel('价格')
plt.title('ETH和BTC现货价格走势')
plt.legend()
plt.grid(True)
plt.show()

# Plot ETH and BTC basis rates and APRs
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 12))

# ETH basis rates and APRs
axes[0, 0].plot(data.index, data['ETH次季价差率'], label='ETH次季价差率', color='blue')
axes[0, 0].plot(data.index, data['ETH当季价差率'], label='ETH当季价差率', color='green')
axes[0, 0].set_title('ETH次季和当季价差率走势')
axes[0, 0].legend()
axes[0, 0].grid(True)

axes[0, 1].plot(data.index, data['ETH次季APR'], label='ETH次季APR', color='blue')
axes[0, 1].plot(data.index, data['ETH当季APR'], label='ETH当季APR', color='green')
axes[0, 1].set_title('ETH次季和当季APR走势')
axes[0, 1].legend()
axes[0, 1].grid(True)

# BTC basis rates and APRs
axes[1, 0].plot(data.index, data['BTC次季价差率'], label='BTC次季价差率', color='orange')
axes[1, 0].plot(data.index, data['BTC当季价差率'], label='BTC当季价差率', color='red')
axes[1, 0].set_title('BTC次季和当季价差率走势')
axes[1, 0].legend()
axes[1, 0].grid(True)

axes[1, 1].plot(data.index, data['BTC次季APR'], label='BTC次季APR', color='orange')
axes[1, 1].plot(data.index, data['BTC当季APR'], label='BTC当季APR', color='red')
axes[1, 1].set_title('BTC次季和当季APR走势')
axes[1, 1].legend()
axes[1, 1].grid(True)

plt.tight_layout()
plt.show()


# # Calculate correlation matrix
# correlation_matrix = data[['ETH现货价格', 'ETH次季价差率', 'ETH次季APR', 'ETH当季价差率', 'ETH当季APR',
#                            'BTC现货价格', 'BTC次季价差率', 'BTC次季APR', 'BTC当季价差率', 'BTC当季APR']].corr()
#
# # Display the correlation matrix
# correlation_matrix


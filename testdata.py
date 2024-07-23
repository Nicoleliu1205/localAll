import matplotlib.pyplot as plt

import pandas as pd

# Load the provided Excel file
file_path = 'C:\\Users\\EDY\\Desktop'
data = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
data.head()


# Convert the ������ to datetime type
data['����'] = pd.to_datetime(data['����'])

# Set ���� as the index
data.set_index('����', inplace=True)

# Plot ETH and BTC spot prices
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['ETH�ֻ��۸�'], label='ETH�ֻ��۸�', color='blue')
plt.plot(data.index, data['BTC�ֻ��۸�'], label='BTC�ֻ��۸�', color='orange')
plt.xlabel('����')
plt.ylabel('�۸�')
plt.title('ETH��BTC�ֻ��۸�����')
plt.legend()
plt.grid(True)
plt.show()

# Plot ETH and BTC basis rates and APRs
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 12))

# ETH basis rates and APRs
axes[0, 0].plot(data.index, data['ETH�μ��۲���'], label='ETH�μ��۲���', color='blue')
axes[0, 0].plot(data.index, data['ETH�����۲���'], label='ETH�����۲���', color='green')
axes[0, 0].set_title('ETH�μ��͵����۲�������')
axes[0, 0].legend()
axes[0, 0].grid(True)

axes[0, 1].plot(data.index, data['ETH�μ�APR'], label='ETH�μ�APR', color='blue')
axes[0, 1].plot(data.index, data['ETH����APR'], label='ETH����APR', color='green')
axes[0, 1].set_title('ETH�μ��͵���APR����')
axes[0, 1].legend()
axes[0, 1].grid(True)

# BTC basis rates and APRs
axes[1, 0].plot(data.index, data['BTC�μ��۲���'], label='BTC�μ��۲���', color='orange')
axes[1, 0].plot(data.index, data['BTC�����۲���'], label='BTC�����۲���', color='red')
axes[1, 0].set_title('BTC�μ��͵����۲�������')
axes[1, 0].legend()
axes[1, 0].grid(True)

axes[1, 1].plot(data.index, data['BTC�μ�APR'], label='BTC�μ�APR', color='orange')
axes[1, 1].plot(data.index, data['BTC����APR'], label='BTC����APR', color='red')
axes[1, 1].set_title('BTC�μ��͵���APR����')
axes[1, 1].legend()
axes[1, 1].grid(True)

plt.tight_layout()
plt.show()


# # Calculate correlation matrix
# correlation_matrix = data[['ETH�ֻ��۸�', 'ETH�μ��۲���', 'ETH�μ�APR', 'ETH�����۲���', 'ETH����APR',
#                            'BTC�ֻ��۸�', 'BTC�μ��۲���', 'BTC�μ�APR', 'BTC�����۲���', 'BTC����APR']].corr()
#
# # Display the correlation matrix
# correlation_matrix


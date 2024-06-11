import os
import matplotlib.pyplot as plt

def read_data(file_path):
  data = []
  with open(file_path, 'r') as file:
    for line in file:
      parts = line.strip().split(' ', 2)
      if len(parts) == 3:
        num = int(parts[0])
        boolean = parts[1] == 'True'
        lst = eval(parts[2])  # 注意：eval可能会带来安全问题，仅在受信任的数据上使用
        data.append(lst)
  return data

def plot_data(data):
  for i in range(15):
    plt.figure(figsize=(14, 8))
    subset = data[20*i:20*i+20]
    for lst in subset:
        plt.plot(lst)
    plt.title('Line Plots from List Data')
    plt.xlabel('Index')
    plt.ylabel('Value')

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"res/gasprice{i}.png", dpi=300)

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    result_path = os.path.join(directory, "result.txt")
    data = read_data(result_path)
    plot_data(data)

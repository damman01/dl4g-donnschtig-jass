import os
from pathlib import Path

def count_lines(directory_path):
    total_lines = 0
    file_list = []

    for file in Path(directory_path).rglob('*.txt'):
        file_list.append(file)
    for filename in file_list:
        print("filename: ", filename)
        with open(os.path.join(directory_path, filename), 'r') as f:
            content = f.read()
            total_lines += content.count('\n')
    return total_lines

if __name__ == '__main__':
    path = 'D:/Git/dl4g-donnschtig-jass/training_play/gamelogs/'
    total_lines = count_lines(path)
    print(f'Total lines in {path}: {total_lines}')

# Total lines in D:/Git/dl4g-donnschtig-jass/training_play/gamelogs/: 36901728
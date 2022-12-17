import os
import string


# base_dir = ' '
# new_dir = 'C:\\Users\\arteo\\PycharmProjects\\TensorFlow\\'
# with open(os.path.join(base_dir, 'test.txt'), 'w') as file:
#     file.write('test')

digits = {string.digits[x]: str(x+48) for x in range(10)}

upper_case = {string.ascii_uppercase[x]: str(x+65) for x in range(26)}

lower_case = {string.ascii_lowercase[x]: str(x+97) for x in range(26)}

res = {}

res.update(digits)
res.update(upper_case)
res.update(lower_case)

dir_digits = {x: str(x) for x in range(10)}
dir_upper = {x: string.ascii_uppercase[x-10] for x in range(10, 36)}
dir_lower = {x: string.ascii_lowercase[x-36] for x in range(36, 62)}

res_dir = {}
res_dir.update(dir_digits)
res_dir.update(dir_upper)
res_dir.update(dir_lower)





# for dir in os.listdir(base_dir):
#     counter = 0
#     for file in os.listdir(os.path.join(base_dir, dir)):
#         cur_path = os.path.join(base_dir, dir)
#         symbol = dir.lstrip('Sample').lstrip('0')
#         code = res[res_dir[symbol]]
#         name = f'{code}-{counter}.png'
#         new_path = os.path.join(cur_path, name)
#         os.rename(f'{cur_path}\\{file}', new_path)
#         counter +=1
#
# for file in os.listdir(new_dir):
#     if '.png' in file:
#         path = os.path.join(new_dir, file)
#         os.remove(path)

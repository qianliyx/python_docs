

a = 10
b = 11

def test():
    c = 12
    res = locals()
    print(f'函数test的局部变量：{res}')


d = globals()
print(f'文件test.py的全局变量：{d}')
test()

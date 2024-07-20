def reader(path):
    with open(path, 'r') as f:
        data = f.readlines()
    for i, d in enumerate(data):
        data[i] = d.strip().split(' ')
    ret = []
    for d in data:
        tmp = dict()
        tmp['time'] = d[3]
        tmp['op'] = d[5]
        tmp['name'] = d[6]
        ret.append(tmp)
    return ret
        

if __name__ == '__main__':
    data = reader('log/transformer.log')
    print(data)
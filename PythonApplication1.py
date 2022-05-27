from copy import deepcopy

def combine(m, n):
    a = len(m)
    c = ''
    count = 0
    for i in range(a):
        if(m[i] == n[i]):
            c += m[i]
        elif(m[i] != n[i]):
            c += '-'
            count += 1

    if(count > 1):
        return None
    else:
        return c

def sortfunction(x):
    w = x[1]
    w = w.replace("-","2")
    return int(w)

def findPI(data):
    answer = []

    size = len(data)
    im = []
    im2 = []
    mark = [0]*size
    m = 0

    for i in range(size):
        for j in range(i+1, size):
            c = combine(data[i][1], data[j][1])
            if c != None:
                s = data[i][0]+data[j][0]
                s.sort()
                im.append([s,c])
                mark[i] = 1
                mark[j] = 1
            else:
                continue

    size2 = len(im)
    mark2 = [0]*size2

    for p in range(size2):
        for n in range(p+1, size2):
            if(mark2[n] == 0):
                if( im[p][1] == im[n][1]):
                    mark2[n] = 1

    for r in range(size2):
        if(mark2[r] == 0):
            im2.append(im[r])

    for q in range(size):
        if( mark[q] == 0 ):
            answer.append(data[q])
            m = m+1

    if(m == size or size == 1):
        return answer
    else:
        return answer + findPI(im2)

def tableprint(table,minterm):
    print("\t",end='')

    for i in range(len(table[0])):
        cnt = 0

        for j in range(len(table)):
            if(table[j][i] == '+'): cnt += 1
        if(cnt < len(table)):
            print(minterm[i+2],end="\t")

    print()

    cnt = 1

    for i in table:
        w = 0
        for j in i:
            if(j == "+"):
                w += 1

        if(w < len(i)):
            print('P'+str(cnt), end='\t')

            for j in i:
                if(j != '+'):
                    print(j, end='\t')

            print()
        cnt += 1

    print('\n\n\n')

def findepi(table, answer):
    for i in range(len(table[0])):
        cnt = 0

        for j in range(len(table)):
            if(table[j][i] == 'V'):
                cnt += 1

        if(cnt == 1):
            for j in range(len(table)):
                if(table[j][i] == 'V'):
                    print('P'+str(j+1)+' is epi')
                    answer.append(j+1)
                    for w in range(len(table[0])):
                        if(table[j][w] == 'V'):
                            for q in range(len(table)):
                                table[q][w] = '+'
                        table[j][w] = '+'
                    break



def column_dominance(table,minterm):
    for i in range(len(table[0])):
        for j in range(len(table[0])):
            if(table[0][i] != '+' and table[0][j] != '+' and i != j):
                cnt = 0
                for w in range(len(table)):
                    if(table[w][i] == ' ' and table[w][j] == 'V'):
                        cnt += 1

                if(cnt == 0):
                    for w in range(len(table)):
                        table[w][i] = '+'

def row_dominance(table, minterm):
    for i in range(len(table)):
        for j in range(len(table)):
            cnt = 0
            cnt2 = 0

            for w in range(len(table[i])):
                if(table[i][w] == '+'): cnt += 1

            for w in range(len(table[j])):
                if(table[j][w] == '+'): cnt2 += 1

            if(len(table[i]) != cnt and len(table[j]) != cnt and i != j):
                cnt = 0
                for w in range(len(table[i])):
                    if(table[i][w] == ' ' and table[j][w] == 'V'):
                        cnt += 1

                if(cnt == 0):
                    table[j] = ['+' for i in minterm[2:]]

def petrick(table,minterm,answer):
    print('m'+str(minterm[2:])+'=')

    for i in answer:
        print('P'+str(i), end='')
    for i in range(len(table[0])):
        cnt = 0
        for j in range(len(table)):
            if(table[j][i] == '+'): cnt += 1

        result = ''
        if(cnt != len(table)):
            result += '('
            for j in range(len(table)):
                if(table[j][i] == 'V'):
                    result += 'P'+str(j+1)+'+'

            result = result[:-1]
            result += ')'
            print(result,end='')

def solution(minterm):
    data = []

    for i in minterm[2:]:
        w = i
        c = ''
        for j in reversed(list(range(minterm[0]))):
            if(2**j <= i):
                i -= 2**j
                c += '1'
            else:
                c += '0'

        data.append([[w],c])

    pi = findPI(data)
    pi.sort(key=sortfunction)

    #pi 구하기 끝

    table = []
    cnt = 0

    for i in pi:
        table.append([])

        for j in minterm[2:]:
            if(j in i[0]):
                table[cnt].append('V')
            else:
                table[cnt].append(' ')

        cnt += 1

    print('pi 결과 값')
    tableprint(table,minterm)

    answer = []

    while(True):
        copy_table = deepcopy(table)

        print('epi를 찾은 결과값')
        findepi(table,answer)
        tableprint(table,minterm)

        print('column dominance 결과값')
        column_dominance(table,minterm)
        tableprint(table,minterm)

        print('row dominance 결과값')
        row_dominance(table,minterm)
        tableprint(table,minterm)

        if(copy_table == table):
            break

    print('페트릭 메소드:')
    petrick(table,minterm, answer)

result = solution([3,6,0,1,2,5,6,7])

#[3,6,0,1,2,5,6,7]
#[4,11,0,2,5,6,7,8,10,12,13,14,15]
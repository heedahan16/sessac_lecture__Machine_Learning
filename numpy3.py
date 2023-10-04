# 1. 1~100까지 난수가 들어가있는 2*10*10 배열을 만들고 2. 50보다 크거나 같은 값은 1, 50보다 작은 값은 2로 변환하고 3. 2번째 배열에 아래와 같이 붉은색 위치(56~100)만 뽑는 코드 작성

import numpy as np

# 1~100까지 난수가 들어가있는 2*10*10 배열을 만들기
print("step1")
x = np.random.randint(1, 100, size=(2, 10, 10))
print(x)
print()

# 50보다 크거나 같은 값은 1, 50보다 작은 값은 2로 변환하기
print("step2") 
y = np.where(x > 5, 1, 2)
print(y)
print()

# 2번째 배열에 아래와 같이 붉은색 위치(56~100)만 뽑기
print("step3")
z = y[1][5:10, 5:10]
print(z)
print()
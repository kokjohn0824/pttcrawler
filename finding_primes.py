import time


def main():
    time0 = time.time()
    nums = []
    for j in range(1, int(input("請輸入想要查詢的質數最大值:"))+1):
        nums.append(j)

    list_1 = list.copy(nums)
    print("start finding...")
    time.sleep(0.5)
    for i in nums:
        if i >= 3:
            a = i
            b = i-1
            while b >= 2:
                if nums[a-1] % nums[b-1] == 0:
                    list_1[a-1] = 1
                    break
                else:
                    b -= 1
                    continue

    prime_list  =  list.copy(list(set(list_1)))
    prime_list.sort()
    # print(list(prime_list))
    for x in prime_list:
        print(x)
    time_finish = time.time()
    print("完成時間(sec):" + str(time_finish-time0))


if __name__ == '__main__':
    main()






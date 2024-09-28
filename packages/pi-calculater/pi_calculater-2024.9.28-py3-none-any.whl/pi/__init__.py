from os import environ
from datetime import datetime
NO_SHOWING_TIME_KEYWORD = 'PI_CALCULATER_NO_SHOWING_TIME'
def chudnovsky_naive(digits:int)->str:
    """
    使用 Chudnovsky 公式计算圆周率小数点后 n 位
    :param digits: 位数
    :return: π
    """
    if not NO_SHOWING_TIME_KEYWORD in environ:
        start_time = datetime.now()
    import math
    digits *= 2  # 要先乘2，不然计算出来只有 n/2 位
    one = 10 ** digits
    k = 1
    ak = one
    asum = one  # 10 ** digits
    bsum = 0

    # ak=0 时说明 ak 太小了，超过了规定的精度，这时停止计算
    while ak:
        ak = 24 * ak * -(6 * k - 5) * (2 * k - 1) * (6 * k - 1) // ((k * 640320) ** 3)
        asum += ak
        bsum += k * ak
        k += 1

    denominator = 13591409 * asum + 545140134 * bsum

    # 注意：要用 math.isqrt() 而非 math.sqrt()。
    # math.sqrt() 是将整数转换为浮点数，结果也是浮点数，
    # 10005*one 这么大的整数作为参数传入会报错。
    # math.isqrt(x) 用于计算 int(sqrt(x))，
    # 对于非常大的整数同样生效且计算速度很快。
    numerator = 426880 * one * math.isqrt(10005 * one)
    pi = numerator // denominator
    if not NO_SHOWING_TIME_KEYWORD:
        print('Calculated pi used '+str(datetime.now()-start_time)+' seconds.')
    return pi


def chudnovsky_binsplit(digits:int)-> str:
    """
    使用 Chudnovsky 公式和 binary splitting 算法计算圆周率小数点后 n 位（更快）
    :param digits: 要计算的位数
    :return: π
    """
    if not NO_SHOWING_TIME_KEYWORD in environ:
        start_time = datetime.now()
    import math
    digits *= 2

    # 返回 P, Q, B, T
    # 此时 B=1，所以只返回 P, Q, T
    def binsplit(a, b):
        # 直接求的情况
        if b - a == 1:
            # 特殊情况：a = 0
            if a == 0:
                Pab = Qab = 1
            else:
                Pab = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
                Qab = 640320 ** 3 // 24 * a ** 3
            Tab = (13591409 + 545140134 * a) * Pab
            # 对 (-1)^k 这个因子进行处理
            if a & 1:
                Tab = -Tab
            return Pab, Qab, Tab
        else:
            m = (a + b) // 2
            Pam, Qam, Tam = binsplit(a, m)
            Pmb, Qmb, Tmb = binsplit(m, b)
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
            return Pab, Qab, Tab

    # 要计算多少项
    # Chudnovsky 公式每计算一项，正确位数会增加 14 位，
    # 所以要计算 digits//14 + 1 项
    # 想知道原因的读者可以参考 [3] 中 Page 44 的 Theorem 10.13
    terms = digits // 14 + 1
    P, Q, T = binsplit(0, terms)
    pi = Q * 426880 * math.isqrt(10005 * 10 ** digits) // T
    if not NO_SHOWING_TIME_KEYWORD:
        print('Calculated pi used '+str(datetime.now()-start_time)+' seconds.')
    return pi


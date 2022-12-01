"""
測試print效能影響，測試條件
使用10萬次回圈進行以下測試:
1. 不列印任何字串
2. 列印1個字串
3. 列印10個字串
4. 列印100個字串(單行)
5. 列100個字串(多行)

使用100萬次回圈進行以下測試:
1. 不列印任何字串
2. 列印1個字串
3. 列印10個字串
4. 列印100個字串(單行)
5. 列100個字串(多行)

"""
import time

loop_10_0000 = 10 * 10000  # 10萬次
loop_100_0000 = 100 * 10000  # 100萬次
results = []


def test_print_0char(loop_count):
    start = time.time()
    for i in range(loop_count):
        pass

    return f'測試條件: 進行{loop_count / 10000}萬次回圈,不列印任何字元,消耗時間為{round(time.time() - start, 3)}秒'


def test_print_10chars(loop_count):
    start = time.time()
    for i in range(loop_count):
        print("0123456789")

    return f'測試條件: 進行{loop_count / 10000}萬次回圈,列印10個字元,消耗時間為{round(time.time() - start, 3)}秒'


def test_print_100chars(loop_count):
    start = time.time()
    for i in range(loop_count):
        print("123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 ")

    return f'測試條件: 進行{loop_count / 10000}萬次回圈,列印100個字元,消耗時間為{round(time.time() - start, 3)}秒'


def test_print_100char_with_new_line(loop_count):
    start = time.time()
    for i in range(loop_count):
        print("""
        0123456789
        0123456789
        0123456789
        0123456789
        0123456789
        0123456789
        0123456789
        0123456789
        0123456789
        0123456789
        """)

    return f'測試條件: 進行{loop_count / 10000}萬次回圈,列印100個字元且換行,消耗時間為{round(time.time() - start, 3)}秒'


results.append(test_print_0char(loop_10_0000))
results.append(test_print_10chars(loop_10_0000))
results.append(test_print_100chars(loop_10_0000))
results.append(test_print_100char_with_new_line(loop_10_0000))

results.append(test_print_0char(loop_100_0000))
results.append(test_print_10chars(loop_100_0000))
results.append(test_print_100chars(loop_100_0000))
results.append(test_print_100char_with_new_line(loop_100_0000))

for row in results:
    print(row)

"""
測試條件：進行10.0萬次回圈,不列印任何字元,消耗時間為0.003秒
測試條件：進行10.0萬次回圈,列印10個字元,消耗時間為0.962秒
測試條件：進行10.0萬次回圈,列印100個字元,消耗時間為1.64秒
測試條件：進行10.0萬次回圈,列印100個字元且換行,消耗時間為11.883秒

測試條件：進行100.0萬次回圈,不列印任何字元,消耗時間為0.02秒
測試條件：進行100.0萬次回圈,列印10個字元,消耗時間為9.753秒
測試條件：進行100.0萬次回圈,列印100個字元,消耗時間為16.41秒
測試條件：進行100.0萬次回圈,列印100個字元且換行,消耗時間為122.504秒
"""

"""混合排序算法：快速排序 + 插入排序（阈值可配置，默认 16）"""

# 默认阈值，子数组长度 < 阈值时切换到插入排序
DEFAULT_THRESHOLD = 16
# 三数取中分区至少需要 4 个元素，否则 pivot 索引可能重叠
MIN_THRESHOLD = 4


def insertion_sort(arr, left, right):
    """对 arr[left..right] 做原地插入排序"""
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def _partition(arr, left, right):
    """三数取中选 pivot，返回分区后 pivot 的下标"""
    mid = (left + right) // 2
    # 排序 left, mid, right，取中值放到 right-1 作为 pivot
    if arr[left] > arr[mid]:
        arr[left], arr[mid] = arr[mid], arr[left]
    if arr[left] > arr[right]:
        arr[left], arr[right] = arr[right], arr[left]
    if arr[mid] > arr[right]:
        arr[mid], arr[right] = arr[right], arr[mid]
    # 把 pivot 放到 right-1
    arr[mid], arr[right - 1] = arr[right - 1], arr[mid]
    pivot = arr[right - 1]

    i = left
    j = right - 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while j >= left and arr[j] > pivot:
            j -= 1
        if i >= j:
            break
        arr[i], arr[j] = arr[j], arr[i]
    # 把 pivot 放到正确位置
    arr[i], arr[right - 1] = arr[right - 1], arr[i]
    return i


def _quick_sort(arr, left, right, threshold):
    """对 arr[left..right] 做混合排序

    当子数组长度 >= threshold 时使用快速排序分区；
    当子数组长度 < threshold 时切换到插入排序。
    """
    while right - left + 1 >= threshold:
        # 快速排序分区
        pivot_idx = _partition(arr, left, right)
        # 对较小的子数组先递归（较大的用循环处理，减少递归深度）
        if pivot_idx - left < right - pivot_idx:
            _quick_sort(arr, left, pivot_idx - 1, threshold)
            left = pivot_idx + 1
        else:
            _quick_sort(arr, pivot_idx + 1, right, threshold)
            right = pivot_idx - 1
    # 子数组长度 < threshold，切换到插入排序
    if right > left:
        insertion_sort(arr, left, right)


def hybrid_sort(arr, threshold=DEFAULT_THRESHOLD):
    """混合排序入口：原地排序

    Args:
        arr: 待排序列表
        threshold: 快排/插排切换阈值，默认 16，最小 4
    Returns:
        排序后的列表（原地修改）
    """
    if len(arr) <= 1:
        return arr
    threshold = max(threshold, MIN_THRESHOLD)
    _quick_sort(arr, 0, len(arr) - 1, threshold)
    return arr


# ---------- 测试用例 ----------

def test_normal():
    arr = [38, 27, 43, 3, 9, 82, 10, 55, 12, 7, 99, 1, 66, 21, 8, 30,
           44, 13, 70, 5, 18, 60, 77, 22, 14, 88, 33, 40, 50, 6]
    expected = sorted(arr)
    hybrid_sort(arr)
    assert arr == expected, f"普通数组失败: {arr}"
    print("PASS  普通数组")


def test_sorted():
    arr = list(range(1, 31))
    expected = arr[:]
    hybrid_sort(arr)
    assert arr == expected, f"有序数组失败: {arr}"
    print("PASS  有序数组")


def test_reversed():
    arr = list(range(30, 0, -1))
    expected = sorted(arr)
    hybrid_sort(arr)
    assert arr == expected, f"逆序数组失败: {arr}"
    print("PASS  逆序数组")


def test_duplicates():
    arr = [5, 3, 5, 1, 3, 5, 1, 3, 5, 1, 3, 5, 1, 3, 5, 1, 3, 5, 1, 3,
           5, 1, 3, 5, 1, 3, 5, 1, 3, 5]
    expected = sorted(arr)
    hybrid_sort(arr)
    assert arr == expected, f"重复元素数组失败: {arr}"
    print("PASS  重复元素数组")


def test_small():
    """长度小于 16 的数组直接走插入排序"""
    arr = [7, 3, 9, 1, 5, 8, 2, 6, 4]
    expected = sorted(arr)
    hybrid_sort(arr)
    assert arr == expected, f"小数组失败: {arr}"
    print("PASS  小数组(<16)")


def test_edge():
    arr = []
    hybrid_sort(arr)
    assert arr == [], f"空数组失败: {arr}"
    arr = [1]
    hybrid_sort(arr)
    assert arr == [1], f"单元素数组失败: {arr}"
    arr = [2, 1]
    hybrid_sort(arr)
    assert arr == [1, 2], f"两元素数组失败: {arr}"
    print("PASS  边界用例")


def test_custom_threshold():
    """自定义阈值：threshold=4（最小值）和 threshold=32"""
    arr1 = [38, 27, 43, 3, 9, 82, 10, 55, 12, 7, 99, 1, 66, 21, 8, 30,
            44, 13, 70, 5, 18, 60, 77, 22, 14, 88, 33, 40, 50, 6]
    expected1 = sorted(arr1)
    hybrid_sort(arr1, threshold=4)
    assert arr1 == expected1, f"threshold=4 失败: {arr1}"
    print("PASS  自定义阈值 threshold=4")

    arr2 = list(range(100, 0, -1))
    expected2 = sorted(arr2)
    hybrid_sort(arr2, threshold=32)
    assert arr2 == expected2, f"threshold=32 失败: {arr2}"
    print("PASS  自定义阈值 threshold=32")

    # 阈值小于 MIN_THRESHOLD 时自动 clamp 到 4
    arr3 = [5, 3, 8, 1, 9, 2, 7, 4, 6]
    expected3 = sorted(arr3)
    hybrid_sort(arr3, threshold=1)
    assert arr3 == expected3, f"threshold=1(clamp) 失败: {arr3}"
    print("PASS  阈值 clamp 到 MIN_THRESHOLD")


if __name__ == "__main__":
    test_normal()
    test_sorted()
    test_reversed()
    test_duplicates()
    test_small()
    test_edge()
    test_custom_threshold()
    print("\n全部测试通过!")

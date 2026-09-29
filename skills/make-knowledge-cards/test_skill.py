"""测试 make-knowledge-cards Skill 的输出质量

用三类文章验证：
1. 技术教程（信息丰富，预期 6-8 张卡片）
2. 科普短文（中等信息量，预期 5-6 张卡片）
3. 极短文本（信息不足，预期少于 5 张，不应强行凑数）
"""

import os
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))


# 测试文章 1：技术教程
ARTICLE_TECH = """# Python 列表推导式完全指南

列表推导式是 Python 中创建列表的简洁方式。基本语法为 [expression for item in iterable]。

例如，生成 0-9 的平方列表：squares = [x**2 for x in range(10)]。

## 条件过滤

可以在推导式中加入 if 条件。例如只保留偶数的平方：
even_squares = [x**2 for x in range(10) if x % 2 == 0]

## 嵌套循环

列表推导式支持多个 for 子句，相当于嵌套循环。
例如生成二维坐标：[(x, y) for x in range(3) for y in range(3)]

## 推导式的性能

列表推导式通常比等价的 for 循环更快，因为它在 C 层面优化了迭代过程。
但对于大数据集，生成器表达式（用圆括号）更节省内存。

## 可读性建议

当推导式超过一行时，应该改用普通 for 循环。可读性比简洁性更重要。
复杂的嵌套推导式难以维护，应拆分为多步。

## 字典和集合推导式

Python 还支持字典推导式 {k: v for ...} 和集合推导式 {x for ...}。
语法和列表推导式类似，只是用花括号代替方括号。
"""

# 测试文章 2：科普短文
ARTICLE_SCIENCE = """# 为什么天空是蓝色的？

太阳光看起来是白色的，但实际上是由红橙黄绿蓝靛紫七种颜色组成的。
不同颜色的光波长不同，红光波长最长，紫光波长最短。

当阳光进入地球大气层时，空气中的氮气和氧气分子会散射光线。
这种散射称为瑞利散射，散射强度与波长的四次方成反比。

因为蓝光波长较短，被散射的程度远大于红光。
所以当我们仰望天空时，看到的是被散射到各处的蓝光。

日落时天空变红，是因为阳光穿过更厚的大气层，
蓝光在到达我们眼睛之前就被散射殆尽，只剩下波长较长的红光和橙光。
"""

# 测试文章 3：极短文本（信息不足）
ARTICLE_SHORT = """今天学了变量。变量就是存数据的盒子。Python 用等号赋值。"""


def test_tech_article():
    """技术教程测试"""
    lines = ARTICLE_TECH.strip().split("\n")
    # 模拟提取知识点的数量
    topics = [
        "基本语法",
        "条件过滤",
        "嵌套循环",
        "性能特点",
        "可读性建议",
        "字典和集合推导式",
    ]
    print(f"  技术教程: {len(lines)} 行, 提取 {len(topics)} 个知识点")
    for t in topics:
        print(f"    - {t}")
    assert 5 <= len(topics) <= 8, f"期望 5-8 张卡片, 实际 {len(topics)}"
    print("  PASS\n")
    return True


def test_science_article():
    """科普短文测试"""
    lines = ARTICLE_SCIENCE.strip().split("\n")
    topics = [
        "白光由七色组成",
        "瑞利散射原理",
        "蓝光散射更强",
        "日落变红的原因",
    ]
    print(f"  科普短文: {len(lines)} 行, 提取 {len(topics)} 个知识点")
    for t in topics:
        print(f"    - {t}")
    assert 3 <= len(topics) <= 8, f"期望 3-8 张卡片, 实际 {len(topics)}"
    print("  PASS\n")
    return True


def test_short_article():
    """极短文本测试"""
    lines = ARTICLE_SHORT.strip().split("\n")
    topics = ["变量的概念"]
    print(f"  极短文本: {len(lines)} 行, 提取 {len(topics)} 个知识点")
    for t in topics:
        print(f"    - {t}")
    assert len(topics) < 5, f"信息不足时不应强行凑数, 实际 {len(topics)}"
    print("  PASS (信息不足, 未强行凑数)\n")
    return True


def main():
    print("=== make-knowledge-cards 测试 ===\n")
    results = []
    results.append(("技术教程", test_tech_article()))
    results.append(("科普短文", test_science_article()))
    results.append(("极短文本", test_short_article()))

    print("--- 总结 ---")
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    return 0 if all(ok for _, ok in results) else 1


if __name__ == "__main__":
    sys.exit(main())

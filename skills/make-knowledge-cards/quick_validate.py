"""快速验证 make-knowledge-cards Skill 结构完整性

无第三方依赖，纯标准库实现。
"""

import sys
import os
import re

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_simple_yaml(text):
    """简易 YAML 解析，只支持 key: value 格式（不含嵌套）"""
    result = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([\w]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2)
            # 尝试解析数字
            if re.match(r"^-?\d+$", val):
                result[key] = int(val)
            elif re.match(r"^-?\d+\.\d+$", val):
                result[key] = float(val)
            else:
                result[key] = val
    return result


def validate_skill_md():
    """验证 SKILL.md 格式和内容"""
    path = os.path.join(SKILL_DIR, "SKILL.md")
    if not os.path.exists(path):
        return False, "SKILL.md not found"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 检查 frontmatter
    if not content.startswith("---"):
        return False, "SKILL.md missing frontmatter"

    parts = content.split("---", 2)
    if len(parts) < 3:
        return False, "SKILL.md frontmatter not closed"

    fm_text = parts[1].strip()
    fm = parse_simple_yaml(fm_text)
    if "name" not in fm or "description" not in fm:
        return False, "frontmatter missing name or description"

    name = fm["name"]
    if not re.match(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$", name):
        return False, f"invalid name: {name}"

    desc = fm["description"]
    if len(desc) > 200:
        return False, f"description too long ({len(desc)} chars, max 200)"

    body = parts[2].strip()
    if len(body) < 50:
        return False, "body too short"

    return True, f"SKILL.md OK (name={name})"


def validate_openai_yaml():
    """验证 agents/openai.yaml"""
    path = os.path.join(SKILL_DIR, "agents", "openai.yaml")
    if not os.path.exists(path):
        return False, "agents/openai.yaml not found"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 检查必需的 key（不使用 yaml 库，用正则）
    required_keys = ["model", "temperature", "max_tokens", "system_prompt"]
    for key in required_keys:
        if not re.search(rf"^{key}\s*:", content, re.MULTILINE):
            return False, f"openai.yaml missing key: {key}"

    # 检查 temperature 值
    temp_match = re.search(r"^temperature:\s*([\d.]+)", content, re.MULTILINE)
    if temp_match:
        temp = float(temp_match.group(1))
        if not 0 <= temp <= 2:
            return False, f"temperature out of range: {temp}"

    # 检查 system_prompt 长度（提取 | 后的内容）
    sp_match = re.search(r"system_prompt:\s*\|(.*)", content, re.DOTALL)
    if sp_match:
        prompt_text = sp_match.group(1).strip()
        if len(prompt_text) < 50:
            return False, "system_prompt too short"

    return True, "openai.yaml OK"


def validate_structure():
    """验证目录结构"""
    expected = ["SKILL.md", "agents", os.path.join("agents", "openai.yaml")]
    for rel in expected:
        path = os.path.join(SKILL_DIR, rel)
        if not os.path.exists(path):
            return False, f"missing: {rel}"

    return True, "structure OK"


def main():
    checks = [
        ("Directory structure", validate_structure),
        ("SKILL.md", validate_skill_md),
        ("agents/openai.yaml", validate_openai_yaml),
    ]

    all_pass = True
    for label, check in checks:
        ok, msg = check()
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}: {msg}")
        if not ok:
            all_pass = False

    print()
    if all_pass:
        print("All checks passed!")
        return 0
    else:
        print("Validation FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())

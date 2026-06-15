import pyperclip

# 定义128位映射表
dictionary = "0123456789~!@#$%^&*_+[];',./{}:|<>?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ=`¡¢£¤¥¦§©ª¬®¯°±²³µ¿ØĀāĂăĄąĆćĈĉĊċČčĎďĐđĒē"
# 添加一个特殊字符作为负数标记（选择字典中不常用的字符）
NEGATIVE_SIGN = '​​Ω'
FLOAT_SIGN = '∑'
DIVIDE_SIGN = '∞'
VECTOR_SEPARATOR = '∫'
LEFT_BRACKET = '【'
RIGHT_BRACKET = '】'

def compress_number(num):
    """压缩单个数字为映射表中的字符或128进制表示，处理负数"""
    is_negative = num < 0
    abs_num = abs(num)
    
    if abs_num < len(dictionary):
        result = dictionary[abs_num]
    else:
        result = []
        while abs_num > 0:
            remainder = abs_num % len(dictionary)
            result.append(dictionary[remainder])
            abs_num = abs_num // len(dictionary)
        result = ''.join(reversed(result))
    
    # 如果是负数，添加负号前缀
    return f"{NEGATIVE_SIGN}{result}" if is_negative else result

def compress_item(item):
    """压缩单个元素（数字、字符串、列表或向量）"""
    if isinstance(item, float):
        # 处理小数：保留三位精度，乘以1000，并标记为\f
        rounded = round(item, 3)
        scaled = int(rounded * 1000)
        return f"{FLOAT_SIGN}{compress_number(scaled)}"
    elif isinstance(item, int):
        return f"{compress_number(int(item))}"
    elif isinstance(item, str):
        return f"s{item}"
    elif isinstance(item, tuple) and len(item) == 3:  # 向量处理
        return f"v{compress_item(item[0])}{VECTOR_SEPARATOR}{compress_item(item[1])}{VECTOR_SEPARATOR}{compress_item(item[2])}"
    elif isinstance(item, list):  # 列表处理（单层）
        compressed_items = [compress_item(sub) for sub in item]
        return f"{LEFT_BRACKET}{DIVIDE_SIGN.join(compressed_items)}{RIGHT_BRACKET}"  # 改为方括号
    else:
        raise ValueError(f"Unsupported item type: {type(item)}")

def compress(input_data):
    """压缩数据"""
    if isinstance(input_data, list):
        compressed_items = [compress_item(item) for item in input_data]
        return DIVIDE_SIGN.join(compressed_items)  # 移除外层的方括号
    else:
        return compress_item(input_data)  # 直接返回压缩后的单个元素

def split_into_chunks(text, chunk_size=128):
    """将字符串分割成指定大小的块，确保不分割嵌套结构和单个数据项"""
    chunks = []
    current_chunk = ""
    
    # 按数据项分隔符（反斜杠）拆分，但保留嵌套结构的完整性
    items = []
    i = 0
    n = len(text)
    
    while i < n:
        if text[i] == LEFT_BRACKET:
            # 找到匹配的】
            depth = 1
            j = i + 1
            while j < n and depth > 0:
                if text[j] == LEFT_BRACKET:
                    depth += 1
                elif text[j] == RIGHT_BRACKET:
                    depth -= 1
                j += 1
            # 提取完整的嵌套结构
            nested_item = text[i:j]
            items.append(nested_item)
            i = j
        else:
            # 普通项，找到下一个反斜杠或结束
            j = i
            while j < n and text[j] != DIVIDE_SIGN:
                j += 1
            item = text[i:j]
            items.append(item)
            i = j + 1 if j < n else j
    
    # 现在items中包含完整的嵌套结构和普通项
    for item in items:
        # 跳过空项
        if not item:
            continue
            
        # 如果当前块为空，直接添加
        if not current_chunk:
            new_chunk = item
        else:
            # 尝试添加分隔符和当前项
            new_chunk = current_chunk + DIVIDE_SIGN + item
        
        # 检查是否超出块大小
        if len(new_chunk) <= chunk_size:
            current_chunk = new_chunk
        else:
            # 如果添加后超出大小，保存当前块并开始新块
            if current_chunk:
                chunks.append(f'"{current_chunk}"')
            current_chunk = item
    
    # 添加最后一个块
    if current_chunk:
        chunks.append(f'"{current_chunk}"')
    
    return chunks

# 示例使用
if __name__ == "__main__":
    test_data = [
   (0,1,2),
   (31,3,4)
    ]
    compressed = compress(test_data)
    print("原始输入:", test_data)
    print("压缩结果:", compressed)
    
    # 将压缩结果分割成128字节的块
    chunks = split_into_chunks(compressed, 128)
    print(f"\n分割后的{len(chunks)}节块:")
    chunks_joined = ",".join(chunks)
    print(chunks_joined)

    pyperclip.copy(chunks_joined)
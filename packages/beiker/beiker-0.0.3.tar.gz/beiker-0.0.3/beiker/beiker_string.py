import random,re,json,os

def convert_path_to_system_style(path, system_type):  
    """  
    根据指定操作系统类型，将路径转换为相应的格式。  

    :param path: 待转换的路径  
    :param system_type: 指定的操作系统类型 ('linux' 或 'windows')  
    :return: 转换后的路径  
    """  
    if system_type.lower() == 'windows':  
        # 将路径中的斜杠替换为反斜杠  
        return path.replace('/', '\\')  
    elif system_type.lower() == 'linux':  
        # 将路径中的反斜杠替换为斜杠  
        return path.replace('\\', '/')  
    else:  
        raise ValueError("system_type must be either 'linux' or 'windows'.")  
        
def convert_path_to_native_style(generic_path):  
    """  
    根据当前操作系统，将通用路径转换为原生路径样式。  

    :param generic_path: 通用格式的文件路径（使用正斜杠 / 作为分隔符）  
    :return: 转换后的文件路径  
    """  
    # 检查当前操作系统  
    if os.name == 'nt':  # Windows  
        # 将通用路径转换为Windows路径  
        native_path = generic_path.replace('/', '\\')  
    else:  # Linux, macOS, etc.  
        # 将通用路径转换为Linux/Unix路径  
        native_path = generic_path.replace('\\', '/')  
    return native_path  

def convert_coords_to_json(coords_str):
    """
    Convert a string of coordinates in the format "[(x1, y1), (x2, y2), ...]" to a JSON array.

    :param coords_str: A string representing a list of coordinates.
    :return: A JSON string representing the array of coordinates.
    """
    # 去除字符串中的括号并按逗号分割成列表
    points = coords_str.strip('[]').split('), (')

    # 初始化 JSON 数组
    json_array = []

    # 遍历每个坐标点，将其转换为 JSON 对象
    for point in points:
        # 移除多余的空格和括号，然后按逗号分割 x 和 y 值
        x, y = point.strip('()').split(',')
        # 将坐标点添加到 JSON 数组中
        json_array.append({"x": int(x), "y": int(y)})

    # 将数组转换为 JSON 字符串
    return json.dumps(json_array)

def remove_all_whitespaces(input_string):
    """
    去除字符串中所有不可见字符或空格。包括：
    空格 ' '：普通的空格字符。
    制表符 '\t'：通常用于文本对齐的字符。
    换行符 '\n'：在文本中开始新行的字符。
    回车符 '\r'：在某些文本环境中用于回到行的开头。
    换页符 '\f'：用于分隔页面的字符。
    垂直制表符 '\v'：在文本中创建垂直分隔的字符。
    """
    # 创建一个转换表，将所有空白字符映射到None
    return input_string.translate(str.maketrans('', '', ' \t\n\r\f\v'))

def is_labels_series(series, values=['男', '女'], labels=('性别', '未识别')):
    """
    检查Series是否在values列表中,如果在就返回True,并将labels第一个元素返回，否则返回False,并将labels第二个元素返回。
    如果Series为空，那么返回False,并返回labels的第二个元素。

    参数:
    series : pd.Series
        要检查的Series。
    values : list
        认为是labels标签的列表，默认为['男', '女']。
    labels : tuple
        包含两个元素的元组，第一个元素是Series在values中时返回的标签，第二个元素是Series不在values中时返回的标签。

    返回:
    tuple
        包含一个布尔值和一个标签。布尔值表示Series是否完全由values中的元素组成，标签是相应的labels元素。
    """
    # 检查Series是否为空
    if series.empty:
        return False, labels[1]
    
    unique_values = series.unique()
    is_subset = set(unique_values).issubset(set(values))
    return is_subset, labels[0] if is_subset else labels[1]

def contains_empty_string(lst):
    """
    检查列表中是否包含空字符串，并返回空字符串元素的位置列表。

    参数:
    lst : list
        要检查的列表。

    返回:
    tuple
        包含一个布尔值，指示列表中是否包含空字符串，以及一个列表，包含所有空字符串元素的位置。
    """
    empty_string_positions = [index for index, value in enumerate(lst) if value == '']
    contains_empty = bool(empty_string_positions)  # 如果位置列表不为空，则包含空字符串
    return contains_empty, empty_string_positions

def generate_unique_column_name(existing_names, base_name):  
    """  
    生成一个唯一的列名，如果base_name已经存在于existing_names中，则在末尾添加随机数字。  

    参数:  
    existing_names : list  
        已存在的列名列表。  
    base_name : str  
        基础列名。  

    返回:  
    str  
        唯一的列名。  
    """  
    new_name = base_name  
    while new_name in existing_names:  
        new_name = f"{base_name}_{random.randint(1, 99)}"  # 在基础列名后添加随机数字  
    return new_name  

def extract_str_from_pattern_in_json_list(json_list, pattern): 
    """
    用正则表达式从json中获取匹配的字符串。
    """ 
    # 遍历每个条目  
    for entry in json_list:  
        # 在 head 中查找匹配  
        if 'head' in entry:  
            for item in entry['head']:  
                matches = re.findall(pattern, item)  
                if matches:  
                    # 如果找到匹配，返回结果  
                    return ' '.join(matches)  

        # 在 tail 中查找匹配  
        if 'tail' in entry:  
            for item in entry['tail']:  
                matches = re.findall(pattern, item)  
                if matches:  
                    # 如果找到匹配，返回结果  
                    return ' '.join(matches)  

    # 如果没有找到匹配，返回空字符串  
    return ''  
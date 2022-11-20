import sqlite3
from sqlite3 import Error
from androguard.misc import AnalyzeAPK


def connection():
    try:
        con = sqlite3.connect('test.db')
        return con
    except Error:
        print(Error)
        exit(-1)

def create_table(con):
    cursor_db = con.cursor()
    sql = 'SELECT COUNT(*) FROM sqlite_master Where name ="virus"'
    cursor_db.execute(sql)
    flag = cursor_db.fetchone()
    if flag[0]:
        print("Table is exist")
    else:
        cursor_db.execute("CREATE TABLE virus(MD5 string(32),sha1 string(40),sha256 string(64), category text, shap text)")
        con.commit()

def insert_line(con,data_list):
    cursor_db = con.cursor()
    flag = len(select_line(con,data_list[0]))
    if flag==0:
        sql ="INSERT INTO virus VALUES({});".format(("?,"*len(data_list))[:-1])
        cursor_db.execute(sql,tuple(data_list))
        con.commit()
    #if문 안거치는 것은 기존에 존재하는 것

def select_line(con,hash):
    cursor_db = con.cursor()
    sql=f"SELECT * FROM virus WHERE MD5 = {hash[0]} AND sha1 = {hash[1]} AND sha256 = {hash[2]}"
    cursor_db.execute(sql)
    data = cursor_db.fetchall()
    return data
    
def delete_line(con,hash):
    cursor_db = con.cursor()
    sql=f"DELETE FROM virus WHERE MD5 = {hash[0]} AND sha1 = {hash[1]} AND sha256 = {hash[2]}"
    cursor_db.execute(sql)
    con.commit()
      
if __name__=="__main__":
    ##DB 연결 및 구축 중
    con = connection()
    create_table(con)

    ## 테스트 셋
    data_list = ["123","123","123","123","123"] #타입 선언["md5","sha1","sha256","기타 정보들..."]
    
    print("[*]데이터 추가 중")
    insert_line(con,data_list)
    data = select_line(con,data_list)
    print("데이터 산출물")
    print(data)
    print("\n")
    
    
    print("[*]데이터 삭제 중")
    delete_line(con,data_list)
    data = select_line(con,data_list)
    print("데이터 산출물")
    print(data)
    
    ##1단계
    ##들어오는 apk에 대해서 hash lib 조회해서 만일 개수가 0이면,
    ##머신러닝으로 넘어가고 1이면, 바로 반환
    
    ##2단계
    ##만일 머신러닝을 거쳐 나온 결과물을 inser_line 함수를 이용해
    ##넣음
    
    
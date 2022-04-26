import os
# from config import mysql
import pymysql
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


def findSimilarity(text, content, id):
    '''

    :param text:  생성된 단락
    :param reviewContent: 데이터 베이스에 저장된 content
    :return: 겹치는 문장 리스트

    '''
    textList = text.split(' ')
    contentList = content.split(' ')
    result = []

    for i in range(len(contentList)):
        if i + 6 > len(contentList): break

        fiveWordList = contentList[i:i + 6]  # 비교할 content 영역

        for j in range(len(textList)):
            if j + 6 > len(textList): break

            if (fiveWordList == textList[j:j + 6]):
                originText = " ".join(textList[j:j + 6])
                result.append((originText, id))

    return result


# DataBase 에서 Id, Contents Load
def read_contents_from_database():
    try:
        conn = pymysql.connect(
            host=config['MYSQL_CONFIG']['sql_host'],
            user=config['MYSQL_CONFIG']['user'],
            password=config['MYSQL_CONFIG']['password'],
            db=config['MYSQL_CONFIG']['db'],
            charset=config['MYSQL_CONFIG']['charset']
        )
        curs = conn.cursor()

        sql = "select id, contents from dummy"

        curs.execute(sql)

        contentList = curs.fetchall()

    except Exception as e:
        print(e)
        return e

    finally:
        curs.close()
        conn.close()

    return contentList


def make_similarity_response_data(text):
    start = time.time()  # 시작 시간 저장
    contentList = read_contents_from_database()

    if contentList is Exception:
        return "데이터 베이스를 읽는데 실패했습니다."

    result = {}
    similaritySentenceList = []
    firstList = []

    contentsSize = len(contentList)  # Contents 사이즈
    for i in range(contentsSize):
        content = contentList[i][1]  # Content
        review_id = contentList[i][0]

        contentAndId = findSimilarity(text, content, review_id)  # 유사도 검출
        if contentAndId:  # list 가 있을 경우

            for items in contentAndId:
                firstList.append(items)

    secondList = []  # 중복되지 않은 Content 리스트
    for items in firstList:
        if not items[0] in secondList:
            secondList.append(items[0])

    for index, content in enumerate(secondList):
        newList = []
        if index %3 == 0 :
            newDict = {"id": str(index), "originText": content}
            newDict["similaritySearchData"] = newList
            similaritySentenceList.append(newDict)
            print(newDict)
            count = 0
            for items in firstList: #firstList => [(,reviewId),(,reviewId),(,reviewId) ... ]
                if content == items[0]:
                    # newList.append(items[1])
                    strCount = str(index) + "_" + str(count)
                    childDic = {"id": strCount, "originText" : items[1]}
                    newList.append(childDic)
                    count += 1
        else:
            pass

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    result["similaritySentenceList"] = similaritySentenceList

    return result

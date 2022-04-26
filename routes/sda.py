from flask import request, make_response
from flask_restx import Resource, Namespace
import tensorflow as tf

from service.generate import response_body_sda
from service.similarity import make_similarity_response_data

Sda = Namespace('sda')

@Sda.route('/gen')
class generate(Resource):
    def get(self):
        hello = {"Hello":"hello"}
        return make_response(hello, 200)

    def post(self):
        try:
            print(request)
            keyword = request.json.get("keyword") #입력 키워드
            size = int(request.json.get("size")) #문장 갯수
            type = request.json.get("type") #치과 or 한의원
            print("Post Data 형식")
            print(keyword)
            print(size)
            print(type)


            # 키워드가 존재하지 않을 시
            if len(keyword) == 0:
                raise Exception('text가 존재하지 않습니다.')

            #여기서 문장 생성 구문 실행 ....
            generatedText = response_body_sda(keyword, size)

        # except tf.errors.ResourceExhaustedError:
        #     result = 'GPU 메모리 사용량을 초과하였습니다'
        #     return make_response(result, 401)

        except Exception as e:
            # e 는 에러 종류
            result = {'error': str(e)}
            return make_response(result, 401)

        return make_response(generatedText, 200)


# 유사도 검출
@Sda.route('/similarity')
class Similarity(Resource):
    def post(self):

        #로직 5단어 같으면 해당 Content 반환
        # 1) 내부로직 -> 소유하는 Content 와 유사도 검출

        text = request.json.get("text")  # 입력 텍스트 ( 생성 문장 )

        result = make_similarity_response_data(text)

        # 2) 외부로직 -> 네이버 OpenAPI 를 사용하여 네이버 글에서 유사도 검출

        ##
        ##
        ##
        ##

        return make_response(result, 200)


# 의료법 체크
@Sda.route('/check')
class CheckRule(Resource):
    def get(self):

        # 생성예정

        return make_response()
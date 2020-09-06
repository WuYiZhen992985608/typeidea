import uuid


USER_KEY = 'uid'
TEN_YEARS = 60*60*24*365*10


class UserIDMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response


    def __call__(self,request):
        # 接受请求，先生成uid，并赋值给request
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        # 设置cookie，只在服务端能访问
        response.set_cookie(USER_KEY,uid,max_age=TEN_YEARS,httponly=True)
        return response

    # 生成随机数uid
    def generate_uid(self,request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid
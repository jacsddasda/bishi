# backend/index.py
from run import app
from werkzeug.wrappers import Request

# 华为云函数计算FC入口函数
def handler(event, context):
    # 解析HTTP请求
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    headers = event.get('headers', {})
    body = event.get('body', '')
    query_string = event.get('queryString', '')
    
    # 构建WSGI环境
    environ = {
        'REQUEST_METHOD': http_method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('Content-Type', ''),
        'CONTENT_LENGTH': str(len(body)),
        'wsgi.input': body,
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False
    }
    
    # 处理请求
    response_status = []
    response_headers = []
    
    def start_response(status, headers):
        response_status.append(status)
        response_headers.append(headers)
        return lambda data: None
    
    # 调用Flask应用
    response_body = b''
    for part in app(environ, start_response):
        if isinstance(part, bytes):
            response_body += part
        else:
            response_body += part.encode('utf-8')
    
    # 解析状态码
    status_code = 200
    if response_status:
        status_str = response_status[0]
        status_code = int(status_str.split()[0])
    
    # 构建响应头
    response_headers_dict = {}
    if response_headers:
        for header in response_headers[0]:
            response_headers_dict[header[0]] = header[1]
    
    # 构造返回结果
    return {
        'statusCode': status_code,
        'headers': response_headers_dict,
        'body': response_body.decode('utf-8')
    }

# 智能简历分析系统 - 华为云函数计算FC部署指南

## 1. 准备工作

### 1.1 华为云账号注册
- 访问 https://www.huaweicloud.com/ 注册华为云账号
- 完成实名认证

### 1.2 安装华为云CLI（可选）
- 下载并安装华为云CLI：https://support.huaweicloud.com/devg-cli/cli_03_0002.html
- 配置CLI凭证：
  ```bash
  hcloud configure
  ```

### 1.3 项目准备
- 确保项目已推送到GitHub仓库
- 确保 `backend/requirements.txt` 文件包含所有必要的依赖
- 确保项目在本地可以正常运行

## 2. 华为云函数计算FC部署

### 2.1 登录华为云控制台
- 访问 https://console.huaweicloud.com/
- 登录华为云账号

### 2.2 创建函数服务
1. **进入函数服务控制台**：
   - 点击控制台左侧导航栏，选择「服务列表」→「计算」→「函数服务」

2. **创建函数**：
   - 点击「创建函数」按钮
   - 选择「HTTP触发器」模板
   - 点击「下一步：函数配置」

3. **配置函数基本信息**：
   - 函数名称：`resume-analysis-api`
   - 运行环境：`Python 3.8`
   - 函数入口：`index.handler`（稍后会创建）
   - 内存规格：选择 `512MB`
   - 超时时间：设置为 `60` 秒
   - 点击「下一步：代码配置」

4. **配置代码**：
   - 代码来源：选择「从GitHub仓库获取」
   - 仓库地址：输入你的GitHub仓库地址（例如：`https://github.com/YOUR_USERNAME/resume-analysis-system.git`）
   - 分支：`master`
   - 代码目录：`backend`
   - 点击「下一步：触发器配置」

5. **配置触发器**：
   - 触发器类型：`HTTP触发器`
   - 触发器名称：`http-trigger`
   - 访问路径：`/api/{proxy}`
   - 认证方式：`匿名访问`
   - 点击「下一步：环境变量」

6. **配置环境变量**：
   - 点击「添加环境变量」
   - 添加以下环境变量（如果使用Redis）：
     | 变量名 | 值 |
     |-------|-----|
     | REDIS_HOST | 你的Redis主机地址 |
     | REDIS_PORT | 6379 |
     | REDIS_PASSWORD | 你的Redis密码 |
     | REDIS_DB | 0 |
   - 点击「下一步：确认」

7. **确认配置**：
   - 检查所有配置信息
   - 点击「创建函数」

### 2.3 创建入口文件
1. **在GitHub仓库中创建 `index.py` 文件**：
   ```python
   # backend/index.py
   from run import app
   from werkzeug.wrappers import Request, Response

   def handler(event, context):
       # 解析请求
       request = Request(event['body'])
       request.environ['REQUEST_METHOD'] = event['httpMethod']
       request.environ['PATH_INFO'] = event['path']
       request.environ['QUERY_STRING'] = event.get('queryString', '')
       
       # 处理请求
       response = app(request.environ, start_response)
       
       # 构造响应
       return {
           'statusCode': response.status_code,
           'headers': dict(response.headers),
           'body': ''.join(response)
       }

   def start_response(status, headers):
       pass
   ```

2. **更新 `run.py` 文件**：
   - 确保 `run.py` 文件中的 `app` 变量是全局可访问的
   - 确保服务启动代码在 `if __name__ == '__main__':` 块中

### 2.4 配置依赖
1. **确保 `requirements.txt` 文件包含所有必要的依赖**：
   ```
   Flask==2.0.1
   Flask-CORS==5.0.0
   PyPDF2==2.11.0
   python-dotenv==0.19.0
   redis==4.5.1
   requests==2.28.1
   ```

2. **部署依赖**：
   - 在函数服务控制台中，找到你的函数
   - 点击「依赖管理」
   - 点击「安装依赖」
   - 选择「从requirements.txt安装」
   - 点击「确定」

### 2.5 测试函数
1. **在函数服务控制台中**：
   - 找到你的函数
   - 点击「测试」
   - 选择「HTTP触发器测试事件」
   - 配置测试事件：
     ```json
     {
       "httpMethod": "GET",
       "path": "/api/upload",
       "body": ""
     }
     ```
   - 点击「测试」
   - 查看测试结果

## 3. 前端页面部署

### 3.1 部署到华为云OBS
1. **进入对象存储服务控制台**：
   - 点击控制台左侧导航栏，选择「服务列表」→「存储」→「对象存储服务OBS」

2. **创建存储桶**：
   - 点击「创建存储桶」
   - 桶名称：`resume-analysis-frontend`
   - 区域：选择与函数服务相同的区域
   - 存储类别：`标准存储`
   - 点击「创建桶」

3. **上传前端文件**：
   - 进入创建的存储桶
   - 点击「上传对象」
   - 上传 `frontend` 目录中的所有文件

4. **配置静态网站托管**：
   - 点击「基础配置」→「静态网站托管」
   - 点击「编辑」
   - 开启「静态网站托管」
   - 默认首页：`index.html`
   - 点击「保存」

5. **获取访问地址**：
   - 在静态网站托管配置页面，复制「访问域名」

### 3.2 更新前端API地址
1. **修改 `frontend/script.js` 文件**：
   ```javascript
   // 将这里的地址修改为你的函数服务地址
   fetch('https://your-function-service-url/api/upload', {
       // ...
   });

   // 和
   fetch('https://your-function-service-url/api/score', {
       // ...
   });
   ```

2. **重新上传 `script.js` 文件**：
   - 将修改后的 `script.js` 文件上传到OBS存储桶

## 4. 配置跨域访问

### 4.1 配置函数服务CORS
1. **在函数服务控制台中**：
   - 找到你的函数
   - 点击「配置」→「触发器管理」
   - 点击「编辑」HTTP触发器
   - 在「CORS配置」中，添加前端页面的域名
   - 点击「保存」

### 4.2 配置OBS CORS
1. **在对象存储服务控制台中**：
   - 找到你的存储桶
   - 点击「权限管理」→「CORS配置」
   - 点击「添加规则」
   - 来源：`*`（或你的函数服务域名）
   - 允许的方法：`GET, POST, OPTIONS`
   - 允许的头部：`*`
   - 点击「确定」

## 5. 测试部署

### 5.1 测试后端API
- 使用Postman或curl测试API：
  ```bash
  # 测试上传接口
  curl -X POST -F "file=@your_resume.pdf" https://your-function-service-url/api/upload

  # 测试评分接口
  curl -X POST -H "Content-Type: application/json" -d '{"resume_info": {...}, "job_description": "Python开发工程师"}' https://your-function-service-url/api/score
  ```

### 5.2 测试前端页面
- 访问OBS静态网站托管的域名，例如：
  ```
  https://resume-analysis-frontend.obs.cn-north-1.myhuaweicloud.com
  ```
- 测试上传简历和评分功能

## 6. 常见问题解决

### 6.1 依赖安装失败
- 确保 `requirements.txt` 文件格式正确
- 确保所有依赖都可以在华为云FC环境中安装
- 尝试使用 `pip freeze > requirements.txt` 生成依赖文件

### 6.2 函数启动失败
- 检查函数入口配置是否正确
- 检查 `index.py` 文件是否存在且格式正确
- 查看函数日志，了解具体错误信息

### 6.3 跨域错误
- 确保函数服务和OBS都配置了正确的CORS规则
- 确保前端代码中的API地址正确

### 6.4 内存不足
- 尝试增加函数的内存规格
- 优化代码，减少内存使用

## 7. 生产环境优化

### 7.1 性能优化
- 使用Redis缓存提高响应速度
- 优化PDF解析和信息提取算法
- 启用函数实例预留，减少冷启动时间

### 7.2 安全优化
- 添加文件类型验证和大小限制
- 使用HTTPS协议
- 实现请求速率限制
- 配置函数访问控制

### 7.3 监控和日志
- 配置函数日志收集
- 设置监控告警
- 定期查看函数执行情况

## 8. 总结

通过以上步骤，你已经成功将智能简历分析系统部署到华为云函数计算FC。系统现在可以：

1. 接收PDF简历并解析
2. 提取关键信息
3. 与岗位需求进行匹配评分
4. 通过前端页面展示结果

如果遇到任何问题，请参考「常见问题解决」部分，或查阅华为云函数服务文档。

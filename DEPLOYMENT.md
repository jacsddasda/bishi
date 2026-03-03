# 智能简历分析系统部署指南

## 1. 准备工作

### 1.1 安装Git
- 下载并安装Git：https://git-scm.com/downloads
- 配置Git用户名和邮箱：
  ```bash
  git config --global user.name "你的用户名"
  git config --global user.email "你的邮箱"
  ```

### 1.2 创建GitHub账号
- 访问 https://github.com/ 注册账号
- 创建一个新的仓库，例如 `resume-analysis-system`

## 2. 项目初始化和推送到GitHub

### 2.1 初始化Git仓库
在项目根目录执行：

```bash
# 进入项目目录
cd c:\Users\zwh\Documents\trae_projects\bishi

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交初始版本
git commit -m "Initial commit: 智能简历分析系统"
```

### 2.2 关联GitHub仓库
```bash
# 关联远程仓库（将YOUR_USERNAME替换为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/resume-analysis-system.git

# 推送代码到GitHub
git push -u origin master
```

## 3. 微信云服务器托管部署

### 3.1 登录微信云开发平台
- 访问 https://console.cloud.tencent.com/tcb
- 登录微信开发者账号

### 3.2 创建云开发环境
1. 点击「新建」创建一个云开发环境
2. 填写环境名称，例如 `resume-analysis`
3. 选择「按量付费」模式
4. 点击「立即开通」

### 3.3 部署后端服务

#### 方法一：使用云函数
1. 在云开发控制台中，进入「云函数」页面
2. 点击「新建」创建一个云函数
3. 填写函数名称，例如 `resume-analysis-api`
4. 选择运行环境为 `Python 3.8`
5. 选择「从本地上传代码」
6. 上传整个 `backend` 目录
7. 点击「下一步」
8. 设置触发方式为「HTTP触发」
9. 配置HTTP触发路径为 `/api`
10. 点击「完成」

#### 方法二：使用容器服务
1. 在云开发控制台中，进入「容器服务」页面
2. 点击「新建」创建一个容器
3. 选择「GitHub代码仓库」
4. 关联你的GitHub账号
5. 选择 `resume-analysis-system` 仓库
6. 配置构建命令：
   ```bash
   cd backend && pip install -r requirements.txt
   ```
7. 配置启动命令：
   ```bash
   cd backend && python run.py
   ```
8. 点击「下一步」
9. 配置端口映射为 `5000`
10. 点击「完成」

### 3.4 部署前端页面
1. 在云开发控制台中，进入「静态网站托管」页面
2. 点击「开启」静态网站托管
3. 上传整个 `frontend` 目录
4. 点击「部署」

### 3.5 配置跨域访问
1. 在云开发控制台中，进入「安全配置」页面
2. 将后端服务的域名添加到「跨域访问白名单」
3. 保存配置

## 4. 环境变量配置

### 4.1 后端服务环境变量
在云开发控制台中，为后端服务配置以下环境变量：

| 变量名 | 值 | 说明 |
|-------|-----|------|
| REDIS_HOST | redis-xxxxx.redis.rds.aliyuncs.com | Redis主机地址（如果使用Redis） |
| REDIS_PORT | 6379 | Redis端口 |
| REDIS_PASSWORD | your_redis_password | Redis密码 |
| REDIS_DB | 0 | Redis数据库编号 |

### 4.2 前端配置
修改 `frontend/script.js` 文件中的API地址：

```javascript
// 将这里的地址修改为你的后端服务地址
fetch('https://your-backend-service/api/upload', {
    // ...
});

// 和
fetch('https://your-backend-service/api/score', {
    // ...
});
```

## 5. 测试部署

### 5.1 测试后端API
使用Postman或curl测试API：

```bash
# 测试上传接口
curl -X POST -F "file=@your_resume.pdf" https://your-backend-service/api/upload

# 测试评分接口
curl -X POST -H "Content-Type: application/json" -d '{"resume_info": {...}, "job_description": "Python开发工程师"}' https://your-backend-service/api/score
```

### 5.2 测试前端页面
访问静态网站托管的域名，例如：
```
https://your-static-website.tcloudbase.com
```

## 6. 常见问题解决

### 6.1 跨域错误
- 确保在后端服务中启用了CORS
- 确保在云开发控制台中配置了正确的跨域访问白名单

### 6.2 依赖安装失败
- 确保 `requirements.txt` 文件包含了所有必要的依赖
- 尝试使用 `pip install --upgrade pip` 升级pip

### 6.3 服务启动失败
- 检查云函数的日志输出
- 确保端口配置正确
- 检查环境变量是否配置正确

## 7. 生产环境优化

### 7.1 性能优化
- 使用Redis缓存提高响应速度
- 启用Gunicorn等WSGI服务器
- 配置CDN加速静态资源

### 7.2 安全优化
- 添加文件类型验证
- 设置文件大小限制
- 使用HTTPS协议
- 实现请求速率限制

### 7.3 监控和日志
- 配置日志收集
- 设置监控告警
- 定期备份数据

## 8. 总结

通过以上步骤，你已经成功将智能简历分析系统部署到微信云服务器托管。系统现在可以：

1. 接收PDF简历并解析
2. 提取关键信息
3. 与岗位需求进行匹配评分
4. 通过前端页面展示结果

如果遇到任何问题，请参考「常见问题解决」部分，或查阅微信云开发文档。

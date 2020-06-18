# msgboard
My first django demo
# 简单的djanggo项目--留言板
内容包括：
- 两个页面: 1.登录页 2.留言展示与输入.  登录成功后自动跳转, 允许登出. 
- 所有用户能够浏览留言内容, 支持页面不刷新翻页查看. 
- 所有用户都能查看留言榜, 展示 TOP10 留言数量的用户昵称. 
- 只有登录用户允许留言. - 留言内容存储到 MongoDB 中, 查询时使用 Redis 缓存. 
- 自己本机搭建 Redis, MongoDB. 地址放配置文件中, 可修改. 
- 完善的异常处理与日志记录. 
### 涉及技术
- django
- Redis
- mongodb
- html
- Restful风格

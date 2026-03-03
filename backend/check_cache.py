from app.utils.cache import get_cache

# 查看特定简历的缓存
cache_key = "resume:赵文豪简历.pdf"
cached_data = get_cache(cache_key)

if cached_data:
    print("缓存数据：")
    print(f"文本长度：{len(cached_data.get('text', ''))} 字符")
    print("提取的信息：")
    print(f"基本信息：{cached_data.get('info', {}).get('basic_info', {})}")
    print(f"求职信息：{cached_data.get('info', {}).get('job_info', {})}")
    print(f"背景信息：{cached_data.get('info', {}).get('background_info', {})}")
else:
    print("缓存中没有找到该简历的数据")
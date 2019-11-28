
import hashlib
import re
def get_md5(url):
    # 如果是字符串类型 转一下字符编码
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# 正则获取时间
def regular_get_data(value):
    match_re_create = re.match('.*?(\d+.*)', value)
    if match_re_create:
        create_at = match_re_create.group(1)
    else:
        create_at = '1970-01-01'
    return create_at


import hashlib
def get_md5(url):
    # 如果是字符串类型 转一下字符编码
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


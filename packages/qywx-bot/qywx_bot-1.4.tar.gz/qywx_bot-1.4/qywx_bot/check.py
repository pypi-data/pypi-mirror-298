def text(s: str, max_bytes=2048) -> None:
    if not isinstance(s, str): raise TypeError("send_text error: The content must be a string!")
    # 将字符串转换为UTF-8编码的字节序列
    byte_array = s.encode('utf-8')
    # 检查字节序列的长度是否超过2048字节
    if len(byte_array) > max_bytes: raise ValueError("send_text error: The content is over 2048 bytes!")
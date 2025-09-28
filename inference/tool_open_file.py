from qwen_agent.tools.base import BaseTool, register_tool
import os

@register_tool('read_file', allow_overwrite=True)
class ReadFileTool(BaseTool):
    """
    用于读取指定文件内容的工具
    
    使用说明：
    - 需要提供参数path，指定要读取的文件路径
    - 路径可以是绝对路径，也可以是相对于当前工作目录的相对路径
    - 支持读取文本文件（如txt、py、md等）
    - 大文件会被截断显示，避免内容过多
    """
    
    def __init__(self):
        super().__init__()
        self.description = {
            "name": "read_file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要读取的文件路径，可以是绝对路径或相对路径"
                    }
                },
                "required": ["path"]
            },
            "description": "读取指定文件的内容并返回"
        }
        # 设置最大读取字节数，防止大文件占用过多资源
        self.MAX_BYTES = 1024 * 1024  # 1MB
    
    def call(self, params: dict = None, **kwargs) -> str:
        """执行工具，读取指定文件的内容"""
        if not params or "path" not in params:
            return "错误：请提供要读取的文件路径（path参数）"
        
        file_path = params["path"]
        
        try:
            # 规范化路径
            file_path = os.path.abspath(file_path)
            
            # 检查路径是否存在
            if not os.path.exists(file_path):
                return f"错误：文件不存在 - {file_path}"
            
            # 检查是否是文件
            if not os.path.isfile(file_path):
                return f"错误：指定的路径不是一个文件 - {file_path}"
            
            # 检查文件大小
            file_size = os.path.getsize(file_path)
            if file_size > self.MAX_BYTES:
                return f"警告：文件过大（{file_size}字节），超过最大限制（{self.MAX_BYTES}字节），无法读取"
            
            # 尝试读取文件内容，支持多种编码
            encodings = ['utf-8', 'gbk', 'latin-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                return f"错误：无法解码文件内容，可能是二进制文件 - {file_path}"
            
            return f"文件 {file_path} 的内容：\n\n{content}\n\n文件读取完毕"
            
        except Exception as e:
            return f"读取文件时出错: {str(e)}"
    
    def check_params(self, params: dict) -> bool:
        """检查参数是否有效，确保提供了有效的path参数"""
        return params is not None and "path" in params and isinstance(params["path"], str) and len(params["path"].strip()) > 0
    
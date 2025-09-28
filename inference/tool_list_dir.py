from qwen_agent.tools.base import BaseTool, register_tool
import os

@register_tool('list_directory', allow_overwrite=True)
class ListDirectoryTool(BaseTool):
    """
    用于列出指定目录下所有文件和文件夹的工具
    
    使用说明：
    - 需要提供参数path，指定要查看的目录路径
    - 路径可以是绝对路径，也可以是相对于当前工作目录的相对路径
    - 返回结果包括项目名称和类型（文件或文件夹）
    """
    
    def __init__(self):
        super().__init__()
        self.description = {
            "name": "list_directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "要列出内容的目录路径，可以是绝对路径或相对路径"
                    }
                },
                "required": ["path"]
            },
            "description": "列出指定目录下的所有文件和文件夹"
        }
    
    def call(self, params: dict = None, **kwargs) -> str:
        """执行工具，列出指定目录的所有文件和文件夹"""
        if not params or "path" not in params:
            return "错误：请提供要查看的目录路径（path参数）"
        
        target_path = params["path"]
        
        try:
            # 规范化路径
            target_path = os.path.abspath(target_path)
            
            # 检查路径是否存在
            if not os.path.exists(target_path):
                return f"错误：路径不存在 - {target_path}"
            
            # 检查是否是目录
            if not os.path.isdir(target_path):
                return f"错误：指定的路径不是一个目录 - {target_path}"
            
            # 获取目录中的所有项目
            items = os.listdir(target_path)
            
            # 收集结果，区分文件和文件夹
            result = []
            for item in items:
                item_path = os.path.join(target_path, item)
                if os.path.isdir(item_path):
                    result.append(f"📁 文件夹: {item}")
                else:
                    result.append(f"📄 文件: {item}")
            
            if not result:
                return f"目录 {target_path} 为空"
            
            return f"目录 ({target_path}) 中的内容:\n" + "\n".join(result)
            
        except Exception as e:
            return f"获取目录内容时出错: {str(e)}"
    
    def check_params(self, params: dict) -> bool:
        """检查参数是否有效，确保提供了path参数"""
        return params is not None and "path" in params and isinstance(params["path"], str) and len(params["path"].strip()) > 0
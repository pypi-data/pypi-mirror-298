import warnings

try:
    from typing import Any, Dict, List, Literal, Optional, Tuple, Union, Callable, Set, Type 
    from langchain_core.tools import BaseTool
    from langchain_community.tools import _module_lookup
    from pydantic.v1 import BaseModel
    import json
except ImportError:
    warnings.warn("Langchain dependencies are not installed. To use LangchainTools, install the required packages with 'pip install taskflowai[langchain_tools]'")

class LangchainTools:
    @staticmethod
    def _check_dependencies():
        if 'BaseTool' not in globals() or '_module_lookup' not in globals():
            raise ImportError("Langchain dependencies are not installed. To use LangchainTools, install the required packages with 'pip install taskflowai[langchain_tools]'")

    @staticmethod
    def _wrap(langchain_tool: Type[BaseTool]) -> Callable:
        def wrapped_tool(**kwargs: Any) -> str:
            tool_instance = langchain_tool()
            # Convert kwargs to a single string input
            tool_input = json.dumps(kwargs)
            return tool_instance.run(tool_input)
        
        tool_instance = langchain_tool()
        name = getattr(tool_instance, 'name', langchain_tool.__name__)
        description = getattr(tool_instance, 'description', "No description available")
        
        doc_parts = []
        doc_parts.append(f"- {name}:")
        doc_parts.append(f"    Description: {description}")
        
        args_schema = getattr(langchain_tool, 'args_schema', None) or getattr(tool_instance, 'args_schema', None)
        if args_schema and issubclass(args_schema, BaseModel):
            doc_parts.append("    Arguments:")
            for field_name, field in args_schema.__fields__.items():
                field_desc = field.field_info.description or "No description"
                doc_parts.append(f"      - {field_name}: {field_desc}")
        
        wrapped_tool.__name__ = name
        wrapped_tool.__doc__ = "\n".join(doc_parts)
        return wrapped_tool
    
    @classmethod
    def get_tool(cls, tool_name: str) -> Callable:
        cls._check_dependencies()
        """
        Retrieve and wrap a specified Langchain tool.

        Args:
            tool_name (str): Name of the Langchain tool to retrieve.

        Returns:
            Callable: A wrapped Langchain tool as a callable function.

        Raises:
            ValueError: If an unknown tool name is provided.

        Example:
            >>> tool = LangchainTools.get_tool("WikipediaQueryRun")
        """
        if tool_name not in _module_lookup:
            raise ValueError(f"Unknown Langchain tool: {tool_name}")
        
        module_path = _module_lookup[tool_name]
        module = __import__(module_path, fromlist=[tool_name])
        tool_class = getattr(module, tool_name)
        
        wrapped_tool = LangchainTools._wrap(tool_class)
        return wrapped_tool

    @classmethod
    def list_available_tools(cls) -> List[str]:
        """
        List all available Langchain tools.

        Returns:
            List[str]: A list of names of all available Langchain tools.

        Raises:
            ImportError: If langchain-community is not installed.

        Example:
            >>> tools = LangchainTools.list_available_tools()
            >>> "WikipediaQueryRun" in tools
            True
        """
        try:
            from langchain_community.tools import _module_lookup
        except ImportError:
            print("Error: langchain-community is not installed. Please install it using 'pip install langchain-community'.")
            return []
        
        return list(_module_lookup.keys())

    @classmethod
    def get_tool_info(cls, tool_name: str) -> dict:
        """
        Retrieve information about a specific Langchain tool.

        Args:
            tool_name (str): The name of the Langchain tool.

        Returns:
            dict: A dictionary containing the tool's name, description, and module path.

        Raises:
            ValueError: If an unknown tool name is provided.

        Example:
            >>> info = LangchainTools.get_tool_info("WikipediaQueryRun")
            >>> "name" in info and "description" in info and "module_path" in info
            True
        """
        if tool_name not in _module_lookup:
            raise ValueError(f"Unknown Langchain tool: {tool_name}")
        
        module_path = _module_lookup[tool_name]
        module = __import__(module_path, fromlist=[tool_name])
        tool_class = getattr(module, tool_name)
        
        tool_instance = tool_class()
        name = getattr(tool_instance, 'name', tool_class.__name__)
        description = getattr(tool_instance, 'description', "No description available")
        
        return {
            "name": name,
            "description": description,
            "module_path": module_path
        }

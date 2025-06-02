import json
from typing import Dict, Any, List, Tuple
from app.common.openai_clinet import call_openai_api


class ParameterResolver:
    @staticmethod
    async def resolve_parameters(
        user_input: str, required_params: List[str]
    ) -> Dict[str, Any]:
        """解析用户输入中的参数"""
        try:
            prompt = f"""
            从用户输入中提取以下参数:
            {', '.join(required_params)}

            用户输入: {user_input}

            如果参数有多个可能值，请按以下规则处理：
            1. 时间参数：优先选择最明确的时间表达
            2. 数值参数：优先选择具体数值而非范围
            3. 分类参数：优先选择明确提到的分类
            4. 如有多个同类参数，选择距离关键词最近的一个

            **严格要求：只返回有效的JSON格式，不要添加任何解释或说明**
            
            返回格式示例:
            {{
                "parameters": {{"参数名": "参数值"}},
                "ambiguities": [{{
                    "param": "参数名",
                    "options": ["候选值1", "候选值2"],
                    "selected": "选中值",
                    "reason": "选择原因"
                }}]
            }}
            """

            response = await call_openai_api(
                [
                    {"role": "system", "content": "你是一个参数提取专家。只返回有效的JSON格式，不要添加任何其他内容。"},
                    {"role": "user", "content": prompt},
                ]
            )

            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()

            result = json.loads(response)
            return result["parameters"], result.get("ambiguities", [])

        except json.JSONDecodeError as e:
            raise ValueError(f"AI返回的不是有效JSON格式: {response}, 错误: {e}")
        except Exception as e:
            raise ValueError(f"参数解析失败: {e}")

    @staticmethod
    async def resolve_parameter_conflicts(
        params: Dict[str, Any], ambiguities: List[Dict]
    ) -> Tuple[Dict[str, Any], List[Dict]]:
        """处理参数冲突和歧义"""
        resolved_params = params.copy()
        unresolved_conflicts = []

        for ambiguity in ambiguities:
            param = ambiguity["param"]
            if len(ambiguity["options"]) > 1:
                if not ambiguity.get("selected"):
                    unresolved_conflicts.append(ambiguity)
                else:
                    resolved_params[param] = ambiguity["selected"]

        return resolved_params, unresolved_conflicts

    @staticmethod
    def validate_parameters(params: Dict[str, Any], required_params: List[str]) -> bool:
        """验证是否所有必需参数都已提供"""
        return all(param in params for param in required_params)

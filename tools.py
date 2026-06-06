"""
AI Metrics Tools - AI指标工具
支持指标设计、收集、分析
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIMetricsTools:
    """
    AI指标工具
    支持：设计、收集、分析
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def design_metrics_system(self, application: str, goals: List[str]) -> Dict:
        """设计指标系统"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        goals_text = ", ".join(goals)

        prompt = f"""请为{application}设计指标系统：

目标：{goals_text}

请返回JSON格式：
{{
    "metrics": [
        {{"name": "指标名", "type": "类型", "unit": "单位"}}
    ],
    "collection": "收集方案",
    "tools": ["推荐工具"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"metrics": content}

    def generate_prometheus_config(self, services: List[str]) -> str:
        """生成Prometheus配置"""
        if not self.client:
            return "LLM客户端未配置"

        services_text = ", ".join(services)

        prompt = f"""请生成Prometheus配置：

服务：{services_text}

要求：
1. 抓取配置
2. 告警规则
3. 记录规则"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def generate_custom_metrics(self, service: str, business_metrics: List[str]) -> str:
        """生成自定义指标"""
        if not self.client:
            return "LLM客户端未配置"

        metrics_text = ", ".join(business_metrics)

        prompt = f"""请为{service}生成自定义指标：

业务指标：{metrics_text}

要求：
1. 指标定义
2. 采集代码
3. 注册配置"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def design_alerting(self, metrics: List[str], thresholds: Dict) -> Dict:
        """设计告警"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        metrics_text = ", ".join(metrics)
        thresholds_text = json.dumps(thresholds, ensure_ascii=False)

        prompt = f"""请设计告警规则：

指标：{metrics_text}
阈值：{thresholds_text}

请返回JSON格式：
{{
    "alerts": [
        {{"name": "告警名", "condition": "条件", "severity": "级别"}}
    ]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"alerting": content}

    def analyze_metrics(self, metrics_data: Dict) -> Dict:
        """分析指标"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        data_text = json.dumps(metrics_data, ensure_ascii=False)

        prompt = f"""请分析以下指标数据：

{data_text}

请返回JSON格式：
{{
    "summary": "总结",
    "trends": ["趋势"],
    "anomalies": ["异常"],
    "recommendations": ["建议"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"analysis": content}

    def generate_dashboards(self, service: str, metrics: List[str]) -> str:
        """生成仪表板"""
        if not self.client:
            return "LLM客户端未配置"

        metrics_text = ", ".join(metrics)

        prompt = f"""请为{service}生成Grafana仪表板：

指标：{metrics_text}

要求：
1. 概览面板
2. 详细面板
3. 告警面板"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content


def create_tools(**kwargs) -> AIMetricsTools:
    """创建指标工具"""
    return AIMetricsTools(**kwargs)


if __name__ == "__main__":
    tools = create_tools()

    print("AI Metrics Tools")
    print()

    # 测试
    system = tools.design_metrics_system("电商应用", ["转化率", "留存率"])
    print(json.dumps(system, ensure_ascii=False, indent=2))

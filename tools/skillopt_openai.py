"""
SkillOpt API Client: OpenAI Standard Implementation

Drop-in replacement for SkillOpt's azure_openai.py.
Uses standard OpenAI client instead of Azure-specific implementation.

Usage:
    from skillopt_openai import SkillOptClient
    
    client = SkillOptClient(
        api_key="sk-...",
        optimizer_model="gpt-4",
        target_model="gpt-3.5-turbo"
    )
    
    # Use like standard OpenAI client
    response = client.generate_skill_edits(...)
"""

import os
from typing import Optional, Dict, List, Any
from openai import OpenAI, AzureOpenAI


class SkillOptClient:
    """Unified client for SkillOpt training with OpenAI or Azure endpoints."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        optimizer_model: str = "gpt-4",
        target_model: str = "gpt-3.5-turbo",
        use_azure: bool = False,
        azure_endpoint: Optional[str] = None,
        azure_api_version: str = "2024-05-01-preview",
    ):
        """
        Initialize SkillOpt client.
        
        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
            optimizer_model: Model for generating skill edits (e.g., 'gpt-4', 'gpt-5.5')
            target_model: Model running as agent (e.g., 'gpt-3.5-turbo')
            use_azure: If True, use Azure OpenAI endpoint
            azure_endpoint: Azure endpoint URL (uses AZURE_OPENAI_ENDPOINT if not provided)
            azure_api_version: Azure API version
        """
        self.optimizer_model = optimizer_model
        self.target_model = target_model
        self.use_azure = use_azure
        
        if use_azure:
            endpoint = azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
            key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
            
            if not endpoint or not key:
                raise ValueError(
                    "Azure mode requires AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY "
                    "(or pass as parameters)"
                )
            
            self.client = AzureOpenAI(
                api_key=key,
                api_version=azure_api_version,
                azure_endpoint=endpoint,
            )
        else:
            # Standard OpenAI
            key = api_key or os.getenv("OPENAI_API_KEY")
            
            if not key:
                raise ValueError(
                    "OpenAI mode requires OPENAI_API_KEY environment variable "
                    "or api_key parameter"
                )
            
            self.client = OpenAI(api_key=key)
    
    def generate_skill_edits(
        self,
        skill_doc: str,
        rollout_results: List[Dict[str, Any]],
        domain: str = "qa",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Dict[str, Any]:
        """
        Generate skill edits based on rollout failures.
        
        Args:
            skill_doc: Current skill document (markdown)
            rollout_results: List of {task, output, target, score}
            domain: Task domain (affects prompt)
            temperature: Sampling temperature
            max_tokens: Max tokens for response
        
        Returns:
            {
                "edits": [{"type": "add/delete/replace", "section": "...", "content": "..."}],
                "reasoning": "Why these edits help",
                "improvement_estimate": 0.8
            }
        """
        # Build context from rollout failures
        failures = [r for r in rollout_results if r.get("score", 1.0) < 0.8]
        
        if not failures:
            return {"edits": [], "reasoning": "No improvement opportunities", "improvement_estimate": 0.0}
        
        prompt = self._build_edit_prompt(skill_doc, failures, domain)
        
        response = self.client.chat.completions.create(
            model=self.optimizer_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing agent performance and optimizing instruction sets."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return self._parse_edits(response.choices[0].message.content)
    
    def evaluate_skill(
        self,
        skill_doc: str,
        test_cases: List[Dict[str, Any]],
        domain: str = "qa",
        temperature: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Evaluate skill on test cases using target model.
        
        Args:
            skill_doc: Skill document (markdown)
            test_cases: List of {question, context, expected_answer, ...}
            domain: Task domain
            temperature: Sampling temperature
        
        Returns:
            {
                "scores": [0.9, 0.8, ...],
                "accuracy": 0.85,
                "failures": [...]
            }
        """
        results = []
        failures = []
        
        for case in test_cases:
            prompt = self._build_agent_prompt(skill_doc, case, domain)
            
            response = self.client.chat.completions.create(
                model=self.target_model,
                messages=[
                    {"role": "system", "content": skill_doc},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=500,
            )
            
            output = response.choices[0].message.content
            score = self._score_output(output, case.get("expected_answer", ""))
            
            results.append(score)
            
            if score < 0.8:
                failures.append({
                    "task": case.get("question", ""),
                    "output": output,
                    "expected": case.get("expected_answer", ""),
                    "score": score
                })
        
        return {
            "scores": results,
            "accuracy": sum(results) / len(results) if results else 0,
            "failures": failures,
        }
    
    def _build_edit_prompt(self, skill_doc: str, failures: List[Dict], domain: str) -> str:
        """Build prompt for skill optimizer."""
        failure_text = "\n".join([
            f"- Task: {f.get('task', '')}\n"
            f"  Output: {f.get('output', '')}\n"
            f"  Expected: {f.get('target', '')}\n"
            f"  Score: {f.get('score', 0)}"
            for f in failures[:5]  # Show first 5 failures
        ])
        
        return f"""
Current skill document:
```
{skill_doc}
```

Recent failures (where agent underperformed):
{failure_text}

Generate 1-3 specific edits to improve the skill document:
- For ADD: what instruction to insert?
- For DELETE: what section is harmful?
- For REPLACE: what's the better instruction?

Return JSON:
{{
  "edits": [
    {{"type": "add", "section": "...", "content": "..."}},
  ],
  "reasoning": "Why this helps with the failures",
  "improvement_estimate": 0.8
}}
"""
    
    def _build_agent_prompt(self, skill_doc: str, case: Dict, domain: str) -> str:
        """Build prompt for agent rollout."""
        if domain == "qa":
            return f"""
Question: {case.get('question', '')}
Context: {case.get('context', '')}

Answer:
"""
        return str(case)
    
    def _score_output(self, output: str, expected: str) -> float:
        """Simple scoring: check if expected answer is in output."""
        if not expected:
            return 0.5
        
        # Fuzzy matching (in real impl, use semantic similarity)
        score = 0.5
        if expected.lower() in output.lower():
            score = 0.95
        elif any(word in output.lower() for word in expected.lower().split()):
            score = 0.75
        
        return score
    
    def _parse_edits(self, response_text: str) -> Dict[str, Any]:
        """Parse optimizer response into structured edits."""
        import json
        
        try:
            # Try to extract JSON from response
            if "{" in response_text:
                json_str = response_text[response_text.index("{"):response_text.rindex("}")+1]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback: return empty edits
        return {
            "edits": [],
            "reasoning": response_text[:200],
            "improvement_estimate": 0.0
        }


def create_skillopt_client(
    api_key: Optional[str] = None,
    optimizer_model: str = "gpt-4",
    target_model: str = "gpt-3.5-turbo",
    use_azure: bool = False,
) -> SkillOptClient:
    """Factory function for creating SkillOpt client."""
    
    # Auto-detect Azure vs OpenAI based on env vars
    if not use_azure:
        use_azure = bool(os.getenv("AZURE_OPENAI_ENDPOINT"))
    
    return SkillOptClient(
        api_key=api_key,
        optimizer_model=optimizer_model,
        target_model=target_model,
        use_azure=use_azure,
    )


# Example usage
if __name__ == "__main__":
    # Initialize client (auto-detects Azure vs OpenAI)
    client = create_skillopt_client(
        optimizer_model="gpt-4",
        target_model="gpt-3.5-turbo"
    )
    
    # Example skill
    example_skill = """
# Question Answering Skill

You are a helpful question-answering assistant.

## Context Handling
- Read all provided context carefully
- Extract relevant information
- Cite sources when possible

## Answer Quality
- Be concise and direct
- Answer only what is asked
- Admit uncertainty when appropriate
"""
    
    # Example test cases
    test_cases = [
        {
            "question": "What is the capital of France?",
            "context": "France is a country in Europe. Paris is its capital.",
            "expected_answer": "Paris"
        }
    ]
    
    # Evaluate
    results = client.evaluate_skill(example_skill, test_cases)
    print(f"Accuracy: {results['accuracy']:.2%}")
    print(f"Failures: {len(results['failures'])}")
    
    # Generate edits if failures
    if results['failures']:
        edits = client.generate_skill_edits(
            example_skill,
            results['failures']
        )
        print(f"Generated {len(edits['edits'])} edits")

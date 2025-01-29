from litellm import completion
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Dictionary of model configurations
MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    # "gpt-3.5": {
    #     "model": "openai/gpt-3.5-turbo",
    #     "api_key_env": "OPENAI_API_KEY",
    #     "description": "Fast and cost-effective model"
    # },
    "claude-3-5-sonnet-20241022": {
        "model": "anthropic/claude-3-5-sonnet-20241022",
        "api_key_env": "ANTHROPIC_API_KEY",
        "description": "Latest Claude 3 Sonnet - balanced performance and speed"
    },
    "gemini": {
        "model": "gemini/gemini-2.0-flash-exp",
        "api_key_env": "GEMINI_API_KEY",
        "description": "Google's Gemini Pro model"
    }
}

def setup_api_keys() -> None:
    """Load API keys from environment variables"""
    load_dotenv()
    
    # Verify if keys are loaded and properly formatted
    required_keys = {
        "OPENAI_API_KEY": "sk-",
        "ANTHROPIC_API_KEY": "sk-ant-",
        "GEMINI_API_KEY": "AIzaSy"
    }
    
    for key, prefix in required_keys.items():
        value = os.getenv(key)
        if not value:
            print(f"Warning: {key} is not set")
        elif not value.startswith(prefix):
            print(f"Warning: {key} format looks incorrect (should start with '{prefix}')")

def test_model(model_name: str, prompt: str) -> None:
    """Test a specific model with a given prompt"""
    if model_name not in MODEL_CONFIGS:
        print(f"Model {model_name} not found in configurations")
        return

    config = MODEL_CONFIGS[model_name]
    api_key = os.getenv(config["api_key_env"])
    
    if not api_key:
        print(f"Warning: {config['api_key_env']} not set")
        return

    try:
        print(f"\n=== Testing {model_name} ===")
        print(f"Description: {config['description']}")
        
        messages = [{"role": "user", "content": prompt}]
        response = completion(
            model=config["model"],
            messages=messages,
            api_key=api_key
        )
        
        content = response.choices[0].message.content
        print("\nResponse:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        
    except Exception as e:
        print(f"Error with {model_name}: {str(e)}")

def main():
    setup_api_keys()
    
    # Print available models with descriptions
    print("Available models:")
    for name, config in MODEL_CONFIGS.items():
        print(f"- {name}: {config.get('description', 'No description available')}")
    
    # Test prompt
    prompt = "Write a short poem about artificial intelligence"
    
    # Test all available models
    for model_name in MODEL_CONFIGS:
        test_model(model_name, prompt)

if __name__ == "__main__":
    main()

from litellm import completion
import os
from typing import Dict, Any
from dotenv import load_dotenv
import argparse

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

class TextSplitter:
    def __init__(self):
        setup_api_keys()
        # Support multiple models
        self.models = ["claude-3-5-sonnet-20241022", "gemini"]
        
    def split_text_with_model(self, text: str, model_name: str) -> list[str]:
        """Split text using a specific model"""
        if not text:
            return []
            
        config = MODEL_CONFIGS[model_name]
        api_key = os.getenv(config["api_key_env"])
        
        if not api_key:
            raise ValueError(f"API key not found for {model_name}")
            
        prompt = f"""Split this text into natural, learnable segments. Each segment should:
- Be self-contained and meaningful
- Be around 1-2 sentences long
- Preserve the original meaning and flow
- Not be too long or complex

Text to split:
{text}

Return only the segments as a Python list of strings, with no additional text or explanation."""

        try:
            response = completion(
                model=config["model"],
                messages=[{"role": "user", "content": prompt}],
                api_key=api_key
            )
            
            content = response.choices[0].message.content
            
            # Try to safely evaluate the response as a Python list
            try:
                segments = eval(content)
                if isinstance(segments, list) and all(isinstance(s, str) for s in segments):
                    return segments
            except:
                pass
                
            # Fallback: Split by newlines if response isn't a valid Python list
            segments = [s.strip() for s in content.split('\n') if s.strip()]
            return segments
            
        except Exception as e:
            print(f"Error splitting text with {model_name}: {str(e)}")
            return None
            
    def split_text_all_models(self, text: str) -> Dict[str, list[str]]:
        """Split text using all available models and return results"""
        results = {}
        for model in self.models:
            try:
                segments = self.split_text_with_model(text, model)
                if segments:
                    results[model] = segments
            except Exception as e:
                print(f"Error with {model}: {str(e)}")
                continue
        return results

def test_text_splitter():
    """Test the TextSplitter class with sample texts"""
    splitter = TextSplitter()
    
    test_cases = [
        {
            "name": "Short paragraph",
            "text": "Artificial Intelligence is changing our world. It helps us solve complex problems and automate tasks. The future of AI looks promising.",
        },
        {
            "name": "Lyrics format",
            "text": """In the digital age we live
Technology grows and thrives
AI leads the way ahead
Making changes in our lives""",
        },
        {
            "name": "Long paragraph",
            "text": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. Deep learning, a subset of machine learning, uses artificial neural networks to analyze different factors with a structure that mimics the human brain. These technologies are revolutionizing various industries including healthcare, finance, and transportation.",
        }
    ]
    
    print("\n=== Testing TextSplitter ===\n")
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print("Input text:")
        print("-" * 50)
        print(test_case['text'])
        print("-" * 50)
        
        # Get results from all models
        results = splitter.split_text_all_models(test_case['text'])
        
        # Print results for each model
        for model, segments in results.items():
            print(f"\n{model} split result:")
            print("-" * 50)
            if segments:
                for i, segment in enumerate(segments, 1):
                    print(f"{i}. {segment}")
            else:
                print("Error: No segments returned")
            print("-" * 50)
        
        print("\n" + "=" * 80 + "\n")

def main():
    setup_api_keys()
    
    # Add command line argument parsing
    parser = argparse.ArgumentParser(description='Test LiteLLM functionality')
    parser.add_argument('--test-split', action='store_true', help='Test text splitting functionality')
    parser.add_argument('--test-models', action='store_true', help='Test model responses')
    args = parser.parse_args()
    
    if args.test_split:
        test_text_splitter()
    elif args.test_models:
        # Original model testing code
        print("Available models:")
        for name, config in MODEL_CONFIGS.items():
            print(f"- {name}: {config.get('description', 'No description available')}")
        
        prompt = "Write a short poem about artificial intelligence"
        for model_name in MODEL_CONFIGS:
            test_model(model_name, prompt)
    else:
        print("Please specify a test to run:")
        print("  --test-split   Test text splitting functionality")
        print("  --test-models  Test model responses")

if __name__ == "__main__":
    main()

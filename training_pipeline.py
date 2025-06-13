"""
LLM Training Pipeline for GUARDIAN Convergence AI
Implements multiple training approaches using validated, bias-free data
"""

import json
import pandas as pd
from typing import List, Dict, Any
from utils.convergence_ai import ConvergenceAI
import logging

class GuardianTrainingPipeline:
    """
    Training pipeline for custom LLM training using Convergence AI validated data
    """
    
    def __init__(self, convergence_ai: ConvergenceAI):
        self.convergence_ai = convergence_ai
        self.training_formats = {
            'openai': self._format_for_openai,
            'huggingface': self._format_for_huggingface,
            'anthropic': self._format_for_anthropic,
            'custom': self._format_for_custom
        }
        
    def export_training_data(self, format_type: str = 'openai', min_quality: float = 0.8) -> str:
        """
        Export validated training data in specified format
        
        Args:
            format_type: 'openai', 'huggingface', 'anthropic', or 'custom'
            min_quality: Minimum quality threshold for training data
        
        Returns:
            Path to exported training file
        """
        # Get validated outputs above quality threshold
        validated_data = []
        for output in self.convergence_ai.validated_outputs:
            quality_score = (
                output['quality_scores']['confidence'] * 
                output['quality_scores']['bias_mitigation'] * 
                output['quality_scores']['poisoning_resistance']
            )
            
            if quality_score >= min_quality:
                validated_data.append(output)
        
        if not validated_data:
            raise ValueError("No validated data meets quality threshold")
        
        # Format data for specified platform
        formatter = self.training_formats[format_type]
        formatted_data = formatter(validated_data)
        
        # Export to file
        filename = f"guardian_training_data_{format_type}.jsonl"
        with open(filename, 'w') as f:
            for item in formatted_data:
                f.write(json.dumps(item) + '\n')
        
        logging.info(f"Exported {len(formatted_data)} training examples to {filename}")
        return filename
    
    def _format_for_openai(self, validated_data: List[Dict]) -> List[Dict]:
        """Format data for OpenAI fine-tuning"""
        formatted = []
        for item in validated_data:
            formatted.append({
                "messages": [
                    {"role": "user", "content": item['input']},
                    {"role": "assistant", "content": item['output']}
                ]
            })
        return formatted
    
    def _format_for_huggingface(self, validated_data: List[Dict]) -> List[Dict]:
        """Format data for HuggingFace training"""
        formatted = []
        for item in validated_data:
            formatted.append({
                "instruction": item['input'],
                "response": item['output'],
                "quality_score": (
                    item['quality_scores']['confidence'] * 
                    item['quality_scores']['bias_mitigation'] * 
                    item['quality_scores']['poisoning_resistance']
                )
            })
        return formatted
    
    def _format_for_anthropic(self, validated_data: List[Dict]) -> List[Dict]:
        """Format data for Anthropic Claude fine-tuning"""
        formatted = []
        for item in validated_data:
            formatted.append({
                "prompt": f"Human: {item['input']}\n\nAssistant:",
                "completion": f" {item['output']}"
            })
        return formatted
    
    def _format_for_custom(self, validated_data: List[Dict]) -> List[Dict]:
        """Format data for custom training frameworks"""
        return validated_data  # Return full data with metadata
    
    def generate_training_report(self) -> Dict[str, Any]:
        """Generate comprehensive training data report"""
        validated_data = self.convergence_ai.validated_outputs
        
        if not validated_data:
            return {"status": "no_training_data"}
        
        # Calculate statistics
        quality_scores = []
        bias_scores = []
        poison_scores = []
        confidence_scores = []
        
        for item in validated_data:
            qs = item['quality_scores']
            quality_scores.append(qs['confidence'] * qs['bias_mitigation'] * qs['poisoning_resistance'])
            bias_scores.append(qs['bias_mitigation'])
            poison_scores.append(qs['poisoning_resistance'])
            confidence_scores.append(qs['confidence'])
        
        # Domain analysis
        domains = self._analyze_domains(validated_data)
        
        return {
            "total_validated_examples": len(validated_data),
            "avg_quality_score": sum(quality_scores) / len(quality_scores),
            "avg_bias_mitigation": sum(bias_scores) / len(bias_scores),
            "avg_poisoning_resistance": sum(poison_scores) / len(poison_scores),
            "avg_confidence": sum(confidence_scores) / len(confidence_scores),
            "domain_distribution": domains,
            "recommended_training_size": min(len(validated_data), 10000),
            "data_quality_assessment": self._assess_data_quality(quality_scores)
        }
    
    def _analyze_domains(self, validated_data: List[Dict]) -> Dict[str, int]:
        """Analyze domain distribution in training data"""
        domains = {
            'cybersecurity': 0,
            'ai_policy': 0,
            'quantum': 0,
            'general': 0
        }
        
        for item in validated_data:
            text = item['input'].lower() + " " + item['output'].lower()
            
            if any(term in text for term in ['cyber', 'security', 'threat', 'vulnerability']):
                domains['cybersecurity'] += 1
            elif any(term in text for term in ['quantum', 'qubit', 'superposition']):
                domains['quantum'] += 1
            elif any(term in text for term in ['policy', 'regulation', 'compliance', 'governance']):
                domains['ai_policy'] += 1
            else:
                domains['general'] += 1
        
        return domains
    
    def _assess_data_quality(self, quality_scores: List[float]) -> str:
        """Assess overall training data quality"""
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        if avg_quality >= 0.9:
            return "Excellent - Ready for production fine-tuning"
        elif avg_quality >= 0.8:
            return "Good - Suitable for domain-specific training"
        elif avg_quality >= 0.7:
            return "Fair - Consider filtering for higher quality subset"
        else:
            return "Poor - Recommend collecting more validated data"


# Training Options Guide
"""
## LLM Training Options with GUARDIAN

### 1. OpenAI Fine-tuning
- Use validated data with OpenAI's fine-tuning API
- Format: {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
- Cost: $8/1M tokens training, $12/1M tokens inference
- Best for: GPT-3.5/4 customization

### 2. HuggingFace Transformers
- Train open-source models (Llama 2, Mistral, etc.)
- Use QLoRA for efficient fine-tuning
- Cost: GPU time only (~$1-5/hour)
- Best for: Custom models with full control

### 3. Local Training with Ollama
- Train completely local models
- Use validated data for continuous improvement
- Cost: Hardware only
- Best for: Privacy-sensitive applications

### 4. Anthropic Constitutional AI
- Use validated data to train Constitutional AI principles
- Format data with human feedback patterns
- Best for: Safety-focused applications

### 5. Recursive Self-Training (Automated)
- Already implemented in Convergence AI
- Automatically improves with usage
- Zero additional cost
- Best for: Continuous improvement without manual intervention
"""

def create_training_config(approach: str) -> Dict[str, Any]:
    """Create training configuration for different approaches"""
    
    configs = {
        'openai_finetuning': {
            'platform': 'OpenAI',
            'model_base': 'gpt-3.5-turbo',
            'training_steps': 3,
            'learning_rate': 0.0001,
            'batch_size': 1,
            'validation_split': 0.2,
            'cost_estimate': '$50-200 for 1000 examples'
        },
        
        'huggingface_lora': {
            'platform': 'HuggingFace',
            'model_base': 'microsoft/DialoGPT-medium',
            'training_method': 'LoRA',
            'rank': 16,
            'alpha': 32,
            'dropout': 0.1,
            'learning_rate': 0.0002,
            'epochs': 3,
            'cost_estimate': '$20-100 for GPU time'
        },
        
        'local_ollama': {
            'platform': 'Ollama',
            'model_base': 'llama2:7b',
            'training_method': 'Adapter',
            'context_length': 4096,
            'temperature': 0.7,
            'cost_estimate': 'Hardware only'
        },
        
        'recursive_training': {
            'platform': 'Convergence AI',
            'method': 'Automatic validation and improvement',
            'quality_threshold': 0.8,
            'bias_threshold': 0.7,
            'poison_threshold': 0.75,
            'cost_estimate': 'Included in system'
        }
    }
    
    return configs.get(approach, {})


if __name__ == "__main__":
    # Example usage
    from utils.convergence_ai import ConvergenceAI
    
    # Initialize Convergence AI
    convergence = ConvergenceAI()
    
    # Create training pipeline
    pipeline = GuardianTrainingPipeline(convergence)
    
    # Generate training report
    report = pipeline.generate_training_report()
    print("Training Data Report:", json.dumps(report, indent=2))
    
    # Export training data for OpenAI
    if report['total_validated_examples'] > 0:
        training_file = pipeline.export_training_data('openai', min_quality=0.8)
        print(f"Training data exported to: {training_file}")
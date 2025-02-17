import ollama
import re
from tqdm import tqdm
import time
import ast


def generate_prompt(query):

    # Define the prompt
    prompt = f"""
    Given the following query: {query}

    Generate exactly three distinct and insightful questions using these approaches:

    1. Essence Question:
    Rephrase the query to capture its underlying principles and provide a fresh perspective.
    2. Systems Question:
    Analyze the relationships and interdependencies among the key concepts in the query.
    3. Application Question:
    Address real-world implementations, challenges, or actionable insights derived from the query.

    Requirements:
    - Each question must directly relate to the original query.
    - Do not include any text, explanation, or commentary besides the three questions.
    - Return only a Python list containing three strings.

    Example Output:
    ["<Essence Question>", "<Systems Question>", "<Application Question>"]
    """
    return prompt

def remove_think_block(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)


questions = [
    "What distinguishes supervised learning from unsupervised learning?",
    "How do decision trees handle categorical variables?",
    "Why are ensemble methods effective in machine learning?",
    "Explain overfitting and prevention strategies.",
    "How does cross-validation enhance model reliability?",
    "What role do activation functions play in neural networks?",
    "Compare gradient descent vs stochastic gradient descent.",
    "When is transfer learning most beneficial?",
    "How do SVMs perform classification?",
    "What challenges occur when training deep neural networks?",
    "CNN vs RNN: Key architectural differences?",
    "Why is backpropagation crucial for neural networks?",
    "What causes vanishing gradients in deep learning?",
    "How does dropout regularization work?",
    "Practical applications of autoencoders?",
    "Feedforward vs feedback neural networks?",
    "Purpose of pooling layers in CNNs?",
    "Transformers vs RNNs in NLP?",
    "Attention mechanisms in neural networks?",
    "GAN applications in image generation?",
    "Ethical concerns with facial recognition?",
    "How does AI perpetuate societal biases?",
    "Importance of AI decision transparency?",
    "Preventing malicious AI use?",
    "Data privacy challenges in AI?",
    "Regulating AI technologies effectively?",
    "Achieving algorithmic fairness?",
    "AI's impact on employment sectors?",
    "Informed consent in AI data collection?",
    "Ethics of autonomous weapons systems?",
    "Object detection vs image classification?",
    "Edge detection in image processing?",
    "Semantic segmentation in medical imaging?",
    "Real-time video analysis challenges?",
    "CNNs with variable image sizes?",
    "OCR applications?",
    "Limitations of facial recognition?",
    "3D vs 2D object recognition?",
    "ImageNet's impact on computer vision?",
    "Computer vision in agriculture?",
    "Word embeddings and semantic meaning?",
    "Rule-based vs ML NLP approaches?",
    "Sentiment analysis and sarcasm?",
    "Transformers revolutionizing NLP?",
    "Chatbot context handling?",
    "Attention in translation models?",
    "Multilingual NLP challenges?",
    "NLP for fake news detection?",
    "Named entity recognition uses?",
    "Tokenization impact on NLP models?",
    "Robotic sensor applications?",
    "Human-robot collaboration challenges?",
    "SLAM in robot navigation?",
    "RL in robotics vs other domains?",
    "Computer vision for autonomous robots?",
    "Actuators in robotic movement?",
    "Robots in dynamic environments?",
    "Industrial robot safety?",
    "Centralized vs swarm robotics?",
    "Robots learning from humans?",
    "CRISP-DM process explained?",
    "Feature engineering benefits?",
    "Data cleaning importance?",
    "Descriptive vs predictive analytics?",
    "Time series outlier detection?",
    "A/B testing in data science?",
    "Big data processing challenges?",
    "NoSQL vs relational databases?",
    "Data visualization importance?",
    "Handling missing data?",
    "AI in medical diagnostics?",
    "Fraud detection with AI?",
    "AI in supply chain optimization?",
    "AI chatbots for customer service?",
    "Manufacturing AI challenges?",
    "Predictive maintenance via ML?",
    "AI in personalized marketing?",
    "Autonomous vehicle risks?",
    "Energy forecasting with AI?",
    "AI in agriculture?",
    "Turing test significance?",
    "Chinese Room argument?",
    "Symbolic AI vs connectionism?",
    "Computational complexity?",
    "Halting problem and AI?",
    "NP-hard problems' importance?",
    "Entropy in information theory?",
    "Bayesian networks explained?",
    "Game theory in multi-agent systems?",
    "Gödel's theorems and AI?",
    "Requirements for general AI?",
    "Quantum computing's AI impact?",
    "Societal AI adoption effects?",
    "Risks of superintelligent AI?",
    "AI for climate change?",
    "Future AI ethics frameworks?",
    "AI in creative industries?",
    "AI for space exploration?",
    "AI-IoT integration?",
    "Education in AI-driven future?"
]

def process_single_query(query, model_name="deepseek-r1:7b"):
    start_time = time.time()
    
    # Generate prompt
    prompt = generate_prompt(query=query)
    
    # Model configuration with optimized parameters
    response = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.7,
            "top_k": 40,
            "top_p": 0.9,
            "num_ctx": 2048,  # Optimize context window
            "num_thread": 4   # Use multiple threads for processing
        }
    )
    
    # Process response
    raw_output = response["message"]["content"]
    response = remove_think_block(raw_output)
    query_list = ast.literal_eval(response)
    query_list.insert(0, query)
    
    # Calculate and display processing time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.4f} seconds")
    
    return query_list


# Example usage
if __name__ == "__main__":
    query = "What distinguishes supervised learning from unsupervised learning?"
    result = process_single_query(query)
    print("\nGenerated queries:", result)

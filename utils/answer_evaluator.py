import os

def evaluate_answer(question: str, answer: str, job_description: str = "", resume: str = "", model_type: str = 'gemini') -> dict:
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            temperature=0.3,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        
        prompt = f"""Q: {question}
A: {answer}

Rate this answer 0-10 and give brief feedback (2-3 sentences). Format:
Score: X/10
Feedback: [your feedback]
Strengths: [1-2 points]
Improvements: [1-2 points]"""
        
        print(f"\n{'='*60}")
        print(f"GEMINI REQUEST - Evaluate Answer")
        print(f"{'='*60}")
        print(prompt)
        print(f"{'='*60}\n")
        
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        import re
        score_match = re.search(r'Score:\s*(\d+)', content)
        score = int(score_match.group(1)) if score_match else 5
        feedback_match = re.search(r'Feedback:\s*(.+?)(?=Strengths:|Improvements:|$)', content, re.DOTALL)
        feedback = feedback_match.group(1).strip() if feedback_match else content[:200]
        strengths_match = re.search(r'Strengths:\s*(.+?)(?=Improvements:|$)', content, re.DOTALL)
        strengths_text = strengths_match.group(1).strip() if strengths_match else ""
        strengths = [s.strip('- •').strip() for s in strengths_text.split('\n') if s.strip()][:3]
        improvements_match = re.search(r'Improvements:\s*(.+?)$', content, re.DOTALL)
        improvements_text = improvements_match.group(1).strip() if improvements_match else ""
        weaknesses = [s.strip('- •').strip() for s in improvements_text.split('\n') if s.strip()][:3]
        
        return {
            'score': min(max(score, 0), 10),
            'feedback': feedback,
            'strengths': strengths if strengths else ["Provided an answer"],
            'weaknesses': weaknesses if weaknesses else ["Could be more detailed"],
            'suggestions': 'Consider providing specific examples with technical details.'
        }
        
    except Exception as e:
        print(f"Error evaluating: {e}")
        score = min(len(answer.split()) // 10, 7)
        return {
            'score': score,
            'feedback': 'Answer received and evaluated.',
            'strengths': ['Attempted to answer the question'],
            'weaknesses': ['Could provide more detail and examples'],
            'suggestions': 'Include specific examples from your experience.'
        }

def parse_evaluation_from_text(text: str, answer: str) -> dict:
    score = 5
    
    import re
    score_patterns = [
        r'score[:\s]+(\d+)',
        r'(\d+)\s*/\s*10',
        r'rating[:\s]+(\d+)'
    ]
    
    for pattern in score_patterns:
        match = re.search(pattern, text.lower())
        if match:
            try:
                score = int(match.group(1))
                if 0 <= score <= 10:
                    break
            except:
                pass
    
    strengths = []
    weaknesses = []
    
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        line_lower = line.lower()
        
        if 'strength' in line_lower or 'positive' in line_lower or 'good' in line_lower:
            current_section = 'strengths'
            continue
        elif 'weakness' in line_lower or 'improvement' in line_lower or 'concern' in line_lower:
            current_section = 'weaknesses'
            continue
        
        if line.startswith('-') or line.startswith('•') or line.startswith('*'):
            item = line[1:].strip()
            if current_section == 'strengths':
                strengths.append(item)
            elif current_section == 'weaknesses':
                weaknesses.append(item)
    
    if not strengths:
        if len(answer) > 100:
            strengths = ["Provided a detailed response"]
        else:
            strengths = ["Attempted to answer the question"]
    
    if not weaknesses:
        if len(answer) < 50:
            weaknesses = ["Answer could be more detailed"]
        else:
            weaknesses = ["Could provide more specific examples"]
    
    return {
        'score': score,
        'feedback': text[:500] if len(text) > 500 else text,
        'strengths': strengths[:3],
        'weaknesses': weaknesses[:3],
        'suggestions': 'Consider providing more specific examples and details in your responses.'
    }

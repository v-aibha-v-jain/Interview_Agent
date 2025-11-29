import os
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List

def extract_skills_with_gemini(text: str, doc_type: str = "job description") -> List[str]:
    try:
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            temperature=0,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        
        prompt = f"List ONLY the technical skills from this {doc_type} (comma-separated, max 10 skills):\n\n{text[:1500]}"
        
        print(f"\n{'='*60}")
        print(f"GEMINI REQUEST - Extract Skills from {doc_type.upper()}")
        print(f"{'='*60}")
        print(prompt)
        print(f"{'='*60}\n")
        
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        skills = [s.strip() for s in content.split(',')]
        return [s for s in skills if len(s) > 1 and len(s) < 30][:10]
    except Exception as e:
        print(f"Error with Gemini: {e}")
        return extract_skills_local(text)

def extract_skills_local(text: str) -> List[str]:
    tech_keywords = [
        'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue', 'svelte',
        'node.js', 'nodejs', 'express', 'django', 'flask', 'spring', 'springboot',
        'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis', 'dynamodb',
        'aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes', 'k8s',
        'git', 'ci/cd', 'jenkins', 'github actions', 'gitlab',
        'rest api', 'rest', 'api', 'graphql', 'grpc', 'soap',
        'html', 'css', 'sass', 'scss', 'tailwind', 'bootstrap',
        'webpack', 'vite', 'babel', 'npm', 'yarn',
        'microservices', 'serverless', 'lambda', 'agile', 'scrum', 'devops',
        'machine learning', 'ml', 'ai', 'deep learning', 'data science',
        'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'scikit-learn',
        'nlp', 'computer vision', 'opencv', 'llm',
        'c++', 'c#', '.net', 'go', 'golang', 'rust', 'ruby', 'php',
        'cassandra', 'elasticsearch', 'kafka', 'rabbitmq',
        'testing', 'jest', 'pytest', 'selenium', 'junit'
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in tech_keywords:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return list(set(found_skills))[:10]

def generate_interview_questions(job_description: str, resume: str, model_type: str = 'gemini') -> List[dict]:
    job_skills = extract_skills_with_gemini(job_description, "job description")
    resume_skills = extract_skills_local(resume)
    try:
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            temperature=0.7,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        
        skills_summary = f"Job requires: {', '.join(job_skills[:8])}\nCandidate has: {', '.join(resume_skills[:8])}"
        
        prompt = f"""{skills_summary}

Generate 5 interview questions (mix of technical and behavioral). Format:
1. [Question text]
2. [Question text]
..."""
        
        print(f"\n{'='*60}")
        print(f"GEMINI REQUEST - Generate Questions")
        print(f"{'='*60}")
        print(prompt)
        print(f"{'='*60}\n")
        
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        questions = parse_questions_from_text(content)
        if len(questions) < 5:
            fallback = [
                {'question': f"Tell me about your experience with {job_skills[0] if job_skills else 'this role'}.", 'category': 'Technical', 'difficulty': 'Medium'},
                {'question': 'Describe a challenging project you worked on and the outcome.', 'category': 'Experience', 'difficulty': 'Medium'},
                {'question': 'How do you handle tight deadlines and pressure?', 'category': 'Behavioral', 'difficulty': 'Easy'},
                {'question': 'What motivates you in your work?', 'category': 'Behavioral', 'difficulty': 'Easy'},
                {'question': 'Where do you see yourself in 2-3 years?', 'category': 'Behavioral', 'difficulty': 'Easy'}
            ]
            questions.extend(fallback[:5 - len(questions)])
        
        return questions[:5]
        
    except Exception as e:
        print(f"Error generating questions: {e}")
        questions = []
        for skill in (job_skills + resume_skills)[:3]:
            questions.append({'question': f"Tell me about your experience with {skill}.", 'category': 'Technical', 'difficulty': 'Medium'})
        
        questions.extend([
            {'question': 'Describe a challenging project you completed.', 'category': 'Experience', 'difficulty': 'Medium'},
            {'question': 'How do you approach problem-solving?', 'category': 'Behavioral', 'difficulty': 'Easy'}
        ])
        
        return questions[:5]

def parse_questions_from_text(text: str) -> List[dict]:
    questions = []
    lines = text.split('\n')
    
    categories = ['Technical', 'Behavioral', 'Experience', 'Problem-solving']
    difficulties = ['Easy', 'Medium', 'Hard']
    cat_idx = 0
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 10:
            continue
        
        question_text = None
        
        if any(line.startswith(f"{i}.") or line.startswith(f"{i})") for i in range(1, 20)):
            question_text = line.split('.', 1)[-1].split(')', 1)[-1].strip()
        elif line.lower().startswith(('what', 'how', 'why', 'describe', 'tell', 'explain', 'can you', 'have you', 'do you')):
            question_text = line
        
        if question_text and len(question_text) > 15:
            questions.append({
                'question': question_text,
                'category': categories[cat_idx % len(categories)],
                'difficulty': difficulties[cat_idx % len(difficulties)]
            })
            cat_idx += 1
    
    return questions[:10]

def generate_followup_question(original_question: str, answer: str, model_type: str = 'gemini') -> dict:
    try:
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            temperature=0.7,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        
        prompt = f"""Previous Q: {original_question}
Previous A: {answer}

Generate 1 follow-up question to dig deeper. Just write the question."""
        
        print(f"\n{'='*60}")
        print(f"GEMINI REQUEST - Generate Follow-up Question")
        print(f"{'='*60}")
        print(prompt)
        print(f"{'='*60}\n")
        
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)
        
        followup_text = content.strip()
        
        for prefix in ["Follow-up:", "Question:", "Q:", "Next:", "Here's", "Here is"]:
            if followup_text.startswith(prefix):
                followup_text = followup_text[len(prefix):].strip()
        
        if len(followup_text) < 20 or '?' not in followup_text:
            return generate_followup_fallback(original_question, answer)
        
        return {
            'question': followup_text,
            'category': 'Follow-up',
            'difficulty': 'Hard'
        }
        
    except Exception as e:
        print(f"Error generating follow-up: {e}")
        return generate_followup_fallback(original_question, answer)

def generate_followup_fallback(original_question: str, answer: str) -> dict:
    import re
    
    answer_lower = answer.lower()
    question_lower = original_question.lower()
    
    topic_match = re.search(r'(?:about|with|experience with|using|in)\s+([A-Za-z][A-Za-z\s.]+?)(?:\?|\.|\s+What)', original_question, re.IGNORECASE)
    main_topic = topic_match.group(1).strip() if topic_match else "this"
    
    if any(word in answer_lower for word in ['project', 'built', 'developed', 'created', 'worked on']):
        question_text = f"Can you describe the technical challenges you faced while working with {main_topic} and how you solved them?"
    elif len(answer.split()) < 20:
        question_text = f"Could you provide a specific real-world example of how you've used {main_topic} in production?"
    elif 'api' in question_lower or 'rest' in question_lower:
        question_text = "How do you handle API authentication, error handling, and rate limiting in your implementations?"
    elif 'react' in question_lower or 'frontend' in question_lower:
        question_text = "Can you explain how you handle state management and component lifecycle in your applications?"
    else:
        question_text = f"What performance optimizations have you implemented when using {main_topic}?"
    
    return {
        'question': question_text,
        'category': 'Follow-up',
        'difficulty': 'Hard'
    }

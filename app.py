import streamlit as st
import os
from dotenv import load_dotenv
from utils.document_processor import extract_text_from_file
from utils.question_generator import generate_interview_questions
from utils.answer_evaluator import evaluate_answer

load_dotenv()
st.set_page_config(
    page_title="AI Interview Agent",
    page_icon="🎯",
    layout="wide"
)

if 'job_description' not in st.session_state:
    st.session_state.job_description = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0
if 'evaluations' not in st.session_state:
    st.session_state.evaluations = []
if 'ai_model' not in st.session_state:
    st.session_state.ai_model = 'gemini'
st.title("🎯 AI Interview Agent")
st.markdown("Upload job description and resume to generate tailored interview questions and evaluate responses.")
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.ai_model = 'gemini'
    st.success("✅ Using Google Gemini 2.5 Flash")
    st.info("Latest model with generous free tier")
    
    st.markdown("---")
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. Upload Job Description
    2. Upload Candidate Resume
    3. Generate Questions
    4. Enter Answers
    5. Evaluate Responses
    """)
tab1, tab2, tab3 = st.tabs(["📤 Upload Documents", "❓ Questions", "📊 Evaluation"])
with tab1:
    st.header("Upload Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Job Description")
        job_desc_option = st.radio(
            "Input method:",
            ["Upload File", "Paste Text"],
            key="job_desc_option"
        )
        
        if job_desc_option == "Upload File":
            job_file = st.file_uploader(
                "Upload Job Description",
                type=['txt', 'pdf', 'docx'],
                key="job_file"
            )
            if job_file:
                st.session_state.job_description = extract_text_from_file(job_file)
                st.success("✅ Job description loaded!")
                with st.expander("Preview"):
                    st.text_area("Job Description", st.session_state.job_description, height=200, disabled=True)
        else:
            job_text = st.text_area(
                "Paste Job Description",
                height=200,
                key="job_text_input"
            )
            if job_text:
                st.session_state.job_description = job_text
                st.success("✅ Job description loaded!")
    
    with col2:
        st.subheader("Candidate Resume")
        resume_option = st.radio(
            "Input method:",
            ["Upload File", "Paste Text"],
            key="resume_option"
        )
        
        if resume_option == "Upload File":
            resume_file = st.file_uploader(
                "Upload Resume",
                type=['txt', 'pdf', 'docx'],
                key="resume_file"
            )
            if resume_file:
                st.session_state.resume_text = extract_text_from_file(resume_file)
                st.success("✅ Resume loaded!")
                with st.expander("Preview"):
                    st.text_area("Resume", st.session_state.resume_text, height=200, disabled=True)
        else:
            resume_text = st.text_area(
                "Paste Resume",
                height=200,
                key="resume_text_input"
            )
            if resume_text:
                st.session_state.resume_text = resume_text
                st.success("✅ Resume loaded!")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Generate Interview Questions", use_container_width=True, type="primary"):
            if st.session_state.job_description and st.session_state.resume_text:
                with st.spinner("Generating tailored interview questions..."):
                    try:
                        st.session_state.questions = generate_interview_questions(
                            st.session_state.job_description,
                            st.session_state.resume_text,
                            st.session_state.ai_model
                        )
                        st.session_state.current_question_idx = 0
                        st.session_state.evaluations = []
                        st.success(f"✅ Generated {len(st.session_state.questions)} questions!")
                        st.info("Navigate to the 'Questions' tab to view and answer them.")
                    except Exception as e:
                        st.error(f"Error generating questions: {str(e)}")
            else:
                st.error("⚠️ Please upload both job description and resume first!")
with tab2:
    st.header("Interview Questions")
    
    if not st.session_state.questions:
        st.info("👆 Please upload documents and generate questions in the 'Upload Documents' tab first.")
    else:
        st.progress((st.session_state.current_question_idx) / len(st.session_state.questions))
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("⬅️ Previous") and st.session_state.current_question_idx > 0:
                st.session_state.current_question_idx -= 1
                st.rerun()
        with col2:
            st.markdown(f"### Question {st.session_state.current_question_idx + 1} of {len(st.session_state.questions)}")
        with col3:
            if st.button("Next ➡️") and st.session_state.current_question_idx < len(st.session_state.questions) - 1:
                st.session_state.current_question_idx += 1
                st.rerun()
        
        st.markdown("---")
        current_q = st.session_state.questions[st.session_state.current_question_idx]
        
        st.markdown(f"### {current_q['question']}")
        if 'category' in current_q:
            st.caption(f"📌 Category: {current_q['category']}")
        answer_key = f"answer_{st.session_state.current_question_idx}"
        answer = st.text_area(
            "Enter candidate's answer:",
            height=200,
            key=answer_key
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Evaluate This Answer", type="primary", use_container_width=True):
                if answer.strip():
                    with st.spinner("Evaluating answer..."):
                        try:
                            evaluation = evaluate_answer(
                                current_q['question'],
                                answer,
                                st.session_state.job_description,
                                st.session_state.resume_text,
                                st.session_state.ai_model
                            )
                            eval_data = {
                                'question_idx': st.session_state.current_question_idx,
                                'question': current_q['question'],
                                'answer': answer,
                                'evaluation': evaluation
                            }
                            existing_idx = next((i for i, e in enumerate(st.session_state.evaluations) 
                                               if e['question_idx'] == st.session_state.current_question_idx), None)
                            if existing_idx is not None:
                                st.session_state.evaluations[existing_idx] = eval_data
                            else:
                                st.session_state.evaluations.append(eval_data)
                            
                            st.success("✅ Answer evaluated! Check the 'Evaluation' tab for details.")
                        except Exception as e:
                            st.error(f"Error evaluating answer: {str(e)}")
                else:
                    st.warning("⚠️ Please enter an answer first!")
        
        with col2:
            if st.button("🔄 Generate Follow-up Question", use_container_width=True):
                if answer.strip():
                    with st.spinner("Generating follow-up question..."):
                        try:
                            from utils.question_generator import generate_followup_question
                            followup_q = generate_followup_question(
                                current_q['question'],
                                answer,
                                st.session_state.ai_model
                            )
                            st.session_state.questions.insert(
                                st.session_state.current_question_idx + 1,
                                followup_q
                            )
                            
                            st.success("✅ Follow-up question generated! Click 'Next' to see it.")
                        except Exception as e:
                            st.error(f"Error generating follow-up: {str(e)}")
                else:
                    st.warning("⚠️ Please enter an answer first!")
with tab3:
    st.header("Answer Evaluations")
    
    if not st.session_state.evaluations:
        st.info("👆 Answer some questions first to see evaluations here.")
    else:
        total_questions = len(st.session_state.questions)
        answered_questions = len(st.session_state.evaluations)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions", total_questions)
        with col2:
            st.metric("Answered", answered_questions)
        with col3:
            avg_score = sum(e['evaluation'].get('score', 0) for e in st.session_state.evaluations) / len(st.session_state.evaluations)
            st.metric("Average Score", f"{avg_score:.1f}/10")
        
        st.markdown("---")
        for eval_data in st.session_state.evaluations:
            with st.expander(f"Q{eval_data['question_idx'] + 1}: {eval_data['question'][:80]}...", expanded=True):
                st.markdown(f"**Question:** {eval_data['question']}")
                st.markdown(f"**Answer:** {eval_data['answer']}")
                
                evaluation = eval_data['evaluation']
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    score = evaluation.get('score', 0)
                    st.metric("Score", f"{score}/10")
                
                with col2:
                    st.markdown(f"**Feedback:** {evaluation.get('feedback', 'N/A')}")
                
                if 'strengths' in evaluation:
                    st.markdown("**✅ Strengths:**")
                    for strength in evaluation['strengths']:
                        st.markdown(f"- {strength}")
                
                if 'weaknesses' in evaluation:
                    st.markdown("**⚠️ Areas for Improvement:**")
                    for weakness in evaluation['weaknesses']:
                        st.markdown(f"- {weakness}")
        
        st.markdown("---")
        if st.button("📥 Export Evaluation Report"):
            report = "# Interview Evaluation Report\n\n"
            report += f"**Total Questions:** {total_questions}\n"
            report += f"**Answered Questions:** {answered_questions}\n"
            report += f"**Average Score:** {avg_score:.1f}/10\n\n"
            
            for eval_data in st.session_state.evaluations:
                report += f"\n## Question {eval_data['question_idx'] + 1}\n"
                report += f"**Q:** {eval_data['question']}\n\n"
                report += f"**A:** {eval_data['answer']}\n\n"
                report += f"**Score:** {eval_data['evaluation'].get('score', 0)}/10\n\n"
                report += f"**Feedback:** {eval_data['evaluation'].get('feedback', 'N/A')}\n\n"
            
            st.download_button(
                label="Download Report",
                data=report,
                file_name="interview_evaluation_report.md",
                mime="text/markdown"
            )

import streamlit as st
import ollama
from resume_utils import parse_resume
from jd_matcher import get_similarity
from chatbot import HRChatbot

# Check Ollama status
@st.cache_data
def check_ollama_status():
    """Check if Ollama is running and has models"""
    try:
        models = ollama.list()
        if models['models']:
            return True, [model['name'] for model in models['models']]
        else:
            return False, []
    except Exception as e:
        return False, str(e)

st.set_page_config(page_title="Career Fit Analyzer", layout="wide")
st.title("🎯 Career Fit Analyzer - Know Your Match!")

# Add candidate-friendly introduction
st.markdown("""
### 👋 Welcome, Job Seekers!
Upload your resume and paste a job description to:
- **Get instant feedback** on how well you match the role
- **Discover skill gaps** you need to address
- **Prepare for interviews** with likely questions
- **Improve your application** with AI-powered insights
""")

# Check Ollama status
ollama_running, model_info = check_ollama_status()

if not ollama_running:
    st.error("❌ AI service is not available. Please try again later.")
    st.stop()

# Initialize session state
if "processed" not in st.session_state:
    st.session_state.processed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Upload Your Resume")
    resume_file = st.file_uploader("Choose your resume (PDF)", type=["pdf"])
    
with col2:
    st.subheader("📝 Job Description")
    jd_text = st.text_area("Paste the job description here", height=200)

if st.button("🔍 Analyze My Fit", type="primary", use_container_width=True) and resume_file and jd_text:
    try:
        with st.spinner("🔍 Analyzing your resume..."):
            candidate = parse_resume(resume_file)
        st.session_state.candidate = candidate
        
        with st.spinner("📊 Calculating your match score..."):
            score = get_similarity(candidate["full_text"], jd_text)
        st.session_state.score = score
        st.session_state.jd_text = jd_text
        
        # Initialize HR Bot with error handling
        try:
            st.session_state.hr_bot = HRChatbot(candidate, jd_text, score)
            st.session_state.chat_history = []
            st.session_state.processed = True
            st.success("✅ Analysis completed!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error initializing analyzer: {str(e)}")
    except Exception as e:
        st.error(f"❌ Error processing: {str(e)}")

if st.session_state.get("processed"):
    candidate = st.session_state.candidate
    score = st.session_state.score
    jd_text = st.session_state.jd_text
    hr_bot = st.session_state.hr_bot
    
    # Results Section
    st.header("📊 Your Results")
    
    # Score display with interpretation
    score_percentage = score * 100
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("🎯 Match Score", f"{score_percentage:.1f}%")
    
    with col2:
        if score_percentage >= 80:
            st.success("🟢 Excellent Match!")
            advice = "You're a strong candidate for this role!"
        elif score_percentage >= 60:
            st.warning("🟡 Good Match")
            advice = "You have potential, but consider addressing skill gaps."
        else:
            st.error("🔴 Needs Improvement")
            advice = "Significant skill development needed for this role."
    
    with col3:
        st.info(f"💡 {advice}")
    
    # Progress bar
    st.progress(score)
    
    # Detailed Analysis
    st.subheader("📈 Detailed Analysis")
    
    # Auto-generate key insights
    analysis_tabs = st.tabs(["💪 Strengths", "🎯 Gaps", "📝 Interview Prep", "💰 Salary Info"])
    
    with analysis_tabs[0]:
        if st.button("🔍 Analyze My Strengths"):
            with st.spinner("Analyzing your strengths..."):
                strengths = hr_bot.ask("What are this candidate's key strengths that match the job requirements? Be specific and encouraging.")
                st.write(strengths)
    
    with analysis_tabs[1]:
        if st.button("🔍 Find Skill Gaps"):
            with st.spinner("Identifying areas for improvement..."):
                gaps = hr_bot.ask("What skills or experience is this candidate missing for the role? Provide constructive advice on how to develop these skills.")
                st.write(gaps)
    
    with analysis_tabs[2]:
        if st.button("🔍 Get Interview Questions"):
            with st.spinner("Preparing interview questions..."):
                questions = hr_bot.ask("What interview questions is this candidate likely to face? Provide questions with brief tips on how to answer them.")
                st.write(questions)
    
    with analysis_tabs[3]:
        if st.button("🔍 Salary Guidance"):
            with st.spinner("Analyzing salary expectations..."):
                salary = hr_bot.ask("Based on this candidate's experience and the role, what salary range should they expect? Include negotiation tips.")
                st.write(salary)
    
    # Interactive Q&A
    st.header("💬 Ask Questions About This Role")
    st.markdown("Get personalized advice about your application!")
    
    # Candidate-specific suggested questions
    candidate_questions = [
        "How can I improve my chances for this role?",
        "What should I highlight in my cover letter?",
        "How should I prepare for the interview?",
        "What are my biggest strengths for this position?",
        "Should I apply for this role or wait?",
        "How can I stand out from other candidates?",
        "What questions should I ask the interviewer?"
    ]
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💭 Our Conversation")
        for i, (speaker, message) in enumerate(st.session_state.chat_history):
            if speaker == "You":
                st.markdown(f"**🙋 You:** {message}")
            else:
                st.markdown(f"**🤖 Career Advisor:** {message}")
        st.divider()
    
    # Chat input
    user_question = st.text_input(
        "Ask me anything about this role:",
        placeholder="e.g., How can I improve my chances for this position?",
        key="chat_input"
    )
    
    col_ask, col_clear = st.columns([1, 4])
    
    with col_ask:
        if st.button("💬 Ask", type="primary"):
            if user_question.strip():
                try:
                    with st.spinner("🤖 Analyzing..."):
                        # Add candidate context to the question
                        candidate_context = f"As a candidate asking about this role: {user_question}"
                        bot_response = hr_bot.ask(candidate_context)
                    
                    st.session_state.chat_history.append(("You", user_question))
                    st.session_state.chat_history.append(("Career Advisor", bot_response))
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a question!")
    
    with col_clear:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Quick questions for candidates
    st.subheader("🚀 Quick Questions")
    st.markdown("Click on any question to get instant advice:")
    
    cols = st.columns(3)
    for i, question in enumerate(candidate_questions):
        with cols[i % 3]:
            if st.button(question, key=f"candidate_q_{i}"):
                try:
                    with st.spinner("🤖 Thinking..."):
                        bot_response = hr_bot.ask(f"As a candidate: {question}")
                    
                    st.session_state.chat_history.append(("You", question))
                    st.session_state.chat_history.append(("Career Advisor", bot_response))
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Action plan
    st.header("🎯 Your Action Plan")
    if st.button("📋 Generate Action Plan"):
        with st.spinner("Creating your personalized action plan..."):
            action_plan = hr_bot.ask("""
            Create a personalized action plan for this candidate to improve their chances for this role:
            1. Immediate actions (next 24-48 hours)
            2. Short-term goals (next 1-2 weeks)
            3. Long-term development (next 1-3 months)
            4. Application strategy tips
            5. Interview preparation checklist
            """)
            st.markdown(action_plan)

else:
    # Welcome screen with candidate benefits
    st.info("📂 Upload your resume and job description to get started!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 What You'll Get")
        st.markdown("""
        - **Instant Match Score**: See how well you fit the role
        - **Skill Gap Analysis**: Know what to improve
        - **Interview Preparation**: Get likely questions
        - **Salary Guidance**: Know your worth
        - **Application Tips**: Stand out from the crowd
        """)
    
    with col2:
        st.subheader("✨ Success Stories")
        st.markdown("""
        > "Got 87% match score and specific tips. Landed the job!" - *Sarah, Developer*
        
        > "Identified missing skills, took a course, got hired!" - *Mike, Analyst*
        
        > "Interview questions were spot-on. Felt prepared!" - *Lisa, Designer*
        """)
    
    st.subheader("🚀 How It Works")
    st.markdown("""
    1. **Upload** your resume (PDF format)
    2. **Paste** the job description you're interested in
    3. **Get** instant analysis and personalized advice
    4. **Improve** your application based on AI insights
    5. **Apply** with confidence!
    """)
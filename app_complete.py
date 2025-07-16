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

st.set_page_config(page_title="HR Recruiting Chatbot", layout="wide")
st.title("🤖 HR Recruiting Chatbot (Ollama Edition)")

# Check Ollama status
ollama_running, model_info = check_ollama_status()

if not ollama_running:
    st.error("❌ Ollama is not running or no models are installed!")
    st.markdown("""
    **To fix this:**
    1. Install Ollama: https://ollama.ai/
    2. Run in terminal: `ollama serve`
    3. Install a model: `ollama pull llama3.2`
    4. Refresh this page
    """)
    st.stop()
else:
    st.success(f"✅ Ollama is running with {len(model_info)} model(s)")
    with st.expander("📋 Available Models"):
        for model in model_info:
            st.write(f"- {model}")

# Initialize session state
if "processed" not in st.session_state:
    st.session_state.processed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.header("📂 Upload Documents")
    resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("📝 Paste or Type Job Description", height=200)
    
    if st.button("🚀 Process", type="primary") and resume_file and jd_text:
        try:
            with st.spinner("🔍 Parsing resume..."):
                candidate = parse_resume(resume_file)
            st.session_state.candidate = candidate
            
            with st.spinner("📊 Calculating similarity..."):
                score = get_similarity(candidate["full_text"], jd_text)
            st.session_state.score = score
            st.session_state.jd_text = jd_text
            
            # Initialize HR Bot with error handling
            try:
                st.session_state.hr_bot = HRChatbot(candidate, jd_text, score)
                st.session_state.chat_history = []
                st.session_state.processed = True
                st.success("✅ Processing completed!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error initializing HR Bot: {str(e)}")
                st.markdown("""
                **Common solutions:**
                - Run: `ollama pull llama3.2`
                - Or try: `ollama pull llama2`
                - Make sure Ollama is running: `ollama serve`
                """)
        except Exception as e:
            st.error(f"❌ Error processing: {str(e)}")

# Main content
if st.session_state.get("processed"):
    candidate = st.session_state.candidate
    score = st.session_state.score
    jd_text = st.session_state.jd_text
    hr_bot = st.session_state.hr_bot
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Candidate Summary")
        
        # Display candidate info in a cleaner format
        candidate_info = {
            "Name": candidate.get("name", "Not extracted"),
            "Experience": f"{candidate.get('total_experience', 0)} years",
            "Pages": candidate.get("no_of_pages", 0),
            "Key Skills": (", ".join(candidate.get("skills", []))[:100] + "...") if len(", ".join(candidate.get("skills", []))) > 100 else ", ".join(candidate.get("skills", []))

        }
        
        for key, value in candidate_info.items():
            st.write(f"**{key}:** {value}")
        
        # Add expandable section for full text if needed
        with st.expander("📝 View Full Resume Text"):
            st.text_area("Full extracted text:", candidate.get("full_text", ""), height=200, disabled=True)
    
    with col2:
        st.subheader("📊 Matching Analysis")
        
        # Score display
        score_percentage = score * 100
        st.metric("🎯 Match Score", f"{score_percentage:.2f}%")
        
        # Decision logic
        if score_percentage >= 75:
            decision = "✅ Shortlist"
            st.success(f"**Decision:** {decision}")
        else:
            decision = "❌ Reject"
            st.error(f"**Decision:** {decision}")
        
        # Progress bar for visual representation
        st.progress(score)
    
    # HR Bot Reasoning
    st.subheader("🧠 HR Bot Analysis")
    
    reason_question = (
        "Why should this candidate be shortlisted? Provide detailed analysis."
        if decision == "✅ Shortlist"
        else "Why should this candidate be rejected? Provide detailed analysis."
    )
    
    if st.button("🔍 Get Analysis"):
        with st.spinner("🤔 Analyzing..."):
            try:
                reason = hr_bot.ask(reason_question)
                st.markdown(f"**Analysis:**")
                st.write(reason)
            except Exception as e:
                st.error(f"❌ Error getting analysis: {str(e)}")
    
    # Chat Interface
    st.header("💬 Chat with HR Bot")
    st.markdown("Ask any HR-related questions about this candidate!")
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("📝 Chat History")
        for i, (speaker, message) in enumerate(st.session_state.chat_history):
            if speaker == "You":
                st.markdown(f"**🙋 You:** {message}")
            else:
                st.markdown(f"**🤖 HR Bot:** {message}")
        st.divider()
    
    # Chat input
    user_question = st.text_input(
        "Ask a question:",
        placeholder="e.g., What are the candidate's strengths? How does their experience match the role?",
        key="chat_input"
    )
    
    col_ask, col_clear = st.columns([1, 4])
    
    with col_ask:
        if st.button("💬 Ask", type="primary"):
            if user_question.strip():
                try:
                    with st.spinner("🤖 Thinking..."):
                        bot_response = hr_bot.ask(user_question)
                    
                    # Add to chat history
                    st.session_state.chat_history.append(("You", user_question))
                    st.session_state.chat_history.append(("Bot", bot_response))
                    
                    # Clear input and rerun
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a question!")
    
    with col_clear:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Suggested questions
    st.subheader("💡 Suggested Questions")
    suggested_questions = [
        "What are the candidate's key strengths?",
        "How does their experience align with the job requirements?",
        "What skills are missing from their profile?",
        "Would you recommend this candidate for interview?",
        "What interview questions should I ask this candidate?"
    ]
    
    cols = st.columns(len(suggested_questions))
    for i, question in enumerate(suggested_questions):
        with cols[i]:
            if st.button(f"❓ {question}", key=f"suggested_{i}"):
                try:
                    with st.spinner("🤖 Thinking..."):
                        bot_response = hr_bot.ask(question)
                    
                    st.session_state.chat_history.append(("You", question))
                    st.session_state.chat_history.append(("Bot", bot_response))
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

else:
    # Welcome screen
    st.info("📂 Please upload a resume and paste the job description in the sidebar, then click 'Process' to begin.")
    
    # Instructions
    st.subheader("📋 How to Use")
    st.markdown("""
    1. **Upload Resume**: Click on the sidebar and upload a PDF resume
    2. **Add Job Description**: Paste or type the job description in the text area
    3. **Process**: Click the 'Process' button to analyze the match
    4. **Review Results**: Check the candidate summary and match score
    5. **Chat with HR Bot**: Ask questions about the candidate using the chat interface
    """)
    
    st.subheader("🤖 HR Bot Features")
    st.markdown("""
    - **Candidate Analysis**: Get detailed analysis of why a candidate should be shortlisted or rejected
    - **Interactive Chat**: Ask any HR-related questions about the candidate
    - **Match Scoring**: Automated scoring based on resume-JD similarity
    - **Suggested Questions**: Pre-built questions to help with candidate evaluation
    """)
# chatbot.py
import ollama
import json
from typing import Dict, Any, List

class HRChatbot:
    def __init__(self, candidate_data: Dict[str, Any], job_description: str, match_score: float):
        """
        Initialize HR Chatbot with candidate data and job description
        
        Args:
            candidate_data: Dictionary containing candidate information
            job_description: Job description text
            match_score: Similarity score between resume and JD
        """
        self.candidate_data = candidate_data
        self.job_description = job_description
        self.match_score = match_score
        self.model = self._get_available_model()
        
        if not self.model:
            raise Exception("No Ollama models found. Please install a model first: 'ollama pull llama3.2'")
        
        # Create context for the HR bot
        self.context = self._create_context()
    
    def _get_available_model(self) -> str:
        """Get the first available model from Ollama"""
        try:
            models = ollama.list()
            if models['models']:
                # Preferred model order
                preferred_models = ['llama3.2', 'llama3.1', 'llama2', 'mistral', 'codellama']
                
                available_models = [model['name'] for model in models['models']]
                
                # Try to find preferred model
                for preferred in preferred_models:
                    for available in available_models:
                        if preferred in available:
                            return available
                
                # If no preferred model found, return first available
                return available_models[0]
            else:
                return None
        except Exception as e:
            print(f"Error getting models: {e}")
            return None
    
    def _create_context(self) -> str:
        """Create context for the HR chatbot based on candidate and job data"""
        context = f"""
        You are an expert HR assistant helping with candidate evaluation. You have access to the following information:

        CANDIDATE INFORMATION:
        - Name: {self.candidate_data.get('name', 'Not provided')}
        - Total Experience: {self.candidate_data.get('total_experience', 0)} years
        - Resume Pages: {self.candidate_data.get('no_of_pages', 0)}
        - Skills and Experience: {self.candidate_data.get('full_text', '')[:1000]}...

        JOB DESCRIPTION:
        {self.job_description}

        MATCH SCORE: {self.match_score * 100:.2f}%

        INSTRUCTIONS:
        - Provide professional, helpful responses about this candidate
        - Base your analysis on the resume content and job requirements
        - Be objective and constructive in your feedback
        - If asked about hiring decisions, consider the match score and relevant experience
        - Answer HR-related questions about interviewing, evaluation, and candidate assessment
        - Keep responses concise but informative
        """
        return context
    
    def ask(self, question: str) -> str:
        """
        Ask a question to the HR chatbot
        
        Args:
            question: The question to ask
            
        Returns:
            The bot's response
        """
        try:
            # Create the full prompt
            prompt = f"""
            {self.context}
            
            QUESTION: {question}
            
            Please provide a professional HR response based on the candidate information and job requirements provided above.
            """
            
            # Call Ollama with timeout
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'num_predict': 500  # Limit response length
                }
            )
            
            return response['message']['content']
            
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg:
                return f"Model '{self.model}' not found. Please install it with: ollama pull {self.model}"
            elif "connection" in error_msg.lower():
                return "Cannot connect to Ollama. Please make sure Ollama is running (run 'ollama serve' in terminal)."
            else:
                return f"Error: {error_msg}. Please check your Ollama installation."
    
    def get_model_info(self) -> str:
        """Get information about the current model"""
        return f"Using model: {self.model}"
    
    def get_recommendation(self) -> str:
        """Get a detailed recommendation for the candidate"""
        question = f"""
        Based on the candidate's profile and the job requirements, provide a comprehensive recommendation.
        Include:
        1. Key strengths that match the role
        2. Areas of concern or gaps
        3. Overall recommendation (Shortlist/Reject)
        4. Suggested interview focus areas
        """
        return self.ask(question)
    
    def get_interview_questions(self) -> str:
        """Generate relevant interview questions for this candidate"""
        question = f"""
        Based on this candidate's background and the job requirements, suggest 5-7 specific interview questions that would help evaluate:
        1. Technical competency
        2. Experience relevance
        3. Cultural fit
        4. Areas where more clarification is needed
        
        Format as a numbered list with brief explanations.
        """
        return self.ask(question)
    
    def compare_with_requirements(self) -> str:
        """Compare candidate profile with job requirements"""
        question = f"""
        Create a detailed comparison between the candidate's profile and job requirements:
        1. Required skills they possess
        2. Required skills they lack
        3. Experience level match
        4. Additional value they bring
        5. Risk factors to consider
        """
        return self.ask(question)
    
    def get_salary_guidance(self) -> str:
        """Get salary range guidance based on experience and role"""
        question = f"""
        Based on the candidate's experience level ({self.candidate_data.get('total_experience', 0)} years) 
        and the job requirements, provide guidance on:
        1. Appropriate salary range expectations
        2. Negotiation points
        3. Factors that might justify higher/lower offers
        """
        return self.ask(question)
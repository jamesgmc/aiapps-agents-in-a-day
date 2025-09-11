import random
import re


class GameAgent:
    """Agent class for handling questions and move decisions in PSR Tournament"""
    
    def __init__(self):
        """Initialize the game agent"""
        pass
    
    def answer_question(self, question: str) -> str:
        """Generate an answer to the question (simple logic for demo)"""
        # Simple question answering logic
        question_lower = question.lower()
        
        # Math questions
        if "+" in question:
            try:
                # Simple addition - look for pattern "X + Y"
                match = re.search(r'(\d+)\s*\+\s*(\d+)', question)
                if match:
                    num1 = int(match.group(1))
                    num2 = int(match.group(2))
                    return str(num1 + num2)
            except:
                pass
        
        if "-" in question:
            try:
                # Simple subtraction - look for pattern "X - Y"
                match = re.search(r'(\d+)\s*-\s*(\d+)', question)
                if match:
                    num1 = int(match.group(1))
                    num2 = int(match.group(2))
                    return str(num1 - num2)
            except:
                pass
        
        # Common knowledge questions
        if "capital" in question_lower:
            if "australia" in question_lower:
                return "Canberra"
            elif "france" in question_lower:
                return "Paris"
            elif "japan" in question_lower:
                return "Tokyo"
        
        if "color" in question_lower or "colour" in question_lower:
            if "sky" in question_lower:
                return "blue"
            elif "grass" in question_lower:
                return "green"
            elif "sun" in question_lower:
                return "yellow"
        
        # Default fallback answers
        fallback_answers = ["42", "yes", "no", "blue", "red", "green", "1", "10", "100"]
        return random.choice(fallback_answers)
    
    def choose_rps_move(self) -> int:
        """Randomly choose Rock (0), Paper (1), or Scissors (2)"""
        return random.randint(0, 2)

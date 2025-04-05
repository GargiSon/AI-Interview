from groq import Groq
import json

client = Groq(api_key = "Groq Key")

def evaluate_response(response):
    evaluation = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role": "system",
                "content": "You are a highly experienced interviewer evaluating Python interview responses. Provide JSON-based feedback with scores for 'Technical Knowledge', 'Clarity', and 'Confidence' (0-10)."
            },
            {
                "role": "user",
                "content": f"Candidate's response: {response}"
            }
        ],
        temperature=0.20,  #Low because we want to get a clear and concise response
        max_completion_tokens=2048,
        top_p=0.95,
        stream=False,
        stop=None,
    )
    feedback = evaluation.choices[0].message.content

    try:
        feedback_json = json.loads(feedback)

        # Extract scores
        tech_score = feedback_json.get("Technical Knowledge", 0)
        clarity_score = feedback_json.get("Clarity", 0)
        confidence_score = feedback_json.get("Confidence", 0)

        # Calculate the average score
        avg_score = (tech_score + clarity_score + confidence_score) / 3

        # Determine the interview result
        result = "Selected" if avg_score >= 7 else "Rejected"

        # Display scores and result
        print("\n **Interview Feedback:**")
        print(f" Technical Knowledge: {tech_score}/10")
        print(f" Clarity: {clarity_score}/10")
        print(f" Confidence: {confidence_score}/10")
        print(f"\n Final Result: {result} (Average Score: {avg_score:.2f}/10)")

        # Save the result and scores in a JSON file
        result_data = {
            "Technical Knowledge": tech_score,
            "Clarity": clarity_score,
            "Confidence": confidence_score,
            "Average Score": avg_score,
            "Result": result
        }
        
        with open("interview_result.json", "w") as json_file:
            json.dump(result_data, json_file, indent=4)
        print(" Feedback saved to interview_result.json")

    except json.JSONDecodeError:
        print(" Could not parse JSON feedback properly.")

def main():
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role": "system",
                "content": "You are a highly experienced technical interviewer for the IT industry. You specialize in conducting interviews for Python, AWS, and Angular roles. During the interview, you ask clear, relevant, and progressively challenging questions. You evaluate the candidate's responses based on technical accuracy, clarity, and confidence. You provide real-time JSON-based feedback, including a score for each category. Be professional, yet conversational, to create a realistic interview experience."
            },
            {
                "role": "user",
                "content": "I am applying for a Python developer role. Please ask me Python interview questions related to data structures, OOP, and common libraries. Evaluate my responses and give JSON-based feedback with scores for 'Technical Knowledge,' 'Clarity,' and 'Confidence'."
            }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=False,  #If true object returns chunks rather than full response
        stop=None,
    )
    questions = completion.choices[0].message.content
    print(" Interview Questions: ")
    print(questions)
    
    # Simulate the candidate's response (you can replace this with user input)
    candidate_response = input("\n Enter your response: ")
    # candidate_response ="""
    # In Python, a list is a mutable, ordered collection of items, whereas a tuple is immutable. 
    # Lists are more memory-consuming but flexible, while tuples are faster and safer when the data shouldn't change. 
    # The 'append()' method is used to add elements to a list, whereas tuples don't have this method due to their immutability.
    # """
    
    # print("\nCandidate's Response (Static):")
    # print(candidate_response)
    # Evaluate the candidate's response
    evaluate_response(candidate_response)
    
if __name__ == "__main__":
    main()

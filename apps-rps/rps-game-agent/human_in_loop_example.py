#!/usr/bin/env python3
"""
Human-in-the-Loop Agent Example
===============================

This script demonstrates how to use the Human-in-the-Loop functionality
with Azure AI Agents. The agent will request human approval before 
executing any tool calls.

Usage:
    python human_in_loop_example.py

Features demonstrated:
- Tool approval requests
- Human approval/rejection workflow  
- Different types of tool calls
- Interactive console interface
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from agent_v67 import GameAgentV67


def show_introduction():
    """Show introduction to the human-in-the-loop concept"""
    print("""
🤖 HUMAN-IN-THE-LOOP WITH AI AGENTS
====================================

This demonstration shows how to implement human oversight in AI agent workflows.
The agent will:

1. 🔍 Analyze your request
2. 🛠️  Identify tools needed to complete the task
3. ❓ ASK FOR YOUR APPROVAL before executing each tool
4. ✅ Only proceed if you approve
5. 📋 Show you the results

Benefits of Human-in-the-Loop:
• Prevent unwanted or dangerous tool executions
• Maintain human control over AI actions
• Build trust through transparency
• Enable selective approval of operations

Let's try it out!
====================================
    """)


def run_interactive_example():
    """Run an interactive example with user input"""
    show_introduction()
    
    print("Enter your questions. The agent will ask for approval before using tools.")
    print("Type 'quit' to exit.\n")
    
    with GameAgentV67() as agent:
        print(f"🤖 Agent '{agent.agent_name}' is ready!")
        print(f"👤 Player: {agent.player_name}")
        print("-" * 60)
        
        while True:
            try:
                question = input("\n💭 Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not question:
                    continue
                
                print(f"\n🔄 Processing: {question}")
                print("⏳ Agent is thinking...")
                
                answer = agent.answer_question(question)
                
                print(f"\n🎯 Final Answer: {answer}")
                print("-" * 60)
                
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue


def run_predefined_examples():
    """Run predefined examples to show different scenarios"""
    print("""
🎯 PREDEFINED EXAMPLES
======================
Running several examples to demonstrate different tool approval scenarios.
You'll be asked to approve or reject each tool call.
    """)
    
    examples = [
        {
            "question": "What is 25 + 75?",
            "description": "Simple math calculation - should request tool approval"
        },
        {
            "question": "Calculate 12 * 8 + 15",
            "description": "Complex math expression - should request tool approval"
        },
        {
            "question": "Hello, how are you?",
            "description": "Simple greeting - should not require tools"
        },
        {
            "question": "What is 2 to the power of 10? Use 2**10",
            "description": "Power calculation - should request tool approval"
        }
    ]
    
    with GameAgentV67() as agent:
        for i, example in enumerate(examples, 1):
            print(f"\n📝 Example {i}/{len(examples)}")
            print(f"Description: {example['description']}")
            print(f"Question: {example['question']}")
            print("-" * 50)
            
            try:
                answer = agent.answer_question(example['question'])
                print(f"✅ Answer: {answer}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("=" * 60)
    
    print("🎉 All examples completed!")


def show_architecture_info():
    """Show information about the human-in-the-loop architecture"""
    print("""
🏗️  ARCHITECTURE OVERVIEW
=========================

The human-in-the-loop implementation uses Azure AI Agents framework:

1. AGENT SETUP:
   - Creates Azure AI Agent with tools
   - Configures instructions for approval requests
   
2. TOOL APPROVAL FLOW:
   - Agent identifies need for tool use
   - Creates 'requires_action' status with submit_tool_approval
   - Human is prompted for approval/rejection
   - Agent receives approval response
   - Tool is executed only if approved

3. KEY COMPONENTS:
   - run.required_action.submit_tool_approval.tool_calls
   - ToolApproval objects with tool_call_id and approved flag
   - project_client.agents.runs.submit_tool_approvals()

4. HUMAN INTERFACE:
   - Console prompts for approval decisions
   - Clear display of tool name and arguments
   - Yes/No approval workflow
   - Safety through explicit consent

This pattern enables:
✓ Transparent AI operations
✓ Human oversight and control
✓ Selective tool execution
✓ Trust and safety
    """)


if __name__ == "__main__":
    print("🚀 HUMAN-IN-THE-LOOP AGENT DEMONSTRATION")
    print("=========================================")
    
    while True:
        print("\nChoose an option:")
        print("1. 🎯 Run predefined examples")
        print("2. 💬 Interactive mode (enter your own questions)")  
        print("3. 🏗️  Show architecture information")
        print("4. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_predefined_examples()
        elif choice == "2":
            run_interactive_example()
        elif choice == "3":
            show_architecture_info()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
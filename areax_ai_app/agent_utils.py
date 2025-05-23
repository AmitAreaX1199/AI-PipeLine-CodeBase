"""
Utility functions for AI agents in the AreaX AI Pipeline.
Provides reusable components for agent initialization, response handling, and error management.
"""

from agno.agent import Agent
from agno.models.google import Gemini
from rest_framework.response import Response
from rest_framework import status
import os
from dotenv import load_dotenv
from datetime import datetime
from tzlocal import get_localzone_name
import json
from openai import OpenAI
import logging
from .agent_logging import log_agent_interaction, log_error

load_dotenv()
logger = logging.getLogger(__name__)

def initialize_gemini_model(model_id="gemini-2.0-flash"):
    """
    Initialize and return a Gemini model instance.
    
    Args:
        model_id (str): The ID of the Gemini model to initialize.
        
    Returns:
        Gemini: An initialized Gemini model instance.
    """
    return Gemini(id=model_id)

def initialize_agent(instructions, tools=None, show_tool_calls=True):
    """
    Initialize and return an Agent instance with the specified model, tools, and instructions.
    
    Args:
        instructions (str): The instructions for the agent.
        tools (list, optional): List of tools for the agent to use. Defaults to None.
        show_tool_calls (bool, optional): Whether to show tool calls in the response. Defaults to True.
        
    Returns:
        Agent: An initialized Agent instance.
    """
    model = initialize_gemini_model()
    
    return Agent(
        model=model,
        tools=tools,
        instructions=instructions,
        show_tool_calls=show_tool_calls
    )

def get_current_datetime_info():
    """
    Get the current datetime and timezone information.
    
    Returns:
        tuple: A tuple containing (current_datetime_str, timezone_str).
    """
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timezone = get_localzone_name()
    
    return current_datetime, timezone

def process_agent_request(message, agent, log_model, user_reference_number="", user_email=""):
    """
    Process an agent request, log the interaction, and return a formatted response.
    
    Args:
        message (str): The user message to process.
        agent (Agent): The initialized agent to use for processing.
        log_model: The model class to use for logging the interaction.
        user_reference_number (str, optional): User reference number for tracking. Defaults to "".
        user_email (str, optional): User email for tracking. Defaults to "".
        
    Returns:
        Response: A formatted REST framework response.
    """
    if not message:
        return Response(
            {"error": "Message is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        response = agent.run(message)
        
        log_agent_interaction(
            log_model=log_model,
            message=message,
            response=response,
            user_reference_number=user_reference_number,
            user_email=user_email
        )
        
        return Response({
            "status": status.HTTP_200_OK,
            "user_reference_number": user_reference_number,
            "user_email": user_email,
            "response": response
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error processing agent request: {str(e)}")
        log_error("Agent", str(e), user_reference_number, user_email)
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def initialize_openai_client():
    """
    Initialize and return an OpenAI client.
    
    Returns:
        OpenAI: An initialized OpenAI client.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API key")
    
    return OpenAI(api_key=api_key)

def process_openai_request(prompt, model_name="gpt-4", system_instruction="", log_model=None, 
                          user_reference_number="", user_email="", max_tokens=1024):
    """
    Process a request using the OpenAI API, log the interaction, and return a formatted response.
    
    Args:
        prompt (str): The user prompt to process.
        model_name (str): The OpenAI model to use. Defaults to "gpt-4".
        system_instruction (str): The system instruction. Defaults to "".
        log_model: The model class to use for logging the interaction. Defaults to None.
        user_reference_number (str): User reference number for tracking. Defaults to "".
        user_email (str): User email for tracking. Defaults to "".
        max_tokens (int): Maximum tokens for the response. Defaults to 1024.
        
    Returns:
        Response: A formatted REST framework response.
    """
    if not prompt:
        return Response(
            {"error": "Prompt is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        client = initialize_openai_client()
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens
        )
        
        generated_text = response.choices[0].message.content.strip()
        
        if log_model:
            log_agent_interaction(
                log_model=log_model,
                message=prompt,
                response=generated_text,
                user_reference_number=user_reference_number,
                user_email=user_email
            )
        
        return Response({
            "status": status.HTTP_200_OK,
            "user_reference_number": user_reference_number,
            "user_email": user_email,
            "response": generated_text
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error processing OpenAI request: {str(e)}")
        log_error("OpenAI", str(e), user_reference_number, user_email)
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def initialize_together_client():
    """
    Initialize and return a Together client.
    
    Returns:
        Together: An initialized Together client.
    """
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("Missing Together API key")
    
    from together import Together
    return Together(api_key=api_key)

def process_together_request(prompt, model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo", system_instruction="", 
                            log_model=None, user_reference_number="", user_email=""):
    """
    Process a request using the Together API, log the interaction, and return a formatted response.
    
    Args:
        prompt (str): The user prompt to process.
        model_name (str): The Together model to use. Defaults to "meta-llama/Llama-3.3-70B-Instruct-Turbo".
        system_instruction (str): The system instruction. Defaults to "".
        log_model: The model class to use for logging the interaction. Defaults to None.
        user_reference_number (str): User reference number for tracking. Defaults to "".
        user_email (str): User email for tracking. Defaults to "".
        
    Returns:
        Response: A formatted REST framework response.
    """
    if not prompt:
        return Response(
            {"error": "Prompt is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        client = initialize_together_client()
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
        
        ai_response = response.choices[0].message.content if response.choices else "No response"
        
        if log_model:
            log_agent_interaction(
                log_model=log_model,
                message=prompt,
                response=ai_response,
                user_reference_number=user_reference_number,
                user_email=user_email
            )
        
        return Response({
            "status": "200",
            "user_reference_number": user_reference_number,
            "user_email": user_email,
            "response": ai_response
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error processing Together request: {str(e)}")
        log_error("Together", str(e), user_reference_number, user_email)
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

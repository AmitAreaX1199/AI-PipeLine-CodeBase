"""
Logging utilities for AI agents in the AreaX AI Pipeline.
Provides standardized logging for agent interactions.
"""

from datetime import datetime
import logging
from django.db import models

logger = logging.getLogger(__name__)

def log_agent_interaction(log_model, message, response, user_reference_number="", user_email="", additional_data=None):
    """
    Log an agent interaction to the database.
    
    Args:
        log_model: The model class to use for logging the interaction.
        message (str): The user message or prompt.
        response (str): The agent's response.
        user_reference_number (str, optional): User reference number for tracking. Defaults to "".
        user_email (str, optional): User email for tracking. Defaults to "".
        additional_data (dict, optional): Additional data to log. Defaults to None.
        
    Returns:
        log_entry: The saved log entry.
    """
    try:
        log_entry = log_model(
            message=message,
            response=response
        )
        
        if hasattr(log_model, 'user_reference_number') and user_reference_number:
            log_entry.user_reference_number = user_reference_number
            
        if hasattr(log_model, 'user_email') and user_email:
            log_entry.user_email = user_email
            
        if additional_data and isinstance(additional_data, dict):
            for key, value in additional_data.items():
                if hasattr(log_model, key):
                    setattr(log_entry, key, value)
        
        log_entry.save()
        return log_entry
        
    except Exception as e:
        logger.error(f"Error logging agent interaction: {str(e)}")
        return None

def log_error(agent_name, error_message, user_reference_number="", user_email=""):
    """
    Log an error that occurred during agent processing.
    
    Args:
        agent_name (str): The name of the agent where the error occurred.
        error_message (str): The error message.
        user_reference_number (str, optional): User reference number for tracking. Defaults to "".
        user_email (str, optional): User email for tracking. Defaults to "".
    """
    error_data = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "error": error_message
    }
    
    if user_reference_number:
        error_data["user_reference_number"] = user_reference_number
        
    if user_email:
        error_data["user_email"] = user_email
        
    logger.error(f"Agent error: {error_data}")

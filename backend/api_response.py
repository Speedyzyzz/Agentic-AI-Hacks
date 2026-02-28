"""
Standardized API Response Schema for CampaignX

All endpoints must return responses in this consistent format:
{
    "success": bool,
    "data": dict | list | null,
    "error": str | null,
    "message": str | null
}
"""
from typing import Any, Optional, Dict, List, Union
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standardized API response format"""
    success: bool
    data: Optional[Union[Dict[str, Any], List[Any]]] = None
    error: Optional[str] = None
    message: Optional[str] = None


def success_response(
    data: Optional[Union[Dict[str, Any], List[Any]]] = None,
    message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a successful API response
    
    Args:
        data: Response payload (dict or list)
        message: Optional success message
        
    Returns:
        Standardized success response dict
    """
    return {
        "success": True,
        "data": data or {},
        "error": None,
        "message": message
    }


def error_response(
    error: str,
    data: Optional[Union[Dict[str, Any], List[Any]]] = None
) -> Dict[str, Any]:
    """
    Create an error API response
    
    Args:
        error: Error message
        data: Optional partial data (for debugging)
        
    Returns:
        Standardized error response dict
    """
    return {
        "success": False,
        "data": data,
        "error": error,
        "message": None
    }

from fastapi import status, HTTPException

def not_found_exception_check(property, input_value):
    if property == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{input_value} not found")

def not_authorized_exception_check(property_id, input_id):
    if property_id != input_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized action")


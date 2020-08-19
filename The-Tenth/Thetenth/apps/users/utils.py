def jwt_response_payload_handler(token, user=None, request=None):
    """
        jwt ,
    """
    return {
        'token': token,
        'user_id': user.id, 'username': user.username}
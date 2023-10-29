import sb_client
import bcrypt

# Register a new user
def register(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    sb_client.supabase.table('player_data').insert({
        'salt': salt})
    return hashed_password

# Authenticate an existing user
def authenticate(uuid: str, password: str):
    # Query Supabase for the user with the given username
    response = sb_client.supabase.table('player_data').select('password', 'salt').filter('id', 'eq', uuid).execute()
    
    # Check for error in response
    if hasattr(response, 'data') and response.data is None:
        print('Error fetching user:', getattr(response, 'message', 'Unknown error'))
        return False
    
    # If user not found
    if not response.data:
        print('User not found!')
        return False
    
    # Create hashed password with given salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), response.data[0]['salt']).decode('utf-8')

    # Retrieve hashed password from the response
    stored_hashed_password = response.data[0]['password']

    # Compare stored hashed password with hashed version of provided password
    if hashed_password == stored_hashed_password:
        print('Authentication successful!')
        return True
    else:
        print('Invalid password!')
        return False

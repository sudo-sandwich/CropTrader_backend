import sb_client
import bcrypt

# Register a new user
def register(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert user into Supabase
    response = sb_client.supabase.table('users').insert({'username': username, 'password': hashed_password}).execute()
    
    # Check if there's a 'data' attribute in the response and it's None, which indicates an error.
    if hasattr(response, 'data') and response.data is None:
        print('Error registering user:', getattr(response, 'message', 'Unknown error'))
        return

# Authenticate an existing user
def authenticate(username, password):
    # Query Supabase for the user with the given username
    response = sb_client.supabase.table('users').select('password').filter('username', 'eq', username).execute()

    # Check for error in response
    if hasattr(response, 'data') and response.data is None:
        print('Error fetching user:', getattr(response, 'message', 'Unknown error'))
        return False

    # If user not found
    if not response.data:
        print('User not found!')
        return False

    # Retrieve hashed password from the response
    stored_hashed_password = response.data[0]['password']

    # Compare stored hashed password with hashed version of provided password
    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
        print('Authentication successful!')
        return True
    else:
        print('Invalid password!')
        return False

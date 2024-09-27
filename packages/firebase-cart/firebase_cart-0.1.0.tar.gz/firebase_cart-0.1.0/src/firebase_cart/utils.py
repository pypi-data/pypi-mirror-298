import random
import string

def generate_id(prefix='cart_', length=25):
    chars = string.ascii_uppercase + string.digits
    unique_part = ''.join(random.choice(chars) for _ in range(length))
    return prefix + unique_part
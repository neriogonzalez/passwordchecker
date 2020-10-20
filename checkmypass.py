import requests    
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    respuesta = requests.get(url)
    #print(respuesta)
    if respuesta.status_code != 200:
        raise RuntimeError(f'Error fetching: {respuesta.status_code } , check API and try again')
    return respuesta

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.split())
    for h, count in hashes:
        
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response =request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        #print (count)
        if count:
            print(f"Your password: {password} has been leaked: {count} times")
        else:
            print(f"Your password: {password} has not been leaked. You are OK")
    return 'done!'
main(sys.argv[1:])
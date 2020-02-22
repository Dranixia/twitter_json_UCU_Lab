"""
Butynets Danylo
"""
import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import twurl


def irl_processes():
    """
    (None) -> str
    Ignore SSL certificate errors and return data from web page.
    """
    twitter_url = 'https://api.twitter.com/1.1/friends/list.json'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    acct = input('Enter Twitter Account:')
    if len(acct) < 1:
        return 'INVALID ACCOUNT'
    url = twurl.augment(twitter_url,
                        {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    return data


def obtain_dict_key(obj):
    """
    (dict) -> str
    Return requested key from dict, if such exists.
    """
    keys = ', '.join(obj.keys())
    next_category = input("There are " + str(len(obj.keys())) +
                          " following categories: " + keys + '\n')

    while next_category not in list(obj.keys()):
        print("\nInvalid key!")
        next_category = input("There are " + str(len(obj.keys())) +
                              " following categories: " + keys + '\n')
    return next_category


def obtain_list_ind(obj):
    """
    (list) -> int
    Return requested index from list, if such exists.
    """
    num = len(obj)
    next_category = input('There are ' + str(num) +
                          ' elements (from 0 to ' + str(num - 1) + '): ')
    try:
        next_category = int(next_category)
        if next_category not in range(len(obj)):
            print("\nInvalid index!")
            next_category = obtain_list_ind(obj)
    except ValueError:
        print("\nInvalid index!")
        next_category = obtain_list_ind(obj)
    return next_category


def main():
    """
    (None) -> None
    Search through the json file and receive the requested data.
    """
    path = ''

    data = irl_processes()
    if data == 'INVALID ACCOUNT':
        print(data)
        return None

    script = json.loads(data)

    with open('result.json', 'w', encoding='utf-8', errors='ignore') as file:
        json.dump(script, file, ensure_ascii=False, indent=4)

    while isinstance(script, dict) or isinstance(script, list) and len(script) != 0:
        if isinstance(script, dict):
            key = obtain_dict_key(script)
            path += '->' + key
            script = script[key]
        elif isinstance(script, list):
            key = obtain_list_ind(script)
            path += '->' + 'index ' + str(key)
            script = script[key]

    if not script and script != 0:
        script = 'Your data is empty.'
    print("Your path to the data: " + path[2:])
    print('Data:', script)


if __name__ == "__main__":
    main()

import requests


def grab_headers():

    access_key = ''
    secret_key = ''
    return {
        'Content-type': 'application/json',
        'user-agent': 'navi-TG-migration-script',
        'X-ApiKeys': f'accessKey={access_key};secretKey={secret_key}',
    }


def request_data(method, url_mod, **kwargs):

    # set the Base URL
    url = "https://cloud.tenable.com"

    # check for params and set to None if not found
    try:
        params = kwargs['params']
    except KeyError:
        params = None

    # check for a payload and set to None if not found
    try:
        payload = kwargs['payload']
    except KeyError:
        payload = None

    try:
        r = requests.request(method, url + url_mod, headers=grab_headers(), params=params, json=payload, verify=True)
        if r.status_code == 200:
            return r.json()

        if r.status_code == 202:
            # This response is for some successful posts.
            print("\nSuccess!\n")
        elif r.status_code == 404:
            print('\nCheck your query...I can\'t find what you\'re looking for', r)
        elif r.status_code == 429:
            print("\nToo many requests at a time...\n")
        elif r.status_code == 400:
            print("\nThe object you tried to create already exists\n")
        elif r.status_code == 403:
            print("\nYou are not authorized! You need to be an admin\n")
        else:
            print("Something went wrong...Don't be trying to hack me now", r)
    except ConnectionError:
        print("Check your connection...You got a connection error")


def migrate_tgroups():
    tgroups = request_data('GET', '/target-groups')
    d = "Imported by Script"
    for group in tgroups['target_groups']:
        member = group['members']
        name = group['name']
        type = group['type']
        try:
            if name != 'Default':
                payload = {
                    "category_name": str(type),
                    "value": str(name),
                    "description": d,
                    "filters": {
                        "asset": {
                            "and": [
                                {
                                    "field": "ipv4",
                                    "operator": "eq",
                                    "value": str(member),
                                }
                            ]
                        }
                    },
                }

                data = request_data('POST', '/tags/values', payload=payload)

                value_uuid = data["uuid"]
                cat_uuid = data['category_uuid']
                print(f"\nI've created your new Tag - {type} : {name}\n")
                print(f"The Category UUID is : {cat_uuid}\n")
                print(f"The Value UUID is : {value_uuid}\n")
        except:
            pass


if __name__ == '__main__':
    migrate_tgroups()

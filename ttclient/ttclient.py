import argparse
import requests
import json


def main():
    parser = argparse.ArgumentParser(description='Retrieve table tennis equipment data.')
    subparsers = parser.add_subparsers(required=True)

    # Global arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-e', '--equipment-type',
                        required=True,
                        choices=['rubber', 'blade'],
                        help='Type of equipment')

    # Each command
    get_parser = subparsers.add_parser('get', help='Get equipment data', parents=[parent_parser])
    delete_parser = subparsers.add_parser('delete', help='Delete equipment data', parents=[parent_parser])

    # Arguments for each command
    # get
    get_parser.add_argument('-n', '--name',
                            required=False,
                            help='Name of the equipment to retrieve')
    get_parser.set_defaults(func=get)

    # delete
    delete_parser.add_argument('-n', '--name',
                               required=True,
                               help='Name of the equipment to delete')
    delete_parser.add_argument('-s', '--site',
                               required=True,
                               help='Site to delete the equipment from, ' \
                                    'can be a substring of the URL')
    delete_parser.set_defaults(func=delete)

    args = parser.parse_args()
    args.func(args)


def get(args):
    """
    Return all matching equipment items given the name.
    If no name is provided, return all items of the given type.
    """

    if args.name:
        get_with_name(args)
    else:
        get_all(args)


def delete(args):
    """
    Delete the given equipment item from the database (will be repopulated on the next scrape).
    """

    # Confirm deletion
    print(f'Are you sure you want to delete the {get_hostname(args.site)} {args.equipment_type} {args.name}?')
    confirmation = input('Type "yes" to confirm: ')
    if confirmation.lower() != 'yes' and confirmation.lower() != 'y':
        print('Deletion cancelled')
        return

    try:
        response = requests.delete(f'http://localhost:5000/delete/{args.equipment_type}',
                                   json={'name': args.name, 'site': args.site})
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f'{response.json()["error"]}')
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    print(f'Deleted the {get_hostname(args.site)} {args.equipment_type} {args.name}')


def get_with_name(args):
    """
    Return all matching equipment items given the name.
    """

    try:
        response = requests.get(f'http://localhost:5000/{args.equipment_type}s', json={'name': args.name})
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f'{response.json()['error']}')
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    result = response.json()

    if len(result) > 1:
        print(f'Found {len(result)} {args.equipment_type}s matching "{args.name}":')
        print('Name          Price')
        for item in response.json():
            lowestPrice = min(entry['price'] for entry in item['entries'])
            print(item['name'], lowestPrice)
    else:
        # If we only found one item, print its details
        # Start by getting the site with the lowest price
        best_site = result[0]['entries'][0]
        for entry in result[0]['entries']:
            best_site = entry['price'] if (entry['price'] < best_site['price']) else best_site

        print(f'{args.equipment_type.capitalize()} entry {result[0]['name']} found:')
        print(f'  Current Lowest Price:', best_site['price'])
        print(f'    Site: {best_site['url']}\n')
        print(f'  All Time Lowest Price:', result[0]['allTimeLowPrice'])
        # print(f'  URL:', result[0]['url'])
        if len(result[0]['entries']) > 1:
            print(f'  Other Sites:')
            for entry in result[0]['entries']:
                if entry != best_site:
                    print(f'    {entry['url']} - {entry['price']}')


def get_all(args):
    """
    Return all equipment items of the given type. Only prints the name.
    """

    try:
        response = requests.get(f'http://localhost:5000/{args.equipment_type}s')
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f'{response.json()["error"]}')
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    print('Name')
    for item in response.json():
        print(item)


def get_hostname(url):
    """
    Extract the hostname from the given URL.
    """
    return url.split('www.')[-1].split('.com')[0].split('.org')[0].split('.net')[0]


if __name__ == '__main__':
    main()

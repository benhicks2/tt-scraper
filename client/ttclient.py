#!/usr/bin/env python3
"""
Program: ttclient

Description: Retrieve and manage table tennis equipment data.

Usage:
    ttclient get -e <equipment_type> [-n <name>]
    ttclient delete -e <equipment_type> -n <name> -s <site>
"""
import argparse
import requests
import configparser

RED_CODE = '\033[0;31m'
RESET_CODE = '\033[0m'

RUBBER_TYPE = 'rubber'
BLADE_TYPE = 'blade'
ROUTE_MAP = {
    RUBBER_TYPE: 'rubbers',
    BLADE_TYPE: 'blades'
}

def main():
    """
    Main function to parse arguments and call the appropriate function.
    """
    # Retrieve the server from the config file
    server = Server().get()

    parser = argparse.ArgumentParser(description='Retrieve table tennis equipment data.')
    subparsers = parser.add_subparsers(required=True)

    # Global arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-e', '--equipment-type',
                        required=True,
                        choices=[RUBBER_TYPE, BLADE_TYPE],
                        help='Type of equipment')

    # Each command
    get_parser = subparsers.add_parser('get', help='Get equipment data', parents=[parent_parser])
    delete_parser = subparsers.add_parser('delete', help='Delete equipment data', parents=[parent_parser])
    update_parser = subparsers.add_parser('update', help='Update equipment data by re-scraping the given equipment type', parents=[parent_parser])

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

    # update
    update_parser.set_defaults(func=update)

    args = parser.parse_args()
    args.func(args, server)


def get(args: argparse.Namespace, server: str) -> None:
    """
    Return all matching equipment items given the name.
    If no name is provided, return all items of the given type.
    """

    if args.name:
        get_with_name(args, server)
    else:
        get_all(args, server)


def delete(args: argparse.Namespace, server: str) -> None:
    """
    Delete the given equipment item from the database (will be repopulated on the next scrape).
    """

    equipment_type = ROUTE_MAP[args.equipment_type]
    # Confirm deletion
    print(f'Are you sure you want to delete the {get_hostname(args.site)} {args.equipment_type} {args.name}?')
    confirmation = input('Type "yes" to confirm: ')
    if confirmation.lower() != 'yes' and confirmation.lower() != 'y':
        print('Deletion cancelled')
        return

    try:
        response = requests.delete(f'{server}/{equipment_type}',
                                   json={'name': args.name, 'site': args.site})
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f'{response.json()["error"]}')
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    print(f'Deleted the {get_hostname(args.site)} {args.equipment_type} {args.name}')


def update(args: argparse.Namespace, server: str) -> None:
    """
    Update the specified equipment item by re-scraping the given equipment type.
    """
    equipment_type = ROUTE_MAP[args.equipment_type]
    try:
        response = requests.put(f'{server}/{equipment_type}')
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f'{response.json()["error"]}')
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    print(f'{args.equipment_type.capitalize()} data updated successfully')


def get_with_name(args: argparse.Namespace, server: str) -> None:
    """
    Return all matching equipment items given the name.
    """
    page = 1
    equipment_type = ROUTE_MAP[args.equipment_type]
    result = []
    quit = False

    while not quit:
        try:
            response = requests.get(f'{server}/{equipment_type}?name={args.name}&page={page}')
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 404:
                if page > 1:
                    print(f'No more {equipment_type} found with name "{args.name}"')
                else:
                    print(f'No {equipment_type} found with name "{args.name}"')
                return
            raise SystemExit(f'{response.json()['error']}')
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        json = response.json()
        result = json['items']

        if len(result) > 1 or page > 1:
            # If we found multiple items, print their names and lowest prices
            print(f'Found {len(result)} {equipment_type} matching "{args.name}":')
            print(f'{'Name':<50} Current Price')
            for item in result:
                lowestPrice = min(entry['price'] for entry in item['entries'])
                print(f'{item['name']:<50} {lowestPrice}')

            quit = handle_page()
            page += 1
        else:
            # If we only found one item, print its details
            # Start by getting the site with the lowest price
            quit = True
            best_site = result[0]['entries'][0]
            for entry in result[0]['entries']:
                best_site = entry['price'] if (entry['price'] < best_site['price']) else best_site

            print(f'{args.equipment_type.capitalize()} entry {result[0]['name']} found:')
            print(f'  Current Lowest Price:', best_site['price'])
            print(f'    Site: {best_site['url']}')
            print(f'    {turn_red(best_site['is_old'], True)}Last Updated: {best_site['last_updated']}{turn_red(best_site['is_old'], False)}\n')

            print(f'  All Time Lowest Price:', result[0]['all_time_low_price'])
            # print(f'  URL:', result[0]['url'])
            if len(result[0]['entries']) > 1:
                print(f'  Other Sites:')
                for entry in result[0]['entries']:
                    if entry != best_site:
                        print(f'    {turn_red(entry['is_old'], True)}{entry['url']} - {entry['price']} - {entry['last_updated']}{turn_red(entry['is_old'], False)}')


def get_all(args: argparse.Namespace, server: str) -> None:
    """
    Return all equipment items of the given type. Only prints the name.
    """
    equipment_type = ROUTE_MAP[args.equipment_type]
    quit = False
    page = 1

    while not quit:
        try:
            response = requests.get(f'{server}/{equipment_type}?page={page}')
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 404:
                if page > 1:
                    print(f'No more {equipment_type} found')
                else:
                    print(f'No {equipment_type} found')
                return
            raise SystemExit(f'{response.json()["error"]}')
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        json = response.json()

        if not json:
            print(f'No {equipment_type} found')
        else:
            print('Name')
            for item in json['items']:
                print(item['name'])

        quit = handle_page()
        page += 1


def get_hostname(url: str) -> str:
    """
    Extract the hostname from the given URL.
    """
    return url.split('www.')[-1].split('.com')[0].split('.org')[0].split('.net')[0]


def handle_page() -> bool:
    """
    Handle pagination by asking the user if they want to continue.
    """
    try:
        user_in = input("Press Enter to get more results, or type 'exit' to quit: ")
        return user_in.lower() == 'exit'
    except KeyboardInterrupt:
        print('\n')
        return True


def turn_red(should_be_red: bool, turn_on: bool = True) -> str:
    """
    Return the ANSI escape code to turn text red if requested.
    Otherwise return the reset code, or an empty string if no color
    change is needed.
    """
    if should_be_red:
        if turn_on:
            return RED_CODE
        return RESET_CODE
    return ''


class Server():
    """
    Saves the config file server value.
    """
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('clientconfig.ini')
        self.server = config['server']['hostname']

    def get(self) -> str:
        """
        Returns the server.
        """
        return self.server


if __name__ == '__main__':
    main()

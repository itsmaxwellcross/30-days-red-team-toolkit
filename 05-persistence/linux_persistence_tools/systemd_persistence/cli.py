#!/usr/bin/env python3
import argparse
from .persistence.system_service import SystemServicePersistence
from .persistence.user_service import UserServicePersistence
from .persistence.timer_service import TimerServicePersistence
from .detection.scanner import SystemdScanner
from .management.remover import ServiceRemover
from .utils.helpers import generate_service_name

def main():
    parser = argparse.ArgumentParser(description="Linux Systemd Persistence Framework")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', action='store_true', help="List all services")
    group.add_argument('--check-suspicious', action='store_true', help="Hunt suspicious services")

    parser.add_argument('--create-system', type=str, help="Create system service")
    parser.add_argument('--create-user', type=str, help="Create user service")
    parser.add_argument('--create-timer', type=str, help="Create scheduled timer")
    parser.add_argument('--service-name', type=str, help="Custom service name")
    parser.add_argument('--description', type=str, help="Service description")
    parser.add_argument('--interval', type=int, default=10, help="Timer interval (minutes)")
    parser.add_argument('--delete', type=str, help="Delete service by name")
    parser.add_argument('--user-service', action='store_true', help="Target is user service")

    args = parser.parse_args()

    if args.list:
        SystemdScanner.list_services()
    elif args.check_suspicious:
        SystemdScanner.check_suspicious()
    elif args.delete:
        ServiceRemover().remove(args.delete, args.user_service)
    elif args.create_system:
        SystemServicePersistence().create(args.create_system, args.service_name, args.description)
    elif args.create_user:
        UserServicePersistence().create(args.create_user, args.service_name, args.description)
    elif args.create_timer:
        TimerServicePersistence().create(args.create_timer, args.service_name, args.interval)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
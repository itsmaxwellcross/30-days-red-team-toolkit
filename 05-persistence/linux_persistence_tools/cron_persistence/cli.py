#!/usr/bin/env python3
import argparse
from .persistence.user_cron import UserCronPersistence
from .persistence.system_cron import SystemCronPersistence
from .persistence.hourly_daily import ScheduledScriptPersistence
from .persistence.reboot_cron import RebootCronPersistence
from .detection.scanner import CronScanner

def main():
    parser = argparse.ArgumentParser(description="Linux Cron Persistence Framework")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', action='store_true', help='List all cron jobs')
    group.add_argument('--check-suspicious', action='store_true', help='Scan for suspicious jobs')

    parser.add_argument('--install-user', type=str, help='Install user-level cron')
    parser.add_argument('--install-system', type=str, help='Install system cron.d (root)')
    parser.add_argument('--install-hourly', type=str, help='Install hourly script (root)')
    parser.add_argument('--install-daily', type=str, help='Install daily script (root)')
    parser.add_argument('--install-reboot', type=str, help='Install @reboot job')
    parser.add_argument('--interval', type=int, default=10, help='User cron interval (minutes)')

    args = parser.parse_args()

    if args.list:
        CronScanner.list_all()
    elif args.check_suspicious:
        CronScanner.check_suspicious()
    elif args.install_user:
        UserCronPersistence().create(args.install_user, args.interval)
    elif args.install_system:
        SystemCronPersistence().create(args.install_system)
    elif args.install_hourly:
        ScheduledScriptPersistence().hourly(args.install_hourly)
    elif args.install_daily:
        ScheduledScriptPersistence().daily(args.install_daily)
    elif args.install_reboot:
        RebootCronPersistence().create(args.install_reboot)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
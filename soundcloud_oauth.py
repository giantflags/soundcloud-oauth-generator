#!/usr/bin/env python3
"""
SoundCloud OAuth Token Generator

A standalone utility for generating SoundCloud OAuth access tokens with PKCE support.
Handles the complex OAuth 2.1 flow required by SoundCloud's API.

Author: Generated from working Librai Scheduler implementation
License: MIT
"""

import os
import sys
import base64
import hashlib
import secrets
import urllib.parse
import json
from typing import Optional, Tuple


def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import requests
        return True
    except ImportError:
        print("❌ Missing required dependency: requests")
        print("Install with: pip install requests")
        return False


def get_config() -> dict:
    """Get configuration from environment variables"""
    config = {
        'client_id': os.getenv('SOUNDCLOUD_CLIENT_ID'),
        'client_secret': os.getenv('SOUNDCLOUD_CLIENT_SECRET'),
        'redirect_uri': os.getenv('SOUNDCLOUD_REDIRECT_URI'),
        'scope': os.getenv('SOUNDCLOUD_SCOPE', 'upload'),
        'output_file': os.getenv('TOKEN_OUTPUT_FILE'),
        'debug': os.getenv('DEBUG', '').lower() in ('1', 'true', 'yes')
    }

    # Validate required config
    missing = [k for k, v in config.items()
               if k in ['client_id', 'client_secret', 'redirect_uri'] and not v]

    if missing:
        print("❌ Missing required environment variables:")
        for var in missing:
            env_var = f"SOUNDCLOUD_{var.upper()}"
            print(f"   {env_var}")
        print("\nExample setup:")
        print("export SOUNDCLOUD_CLIENT_ID='your_client_id'")
        print("export SOUNDCLOUD_CLIENT_SECRET='your_client_secret'")
        print("export SOUNDCLOUD_REDIRECT_URI='http://localhost:8080/callback'")
        sys.exit(1)

    return config


def generate_pkce_pair() -> Tuple[str, str]:
    """Generate PKCE code verifier and challenge"""
    # Generate code verifier (43-128 characters)
    code_verifier = base64.urlsafe_b64encode(
        secrets.token_bytes(32)
    ).decode('utf-8').rstrip('=')

    # Generate code challenge
    digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(
        digest).decode('utf-8').rstrip('=')

    return code_verifier, code_challenge


def build_authorization_url(config: dict, code_challenge: str, state: str) -> str:
    """Build the SoundCloud authorization URL"""
    auth_params = {
        'client_id': config['client_id'],
        'redirect_uri': config['redirect_uri'],
        'response_type': 'code',
        'scope': config['scope'],
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'state': state
    }

    return f"https://secure.soundcloud.com/authorize?{urllib.parse.urlencode(auth_params)}"


def exchange_code_for_token(config: dict, auth_code: str, code_verifier: str) -> dict:
    """Exchange authorization code for access token with PKCE"""
    import requests

    token_url = "https://secure.soundcloud.com/oauth/token"

    data = {
        'grant_type': 'authorization_code',
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'redirect_uri': config['redirect_uri'],
        'code': auth_code,
        'code_verifier': code_verifier
    }

    if config['debug']:
        print(f"🔧 Token exchange URL: {token_url}")
        print(
            f"🔧 Request data: {json.dumps({k: v for k, v in data.items() if k != 'client_secret'}, indent=2)}")

    print("🔄 Exchanging authorization code for access token...")
    response = requests.post(token_url, data=data, timeout=30)

    if response.status_code != 200:
        print(f"❌ Token exchange failed: {response.status_code}")
        print(f"Response: {response.text}")
        response.raise_for_status()

    token_data = response.json()

    if config['debug']:
        print(
            f"🔧 Token response: {json.dumps({k: v for k, v in token_data.items() if k != 'access_token'}, indent=2)}")

    return token_data


def validate_token(access_token: str, debug: bool = False) -> bool:
    """Validate the access token by calling SoundCloud API"""
    import requests

    test_url = 'https://api.soundcloud.com/me'
    headers = {'Authorization': f'OAuth {access_token}'}

    if debug:
        print(f"🔧 Testing token with: {test_url}")

    try:
        response = requests.get(test_url, headers=headers, timeout=10)

        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('username', 'unknown')
            print(f"✅ Token validated! Authenticated as: {username}")
            return True
        else:
            print(f"❌ Token validation failed: {response.status_code}")
            if debug:
                print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Token validation error: {e}")
        return False


def save_token(token_data: dict, output_file: Optional[str] = None) -> None:
    """Save the token to file or display it"""
    access_token = token_data['access_token']

    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(access_token)
            print(f"💾 Token saved to: {output_file}")
        except Exception as e:
            print(f"❌ Failed to save token to file: {e}")
            print(f"Token: {access_token}")
    else:
        print(f"🔑 Access Token: {access_token}")

    # Also display other useful info
    if 'expires_in' in token_data:
        expires_in = token_data['expires_in']
        print(
            f"⏱️  Token expires in: {expires_in} seconds ({expires_in//3600}h {(expires_in%3600)//60}m)")

    if 'scope' in token_data:
        print(f"🔐 Token scope: {token_data['scope']}")


def main():
    """Main OAuth flow"""
    print("🎵 SoundCloud OAuth Token Generator")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Get configuration
    config = get_config()

    if config['debug']:
        print("🔧 Debug mode enabled")
        print(f"🔧 Client ID: {config['client_id'][:10]}...")
        print(f"🔧 Redirect URI: {config['redirect_uri']}")
        print(f"🔧 Scope: {config['scope']}")

    # Generate PKCE parameters
    code_verifier, code_challenge = generate_pkce_pair()

    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)

    if config['debug']:
        print(f"🔧 Code verifier: {code_verifier}")
        print(f"🔧 Code challenge: {code_challenge}")
        print(f"🔧 State: {state}")

    # Build authorization URL
    auth_url = build_authorization_url(config, code_challenge, state)

    print("\n🌐 Visit this URL to authorize the app:")
    print(auth_url)
    print("\n📝 Steps:")
    print("1. Visit the URL above in your browser")
    print("2. Log in to SoundCloud and authorize the app")
    print("3. You'll be redirected to your configured callback URL")
    print("4. Copy the 'code' parameter from the redirect URL")
    print("5. Paste it below")
    print("\nRedirect URL format:")
    print(f"{config['redirect_uri']}?code=AUTHORIZATION_CODE&state={state}")
    print()

    # Get authorization code from user
    auth_code = input("Enter the authorization code: ").strip()

    if not auth_code:
        print("❌ No authorization code provided")
        sys.exit(1)

    # Exchange code for token
    try:
        token_data = exchange_code_for_token(config, auth_code, code_verifier)
        access_token = token_data['access_token']

        print(
            f"✅ Access token generated: {access_token[:20]}...{access_token[-10:]}")

        # Validate token
        if validate_token(access_token, config['debug']):
            # Save token
            save_token(token_data, config['output_file'])
            print("✅ OAuth flow completed successfully!")
        else:
            print("⚠️  Token generated but validation failed")
            save_token(token_data, config['output_file'])

    except Exception as e:
        print(f"❌ Error: {e}")
        if config['debug']:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

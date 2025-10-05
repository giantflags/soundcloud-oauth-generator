#!/usr/bin/env python3
"""
Example usage of the SoundCloud OAuth Token Generator
"""

import os
import subprocess
import requests


def example_basic_usage():
    """Example: Basic token generation"""
    print("=== Basic Usage Example ===")

    # Set environment variables
    os.environ['SOUNDCLOUD_CLIENT_ID'] = 'your_client_id_here'
    os.environ['SOUNDCLOUD_CLIENT_SECRET'] = 'your_client_secret_here'
    os.environ['SOUNDCLOUD_REDIRECT_URI'] = 'http://localhost:8080/callback'

    # Run the OAuth script
    # subprocess.run(['python', 'soundcloud_oauth.py'])
    print("Run: python soundcloud_oauth.py")


def example_with_token_file():
    """Example: Save token to file"""
    print("\n=== Save Token to File Example ===")

    os.environ['TOKEN_OUTPUT_FILE'] = 'my_soundcloud_token.txt'
    # subprocess.run(['python', 'soundcloud_oauth.py'])
    print("Run: python soundcloud_oauth.py")


def example_use_token():
    """Example: Using the generated token"""
    print("\n=== Using the Token Example ===")

    # Read token from file (example)
    token_file = 'my_soundcloud_token.txt'
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            access_token = f.read().strip()

        # Test API access
        headers = {'Authorization': f'OAuth {access_token}'}
        response = requests.get(
            'https://api.soundcloud.com/me', headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Authenticated as: {user_data.get('username')}")
        else:
            print(f"❌ API call failed: {response.status_code}")
    else:
        print("Token file not found. Generate token first.")


def example_upload_track():
    """Example: Upload a track"""
    print("\n=== Upload Track Example ===")

    # This is pseudocode - you'd need an actual audio file
    """
    headers = {'Authorization': f'OAuth {access_token}'}
    
    with open('my_track.mp3', 'rb') as audio_file:
        files = {'track[asset_data]': audio_file}
        data = {
            'track[title]': 'My Awesome Track',
            'track[description]': 'Generated via API',
            'track[genre]': 'Electronic',
            'track[sharing]': 'public'
        }
        
        response = requests.post('https://api.soundcloud.com/tracks',
                               headers=headers, files=files, data=data)
        
        if response.status_code == 201:
            track_data = response.json()
            print(f"✅ Track uploaded: {track_data.get('permalink_url')}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
    """
    print("Code example above - requires actual audio file")


if __name__ == "__main__":
    example_basic_usage()
    example_with_token_file()
    example_use_token()
    example_upload_track()

# SoundCloud OAuth Token Generator

A standalone Python utility for generating SoundCloud OAuth access tokens with PKCE support. This tool handles the complex OAuth 2.1 flow required by SoundCloud's API.

## Why This Exists

SoundCloud's OAuth implementation requires:
- PKCE (Proof Key for Code Exchange) 
- Specific endpoints (`secure.soundcloud.com`)
- Exact redirect URI matching
- Manual authorization flow

This tool handles all the complexity and provides a working solution.

## Features

- ✅ PKCE support (required by SoundCloud)
- ✅ Correct SoundCloud OAuth endpoints
- ✅ Manual authorization flow
- ✅ Token validation
- ✅ Multiple storage options (file, environment, custom)
- ✅ Configuration via environment variables
- ✅ Detailed error handling and troubleshooting

## Quick Start

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Set Up Your SoundCloud App
1. Go to [SoundCloud Developers](https://soundcloud.com/you/apps)
2. Create or edit your app
3. Set the redirect URI (see configuration below)

### 3. Configure Credentials
```bash
export SOUNDCLOUD_CLIENT_ID="your_client_id"
export SOUNDCLOUD_CLIENT_SECRET="your_client_secret"
export SOUNDCLOUD_REDIRECT_URI="http://localhost:8080/callback"
```

### 4. Generate Token
```bash
python soundcloud_oauth.py
```

## Configuration

### Environment Variables
- `SOUNDCLOUD_CLIENT_ID`: Your app's client ID (required)
- `SOUNDCLOUD_CLIENT_SECRET`: Your app's client secret (required)  
- `SOUNDCLOUD_REDIRECT_URI`: Your app's redirect URI (required)
- `SOUNDCLOUD_SCOPE`: OAuth scope (default: "upload")
- `TOKEN_OUTPUT_FILE`: File to save token (default: stdout only)

### Redirect URI Options
1. **Localhost** (easiest): `http://localhost:8080/callback`
2. **Custom domain**: `https://yourdomain.com/auth/callback`
3. **Custom protocol**: `myapp://oauth/callback`

## Usage Examples

### Basic Usage
```bash
python soundcloud_oauth.py
```

### Save Token to File
```bash
export TOKEN_OUTPUT_FILE="soundcloud_token.txt"
python soundcloud_oauth.py
```

### Custom Scope
```bash
export SOUNDCLOUD_SCOPE="upload,playlist"
python soundcloud_oauth.py
```

## Integration Examples

### Using the Generated Token
```python
import requests

# Load token from file or environment
with open('soundcloud_token.txt', 'r') as f:
    access_token = f.read().strip()

# Make authenticated API call
headers = {'Authorization': f'OAuth {access_token}'}
response = requests.get('https://api.soundcloud.com/me', headers=headers)
print(response.json())
```

### Upload a Track
```python
import requests

headers = {'Authorization': f'OAuth {access_token}'}
files = {'track[asset_data]': open('audio.mp3', 'rb')}
data = {'track[title]': 'My Track'}

response = requests.post('https://api.soundcloud.com/tracks', 
                        headers=headers, files=files, data=data)
print(response.json())
```

## Troubleshooting

### Common Issues
- **403 Forbidden**: Check redirect URI matches exactly
- **Invalid client**: Verify client ID/secret
- **PKCE errors**: This tool handles PKCE automatically

### Debug Mode
```bash
export DEBUG=1
python soundcloud_oauth.py
```

## Requirements

- Python 3.6+
- `requests` library
- SoundCloud developer account

## License

MIT License - feel free to use in your projects!

## Contributing

Issues and pull requests welcome! This tool was created to solve real OAuth challenges with SoundCloud's API.

## Related

- [SoundCloud API Documentation](https://developers.soundcloud.com/docs/api/guide#authentication)
- [OAuth 2.1 Specification](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-05)
- [PKCE Specification](https://www.rfc-editor.org/rfc/rfc7636.html)
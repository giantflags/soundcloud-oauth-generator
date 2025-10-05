# Changelog

All notable changes to the SoundCloud OAuth Token Generator will be documented in this file.

## [1.0.0] - 2025-10-05

### Added
- Initial release of standalone SoundCloud OAuth token generator
- PKCE support (required by SoundCloud API)
- Environment variable configuration
- Token validation
- Multiple output options (stdout, file)
- Debug mode for troubleshooting
- Comprehensive error handling
- Working implementation based on successful Librai Scheduler integration

### Features
- Support for SoundCloud OAuth 2.1 with PKCE
- Configurable redirect URIs (localhost, custom domain, custom protocol)
- Token expiration display
- Scope configuration
- Automatic token validation against SoundCloud API

### Documentation
- Complete README with usage examples
- Troubleshooting guide
- Integration examples
- License (MIT)

### Technical Details
- Uses correct SoundCloud endpoints (`secure.soundcloud.com`)
- Implements proper PKCE flow with SHA256 challenge method
- CSRF protection with state parameter
- Robust error handling and user feedback
# Luma Door Unlocker

A Raspberry Pi-based QR code scanner that automatically checks in guests to Luma events by scanning their QR codes.

## Features

- Real-time QR code scanning using camera
- Automatic Luma API authentication
- Event guest validation and check-in
- Credential management and persistence
- Error handling and retry logic
- Comprehensive logging to files and console

## Hardware Requirements

- Raspberry Pi (3B+ or newer recommended)
- USB Camera or Pi Camera module
- Internet connection

## Software Requirements

- Python 3.8+
- Poetry (for dependency management)
- System dependencies for QR code scanning

## Installation

1. **Install system dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install libzbar0 libzbar-dev

# macOS
brew install zbar

# Fedora/CentOS/RHEL
sudo dnf install zbar-devel
# or
sudo yum install zbar-devel
```

2. **Clone this repository:**
```bash
git clone <repository-url>
cd luma-door-unlocker-using-pi
```

3. **Install Poetry if not already installed:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

4. **Install Python dependencies:**
```bash
# Update lock file and install dependencies
poetry lock
poetry install
```

5. **Set up your Luma credentials:**
```bash
export LUMA_EMAIL="your-email@example.com"
export LUMA_PASSWORD="your-password"
```

## Usage

1. **Start the scanner:**
```bash
# Make sure dependencies are installed first
poetry install

# Run the application
LUMA_EMAIL="your-email@example.com" LUMA_PASSWORD="your-password" poetry run luma-scanner
```

2. Point a camera at Luma event QR codes to automatically check in guests

3. Press Ctrl+C to stop the scanner

4. Check logs in the `logs/` directory for detailed information

## Configuration

Configuration is stored in `config/settings.json`:

- `api`: Luma API settings and headers
- `camera`: Camera device settings
- `qr`: QR code detection patterns

## Project Structure

```
├── src/
│   ├── auth/           # Luma API authentication
│   ├── camera/         # QR code scanning
│   ├── storage/        # Credential management
│   └── utils/          # Configuration and logging utilities
├── config/
│   └── settings.json   # Application configuration
├── logs/               # Application logs (auto-generated)
├── research/
│   └── README.md       # API research documentation
└── credentials.json    # Stored auth credentials (auto-generated)
```

## How It Works

1. **Authentication**: The app authenticates with Luma using your email/password
2. **QR Scanning**: Continuously scans for QR codes using the camera
3. **Validation**: Validates QR codes match Luma check-in format
4. **Check-in**: Uses the Luma API to verify guest registration
5. **Logging**: All activities are logged to both console and timestamped log files

## API Research

See `research/README.md` for detailed API flow documentation including:
- Authentication flow
- QR code format
- Check-in endpoints
- Response formats

## Troubleshooting

### Installation Issues
- **zbar library not found**: Install system dependencies as shown in installation section
- **Poetry lock issues**: Run `poetry lock` to regenerate the lock file
- **Permission issues**: Ensure you have proper permissions for camera access

### Camera Issues
- Ensure camera is connected and recognized by the system
- Check `camera.device_index` in config if using non-default camera
- Verify camera permissions

### Authentication Issues
- Verify email/password credentials
- Check internet connection
- Review stored credentials in `credentials.json`

### QR Code Detection Issues
- Ensure good lighting conditions
- QR code should be clearly visible and not damaged
- Check that QR code follows Luma format: `https://lu.ma/check-in/evt-xxx?pk=g-xxx`

## Development

To run in development mode:

```bash
# Install dev dependencies
poetry install --with dev

# Run with debug output
LUMA_EMAIL="your-email" LUMA_PASSWORD="your-pass" poetry run luma-scanner
```

## Quick Setup Commands

```bash
# Complete setup from scratch
sudo apt-get install libzbar0 libzbar-dev  # System dependencies
poetry lock                                # Update lock file
poetry install                             # Install Python dependencies
export LUMA_EMAIL="your-email@example.com"
export LUMA_PASSWORD="your-password"
poetry run luma-scanner                    # Run the application
```

## License

[Add your license here]

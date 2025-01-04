# NetParse

NetParse is a web-based network command parser built with Django. It allows users to input raw network device output and parse it into structured JSON using TextFSM and Genie parsers.

## Features

- Parse raw network device output into structured JSON.
- Select parsers dynamically via a web UI.
- Dockerized for easy setup and deployment.
- DevContainer support for seamless local development.

## Quickstart

### Using Docker

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/netparse.git
   cd netparse
   ```

2. Build and run the application:
   ```
   docker-compose up
   ```

3. Access the application at [http://localhost:8000](http://localhost:8000).

### Development

1. Open the repository in Visual Studio Code.
2. Install the **Remote - Containers** extension if you don’t have it.
3. Reopen the folder in the container:
   - `Remote-Containers: Reopen in Container` (via Command Palette).
4. Start development in `/usr/src/app`.

## Example

### Input

```
Cisco IOS Software, C2960S Software (C2960S-UNIVERSALK9-M), Version 15.0(2)SE2, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2013 by Cisco Systems, Inc.
Compiled Mon 29-Jul-13 07:45 by prod_rel_team

ROM: Bootstrap program is C2960S boot loader
BOOTLDR: C2960S Boot Loader (C2960S-HBOOT-M) Version 12.2(53r)SE2, RELEASE SOFTWARE (fc1)

Switch uptime is 2 years, 1 week, 5 days, 3 hours, 42 minutes
System returned to ROM by power-on
System image file is "flash:/c2960s-universalk9-mz.150-2.SE2.bin"
Last reload reason: power-on
```

### Output (JSON)

```
{"parsed_output": {"version": {"version_short": "15.0", "platform": "C2960S", "version": "15.0(2)SE2", "image_id": "C2960S-UNIVERSALK9-M", "label": "RELEASE SOFTWARE (fc1)", "os": "IOS", "image_type": "production image", "copyright_years": "1986-2013", "compiled_date": "Mon 29-Jul-13 07:45", "compiled_by": "prod_rel_team", "rom": "Bootstrap program is C2960S boot loader", "bootldr": "C2960S Boot Loader (C2960S-HBOOT-M) Version 12.2(53r)SE2, RELEASE SOFTWARE (fc1)", "hostname": "Switch", "uptime": "2 years, 1 week, 5 days, 3 hours, 42 minutes", "returned_to_rom_by": "power-on", "system_image": "flash:/c2960s-universalk9-mz.150-2.SE2.bin", "last_reload_reason": "power-on"}}}
```

## License

This project is licensed under the MIT License.


# Serial Monitor

A lightweight desktop serial port monitor built with Python and PyQt5.

![Serial Monitor](serial.png)

## Features

- **Dual view** — side-by-side ASCII text and hex display of received data
- **Color-coded output** — TX data in blue, RX data in green, other data in magenta
- **Send ASCII or Hex** — two independent send boxes with optional `\r\n` line ending
- **Configurable port settings** — port name, baud rate, data bits, parity, stop bits, and flow control
- **Text filter** — hide lines that match specified substrings
- **Clear** — one-click view reset

## Requirements

- Python 3.x
- PyQt5
- PyQt5 serial port module

Install dependencies:

```bash
pip install PyQt5 PyQt5-Qt5 PyQt5-sip pyserial
```

> On some systems you may also need:
> ```bash
> pip install PyQt5.sip
> ```

## Usage

```bash
python moniter.py
```

1. Select the **port** and configure **baud rate**, **data bits**, **parity**, **stop bits**, and **flow control** from the toolbar.
2. Click **Open** to connect.
3. Incoming data appears in the left (ASCII) and right (hex) panels.
4. Type in the **Send Ascii** or **Send Hex** box and press Enter (or click the button) to transmit.
5. Use **Filter** to open the filter panel and add substrings — any line containing a filter string will be hidden.
6. Click **Clear** to reset the display.
7. Click **Close** to disconnect the port.

## Project Structure

```
Serial-Monitor/
├── moniter.py                  # Main application
├── testFilter.py               # Standalone filter widget test
├── testBytesRepresetation.py   # Byte/hex representation experiments
└── serial.png                  # Application icon
```

## License

This project is provided as-is without an explicit license.

# TkXTerm - XTerm in Tkinter

[![PyPI](https://img.shields.io/pypi/v/tkxterm?style=flat)](https://pypi.python.org/pypi/tkxterm/)

TkXTerm makes available a Terminal Ttk frame, that have XTerm embedded and it can be used in the Tkinter GUI as a normal frame. It's possible to send any commands to execute it, having back in the code an object that, after the end of the command, contains the exit code and can execute a callback. It's also possible to use XTerm normally.

![](./images/test.png)

This project is born with the purpose of having an embedded and fully functional bash terminal in a Tkinter GUI, to interact with it and run some commands automatically, viewing in real-time the output and the results and having the exit code back into an object in the code.

## Installation

TkXTerm can be installed from PyPI using the command `pip install tkxterm`.
Besides Tkinter, it has XTerm and screen (a GNU software, generally preinstalled in all Linux system) as dependecies. Make sure you have both installed before trying to use this library. Because of these dependencies, this library is available only for Linux system; correct functioning in other systems is not guaranteed.

If you want to change any behaviour or the style of the terminal itself, for example to enable the scrolling or the colors, you can relate to the settings of GNU screen tool and the XTerm settings.

## Usage

### Terminal

TkXTerm makes available the `Terminal` Ttk frame, so all the Ttk Frame options are available.
In addition, it can accept the following options:
- `restore_on_close`, which enables automatic restart of the terminal when it is closed (e.g. by accidentally pressing Ctrl-D);
- `read_interval_ms`, which specifies how many milliseconds should pass between each reading of the terminal to retrieve exit codes;
- `read_length`, which specifies how many bytes to read in each interval.

All these options can be changed like any option of the frame.

> The terminal will only be launched once it has been visible!

> You can manually type a command in the terminal only if the cursor was in its frame!

It has also its methods to interact with the terminal:
- `run_command` is the resposible for run any command you want on the terminal. This method will add an end command to your command, which will print the exit code to capture it. To execute a command in background, use the `background` argument rather than using the classic `&` method, because otherwise the exit code indicates only if the command started correctly or not, and not the actual exit code of the command runned in background. You can also specify a `callback` that will be called immediatly after the command is terminated, this callback receive the Command object as argument.
- `send_string` is the function for the actual sending any string to the terminal, and stores it if the terminal is not ready. With this you can send any string at any moment to the terminal.
- `restart_term` is the procedure for reboot the terminal if it is closed.

Furthermore, it have the properties `ready`, that indicates if the terminal is ready or not, and `end_string`, that returns the string appended at the end of any command executed.

Terminal generates also some events: when the terminal is ready or no more ready, it generates `<<TerminalReady>>` and `<<TerminalClosed>>`; when a command finishes it generates `<<CommandEnded>>` with the referiment to the Command object, while when a string is sent to the terminal, it generates `<<StringSent>>` with the referiment to the string itself.

### Command

The `run_command` method returns an instance of the `Command` class, that hold the command string in the `cmd` property, the exit code of itself in the `exit_code` property, and the callback in the `callback` property.

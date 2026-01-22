# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

This is a Gradle project (Java 8+).

- **Build the project**: `./gradlew build`
- **Run tests/examples**:
  - Standard Test: `./gradlew SystemTray_normal`
  - JavaFX Test: `./gradlew SystemTray_javaFx`
  - SWT Test: `./gradlew SystemTray_swt`
- **Create example JARs**: `./gradlew jarAllExamples`
- **Publish to Maven Local**: `./gradlew publishToMavenLocal`

## Architecture

This is a cross-platform System Tray library for Java supporting Linux (GtkStatusIcon, AppIndicator), macOS (AWT), and Windows (Native, Swing).

### Key Components

- **Public API**: `dorkbox.systemTray.SystemTray` (Singleton facade). Access via `SystemTray.get()`.
- **Menu System**:
  - `dorkbox.systemTray.Menu`: The root menu container.
  - `dorkbox.systemTray.MenuItem`: Individual menu entries.
  - `dorkbox.systemTray.Checkbox`: Checkbox menu items.
  - `dorkbox.systemTray.Separator`: Menu separators.
  - `dorkbox.systemTray.Status`: Status text entry.

### Platform Abstraction

The library uses a **Peer Pattern** to handle platform-specific implementations:

- **Peers** (`dorkbox.systemTray.peer`): Define the contract for implementations.
- **Tray Hierarchy** (`dorkbox.systemTray.ui`): Contains concrete implementations for different platforms.
  - `swing`: Swing-based implementation (cross-platform).
  - `gtk`: Linux native (GtkStatusIcon) and AppIndicator implementations.
  - `osx`: macOS AWT implementation.
  - `awt`: Fallback AWT implementation.
  - `swing/_WindowsNativeTray.java`: Windows native notification icon with Swing menu.

### Selection Logic

- `dorkbox.systemTray.util.AutoDetectTrayType`: Determines which platform implementation to use based on OS and environment (e.g., Gnome vs KDE).
- `SystemTray.FORCE_TRAY_TYPE` property allows overriding auto-detection.
- Linux implementation selection is complex and involves checking GTK versions (2 vs 3), Desktop Environment, and JavaFX/SWT presence (see `SystemTray.get()`).

### Utilities

- `dorkbox.systemTray.util.EventDispatch`: Manages the event dispatch thread (GTK/AppIndicator requires a specific event loop).
- `dorkbox.systemTray.util.SizeAndScaling`: Handles DPI awareness and icon sizing for different OSs.
- `dorkbox.systemTray.util.SystemTrayFixes*`: Applies compatibility fixes for specific OS/JDK versions.

### Important Constraints

- Linux Tray initialization is complex. Initialization *must* happen **outside** the Swing EDT if using AppIndicator or native GTK (the code handles this, but be aware of thread safety implications).
- Tooltips are not supported on AppIndicators (Linux).
- Running as Root on Linux with AppIndicators is problematic (requires dbus fixes).
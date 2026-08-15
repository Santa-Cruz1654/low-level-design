# Music Player — Low-Level Design

A Python-based Low-Level Design (LLD) implementation of a music player system designed to demonstrate clean object-oriented design and commonly used design patterns.

The implementation focuses on separating **what the music player does** from **how individual behaviors are implemented**, making the design easier to extend and test.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Design Goals](#design-goals)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Design Patterns](#design-patterns)
- [Core Components](#core-components)
- [Playback Strategies](#playback-strategies)
- [Device Integration](#device-integration)
- [Execution Flow](#execution-flow)
- [Example Scenario](#example-scenario)
- [How to Run](#how-to-run)
- [Design Decisions](#design-decisions)
- [Future Improvements](#future-improvements)

---

## Overview

The Music Player supports:

- Creating and managing songs
- Creating playlists
- Adding songs to playlists
- Connecting different audio output devices
- Playing an individual song
- Pausing and resuming playback
- Selecting different playback strategies
- Sequential playback
- Random playback
- Custom next-song queues
- Playing the next track
- Playing the previous track
- Maintaining playback history
- Switching between output-device implementations

The system is intentionally implemented as an LLD exercise rather than a production audio player. The external device APIs are mocked/simulated so the focus remains on object-oriented design and design patterns.

---

## Requirements

### Functional Requirements

1. The user can add songs to the music library.
2. The user can create playlists.
3. The user can add songs from the library to playlists.
4. The user can connect an audio output device.
5. The user can play a single song.
6. The user can pause and resume the current song.
7. The user can select a playback strategy.
8. The user can load a playlist.
9. The user can play all tracks in a playlist.
10. The user can play the next track.
11. The user can play the previous track.
12. The user can queue a song to play next.

### Non-Functional / Design Requirements

- Playback behavior should be replaceable without modifying the player.
- Different audio-device APIs should be hidden behind a common interface.
- Object creation should be centralized where appropriate.
- Shared application components should have a single instance.
- The high-level application API should remain simple.
- Components should have focused responsibilities.
- The design should be extensible for additional strategies and devices.

---

## Design Goals

The design separates the system into independent responsibilities:

```text
Models
  ↓
Libraries
  ↓
Managers
  ↓
Strategies / Devices
  ↓
Audio Engine
```

The application interacts primarily with the `MusicPlayerApplication` and `MusicPlayerFacade` instead of directly coordinating every subsystem.

The major design goal is to avoid putting all music-player behavior into one large class.

---

## Project Structure

```text
02-music-player/
│
├── common/
│   ├── __init__.py
│   └── singleton.py
│
├── core/
│   ├── __init__.py
│   └── audio_engine.py
│
├── device/
│   ├── __init__.py
│   ├── i_audio_output_device.py
│   ├── bluetooth_speaker_adapter.py
│   ├── headphones_adapter.py
│   └── wired_speaker_adapter.py
│
├── enums/
│   ├── __init__.py
│   ├── device_type.py
│   └── play_strategy_type.py
│
├── external/
│   ├── __init__.py
│   ├── bluetooth_speaker_api.py
│   ├── headphones_api.py
│   └── wired_speaker_api.py
│
├── factories/
│   ├── __init__.py
│   └── device_factory.py
│
├── library/
│   ├── __init__.py
│   ├── song_library.py
│   └── playlist_library.py
│
├── managers/
│   ├── __init__.py
│   ├── device_manager.py
│   └── strategy_manager.py
│
├── models/
│   ├── __init__.py
│   ├── song.py
│   └── playlist.py
│
├── strategies/
│   ├── __init__.py
│   ├── play_strategy.py
│   ├── sequential_play_strategy.py
│   ├── random_play_strategy.py
│   ├── custom_queue_strategy.py
│   └── playback_history.py
│
├── main.py
├── music_player_application.py
└── music_player_facade.py
```

---

## Architecture

At a high level, the application is organized as:

```text
                         main.py
                            │
                            ▼
                MusicPlayerApplication
                            │
                            ▼
                   MusicPlayerFacade
                    /       |                          /        |                          ▼         ▼         ▼
             Libraries   Managers   AudioEngine
                          /                              ▼       ▼
                DeviceManager  StrategyManager
                     │              │
                     ▼              ▼
                DeviceFactory   PlayStrategy
                     │          /     |                           ▼         ▼      ▼       ▼
                  Adapters  Sequential Random Custom
                     │
                     ▼
               External APIs
```

### High-Level Responsibilities

| Component | Responsibility |
|---|---|
| `Song` | Represents a song |
| `Playlist` | Represents a collection of songs |
| `SongLibrary` | Stores and retrieves songs |
| `PlaylistLibrary` | Creates and manages playlists |
| `AudioEngine` | Maintains playback state and delegates audio output |
| `PlayStrategy` | Defines how tracks are selected |
| `DeviceManager` | Maintains the currently connected output device |
| `StrategyManager` | Provides playback strategies |
| `DeviceFactory` | Creates the appropriate output-device adapter |
| Device adapters | Translate the common device interface to external APIs |
| `MusicPlayerFacade` | Coordinates the music-player subsystems |
| `MusicPlayerApplication` | Provides the application-level API |
| `main.py` | Composition root and demonstration entry point |

---

## Design Patterns

### 1. Strategy Pattern

**Location:** `strategies/`

```text
                 PlayStrategy
                      ▲
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
     Sequential     Random     CustomQueue
```

The `PlayStrategy` abstraction defines operations such as:

- `set_playlist()`
- `has_next()`
- `next()`
- `has_previous()`
- `previous()`
- `add_to_next()`

The concrete strategies implement different playback behaviors.

#### Why Strategy?

Without Strategy, the player could become filled with conditionals:

```text
if sequential:
    ...
elif random:
    ...
elif custom_queue:
    ...
```

With Strategy, the player delegates track-selection behavior to the selected strategy.

Adding another playback mode can therefore be done by introducing another strategy implementation rather than rewriting the player.

---

### 2. Adapter Pattern

**Location:** `device/`

The application works with:

```text
IAudioOutputDevice
```

while the external device APIs expose their own interfaces.

```text
Music Player
     │
     ▼
IAudioOutputDevice
     │
     ├── BluetoothSpeakerAdapter ──► BluetoothSpeakerAPI
     ├── HeadphonesAdapter        ──► HeadphonesAPI
     └── WiredSpeakerAdapter     ──► WiredSpeakerAPI
```

The adapters translate the application's expected interface into the corresponding external API.

#### Why Adapter?

The music player should not depend directly on the implementation details of every external device API.

This also allows another device implementation to be introduced without changing the core playback code.

---

### 3. Factory Pattern

**Location:** `factories/device_factory.py`

`DeviceFactory` maps a `DeviceType` to the corresponding device adapter.

```text
DeviceType.BLUETOOTH
        ↓
BluetoothSpeakerAdapter

DeviceType.WIRED
        ↓
WiredSpeakerAdapter

DeviceType.HEADPHONES
        ↓
HeadphonesAdapter
```

#### Why Factory?

Object creation is centralized instead of being scattered across the application.

The caller only needs to specify the desired device type.

---

### 4. Singleton Pattern

**Location:** `common/singleton.py`

The project uses `SingletonMeta` as a metaclass.

Classes such as:

- `MusicPlayerApplication`
- `MusicPlayerFacade`
- `DeviceManager`
- `StrategyManager`
- library components

can use the metaclass to ensure repeated construction returns the same instance.

The singleton implementation also protects instance creation with a re-entrant lock.

#### Why Singleton?

For this LLD exercise, these components represent shared application state, such as:

- the current connected device
- shared libraries
- the active facade
- shared strategy management

A single instance avoids accidentally creating multiple independent states.

---

### 5. Facade Pattern

**Location:** `music_player_facade.py`

`MusicPlayerFacade` provides a simpler interface over several subsystems:

```text
MusicPlayerFacade
       │
       ├── AudioEngine
       ├── DeviceManager
       ├── StrategyManager
       └── PlaylistLibrary
```

For example, the caller can request:

```text
play_next_track()
```

without knowing:

1. Which strategy is active
2. Which song the strategy selects
3. Which device is connected
4. How the audio engine performs playback

#### Why Facade?

It reduces coupling between the application layer and the internal subsystem structure.

---

## Core Components

### `Song`

Represents the basic song entity.

Typical information includes:

```text
title
artist
path
```

### `Playlist`

Represents a collection of songs and provides playlist-level operations.

### `SongLibrary`

Responsible for storing and finding songs.

### `PlaylistLibrary`

Responsible for creating and managing playlists and adding songs to them.

### `AudioEngine`

Maintains playback-related state:

```text
current song
paused / playing state
```

It receives an `IAudioOutputDevice` and a `Song`, then delegates actual output to the device.

This creates a useful separation:

```text
Strategy → decides WHICH song
AudioEngine → manages playback state
Device → performs audio output
```

---

## Playback Strategies

### Sequential Playback

Songs are played in playlist order:

```text
A → B → C → D
```

The strategy maintains a current index.

### Random Playback

Songs are selected randomly from the remaining songs.

```text
A B C D
 ↓
C
 ↓
A
 ↓
D
 ↓
B
```

The implementation removes each selected song from the remaining collection, preventing it from being selected again during the current playlist run.

A `PlaybackHistory` object is used to support previous-track navigation.

### Custom Queue Playback

Custom queue playback allows songs to be inserted into a queue that takes priority over normal sequential playback.

Example:

```text
Playlist:
A → B → C → D

Queue:
C → A

Playback:
C → A → B → D
```

The implementation uses a `deque` for the next-song queue.

`PlaybackHistory` is used to support previous-track navigation.

---

## Device Integration

The device subsystem separates the application's device abstraction from external APIs.

```text
             IAudioOutputDevice
                     ▲
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
 Bluetooth       Headphones      Wired
 Adapter          Adapter       Adapter
        │            │            │
        ▼            ▼            ▼
 Bluetooth        Headphones     Wired
 API              API            API
```

The application therefore interacts with a common interface rather than directly depending on Bluetooth, wired-speaker, or headphone implementations.

---

## Execution Flow

The main demonstration follows this general flow:

```text
main.py
   │
   ▼
Get MusicPlayerApplication
   │
   ├── Create songs
   ├── Create playlist
   ├── Add songs to playlist
   │
   ├── Connect Bluetooth device
   │
   ├── Play single song
   ├── Pause
   └── Resume
   │
   ├── Select Sequential strategy
   ├── Load playlist
   └── Play all tracks
   │
   ├── Select Random strategy
   ├── Load playlist
   └── Play all tracks
   │
   ├── Select Custom Queue strategy
   ├── Load playlist
   ├── Queue songs
   └── Play all tracks
   │
   └── Test previous-track navigation
```

---

## Example Scenario

The sample application creates a playlist called:

```text
Bollywood Vibes
```

with songs including:

```text
Kesariya
Chaiyya Chaiyya
Tum Hi Ho
Jai Ho
```

It then demonstrates:

1. Bluetooth device connection
2. Individual song playback
3. Pause/resume
4. Sequential playback
5. Random playback
6. Custom queue playback
7. Previous-track navigation

This makes `main.py` a practical demonstration of how the different design patterns work together.

---

## How to Run

From inside the `02-music-player` directory:

```bash
python main.py
```

The project uses simulated external device APIs, so it does not require a real Bluetooth speaker, headphones, or audio hardware.

---

## Design Decisions

### Why separate `AudioEngine` from `PlayStrategy`?

Because deciding the next song and actually playing a song are different responsibilities.

```text
PlayStrategy
    ↓
Which song?

AudioEngine
    ↓
Play that song
```

### Why separate adapters from external APIs?

The external APIs are implementation details. The core application should depend on a stable abstraction.

### Why use a Facade?

The application should not need to coordinate every subsystem itself.

### Why use managers?

Managers provide a focused coordination point for shared subsystems such as devices and strategies.

### Why use a Factory?

Creation logic is centralized and can be extended when new device types are introduced.

---

## Future Improvements

Possible extensions to the current design include:

- Add `stop()` and `resume()` as explicit audio operations
- Add repeat-one and repeat-all playback modes
- Add playlist removal and editing
- Add song removal from playlists
- Add search by artist, album, or title
- Add album and artist models
- Add multiple output-device switching
- Add persistent storage
- Add unit tests
- Add dependency injection for easier testing
- Replace simulated external APIs with real integrations
- Add richer playback state management
- Add Observer-based notifications for playback events
- Add a command layer for undoable player operations
- Add thread-safe playback control for asynchronous audio playback

---

## Design Pattern Summary

| Pattern | Implementation | Purpose |
|---|---|---|
| Strategy | `PlayStrategy` + concrete strategies | Change playback behavior |
| Adapter | Device adapters | Integrate incompatible external APIs |
| Factory | `DeviceFactory` | Centralize device creation |
| Singleton | `SingletonMeta` | Manage shared application state |
| Facade | `MusicPlayerFacade` | Simplify subsystem interaction |

---

## Learning Focus

This project is intended to demonstrate how multiple LLD patterns can work together rather than being implemented in isolation.

The important design relationships are:

```text
Facade
  ↓
Managers
  ↓
Factory / Strategy
  ↓
Adapters
  ↓
External APIs
```

while:

```text
Library
  ↓
Models
```

and:

```text
Strategy
  ↓
AudioEngine
  ↓
Output Device
```

form the main playback flow.

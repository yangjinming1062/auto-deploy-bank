# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Scene** is a lightweight Android navigation and UI composition library by ByteDance that replaces Activities and Fragments. It's designed for high-performance navigation (100ms+ faster startup than Activity) with full Fragment compatibility.

**Modules:**
- `library/scene` - Core Scene framework
- `library/scene_navigation` - Navigation stack management
- `library/scene_ui` - UI utilities
- `library/scene_fragment` - Fragment integration
- `library/scene_dialog` - Dialog support
- `library/scene_shared_element_animation` - Shared element transitions
- `library/scene_ktx` - Kotlin extensions
- `demo` - Sample application (includes Compose examples)

## Build Commands

```bash
# Build debug APK
./gradlew assembleDebug

# Build and install demo app to connected device/emulator
./gradlew installDebug

# Run all unit tests (Robolectric + JUnit)
./gradlew test

# Run tests for a specific module
./gradlew :library:scene:test

# Run a single test class
./gradlew :library:scene:test --tests "com.bytedance.scene.GroupSceneTransactionTests"

# Run a single test method
./gradlew :library:scene:test --tests "com.bytedance.scene.GroupSceneTransactionTests.pushNewSceneShouldBeSuccess"

# Generate javadoc for scene module
./gradlew :library:scene:javadoc

# Clean build
./gradlew clean
```

## Architecture

**Core Pattern:** Scene-based navigation replacing Activity/Fragment
- `Scene` base class (similar to Fragment but view-based, directly manages views)
- `SceneActivity` as container activity
- `NavigationScene` manages stack of Scenes with push/pop operations

**Key Classes:**
- `Scene` - Base class for all pages, implements lifecycle owners
- `SceneLifecycleManager` - Manages Scene lifecycle state transitions
- `GroupScene` - Container Scene that can hold child Scenes at specific view IDs
- `SceneContainer` - ViewGroup for holding Scene views

**Entry Points:**
- Core Scene: `library/scene/src/main/java/com/bytedance/scene/Scene.java`
- Navigation: `library/scene_navigation/src/main/java/com/bytedance/scene/navigation/NavigationScene.java`
- Demo examples: `demo/src/main/java/com/bytedance/scenedemo/`

**Package Structure:**
- `com.bytedance.scene` - Core Scene framework
- `com.bytedance.scene.navigation` - Navigation APIs
- `com.bytedance.scene.fragment` - Fragment compatibility layer
- `com.bytedance.scene.ui` - UI utilities
- `com.bytedance.scene.dialog` - Dialog Scenes
- `com.bytedance.scene.ktx` - Kotlin extensions

## Tech Stack

- **Language:** Java (primary) + Kotlin
- **Min SDK:** 21 (Android 5.0)
- **Target SDK:** 33
- **Test Framework:** Robolectric + JUnit + Truth assertions
- **Build:** Gradle 7.4.2 with Android Gradle Plugin 7.4.2
- **Demo includes:** Jetpack Compose integration

## Key Conventions

- Uses `requireSceneContext()` to get SceneContext
- Lifecycle (entering): `onCreateView` → `onViewCreated` → `onActivityCreated` → `onStart` → `onResume`
- Lifecycle (exiting): `onPause` → `onStop` → `onDestroyView`
- State restoration: `onSaveInstanceState` occurs before `onDestroyView`; state is restored in `onViewStateRestored`
- Navigation: `navigationScene?.push(Scene())` / `pop()`
- Scene inheritance chain for different use cases:
  - `Scene` - base
  - `AppCompatScene` - with AppCompat support
  - `GroupScene` - container for child Scenes

## Technical Notes

- Scene implements `LifecycleOwner`, `SavedStateRegistryOwner`, and `ViewModelStoreOwner` - fully compatible with AndroidX Jetpack
- No R8/ProGuard configuration required
- Supports Parcelable-based state saving for view hierarchy
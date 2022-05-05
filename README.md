# Cross building with conan

该项目演示了如何使用 Conan 管理三方库并交叉编译各个平台下的产物（Android、iOS、macOS、Windows、Linux）

## 软件版本

 - Conan 1.47.0+
 - CMake 3.18+

## 编译当前平台、架构产物

在 Apple Silicon M1 设备上，默认编译出来的产物就是 arm64 架构，而在 Intel Chip 设备上，默认编译出来的产物是 x86_64 架构，我们不需要特殊配置，执行正常的 CMake 初始化和编译指令即可。Windows 和 Linux 等也均是如此。

```bash
# 生成为 Xcode 工程
cmake -Bbuild -GXcode -DCMAKE_BUILD_TYPE=Debug
# 编译工程
cmake --build build --config Debug
```

## 交叉编译

除了编译当前平台下的产物以外，我们更希望能交叉编译其他平台的产物，比如在 arm64 设备上交叉编译出 x86_64 架构的产物，在 macOS 下交叉编译出 iOS、Android 平台产物等需求。这就要求我们要给 CMake 和 Conan 传递一些关键信息，告诉他们我们即将要编译的目标平台是什么，对于 Conan 我们还需要告诉它本机的编译环境是怎样的。

通过一些参数我们可以告诉 CMake 目标平台的一些信息，如下所示：

 - `CMAKE_SYSTEM_NAME` 目标系统，如 iOS、Android
 - `CMAKE_OSX_ARCHITECTURES` Apple 系架构列表，如 arm64、x86_64
 - `CMAKE_OSX_DEPLOYMENT_TARGET` Apple 系最低支持目标系统版本
 - `CMAKE_OSX_SYSROOT` Apple 系目标系统 SDK，如 iphoneos、iphonesimulator
 - `CMAKE_SYSTEM_VERSION` 指定 Android 系统的 API level，如 19、20、21 等
 - `CMAKE_ANDROID_ARCH_ABI` 指定 Android 系统的目标架构，如 x86、x86_64、arm64-v8a、armeabi-v7a
 - `CMAKE_ANDROID_NDK` 指定 Android 交叉编译时 NDK（工具链）的位置信息

而 Conan 支持通过传递 profile 的方式来显示的指定要编译得目标平台、架构和本机编译环境信息。我们使用 [conan.cmake](https://github.com/conan-io/cmake-conan) 简化了 conan install 流程，你只需要在 CMake 初始化时指定 `DCONAN_PROFILE_BUILD` 和 `DCONAN_PROFILE_HOST` 变量告诉 Conan 本机（BUILD）和目标（HOST）系统的 profile 信息即可。如下所示：

```bash
cmake -Bbuild -GXcode \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/macos-x86_64 \
  .... other arguments
```

CMake 脚本中会将 `CONAN_PROFILE_BUILD` 变量和 `CONAN_PROFILE_HOST` 变量的值透传给 conan install，使用本机 profile 将值设置为 `default` 即可，conan 会读取本机默认的 profile 信息。

对于目标系统，我们将保存了所有可能的目标系统和架构信息的 profile 文件存放到了工程的 [.profiles](./.profiles) 目录，需要使用时我们通过命令行指定即可。如下所示：

 > 请注意，Conan 的 BUILD 和 HOST 与 CMake 的一些变量使用刚好相反，一旦概念混淆，将可能导致编译出错。

以下展示了所有可能得交叉编译场景命令，用于编译出各个平台各个架构下的产物，用以参考：

## macOS 交叉编译示例

 - 系统环境：macOS

**Apple Silicon M1 arm64 交叉编译 x86_64**

```bash
# configure
cmake -Bbuild -GXcode \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_OSX_ARCHITECTURES=x86_64 \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/macos-x86_64

# build
cmake --build build --config Debug
```

**Intel Chip 交叉编译 arm64**

```bash
# configure
cmake -Bbuild -GXcode \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/macos-arm64

# build
cmake --build build --config Debug
```

# iOS 交叉编译示例

 - 系统环境：macOS

**macOS 交叉编译 iOS x86_64 模拟器**

```bash
# configure
cmake -Bbuild -GXcode \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/ios-x86_64-iphonesimulator \
  -DCMAKE_SYSTEM_NAME=iOS \
  -DCMAKE_OSX_SYSROOT=iphonesimulator \
  -DCMAKE_OSX_DEPLOYMENT_TARGET=9.3 \
  -DCMAKE_OSX_ARCHITECTURES=x86_64

# build
cmake --build build --config Debug
```

**macOS 交叉编译 iOS arm64 模拟器**

```bash
# configure
cmake -Bbuild -GXcode \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/ios-arm64-iphonesimulator \
  -DCMAKE_SYSTEM_NAME=iOS \
  -DCMAKE_OSX_SYSROOT=iphonesimulator \
  -DCMAKE_OSX_DEPLOYMENT_TARGET=9.3 \
  -DCMAKE_OSX_ARCHITECTURES=arm64

# build
cmake --build build --config Debug
```

**macOS 交叉编译 iOS arm64 真机**

```bash
# configure 请注意更换您的 CMAKE_XCODE_ATTRIBUTE_DEVELOPMENT_TEAM 值用以签名
cmake -Bbuild -GXcode \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/ios-arm64-iphoneos \
  -DCMAKE_SYSTEM_NAME=iOS \
  -DCMAKE_OSX_DEPLOYMENT_TARGET=9.3 \
  -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DCMAKE_XCODE_ATTRIBUTE_DEVELOPMENT_TEAM=569GNZ5392

# build
cmake --build build --config Debug
```

**macOS 交叉编译 iOS armv7 真机**

```bash
# configure 请注意更换您的 CMAKE_XCODE_ATTRIBUTE_DEVELOPMENT_TEAM 值用以签名
cmake -Bbuild -GXcode \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/ios-armv7-iphoneos \
  -DCMAKE_SYSTEM_NAME=iOS \
  -DCMAKE_OSX_DEPLOYMENT_TARGET=9.3 \
  -DCMAKE_OSX_ARCHITECTURES=armv7 \
  -DCMAKE_XCODE_ATTRIBUTE_DEVELOPMENT_TEAM=569GNZ5392

# build
cmake --build build --config Debug
```

## Android 交叉编译示例

在配置 Android 交叉编译前，您需要安装指定版本的 NDK 到系统中，我们推荐使用 Android Studio 来安装。本次测试使用的是 NDK 21.4.7075529，如果您需要使用其他版本，请务必更换 profile 中 `android-ndk` 为其他版本。

 > profile 中的 NDK 与本机 NDK 在这种情况下是重复的，Conan 会根据 profile 指定的 NDK 版本来下载对应的 NDK 到 conan 缓存目录，它会帮我们配置各类变量、工具链信息，而我们自己安装的 NDK 只是为了让 CMake 找到对应的工具链而已。您必须要保证两边使用的版本是一致的。这是一种折中方案，Conan 社区已经在筹划 2.0 版本中使用 conf 字段来配置 NDK 相关信息，可关注 Conan 社区获取更多。

**macOS 交叉编译 Android x86_64**

```bash
# configure 请注意更换 CMAKE_ANDROID_NDK 变量指定正确的 NDK 目录
cmake -Bbuild \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_SYSTEM_NAME=Android \
  -DCMAKE_SYSTEM_VERSION=21 \
  -DCMAKE_ANDROID_ARCH_ABI=x86_64 \
  -DCMAKE_ANDROID_NDK=/Users/admin/Library/Android/sdk/ndk/21.4.7075529 \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/android-x86_64-abi21

# build
cmake --build build --config Debug
```

**macOS 交叉编译 Android x86**

```bash
# configure 请注意更换 CMAKE_ANDROID_NDK 变量指定正确的 NDK 目录
cmake -Bbuild \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_SYSTEM_NAME=Android \
  -DCMAKE_SYSTEM_VERSION=21 \
  -DCMAKE_ANDROID_ARCH_ABI=x86 \
  -DCMAKE_ANDROID_NDK=/Users/admin/Library/Android/sdk/ndk/21.4.7075529 \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/android-x86-abi21

# build
cmake --build build --config Debug
```

**macOS 交叉编译 Android arm64-v8a**

```bash
# configure 请注意更换 CMAKE_ANDROID_NDK 变量指定正确的 NDK 目录
cmake -Bbuild \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_SYSTEM_NAME=Android \
  -DCMAKE_SYSTEM_VERSION=21 \
  -DCMAKE_ANDROID_ARCH_ABI=arm64-v8a \
  -DCMAKE_ANDROID_NDK=/Users/admin/Library/Android/sdk/ndk/21.4.7075529 \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/android-arm64-v8a-abi21

# build
cmake --build build --config Debug
```

**macOS 交叉编译 Android armeabi-v7a**

```bash
# configure 请注意更换 CMAKE_ANDROID_NDK 变量指定正确的 NDK 目录
cmake -Bbuild \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_SYSTEM_NAME=Android \
  -DCMAKE_SYSTEM_VERSION=21 \
  -DCMAKE_ANDROID_ARCH_ABI=armeabi-v7a \
  -DCMAKE_ANDROID_NDK=/Users/admin/Library/Android/sdk/ndk/21.4.7075529 \
  -DCONAN_PROFILE_BUILD=default \
  -DCONAN_PROFILE_HOST=$(pwd)/.profiles/android-armeabi-v7a-abi21

# build
cmake --build build --config Debug
```

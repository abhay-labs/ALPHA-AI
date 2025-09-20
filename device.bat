@echo off
rem ------------------------------
rem ADB Wi-Fi Connection Script (Manual IP Only)
rem ------------------------------

set ADB_PATH=C:\platform-tools\adb.exe
set DEVICE_IP=192.168.29.65
set ADB_PORT=5555

echo Disconnecting old connections...
"%ADB_PATH%" disconnect

echo Setting up device in TCP mode on port %ADB_PORT%...
"%ADB_PATH%" tcpip %ADB_PORT%

echo Waiting for device to initialize...
timeout /t 3 /nobreak

echo Connecting to device at %DEVICE_IP%...
"%ADB_PATH%" connect %DEVICE_IP%:%ADB_PORT%

echo Restarting ADB server...
"%ADB_PATH%" kill-server
"%ADB_PATH%" start-server

echo Final connection to device at %DEVICE_IP%...
"%ADB_PATH%" connect %DEVICE_IP%:%ADB_PORT%

echo Connection process completed.
rem pause   <-- remove this line

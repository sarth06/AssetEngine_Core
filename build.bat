@echo off
echo [AeroCanvas] Starting Native Build Pipeline...

cd C:\Users\User\Desktop\AssetEngine_Core\core_engine\src

echo Compiling Java...
C:\GraalVM\bin\javac.exe Main.java Image.java

echo Forging Native Executable...
C:\GraalVM\bin\native-image.cmd -O3 Main AeroCanvas

echo Moving to Root...
move AeroCanvas.exe ..\..

cd ..\..
echo Build Complete!
pause
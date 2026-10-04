[Setup]
AppName=DataDrain
AppVersion=1.0
AppPublisher=DataDrain
DefaultDirName={autopf}\DataDrain
DefaultGroupName=DataDrain
OutputDir=installer
OutputBaseFilename=DataDrain-Setup
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\DataDrain.exe
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"
Name: "startup"; Description: "Start DataDrain when Windows starts"; GroupDescription: "Startup:"; Flags: unchecked

[Files]
Source: "dist\DataDrain.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DataDrain"; Filename: "{app}\DataDrain.exe"
Name: "{group}\Uninstall DataDrain"; Filename: "{uninstallexe}"
Name: "{autodesktop}\DataDrain"; Filename: "{app}\DataDrain.exe"; Tasks: desktopicon
Name: "{userstartup}\DataDrain"; Filename: "{app}\DataDrain.exe"; Tasks: startup

[Run]
Filename: "{app}\DataDrain.exe"; Description: "Launch DataDrain"; Flags: nowait postinstall skipifsilent
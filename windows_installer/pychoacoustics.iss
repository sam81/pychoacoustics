; Script generated by the Inno Script Studio Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "pychoacoustics"
#define MyAppVersion "0.4.8"
#define MyAppPublisher "Samuele Carcagno"
#define MyAppURL "http://samcarcagno.altervista.org/pychoacoustics/pychoacoustics.html"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{04C26DCA-0F3A-477A-8A0E-FDAC18974A15}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
LicenseFile=Z:\media\ntfsShared\lin_home\auditory\code\pychoacoustics\windows_installer\pychoacoustics_for_win\pychoacoustics\COPYING.txt
InfoBeforeFile=Z:\media\ntfsShared\lin_home\auditory\code\pychoacoustics\windows_installer\pychoacoustics_for_win\pychoacoustics\README.md
OutputBaseFilename=pychoacoustics_{#MyAppVersion}-setup
Compression=lzma2/ultra64
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "hungarian"; MessagesFile: "compiler:Languages\Hungarian.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

;[Tasks]
;Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "Z:\media\ntfsShared\lin_home\auditory\code\pychoacoustics\windows_installer\pychoacoustics_for_win\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\python-3.4.3.amd64\pythonw.exe"; WorkingDir: "{userdocs}"; Parameters: """{app}\pychoacoustics\pychoacoustics.pyw"""; IconFilename: "{app}\pychoacoustics\icons\Machovka_Headphones.ico"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\python-3.4.3.amd64\pythonw.exe"; WorkingDir: "{userdocs}"; Parameters: """{app}\pychoacoustics\pychoacoustics.pyw"""; IconFilename: "{app}\pychoacoustics\icons\Machovka_Headphones.ico"
[Run]
Filename: "{app}\python-3.4.3.amd64\pythonw.exe"; Parameters: """{app}\pychoacoustics\pychoacoustics.pyw"""; WorkingDir: "{userdocs}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

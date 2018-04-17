; -- Example3.iss --
; Same as Example1.iss, but creates some registry entries too.

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=Licitador
AppVersion=1.0
DefaultDirName={pf}\Licitador
;DefaultGroupName=Licitador
UninstallDisplayIcon={app}\Licitador.exe
OutputDir=userdocs:Instalador
DisableProgramGroupPage=yes

[Files]
Source: "C:\Users\ldevo\Desktop\Licitador\dist\Licitador.exe"; DestDir: "{app}"
Source: "C:\Users\ldevo\Desktop\Licitador\dist\iconos\*"; DestDir: "{app}\iconos"
Source: "C:\Users\ldevo\Desktop\Licitador\dist\Licitaciones.db"; DestDir: "{app}"
Source: "C:\Users\ldevo\Desktop\Licitador\dist\splash_screen.png"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\Licitador"; Filename: "{app}\Licitador.exe"
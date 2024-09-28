!define VERSION "%(version)s"
!define APP_NAME "Deposit GUI"
!define ROOT_PATH "%(root_path)s"
!define INSTALLER_PATH "%(installer_path)s"
!define FILENAME "%(filename)s"

!include "MUI2.nsh"

; General
OutFile "${INSTALLER_PATH}\%(filename)s"
InstallDir "$PROGRAMFILES\${APP_NAME}"
Icon "${ROOT_PATH}\src\deposit_gui\res\deposit_icon.ico"
UninstallIcon "${ROOT_PATH}\src\deposit_gui\res\deposit_icon.ico"
VIProductVersion "${VERSION}"
Caption "${APP_NAME} Setup"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${ROOT_PATH}\src\deposit_gui\res\deposit_icon.ico"
!define MUI_UNICON "${ROOT_PATH}\src\deposit_gui\res\deposit_icon.ico"

; Customizing installer text to use APP_NAME
!define MUI_WELCOMEPAGE_TITLE "Welcome to the ${APP_NAME} Setup Wizard"
!define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of ${APP_NAME}. Click 'Next' to continue."
!define MUI_LICENSEPAGE_TEXT_TOP "Please review the license terms before installing ${APP_NAME}."
!define MUI_DIRECTORYPAGE_TEXT_TOP "Choose the folder in which to install ${APP_NAME}."
!define MUI_DIRECTORYPAGE_TEXT_DESTINATION "Setup will install ${APP_NAME} in the following folder. To install in a different folder, click Browse and select another folder. Click Install to start the installation."
!define MUI_INSTFILESPAGE_TEXT "Please wait while ${APP_NAME} is being installed."
!define MUI_FINISHPAGE_TITLE "Installation Complete"
!define MUI_FINISHPAGE_TEXT "${APP_NAME} has been installed on your computer. Click 'Finish' to exit the Setup Wizard."
!define MUI_UNCONFIRMPAGE_TEXT "Are you sure you want to completely remove ${APP_NAME} and all of its components?"
!define MUI_UNINSTFILESPAGE_TEXT "Please wait while ${APP_NAME} is being uninstalled."

!define MUI_WELCOMEFINISHPAGE_BITMAP "${ROOT_PATH}\installer_win\dep_installer.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "${ROOT_PATH}\installer_win\dep_icon.bmp"
!define MUI_HEADERIMAGE_BITMAP_NOSTRETCH

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${ROOT_PATH}\installer_win\license.rtf"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language files
!insertmacro MUI_LANGUAGE "English"

; Override default strings
LangString MUI_TEXT_WELCOME_TITLE ${LANG_ENGLISH} "Welcome to the ${APP_NAME} Setup Wizard"
LangString MUI_TEXT_WELCOME_SUBTITLE ${LANG_ENGLISH} "This wizard will guide you through the installation of ${APP_NAME}. Click 'Next' to continue."
LangString MUI_TEXT_LICENSE_TITLE ${LANG_ENGLISH} "License Agreement"
LangString MUI_TEXT_LICENSE_SUBTITLE ${LANG_ENGLISH} "Please review the license terms before installing ${APP_NAME}."
LangString MUI_TEXT_DIRECTORY_TITLE ${LANG_ENGLISH} "Choose Install Location"
LangString MUI_TEXT_DIRECTORY_SUBTITLE ${LANG_ENGLISH} "Choose the folder in which to install ${APP_NAME}."
LangString MUI_TEXT_INSTFILES_TITLE ${LANG_ENGLISH} "Installing"
LangString MUI_TEXT_INSTFILES_SUBTITLE ${LANG_ENGLISH} "Please wait while ${APP_NAME} is being installed."
LangString MUI_TEXT_FINISH_TITLE ${LANG_ENGLISH} "Installation Complete"
LangString MUI_TEXT_FINISH_SUBTITLE ${LANG_ENGLISH} "${APP_NAME} has been installed on your computer. Click 'Finish' to exit the Setup Wizard."
LangString MUI_TEXT_UNCONFIRM_TITLE ${LANG_ENGLISH} "Uninstall ${APP_NAME}"
LangString MUI_TEXT_UNCONFIRM_SUBTITLE ${LANG_ENGLISH} "Are you sure you want to completely remove ${APP_NAME} and all of its components?"
LangString MUI_TEXT_UNINSTFILES_TITLE ${LANG_ENGLISH} "Uninstalling"
LangString MUI_TEXT_UNINSTFILES_SUBTITLE ${LANG_ENGLISH} "Please wait while ${APP_NAME} is being uninstalled."

Section -PreInstall
  ; Remove all files and directories in the installation path
  ClearErrors
  RMDir /r "$INSTDIR"
  IfErrors nofiles
  nofiles:
SectionEnd

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "${ROOT_PATH}\dist\deposit_gui\*.*"

  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\deposit_gui.exe" "" "$INSTDIR\deposit_gui\res\deposit_icon.ico"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\deposit_gui.exe" "" "$INSTDIR\deposit_gui\res\deposit_icon.ico"

  ; Write uninstall information to registry
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "QuietUninstallString" "$INSTDIR\uninstall.exe /S"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\deposit_gui\res\deposit_icon.ico"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "Your Company Name"
  ; Set estimated size (optional but recommended)
  ; Include LogicLib.nsh and FileFunc.nsh for GetSize
  !include "LogicLib.nsh"
  !include "FileFunc.nsh"
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%%08X" $0
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "EstimatedSize" "$0"

  ; Write the uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  RMDir /r "$INSTDIR"

  ; Remove uninstall information from registry
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

  ; Remove shortcuts
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"
SectionEnd
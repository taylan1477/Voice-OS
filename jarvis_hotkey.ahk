#Requires AutoHotkey v2.0
#SingleInstance Force
Persistent

; ==============================================================================
; J.A.R.V.I.S. HOTKEY CONTROLLER (AutoHotkey v2)
; ==============================================================================
; Desteklenen Kısayollar:
; 1. Ctrl + Alt + F
; 2. Ctrl + A basılıyken F (Ctrl + A + F)
; ==============================================================================

A_IconTip := "Jarvis Voice OS Aktif (Ctrl+A+F veya Ctrl+Alt+F)"

TriggerJarvis() {
    try {
        whr := ComObject("WinHttp.WinHttpRequest.5.1")
        whr.Open("GET", "http://127.0.0.1:8765/listen", false)
        whr.Send()
        TrayTip "Jarvis Dinliyor...", "4 saniye konuşabilirsiniz...", "Iconi"
    } catch as err {
        TrayTip "Jarvis Uyanıyor...", "Sistem aktif değildi, Jarvis başlatılıyor. Konsol açıldıktan sonra tekrar deneyin.", "Iconi"
        ; Jarvis kapalıysa powershell üzerinden otomatik başlat (Çalışma dizinini Run komutuyla veriyoruz)
        Run "powershell.exe -NoExit -Command python main.py", "C:\Projeler\Voice-OS"
    }
}

; 1. Kısayol: Ctrl + Alt + F
^!f::
{
    TriggerJarvis()
}

; 2. Kısayol: Ctrl basılıyken A ve F'ye basmak (Ctrl + A + F)
#HotIf GetKeyState("Ctrl", "P")
a & f::
{
    TriggerJarvis()
}
#HotIf

; 3. Kısayol: Gamepad / Joystick Buton 9 (Örn: Xbox/Playstation Select/Share tuşu)
Joy9::
{
    TriggerJarvis()
}

TrayTip "Jarvis Aktif!", "Ctrl+A+F, Ctrl+Alt+F veya Gamepad Joy9 ile konuşabilirsiniz.", "Iconi"

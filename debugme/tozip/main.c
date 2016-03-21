#include "globals.h"

#include <windows.h>
#include "resource.h"
#include "debugfun.h"

HINSTANCE hInst;
char input[64];
extern int check(char *input);
BOOL THREADBEGIN = FALSE;


BOOL CALLBACK DialogProc(HWND hwndDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch(uMsg)
    {
        case WM_INITDIALOG:
            return TRUE;

        case WM_CLOSE:
            EndDialog(hwndDlg, 0);
            return TRUE;

        case WM_COMMAND:
            switch(LOWORD(wParam))
            {
                case IDC_BTN_QUIT:
                    EndDialog(hwndDlg, 0);
                    return TRUE;

                case IDC_BTN_CHECK:
                    GetDlgItemText(hwndDlg,IDC_INPUT, input,sizeof(input));
                    if( check(input) )
                        MessageBox(NULL,txttab[CONGRATZ], input,MB_OK);
                    else
                        MessageBox(NULL,txttab[FAIL], txttab[QUICHE], MB_ICONSTOP);
                    return TRUE;
                case IDM_QUID:
                    MessageBox(hwndDlg,txttab[W3CHALLS],txttab[ABOUT],MB_OK);
                    return TRUE;
                case IDM_EN:
                    txttab = en;
                    goto changelang;
                case IDM_FR:
                    txttab = fr;
                changelang:
                    SetDlgItemText(hwndDlg, IDC_BTN_QUIT, txttab[QUIT]);
                    SetDlgItemText(hwndDlg, IDC_BTN_CHECK, txttab[CHECK]);
                    return TRUE;

            }
    }
    __asm__ __volatile__(
        "int3;"
        ".byte 0;"
    );
    return FALSE;
}

DWORD WINAPI ThreadProc(LPVOID lpParameter)
{
    THREADBEGIN = TRUE;
    DWORD ret = DialogBox(hInst, MAKEINTRESOURCE(DLG_MAIN), NULL, DialogProc);
    return ret;
}


int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
    hInst = hInstance;
    int ppid = GetParentPID();
    if(HasSamePath(ppid))
    {
        DebugProcess(ppid);
        return 0;
    }

    else
    {
        STARTUPINFO startinfo={0};
        startinfo.cb = sizeof(STARTUPINFO);
		if(CreateProcess(NULL, GetCommandLine(), NULL, NULL, FALSE, 0, NULL, NULL, &startinfo, &procinfo))
		{
		    int cnt;
		    while(!THREADBEGIN)
                Sleep(100);
            while( (cnt=GetCurrentThreadCount())>1)
            {
                Sleep(500);
            }
		}
    }
    return 0;
}

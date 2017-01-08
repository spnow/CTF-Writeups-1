#include "globals.h"

#include <windows.h>
#include <stdio.h>
#include <tlhelp32.h>
#include <Psapi.h>



PROCESS_INFORMATION procinfo;

PROCESSENTRY32 *GetProcessEntry(int pid);
int GetParentPID();
int GetCurrentThreadCount();
int HasSamePath(int pid);
void DebugProcess(int pid);
BOOL FixCode(HANDLE hprocess, HANDLE hthread);

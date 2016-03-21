#include "globals.h"
#include "debugfun.h"

extern DWORD WINAPI ThreadProc(LPVOID lpParameter);
DEBUG_EVENT debugevent;


// stolen from
// http://stackoverflow.com/questions/3749668/
// don't forgt to free() the returned pointer
PROCESSENTRY32 * GetProcessEntry(const int pid)
{
    // get a process list snapshot.
    HANDLE const  snapshot = CreateToolhelp32Snapshot( TH32CS_SNAPPROCESS, 0 );

    // initialize the process entry structure.
    PROCESSENTRY32 *pentry = malloc(sizeof(PROCESSENTRY32));
    memset(pentry, 0,sizeof(PROCESSENTRY32));
    pentry->dwSize = sizeof( PROCESSENTRY32 );

    // get the first process info.
    BOOL  ret = TRUE;
    ret = Process32First( snapshot, pentry );
    while( ret && pentry->th32ProcessID != pid ) {
        ret = Process32Next( snapshot, pentry );
    }
    CloseHandle( snapshot );
    return pentry;
}


int GetParentPID()
{
    PROCESSENTRY32 *pentry = GetProcessEntry(GetCurrentProcessId());
    int ppid = pentry->th32ParentProcessID;
    free(pentry);
    return ppid;
}


int GetCurrentThreadCount()
{
    PROCESSENTRY32 * pentry = GetProcessEntry(GetCurrentProcessId());
    int cnt = pentry->cntThreads;
    free(pentry);
    return cnt;
}



int HasSamePath(int pid)
{
	char filename[MAX_PATH]={0};
	char parentfilename[MAX_PATH]={0};
	HANDLE hp = OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, FALSE, pid);

	if(hp==NULL)
	{
	    #if DEBUG
		fprintf(stderr,"[-] hp==NULL parpid = %i, pid = %li\n", pid, GetCurrentProcessId());
		#endif
		return FALSE;
	}
	if(GetModuleFileName(NULL, filename,MAX_PATH)
	& GetModuleFileNameEx(hp,NULL, parentfilename, MAX_PATH))
	{
        #if DEBUG
		printf("\ncurrent: %s\nparent: %s\n\n",filename,parentfilename);
		#endif
	}
	CloseHandle(hp);
	return (strcmp(parentfilename,filename)==0 ? TRUE : FALSE);
}



BOOL FixCode(HANDLE hprocess, HANDLE hthread)
{
    CONTEXT cont={0};
    cont.ContextFlags = CONTEXT_FULL;
    char nbjunk;
    if(!GetThreadContext(hthread, &cont))
    {
        #if DEBUG
        fprintf(stderr, "GetThreadContext failed: %lx\n", GetLastError());
        #endif
        return FALSE;
    }
    #if DEBUG
    fprintf(stderr, "EIP: %p\n", (void*)cont.Eip);
    #endif
    if(!ReadProcessMemory(hprocess, (void*)cont.Eip, &nbjunk, 1, NULL))
        return FALSE;
    #if DEBUG
    fprintf(stderr, "nbjunk: %i\n", (int)((nbjunk>>2)&7));
    #endif
    nbjunk =  (nbjunk>>2)&7;
    cont.Eip += nbjunk+1;
    cont.Eax = (cont.Eax<<1)|(cont.Eax>>31);
    if(!SetThreadContext(hthread, &cont))
        return FALSE;
    return TRUE;
}


void DebugProcess(int pid)
{
    #if DEBUG
    fprintf(stderr,"[+] Attempting to debug process #%i\n",pid);
    #endif
    HANDLE hprocess;
    if(!(hprocess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid)))
    {
        #if DEBUG
        fprintf(stderr,"[-] OpenProcess failed\n");
        #endif
        TerminateProcess(hprocess,1);
        CloseHandle(hprocess);
        return;
    }
    if(!DebugActiveProcess(pid))
    {
        #if DEBUG
        fprintf(stderr,"[-] DebugActiveProcess failed\n");
        #endif
        TerminateProcess(hprocess,1);
        CloseHandle(hprocess);
        return;
    }
    HANDLE hthread;
    DWORD threadid;
    hthread=CreateRemoteThread(hprocess,NULL,0,(LPTHREAD_START_ROUTINE)&ThreadProc, NULL,0,&threadid);
    if(!hthread)
    {
        #if DEBUG
        fprintf(stderr, "[-] CreateRemoteThread failed: %li\n", GetLastError());
        #endif
        TerminateProcess(hprocess,1);
        CloseHandle(hprocess);
        return;
    }

	while(1)
	{
	    #if DEBUG
	    fprintf(stderr, "WaitForDebugEvent\n");
		#endif
		WaitForDebugEvent(&debugevent, INFINITE);
        #if DEBUG
        fprintf(stderr, "code = %li\n", debugevent.dwDebugEventCode );
        #endif

		if(debugevent.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT)
		{
		    #if DEBUG
			fprintf(stderr,"Debug event: exit process\n");
			#endif
			ContinueDebugEvent(debugevent.dwProcessId, debugevent.dwThreadId, DBG_CONTINUE);
			break;
		}
		else if ( debugevent.dwThreadId==threadid &&
                debugevent.dwDebugEventCode == EXCEPTION_DEBUG_EVENT)
		{
		    unsigned int excode = debugevent.u.Exception.ExceptionRecord.ExceptionCode;
		    #if DEBUG
		    fprintf( stderr, "Exception %08x\nEip = %p\n", excode, debugevent.u.Exception.ExceptionRecord.ExceptionAddress);
		    #endif
		    if(excode==EXCEPTION_BREAKPOINT)
		    {
		        #if DEBUG
		        fprintf(stderr, "Debug event: breakpoint\n");
		        #endif
		        if(!FixCode(hprocess,hthread))
		        {
                    TerminateProcess(hprocess,1);
                    break;
		        }
                ContinueDebugEvent(debugevent.dwProcessId, debugevent.dwThreadId, DBG_CONTINUE);
		    }
            ContinueDebugEvent(debugevent.dwProcessId, debugevent.dwThreadId, DBG_EXCEPTION_NOT_HANDLED);
		}
        else
            ContinueDebugEvent(debugevent.dwProcessId, debugevent.dwThreadId, DBG_EXCEPTION_NOT_HANDLED);
	}
}

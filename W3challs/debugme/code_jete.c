//    #if DEBUG
//	fprintf(stderr, "\nDebugging Process (ID : %i)...\n\n", pid);
//	#endif
//    int thrid;
//
//    if((thrid = GetProcessThread(pid))<0)
//    {
//        #if DEBUG
//        fprintf(stderr, "GetProcessThread failed: %lx\n", GetLastError());
//        #endif
//        CloseHandle(hprocess);
//        return;
//    }
//
//    #if DEBUG
//    fprintf(stderr, "thread id: %i\n", thrid);
//    #endif
//
//    HANDLE hthread;
//    if(!(hthread = OpenThread(THREAD_GET_CONTEXT | THREAD_SET_CONTEXT, FALSE, thrid)))
//    {
//        #if DEBUG
//        fprintf(stderr, "OpenThread failed: %lx\n", GetLastError());
//        #endif
//        CloseHandle(hprocess);
//        return;
//    }


// http://stackoverflow.com/questions/3749668/how-to-query-the-thread-count-of-a-process-using-the-regular-windows-c-c-apis
int GetCurrentThreadCount()
{
    // first determine the id of the current process
    DWORD const  id = GetCurrentProcessId();

    // then get a process list snapshot.
    HANDLE const  snapshot = CreateToolhelp32Snapshot( TH32CS_SNAPALL, 0 );

    // initialize the process entry structure.
    PROCESSENTRY32 entry = { 0 };
    entry.dwSize = sizeof( entry );

    // get the first process info.
    BOOL  ret = true;
    ret = Process32First( snapshot, &entry );
    while( ret && entry.th32ProcessID != id ) {
        ret = Process32Next( snapshot, &entry );
    }
    CloseHandle( snapshot );
    return ret 
        ?   entry.cntThreads
        :   -1;
}

//int GetProcessThread(int pid)
//{
//    THREADENTRY32 threadentry = {0};
//    DWORD thrid=-1;
//    threadentry.dwSize = sizeof(THREADENTRY32);
//    HANDLE hthreadsnap = INVALID_HANDLE_VALUE;
//    hthreadsnap = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, pid);
//    if(hthreadsnap==INVALID_HANDLE_VALUE)
//    {
//        #if DEBUG
//        fprintf(stderr, "[-] CreateTollhelp32Snapshot failed\n");
//        #endif
//        return -1;
//    }
//    if(!Thread32First(hthreadsnap,&threadentry))
//    {
//        #if DEBUG
//        fprintf(stderr,"[-] Thread32First failed\n");
//        #endif
//        return -1;
//    }
//    while(threadentry.th32ThreadID<=0)
//    {
//        if(!Thread32Next(hthreadsnap,&threadentry))
//        {
//            #if DEBUG
//            fprintf(stderr,"[-] Thread32Next failed\n");
//            #endif
//            return -1;
//        }
//    }
//    thrid = threadentry.th32ThreadID;
//
//    CloseHandle(hthreadsnap);
//    return thrid;
//}

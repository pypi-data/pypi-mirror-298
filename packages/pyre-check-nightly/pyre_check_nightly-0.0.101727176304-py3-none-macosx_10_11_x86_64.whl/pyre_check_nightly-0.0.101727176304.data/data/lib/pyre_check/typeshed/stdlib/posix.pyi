import sys

if sys.platform != "win32":
    # Actually defined here, but defining in os allows sharing code with windows
    from os import (
        CLD_CONTINUED as CLD_CONTINUED,
        CLD_DUMPED as CLD_DUMPED,
        CLD_EXITED as CLD_EXITED,
        CLD_TRAPPED as CLD_TRAPPED,
        EX_CANTCREAT as EX_CANTCREAT,
        EX_CONFIG as EX_CONFIG,
        EX_DATAERR as EX_DATAERR,
        EX_IOERR as EX_IOERR,
        EX_NOHOST as EX_NOHOST,
        EX_NOINPUT as EX_NOINPUT,
        EX_NOPERM as EX_NOPERM,
        EX_NOUSER as EX_NOUSER,
        EX_OK as EX_OK,
        EX_OSERR as EX_OSERR,
        EX_OSFILE as EX_OSFILE,
        EX_PROTOCOL as EX_PROTOCOL,
        EX_SOFTWARE as EX_SOFTWARE,
        EX_TEMPFAIL as EX_TEMPFAIL,
        EX_UNAVAILABLE as EX_UNAVAILABLE,
        EX_USAGE as EX_USAGE,
        F_LOCK as F_LOCK,
        F_OK as F_OK,
        F_TEST as F_TEST,
        F_TLOCK as F_TLOCK,
        F_ULOCK as F_ULOCK,
        NGROUPS_MAX as NGROUPS_MAX,
        O_APPEND as O_APPEND,
        O_ASYNC as O_ASYNC,
        O_CREAT as O_CREAT,
        O_DIRECT as O_DIRECT,
        O_DIRECTORY as O_DIRECTORY,
        O_DSYNC as O_DSYNC,
        O_EXCL as O_EXCL,
        O_LARGEFILE as O_LARGEFILE,
        O_NDELAY as O_NDELAY,
        O_NOATIME as O_NOATIME,
        O_NOCTTY as O_NOCTTY,
        O_NOFOLLOW as O_NOFOLLOW,
        O_NONBLOCK as O_NONBLOCK,
        O_RDONLY as O_RDONLY,
        O_RDWR as O_RDWR,
        O_RSYNC as O_RSYNC,
        O_SYNC as O_SYNC,
        O_TRUNC as O_TRUNC,
        O_WRONLY as O_WRONLY,
        P_ALL as P_ALL,
        P_PGID as P_PGID,
        P_PID as P_PID,
        POSIX_SPAWN_CLOSE as POSIX_SPAWN_CLOSE,
        POSIX_SPAWN_DUP2 as POSIX_SPAWN_DUP2,
        POSIX_SPAWN_OPEN as POSIX_SPAWN_OPEN,
        PRIO_PGRP as PRIO_PGRP,
        PRIO_PROCESS as PRIO_PROCESS,
        PRIO_USER as PRIO_USER,
        R_OK as R_OK,
        RTLD_GLOBAL as RTLD_GLOBAL,
        RTLD_LAZY as RTLD_LAZY,
        RTLD_LOCAL as RTLD_LOCAL,
        RTLD_NODELETE as RTLD_NODELETE,
        RTLD_NOLOAD as RTLD_NOLOAD,
        RTLD_NOW as RTLD_NOW,
        SCHED_BATCH as SCHED_BATCH,
        SCHED_FIFO as SCHED_FIFO,
        SCHED_IDLE as SCHED_IDLE,
        SCHED_OTHER as SCHED_OTHER,
        SCHED_RESET_ON_FORK as SCHED_RESET_ON_FORK,
        SCHED_RR as SCHED_RR,
        SCHED_SPORADIC as SCHED_SPORADIC,
        SEEK_DATA as SEEK_DATA,
        SEEK_HOLE as SEEK_HOLE,
        ST_NOSUID as ST_NOSUID,
        ST_RDONLY as ST_RDONLY,
        TMP_MAX as TMP_MAX,
        W_OK as W_OK,
        WCONTINUED as WCONTINUED,
        WCOREDUMP as WCOREDUMP,
        WEXITED as WEXITED,
        WEXITSTATUS as WEXITSTATUS,
        WIFCONTINUED as WIFCONTINUED,
        WIFEXITED as WIFEXITED,
        WIFSIGNALED as WIFSIGNALED,
        WIFSTOPPED as WIFSTOPPED,
        WNOHANG as WNOHANG,
        WNOWAIT as WNOWAIT,
        WSTOPPED as WSTOPPED,
        WSTOPSIG as WSTOPSIG,
        WTERMSIG as WTERMSIG,
        WUNTRACED as WUNTRACED,
        X_OK as X_OK,
        DirEntry as DirEntry,
        _exit as _exit,
        abort as abort,
        access as access,
        chdir as chdir,
        chmod as chmod,
        chown as chown,
        chroot as chroot,
        close as close,
        closerange as closerange,
        confstr as confstr,
        confstr_names as confstr_names,
        cpu_count as cpu_count,
        ctermid as ctermid,
        device_encoding as device_encoding,
        dup as dup,
        dup2 as dup2,
        error as error,
        execv as execv,
        execve as execve,
        fchdir as fchdir,
        fchmod as fchmod,
        fchown as fchown,
        fork as fork,
        forkpty as forkpty,
        fpathconf as fpathconf,
        fspath as fspath,
        fstat as fstat,
        fstatvfs as fstatvfs,
        fsync as fsync,
        ftruncate as ftruncate,
        get_blocking as get_blocking,
        get_inheritable as get_inheritable,
        get_terminal_size as get_terminal_size,
        getcwd as getcwd,
        getcwdb as getcwdb,
        getegid as getegid,
        geteuid as geteuid,
        getgid as getgid,
        getgrouplist as getgrouplist,
        getgroups as getgroups,
        getloadavg as getloadavg,
        getlogin as getlogin,
        getpgid as getpgid,
        getpgrp as getpgrp,
        getpid as getpid,
        getppid as getppid,
        getpriority as getpriority,
        getsid as getsid,
        getuid as getuid,
        initgroups as initgroups,
        isatty as isatty,
        kill as kill,
        killpg as killpg,
        lchown as lchown,
        link as link,
        listdir as listdir,
        lockf as lockf,
        lseek as lseek,
        lstat as lstat,
        major as major,
        makedev as makedev,
        minor as minor,
        mkdir as mkdir,
        mkfifo as mkfifo,
        mknod as mknod,
        nice as nice,
        open as open,
        openpty as openpty,
        pathconf as pathconf,
        pathconf_names as pathconf_names,
        pipe as pipe,
        posix_spawn as posix_spawn,
        posix_spawnp as posix_spawnp,
        pread as pread,
        preadv as preadv,
        putenv as putenv,
        pwrite as pwrite,
        pwritev as pwritev,
        read as read,
        readlink as readlink,
        readv as readv,
        register_at_fork as register_at_fork,
        remove as remove,
        rename as rename,
        replace as replace,
        rmdir as rmdir,
        scandir as scandir,
        sched_get_priority_max as sched_get_priority_max,
        sched_get_priority_min as sched_get_priority_min,
        sched_param as sched_param,
        sched_yield as sched_yield,
        sendfile as sendfile,
        set_blocking as set_blocking,
        set_inheritable as set_inheritable,
        setegid as setegid,
        seteuid as seteuid,
        setgid as setgid,
        setgroups as setgroups,
        setpgid as setpgid,
        setpgrp as setpgrp,
        setpriority as setpriority,
        setregid as setregid,
        setreuid as setreuid,
        setsid as setsid,
        setuid as setuid,
        stat as stat,
        stat_result as stat_result,
        statvfs as statvfs,
        statvfs_result as statvfs_result,
        strerror as strerror,
        symlink as symlink,
        sync as sync,
        sysconf as sysconf,
        sysconf_names as sysconf_names,
        system as system,
        tcgetpgrp as tcgetpgrp,
        tcsetpgrp as tcsetpgrp,
        terminal_size as terminal_size,
        times as times,
        times_result as times_result,
        truncate as truncate,
        ttyname as ttyname,
        umask as umask,
        uname as uname,
        uname_result as uname_result,
        unlink as unlink,
        unsetenv as unsetenv,
        urandom as urandom,
        utime as utime,
        wait as wait,
        wait3 as wait3,
        wait4 as wait4,
        waitpid as waitpid,
        write as write,
        writev as writev,
    )

    if sys.version_info >= (3, 9):
        from os import CLD_KILLED as CLD_KILLED, CLD_STOPPED as CLD_STOPPED, waitstatus_to_exitcode as waitstatus_to_exitcode

    if sys.version_info >= (3, 11):
        from os import login_tty as login_tty

    if sys.platform != "linux":
        from os import chflags as chflags, lchflags as lchflags, lchmod as lchmod

    if sys.platform != "linux" and sys.platform != "darwin":
        from os import EX_NOTFOUND as EX_NOTFOUND

    if sys.platform != "darwin":
        from os import (
            POSIX_FADV_DONTNEED as POSIX_FADV_DONTNEED,
            POSIX_FADV_NOREUSE as POSIX_FADV_NOREUSE,
            POSIX_FADV_NORMAL as POSIX_FADV_NORMAL,
            POSIX_FADV_RANDOM as POSIX_FADV_RANDOM,
            POSIX_FADV_SEQUENTIAL as POSIX_FADV_SEQUENTIAL,
            POSIX_FADV_WILLNEED as POSIX_FADV_WILLNEED,
            RWF_DSYNC as RWF_DSYNC,
            RWF_HIPRI as RWF_HIPRI,
            RWF_NOWAIT as RWF_NOWAIT,
            RWF_SYNC as RWF_SYNC,
            fdatasync as fdatasync,
            getresgid as getresgid,
            getresuid as getresuid,
            pipe2 as pipe2,
            posix_fadvise as posix_fadvise,
            posix_fallocate as posix_fallocate,
            sched_getaffinity as sched_getaffinity,
            sched_getparam as sched_getparam,
            sched_getscheduler as sched_getscheduler,
            sched_rr_get_interval as sched_rr_get_interval,
            sched_setaffinity as sched_setaffinity,
            sched_setparam as sched_setparam,
            sched_setscheduler as sched_setscheduler,
            setresgid as setresgid,
            setresuid as setresuid,
            waitid as waitid,
            waitid_result as waitid_result,
        )

        if sys.version_info >= (3, 10):
            from os import RWF_APPEND as RWF_APPEND

    if sys.platform == "linux":
        from os import (
            GRND_NONBLOCK as GRND_NONBLOCK,
            GRND_RANDOM as GRND_RANDOM,
            MFD_ALLOW_SEALING as MFD_ALLOW_SEALING,
            MFD_CLOEXEC as MFD_CLOEXEC,
            MFD_HUGE_1GB as MFD_HUGE_1GB,
            MFD_HUGE_1MB as MFD_HUGE_1MB,
            MFD_HUGE_2GB as MFD_HUGE_2GB,
            MFD_HUGE_2MB as MFD_HUGE_2MB,
            MFD_HUGE_8MB as MFD_HUGE_8MB,
            MFD_HUGE_16GB as MFD_HUGE_16GB,
            MFD_HUGE_16MB as MFD_HUGE_16MB,
            MFD_HUGE_32MB as MFD_HUGE_32MB,
            MFD_HUGE_64KB as MFD_HUGE_64KB,
            MFD_HUGE_256MB as MFD_HUGE_256MB,
            MFD_HUGE_512KB as MFD_HUGE_512KB,
            MFD_HUGE_512MB as MFD_HUGE_512MB,
            MFD_HUGE_MASK as MFD_HUGE_MASK,
            MFD_HUGE_SHIFT as MFD_HUGE_SHIFT,
            MFD_HUGETLB as MFD_HUGETLB,
            RTLD_DEEPBIND as RTLD_DEEPBIND,
            XATTR_CREATE as XATTR_CREATE,
            XATTR_REPLACE as XATTR_REPLACE,
            XATTR_SIZE_MAX as XATTR_SIZE_MAX,
            copy_file_range as copy_file_range,
            getrandom as getrandom,
            getxattr as getxattr,
            listxattr as listxattr,
            memfd_create as memfd_create,
            removexattr as removexattr,
            setxattr as setxattr,
        )

        if sys.version_info >= (3, 9):
            from os import P_PIDFD as P_PIDFD, pidfd_open as pidfd_open

        if sys.version_info >= (3, 10):
            from os import (
                EFD_CLOEXEC as EFD_CLOEXEC,
                EFD_NONBLOCK as EFD_NONBLOCK,
                EFD_SEMAPHORE as EFD_SEMAPHORE,
                SPLICE_F_MORE as SPLICE_F_MORE,
                SPLICE_F_MOVE as SPLICE_F_MOVE,
                SPLICE_F_NONBLOCK as SPLICE_F_NONBLOCK,
                eventfd as eventfd,
                eventfd_read as eventfd_read,
                eventfd_write as eventfd_write,
                splice as splice,
            )

        if sys.version_info >= (3, 12):
            from os import (
                CLONE_FILES as CLONE_FILES,
                CLONE_FS as CLONE_FS,
                CLONE_NEWCGROUP as CLONE_NEWCGROUP,
                CLONE_NEWIPC as CLONE_NEWIPC,
                CLONE_NEWNET as CLONE_NEWNET,
                CLONE_NEWNS as CLONE_NEWNS,
                CLONE_NEWPID as CLONE_NEWPID,
                CLONE_NEWTIME as CLONE_NEWTIME,
                CLONE_NEWUSER as CLONE_NEWUSER,
                CLONE_NEWUTS as CLONE_NEWUTS,
                CLONE_SIGHAND as CLONE_SIGHAND,
                CLONE_SYSVSEM as CLONE_SYSVSEM,
                CLONE_THREAD as CLONE_THREAD,
                CLONE_VM as CLONE_VM,
                setns as setns,
                unshare as unshare,
            )

    if sys.platform == "darwin":
        if sys.version_info >= (3, 12):
            from os import (
                PRIO_DARWIN_BG as PRIO_DARWIN_BG,
                PRIO_DARWIN_NONUI as PRIO_DARWIN_NONUI,
                PRIO_DARWIN_PROCESS as PRIO_DARWIN_PROCESS,
                PRIO_DARWIN_THREAD as PRIO_DARWIN_THREAD,
            )

    # Not same as os.environ or os.environb
    # Because of this variable, we can't do "from posix import *" in os/__init__.pyi
    environ: dict[bytes, bytes]

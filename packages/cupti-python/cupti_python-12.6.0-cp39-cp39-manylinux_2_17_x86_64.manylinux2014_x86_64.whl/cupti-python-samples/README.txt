# README for CUPTI Python Samples

The CuptiVectorAdd* samples have a simple code which does element by element vector addition.

CuptiVectorAddNumba.py
    CUPTI Python sample which shows use of CUPTI Activity APIs.
    This sample uses CUDA Python with Numba.

    Command line options:
        --profile, -p                       Enable CUPTI based profiling
            Default: OFF

        --output, -o {brief|detailed|none}  Select the profiler output format
            Default: brief

        --help,-h                           Show the usage
    

CuptiVectorAddNumbaCallback.py
    CUPTI Python sample which shows use of CUPTI Callback APIs.
    This sample uses CUDA Python with Numba.

    Command line options:
        --profile, -p                       Enable CUPTI based profiling
            Default: OFF

        --output, -o {brief|detailed|none}  Select the profiler output format
            Default: brief

        --help, -h                          Show the usage
    
CuptiVectorAddDrv.py
    CUPTI Python sample which shows use of CUPTI Activity APIs.
    This sample uses CUDA Python Driver APIs. 
    It also shows how to use CUDA profiler start and stop APIs to define the range of code
    to be profiled.

    Command line options:
        --profile, -p                       Enable CUPTI based profiling
            Default: OFF

        --define-profile-range, -r          Include CUDA profiler start and stop APIs to define the range of code
                                            to be profiled. 
            Default: OFF

        --output, -o {brief|detailed|none}  Select the profiler output format
            Default: brief

        --help, -h                          Show the usage

cupyprof.py
    CUPTI Python sample which shows how to profile a CUDA Python application
    using the CUPTI Python APIs without having to modify the CUDA Python application code.
    This sample shows use of CUPTI Activity APIs and Callback APIs. 
    It also shows how to profile a range of code for a CUDA Python application which uses CUDA profiler start and stop APIs.

    usage: cupyprof.py [-h] [-p {from_start|range}] [-a <activities>] [-o {brief|detailed|none}] [-v] python_file_path [args]

    Command line options:
        --help, -h                          Show the usage

        --profile, -p {from_start|range}
            Enable profiling for entire CUDA python program, or only for the subset between cuProfilerStart and cuProfilerStop
            Default: from_start

        --activity, -a <comma separated list of activities>
            e.g., "kernel,memcpy"
            Use "--help" to view the list of supported activities. To know which activities are enabled by default, see "default_activity_choices" in  cupyprof.py.

        --output, -o {brief|detailed|none}
            Output options: brief, detailed, none.
            Default: brief

        python_file_path      Path to the CUDA Python application

        args                  Any arguments for the Python application


Examples of running samples

1) Run the sample without profiling

$ python3 CuptiVectorAddNumba.py


2) Run the sample with profiling enabled and use default output

$ python3 CuptiVectorAddNumba.py --profile

profiling_enabled:  True
prof_output:  ProfOutput.BRIEF
vector_length:  1048576
threads_per_block:  128
blocks_per_grid:  8192
Activity Kind                  Start                Duration             correlationId        Name
DRIVER                         1714136661470990409  1834876              1                    cuCtxGetCurrent
DRIVER                         1714136661472854473  213                  2                    cuDeviceGetCount
DRIVER                         1714136661472869777  87                   3                    cuDeviceGet
DRIVER                         1714136661472880942  566                  4                    cuDeviceGetAttribute
DRIVER                         1714136661472883507  69                   5                    cuDeviceGetAttribute
DRIVER                         1714136661472906825  3702                 6                    cuDeviceGetName
DRIVER                         1714136661472969577  87                   7                    cuDeviceGetUuid_v2
DRIVER                         1714136661472991812  140587104            8                    cuDevicePrimaryCtxRetain
.
.
.
DRIVER                         1714136661714686225  218                  88                   cuCtxGetCurrent
DRIVER                         1714136661714688211  55                   89                   cuCtxGetDevice
DRIVER                         1714136661714702981  2080                 90                   cuCtxSynchronize
verify_result: PASS


3) Use the cupyprof.py sample to profile a CUDA Python application with profiling range defined and with 'detailed' output

$ python3 cupyprof.py --profile range --output detailed ./CuptiVectorAddDrv.py --define-profile-range
profiling_enabled: False
prof_output: ProfOutput.BRIEF
profile_range: True
vector_length: 1048576
threads_per_block: 128
blocks_per_grid: 8192
MEMCPY "HTOD" [ 1726060107808115285, 1726060107808868469 ] duration 753184, size 4194304, src_kind 1, dst_kind 3, correlation_id 2
        device_id 0, context_id 1, stream_id 13, graph_id 0, graph_node_id 0, channel_id 10, channel_type ASYNC_MEMCPY

OVERHEAD ACTIVITY_BUFFER_REQUEST [1726060107808700601 , 1726060107812384673 ] duration 3684072, THREAD, id 1665656640, correlation id 2
.
.
.
OVERHEAD CUPTI_BUFFER_FLUSH [1726060107814713522 , 1726060107814808283 ] duration 94761, THREAD, id 1025836800, correlation id 0

OVERHEAD CUPTI_BUFFER_FLUSH [1726060107814877891 , 1726060107814890952 ] duration 13061, THREAD, id 1025836800, correlation id 0

verify_result: PASS

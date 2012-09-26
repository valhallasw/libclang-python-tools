libclang-based globals describer
================================

This is a simple python script to get a list of globals from a c/c++ file with the locations they are being used. Due to limitations in libclang, it doesn't show whether it's used in an assignment or not.


Example
-------
This example is included as [test.cpp](test.cpp).

```c++
int i;
int k;

int a() {
    i = 5;
}

int b() {
    int j = i;
    k=i;
}
```

results in:

```
$ python test.py
i at <SourceLocation file 'test.cpp', line 1, column 5>
 >  test.cpp:    5, in a(): i = 5;
 >  test.cpp:    9, in b(): int j = i;
 >  test.cpp:   10, in b(): k=i;
----------------------------------------

k at <SourceLocation file 'test.cpp', line 2, column 5>
 >  test.cpp:   10, in b(): k=i;
----------------------------------------
```

Requirements
------------
libclang and its python bindings. 

Do-this-and-then-it-should-run
------------------------------
On Ubuntu 12.04 x64, at least. This will use clang release 31.

```bash
    git clone https://github.com/valhallasw/libclang-python-tools.git
    cd libclang-python-tools
    svn co http://llvm.org/svn/llvm-project/cfe/branches/release_31/bindings/python/clang/
    curl http://llvm.org/releases/3.1/clang+llvm-3.1-x86_64-linux-ubuntu_12.04.tar.gz | tar -xvz
    LD_LIBRARY_PATH=$(clang+llvm-3.1-x86_64-linux-ubuntu_12.04/bin/llvm-config --libdir) python globals.py
```

On a different platform, select the relevant [clang binaries](http://llvm.org/releases/download.html), and select the python bindings that belong to that release (check the [branches in the svn repository](http://llvm.org/svn/llvm-project/cfe/branches/)).






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
libclang and its python bindings. In my case, I downloaded the [clang binaries](http://llvm.org/releases/download.html), and retrieved the python bindings from the [svn repository](http://llvm.org/svn/llvm-project/cfe/trunk/bindings/python).

In the python bindings, I had to adapt

    def get_cindex_library()

in clang/cindex.py to refer to the correct libclang.so; I extracted the clang binaries in a subdirectory of the python bindings, and used the following:

```python
    import os
    dll = os.path.join(os.path.split(__file__)[0], "clang_package", "lib", "libclang.so")
    return cdll.LoadLibrary(dll)
```

If your operating system has a working libclang.so, you should be able to use the python bindings without downloading the binaries & without adapting the dll path.



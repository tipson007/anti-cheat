for %ext% in (*.cpg, *.cpp, *.dylib) do (
    dir /S /B C:\%ext% | ForEach-Object {
        type $_
        echo.
    }
)

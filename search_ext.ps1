$extensions = "*.cpg", "*.cpp", "*.dylib"

foreach ($ext in $extensions) {
    Get-ChildItem -Path C:\ -Filter $ext -Recurse -File | ForEach-Object {
        Write-Output "Content of $($_.FullName):"
        try {
            Get-Content -Path $_.FullName -Raw
        } catch {
            Write-Output "Could not read file content of $($_.FullName): $_"
        }
        Write-Output ""
    }
}

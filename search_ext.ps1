
$searchDir = "C:\"

$fileExtensions = "*.cpg", "*.cpp", "*.dylib"

foreach ($ext in $fileExtensions) {
    $files = Get-ChildItem -Path $searchDir -Recurse -Filter $ext -ErrorAction SilentlyContinue
    if ($files) {
        foreach ($file in $files) {
            Write-Output "File found: $($file.FullName)"
            Write-Output "----------------"
            try {
                Get-Content -Path $file.FullName -ErrorAction Stop
            } catch {
                Write-Output "Could not read file content: $_"
            }
            Write-Output ""
        }
    }
}

Write-Output "Search completed. Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

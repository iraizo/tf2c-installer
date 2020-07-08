

function install_pip {
    Write-Host "Installing pip"
    $setuptools_url = "https://bootstrap.pypa.io/get-pip.py"
    $get_pip = '' + $save_dir + "\get_pip.py"
    Invoke-WebRequest $setuptools_url -OutFile $get_pip
    python $get_pip
}

function install_dependencies {
    Write-Host "Installing dependencies"
    $dependencies = @("requests", "tqdm","patool","pyunpack","psutil")
    for($i=0; $i -lt $dependencies.length; $i++) {
        pip install $dependencies[$i]
    }
}

function run_script {
    python ".\main.py"
}

function install_python {
    New-Item -ItemType Directory -Force -Path C:/tmp
        
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $output
    
    
    & $output /passive InstallAllUsers=1 PrependPath=1 Include_test=0 
}
   
   
   
   $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        # run evelated

        $url = "https://www.python.org/ftp/python/3.7.6/python-3.7.6-amd64.exe"
        $output = "C:/tmp/python-3.7.6-amd64.exe"
        $save_dir=Resolve-Path ~/Downloads
        
        if (Test-Path $output) {
            Write-Host "Python installed - skipping installation"
            install_pip
            install_dependencies
        } else {
            Write-Host "Installing python, restart the script after installation"
            install_python
        }

        run_script
    
        
    }

    # elevate powershell process
    else {
        Start-Process -FilePath "powershell" -ArgumentList "$('-File ""')$(Get-Location)$('\')$($MyInvocation.MyCommand.Name)$('""')" -Verb runAs
    }
        

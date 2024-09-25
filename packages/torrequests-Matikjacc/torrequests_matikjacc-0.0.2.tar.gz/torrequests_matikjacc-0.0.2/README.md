# Tor Requests

```
pip install torrequests-Matikjacc
```

## Installation

### 1. Firstly find your torrc file. You can find torrc in

```
Tor Browser\Browser\TorBrowser\Data\Tor
```

### 2. Torrc configuration

You need to hash your password using

```ps1
tor --hash-password "Your_password"
```

If it says you don't have tor on Windows download using chocolatey

```ps1
choco install tor 
```

Then add this to 


```
ControlPort 9051
HashedControlPassword 16:yourpassword
CookieAuthentication 1
```

### 3. Then go to Powershell and execute this command

```ps1
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

### 4. Go to Powershell and execute this command:

```ps1
PS C:\Windows\System32\WindowsPowerShell\v1.0> $profile.AllUsersAllHosts
C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1
```

### 5. If the file profile.ps1 was not created previously create it and add following code in it:

Create a directory MyPowershellScripts or something like that

```ps1
. C:\MyPowershellScripts\Start-Tor.ps1
```

### 6. In directory that you created for shell scripts create file Start-Tor.ps1 and give it a content like this

```ps1
function Start-Tor {

    # Configuration
    $torBrowser     = "D:\Tor Browser"       # Put address of root folder of Tor Browser here
    $TOR_Password   = ";Zq!v6oK[?03K!-Gp>4t"     # Input Tor network password here
    $TOR_HOST       = "127.0.0.1"            # Host of local Tor network
    $TOR_PORT       = 9150                   # The port number where Tor runs
    $CTRL_PORT      = 9151                   # The controller port number of Tor

    # Do not modify these
    $tor_location   = "$torBrowser\Browser\TorBrowser\Tor"
    $torrc_defaults = "$torBrowser\Browser\TorBrowser\Data\Tor\torrc-defaults"
    $torrc          = "$torBrowser\Browser\TorBrowser\Data\Tor\torrc"
    $tordata        = "$torBrowser\Browser\TorBrowser\Data\Tor"
    $geoIP          = "$torBrowser\Browser\TorBrowser\Data\Tor\geoip"
    $geoIPv6        = "$torBrowser\Browser\TorBrowser\Data\Tor\geoip6"
    $torExe         = "$tor_location\tor.exe"
    $controllerProcess = $PID
    function Get-OneToLastItem { param ($arr) return $arr[$arr.Length - 2]}

    Write-Host "Generating hash for your Tor password..."
    $TOR_HashPass_RAW  = & "$torExe" --hash-password $TOR_Password | more
    $Tor_HashPass      = Get-OneToLastItem($TOR_HashPass_RAW)

    $TOR_VERSION_RAW   = & "$torExe" --version | more
    $Tor_Version       = Get-OneToLastItem($TOR_VERSION_RAW)

    Write-Host "Running $Tor_Version" -ForegroundColor DarkGray
    Write-Host "Press [Ctrl+C] to stop Tor service."
    & "$torExe" --defaults-torrc $torrc_defaults -f $torrc DataDirectory $tordata GeoIPFile $geoIP GeoIPv6File $geoIPv6 HashedControlPassword $Tor_HashPass +__ControlPort $CTRL_PORT +__SocksPort "${TOR_HOST}:$TOR_PORT IPv6Traffic PreferIPv6 KeepAliveIsolateSOCKSAuth" __OwningControllerProcess $controllerProcess | more
    
}
```

### 7. To verify open new powershell and type

```ps1
Start-Tor
```

#### You should see the following:

```ps1
Generating hash for your Tor password...
Running Tor compiled with clang version 16.0.4
Press [Ctrl+C] to stop Tor service.
```

### 8. Update .env

#### Update .env with your tor password

# After running Start-Tor you can start the script


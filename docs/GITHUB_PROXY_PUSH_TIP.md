# GitHub Push Proxy Tip

This note records a small Windows troubleshooting pattern for GitHub push failures.

## Symptom

`git push origin main` may fail with an HTTPS connection error:

```text
fatal: unable to access 'https://github.com/...':
Failed to connect to github.com port 443
```

This does not always mean the repository, branch, token, or commit is wrong. It can simply mean Git is trying to connect to GitHub directly while the local network requires a proxy.

## Quick Diagnosis

Check whether DNS and TCP 443 behave differently:

```powershell
Resolve-DnsName github.com
Test-NetConnection github.com -Port 443
```

If DNS resolves but `TcpTestSucceeded` is `False`, direct HTTPS access is blocked or unstable.

Then check whether a local proxy is listening:

```powershell
$ports = 7890,7891,7897,1080,10808,10809,8080
Get-NetTCPConnection -State Listen |
  Where-Object { $ports -contains $_.LocalPort } |
  Select-Object LocalAddress,LocalPort,OwningProcess
```

Test the candidate proxy:

```powershell
curl.exe -I --max-time 20 -x http://127.0.0.1:7897 https://github.com
```

If this returns `HTTP/1.1 200 OK`, GitHub can be reached through the proxy.

## One-Time Push Through Local Proxy

Use temporary Git config for one command:

```powershell
git `
  -c http.proxy=http://127.0.0.1:7897 `
  -c https.proxy=http://127.0.0.1:7897 `
  push origin main
```

This avoids changing global Git configuration.

## Verify Remote State

After pushing, compare local `HEAD` and remote `main`:

```powershell
git rev-parse HEAD

git `
  -c http.proxy=http://127.0.0.1:7897 `
  -c https.proxy=http://127.0.0.1:7897 `
  ls-remote origin refs/heads/main
```

The two commit hashes should match.

## Notes

- Replace `7897` with the actual local proxy port on your machine.
- Do not commit secrets, tokens, proxy credentials, or private network details.
- Prefer one-time `git -c ...` options for troubleshooting instead of writing global proxy config.
- If Git reports an authentication error, solve authentication separately. Proxy access only fixes network connectivity.


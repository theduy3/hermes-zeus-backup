# Paperclip remote access and port forwarding

Use this when Paperclip is healthy on the server at `127.0.0.1:3100` but the user cannot open it from their laptop/VPN.

## Key distinction

`127.0.0.1` always means the machine where the browser/command runs.

- On the VPS/container: `http://127.0.0.1:3100` reaches Paperclip.
- On the user's Mac: `http://127.0.0.1:3100` reaches the Mac, not the VPS, so it may show `ERR_CONNECTION_REFUSED`.

## Preferred access path: SSH local port forward

Tell the user to run this on their laptop, keeping the SSH session open:

```bash
ssh -L 3100:127.0.0.1:3100 <ssh-user>@<server-ip>
```

Then open locally:

```text
http://127.0.0.1:3100
```

If local port 3100 is occupied:

```bash
ssh -L 3101:127.0.0.1:3100 <ssh-user>@<server-ip>
```

Then open:

```text
http://127.0.0.1:3101
```

## SSH auth pitfall in containerized Hermes

If Hermes is running inside a container, adding a key to `/home/hermes/.ssh/authorized_keys` may only affect the container user, not the VPS host's SSH daemon. If `ssh hermes@<server-ip>` still prompts for a password or says `Permission denied (publickey,password)`, the SSH login is controlled by the host, not the container.

Do not keep asking the user to retry the same SSH command. Use one of these paths:

1. Try the actual host login user if known, such as `ubuntu@<server-ip>`.
2. Ask the user/provider to install the public key on the host account that owns SSH.
3. If appropriate for a temporary trusted session, expose Paperclip through a narrow TCP proxy or reverse tunnel.

## Temporary direct proxy pattern

Only use this for a trusted/private environment and after considering security. Paperclip may be in `local_trusted` mode; exposing it on a public IP can expose operational control.

A minimal TCP forwarder can bind `<server-public-ip>:3100` and forward to `127.0.0.1:3100`, then the user opens:

```text
http://<server-public-ip>:3100
```

Verify connectivity from the server before telling the user:

```bash
python3 - <<'PY'
import socket
for host in ['127.0.0.1', '<server-public-ip>']:
    s = socket.socket(); s.settimeout(2)
    try:
        s.connect((host, 3100)); print(host, 'connect OK')
    except Exception as e:
        print(host, 'connect FAIL', repr(e))
    finally:
        s.close()
PY
```

## User-facing troubleshooting style

For this user, keep it terse:

- Say why `127.0.0.1` failed in one line.
- Give the exact command to run on the Mac.
- If SSH auth fails, explain container-vs-host auth briefly and switch paths.
- Avoid long networking explanations unless asked.

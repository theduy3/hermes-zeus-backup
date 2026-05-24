# Remote access to local Paperclip on VPS/container

Use this when Paperclip is healthy at `127.0.0.1:3100` from Hermes but the user cannot open it from their local machine.

## Core distinction

- `127.0.0.1` is always relative to the machine/browser making the request.
- If the user opens `http://127.0.0.1:3100` on a Mac, it targets the Mac, not the VPS and not the Hermes container.
- Paperclip commonly binds to loopback inside the runtime/container for safety.

## Preferred access pattern

Use SSH local port forwarding from the user's machine to the VPS host:

```bash
ssh -L 3100:127.0.0.1:3100 <host-user>@<vps-ip>
```

Then open locally:

```text
http://127.0.0.1:3100
```

If local port 3100 is busy:

```bash
ssh -L 3101:127.0.0.1:3100 <host-user>@<vps-ip>
```

Then open `http://127.0.0.1:3101`.

## Important VPS/container pitfall

Hermes may be running inside Docker/container while SSH lands on the VPS host. In that case:

- adding an SSH key to `/home/hermes/.ssh/authorized_keys` inside the container does not enable SSH login to `hermes@<vps-ip>` on the host;
- the host may not even have a `hermes` user (`chown: invalid user: 'hermes:hermes'`);
- the correct SSH account may be `root`, `ubuntu`, or another provider-created host user.

When the user has VPS console/root access and wants `hermes@host` login, create the host user first:

```bash
adduser hermes
mkdir -p /home/hermes/.ssh
echo '<user-public-key>' > /home/hermes/.ssh/authorized_keys
chown -R hermes:hermes /home/hermes/.ssh
chmod 700 /home/hermes/.ssh
chmod 600 /home/hermes/.ssh/authorized_keys
```

Then test from the user machine:

```bash
ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes -L 3100:127.0.0.1:3100 hermes@<vps-ip>
```

If using the existing host root account instead:

```bash
ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes -L 3100:127.0.0.1:3100 root@<vps-ip>
```

## If direct public port is attempted

A proxy bound to `<vps-ip>:3100` from inside the container may be reachable from the container itself but still fail from the user's Mac because provider firewall/security groups, Docker networking, or host firewall block inbound traffic. Do not rely on public exposure as the first fix. Prefer SSH tunneling.

## Debug commands for the user machine

```bash
curl http://127.0.0.1:3100/api/health
ssh -vvv -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes <host-user>@<vps-ip>
```

Look for:

```text
Offering public key: ...
Server accepts key
```

## Reporting style

Keep the guidance terse and command-first. Explicitly say whether commands run on:

- the user's Mac;
- the VPS host/provider console;
- the Hermes container.

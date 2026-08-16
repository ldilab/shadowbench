1) Backend unit: /etc/systemd/system/shadowbench-backend.service
[Unit]
Description=ShadowBench Leaderboard Backend (Uvicorn)
After=network.target

[Service]
Type=simple

# CHANGE THIS to your Linux username
User=user
Group=user

WorkingDirectory=non_agentic/shadowbench-leaderboard

# Use the venv's uvicorn directly (no "source" needed)
ExecStart=.venv/bin/uvicorn backend.app:app --host 0.0.0.0 --port 8200

Restart=on-failure
RestartSec=2

# Good defaults
KillSignal=SIGINT
TimeoutStopSec=30

# If you need environment vars, add lines like:
# Environment="ENV=prod"
# Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target

2) Frontend unit: /etc/systemd/system/shadowbench-frontend.service
[Unit]
Description=ShadowBench Leaderboard Frontend (python http.server)
After=network.target

[Service]
Type=simple

# CHANGE THIS to your Linux username
User=user
Group=user

WorkingDirectory=non_agentic/shadowbench-leaderboard/frontend

ExecStart=/usr/bin/python3 -m http.server 8100 --bind 0.0.0.0

Restart=on-failure
RestartSec=2

KillSignal=SIGINT
TimeoutStopSec=15

[Install]
WantedBy=multi-user.target

3) Install + start

Edit both files and replace YOUR_USERNAME with your actual username.

Reload systemd and start:

sudo systemctl daemon-reload
sudo systemctl enable --now shadowbench-backend.service
sudo systemctl enable --now shadowbench-frontend.service


sudo systemctl start shadowbench-backend.service \
sudo systemctl start shadowbench-frontend.service

4) Check status + logs
systemctl status shadowbench-backend.service
systemctl status shadowbench-frontend.service


Logs (live):

journalctl -u shadowbench-backend.service -f
journalctl -u shadowbench-frontend.service -f

5) Common gotchas

Permissions: systemd won’t expand ~ in paths, so use explicit deployment paths.

Venv: no need to source activate; call the venv binary directly (.../bin/uvicorn).

Ports: 8000/8100 are non-privileged, so running as your user is fine.

Firewall / cloud security group: open inbound TCP 8000/8100 if you need external access.

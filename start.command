#!/bin/bash
cd "$(dirname "$0")"
echo "Starting local server for Stanzza Design and dsgn interior..."
python3 server.py &
SERVER_PID=$!
sleep 1
open "http://localhost:8080"
echo "Servers running:"
echo "  • Stanzza Design : http://localhost:8002/"
echo "  • dsgn interior  : http://localhost:8004/"
echo "  • Launchpad Hub  : http://localhost:8080/"
echo "Press Ctrl+C to stop."
wait $SERVER_PID

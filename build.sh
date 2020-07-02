#!/bin/bash
conan source . -sf src 
conan install . -if build --build missing
conan build . -bf build -sf src
conan export-pkg . OpenVDBPointsUnity/0.0.1@rcldsl/stable -s build_type=Release -sf src -bf build --force

#!/bin/bash
gunicorn password_manager_latest.wsgi:application --reload --bind 0.0.0.0:6989
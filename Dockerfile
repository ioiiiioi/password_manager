# Gunakan base image Python 3.13 slim-bookworm
FROM python:3.13-slim-bookworm

# Set working directory di dalam container
WORKDIR /app

# Nonaktifkan buffering output Python agar log langsung terlihat
ENV PYTHONUNBUFFERED 1

# Instal UV (manajer paket)
RUN pip install uv

# Salin file persyaratan ke working directory dan instal dependensi
# Gunakan --system untuk menginstal ke lingkungan sistem Python
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-deps .

# Salin seluruh kode aplikasi ke working directory
COPY . /app

RUN uv run manage.py migrate --noinput

# Expose port yang digunakan Daphne
EXPOSE 8000

# Perintah default untuk menjalankan Daphne
# Ini bisa ditimpa oleh docker-compose.yml
CMD ["uv", "run", "gunicorn", "-b", "0.0.0.0", "-p", "6989", "core.wsgi:application"]
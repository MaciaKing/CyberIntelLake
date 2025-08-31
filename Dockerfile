FROM bitnami/spark:3.5.0

USER root

# Directorio de trabajo
WORKDIR /app

# Copiar todo (opcional)
COPY . .

# Instalar Python y cron
RUN apt-get update && apt-get install -y python3-pip cron && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Volver a usuario default de Bitnami
#USER 1001

# Mantener contenedor activo
CMD [".docker_init/start.sh"]

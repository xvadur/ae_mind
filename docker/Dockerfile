# AETH: Base image for AE Mind parser
FROM python:3.11-slim
WORKDIR /ae_mind
# AETH: copy all project files into the container
COPY . /ae_mind
# AETH: install required packages once during build
RUN pip install --no-cache-dir -r requirements.txt

# AETH: execute the pipeline by default
ENTRYPOINT ["python", "-m", "ae_mind.src.introspective_parser.run_pipeline"]

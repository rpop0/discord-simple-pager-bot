FROM ubuntu:20.04 as builder-image

RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-dev python3-venv python3-pip python3-wheel build-essential curl && \
	apt-get clean && rm -rf /var/lib/apt/lists/* && curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

RUN python3 -m venv /app/venv

ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir wheel

RUN python3 -m pip install --no-cache-dir -r requirements.txt

FROM ubuntu:20.04 as runner-image

RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-venv && \
	apt-get clean && rm -rf /var/lib/apt/lists/*


COPY --from=builder-image /app/venv /app/venv

WORKDIR /app

COPY . .

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:$PATH"

ENTRYPOINT ["python3", "main.py"]
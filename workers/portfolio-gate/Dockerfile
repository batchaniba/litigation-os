# portfolio-gate runner image for Cloudflare Containers.
# linux/amd64 is required. Node matches the repo engines field (>=22.22).
# python3 is required by the citation gate; git clones the PR head SHA.
FROM node:22.22.0-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends git python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/gate
COPY container/server.mjs container/run-gate.sh ./
RUN chmod +x run-gate.sh \
    && node --version \
    && python3 --version \
    && git --version

EXPOSE 8080
# The `node` user can write /tmp for the clone + npm ci.
USER node
ENV PORT=8080 \
    PORTFOLIO_SKIP_DISK_DOCS=1 \
    VITE_COPY_DOCUMENTS=0 \
    npm_config_update_notifier=false

CMD ["node", "server.mjs"]

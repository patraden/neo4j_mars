# original docker file https://github.com/neo4j/docker-neo4j-publish/tree/d812e34c70a2487fae5ee5cbb7c447b20b346afa
# debian open jdk https://github.com/bell-sw/Liberica/tree/master/docker/repos/liberica-openjdk-debian
# tini release including armhf https://github.com/krallin/tini/releases
#FROM bellsoft/liberica-openjdk-debian:11

#ENV NEO4J_SHA256=6da059f04f86e1a74221eb0103da38a1f645969cbbfe1b37c9de48bf55acabdc \
#    NEO4J_TARBALL=neo4j-community-4.1.3-unix.tar.gz \
#    NEO4J_EDITION=community \
#    NEO4J_HOME="/var/lib/neo4j"
#ARG NEO4J_URI=https://dist.neo4j.org/neo4j-community-4.1.3-unix.tar.gz
#ARG TINI_SHA256="5a9b35f09ad2fb5d08f11ceb84407803a1deff96cbdc0d1222f9f8323f3f8ad4"
#ARG TINI_URI="https://github.com/krallin/tini/releases/download/v0.19.0/tini-armhf"
FROM openjdk:11-jdk-slim

ENV NEO4J_SHA256=6da059f04f86e1a74221eb0103da38a1f645969cbbfe1b37c9de48bf55acabdc \
    NEO4J_TARBALL=neo4j-community-4.1.3-unix.tar.gz \
    NEO4J_EDITION=community \
    NEO4J_HOME="/var/lib/neo4j"
ARG NEO4J_URI=https://dist.neo4j.org/neo4j-community-4.1.3-unix.tar.gz
ARG TINI_SHA256="12d20136605531b09a2c2dac02ccee85e1b874eb322ef6baf7561cd93f93c855"
ARG TINI_URI="https://github.com/krallin/tini/releases/download/v0.18.0/tini"

RUN addgroup --gid 7474 --system neo4j && adduser --uid 7474 --system --no-create-home --home "${NEO4J_HOME}" --ingroup neo4j neo4j

COPY ./local-package/* /tmp/

RUN apt update \
    && apt install -y curl wget gosu jq \
    && curl -L --fail --silent --show-error ${TINI_URI} > /sbin/tini \
    && echo "${TINI_SHA256}  /sbin/tini" | sha256sum -c --strict --quiet \
    && chmod +x /sbin/tini \
    && curl --fail --silent --show-error --location --remote-name ${NEO4J_URI} \
    && echo "${NEO4J_SHA256}  ${NEO4J_TARBALL}" | sha256sum -c --strict --quiet \
    && tar --extract --file ${NEO4J_TARBALL} --directory /var/lib \
    && mv /var/lib/neo4j-* "${NEO4J_HOME}" \
    && rm ${NEO4J_TARBALL} \
    && mv "${NEO4J_HOME}"/data /data \
    && mv "${NEO4J_HOME}"/logs /logs \
    && chown -R neo4j:neo4j /data \
    && chmod -R 777 /data \
    && chown -R neo4j:neo4j /logs \
    && chmod -R 777 /logs \
    && chown -R neo4j:neo4j "${NEO4J_HOME}" \
    && chmod -R 777 "${NEO4J_HOME}" \
    && ln -s /data "${NEO4J_HOME}"/data \
    && ln -s /logs "${NEO4J_HOME}"/logs \
    && mv /tmp/neo4jlabs-plugins.json /neo4jlabs-plugins.json \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -y purge --auto-remove curl

ENV PATH "${NEO4J_HOME}"/bin:$PATH

WORKDIR "${NEO4J_HOME}"

VOLUME /data /logs

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 7474 7473 7687

ENTRYPOINT ["/sbin/tini", "-g", "--", "/docker-entrypoint.sh"]
CMD ["neo4j"]

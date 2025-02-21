FROM openjdk:8-alpine

RUN apk update && apk --no-cache add curl bash xmlstarlet

VOLUME ["/apks"]

WORKDIR /apks 

ARG APKTOOL_VERSION="2.11.0"

RUN curl -sLO https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool \
    && curl -sL -o apktool.jar https://github.com/iBotPeaches/Apktool/releases/download/v${APKTOOL_VERSION}/apktool_${APKTOOL_VERSION}.jar \
    && chmod +x apktool* \
    && mv apktool* /usr/local/bin/

ENTRYPOINT ["apktool"]